
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_unsigned.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: SelectCtrl
-------------------------------------------------------------------------------
entity SelectCtrl is

	generic (
		FlitWidth          : natural := 16; -- FlitWidth (in bit)
		ComHeader          : std_logic_vector;
--		NbTasks            : natural := 4; -- number of Select operation supported
		NbIndexedData      : natural := 4;
		NbSelections       : natural := 4);

	port (
		Reset, Clock       : IN  std_logic;
		
		Tx                 : OUT  std_logic;
		DataOut            : OUT  std_logic_vector(FlitWidth-1 downto 0);
		AckRx              : OUT  std_logic;
		
		DataIn             : IN std_logic_vector(FlitWidth-1 downto 0);
		Rx                 : IN std_logic;
		AckTx              : IN std_logic);

end SelectCtrl;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, Select input to be send given control directive
-------------------------------------------------------------------------------
architecture RTL of SelectCtrl is

	-------------------------------------------------------------------------------
	constant CONFIGURATION_CODE       : std_logic_vector(1 downto 0) :="00";
	constant READCONFIG_CODE          : std_logic_vector(1 downto 0) :="01";
	constant BUFFERING_CODE           : std_logic_vector(1 downto 0) :="10";
	constant VALIDATION_CODE          : std_logic_vector(1 downto 0) :="11";
	-------------------------------------------------------------------------------
	constant TypeBitWidth             : natural := 1;
	constant IndexedDataBitWidth      : natural :=BitWidth(NbIndexedData);
	constant SelectionsBitWidth       : natural :=BitWidth(NbSelections);
	
	constant MaxTaskNumber            : natural := 64;
	constant TasksBitWidth           : natural := Minimum(FlitWidth/2-(SelectionsBitWidth+IndexedDataBitWidth+TypeBitWidth), BitWidth(MaxTaskNumber-1));
	constant NBTask                   : natural := Minimum(2**(TasksBitWidth)-1, MaxTaskNumber);
	
	-------------------------------------------------------------------------------
	signal BranchID_i                 : unsigned(SelectionsBitWidth-1 downto 0);
	signal DataID_i                   : unsigned(SelectionsBitWidth-1 downto 0);
	signal OuptutDataIndex_i          : unsigned(SelectionsBitWidth-1 downto 0);
	signal SendingBufferIndex_i       : std_logic_vector(TasksBitWidth-1 downto 0);
	
--	signal DataIn_i                            : std_logic_vector(FlitWidth-1 downto 0);
	signal DataReq_i, Busy_i                   : std_logic := '0';
	
	signal NetworkAdapter_InputData_i          : std_logic_vector(FlitWidth-1 downto 0);
	signal NetworkAdapter_InputDataValid_i     : std_logic := '0';
			
	signal NetworkAdapter_HeaderValid_i        : std_logic := '0';
	signal NetworkAdapter_PayloadValid_i       : std_logic := '0';
			
	
	signal ValidationInput_i, ValidationOutput_i : std_logic := '0';
	signal SENDING_HEADER_FIFO_OUTPUT_i, SENDING_DATA_FIFO_OUTPUT_i, SENDING_HEADER_FIFO_INPUT_i, SENDING_DATA_FIFO_INPUT_i : std_logic_vector(FlitWidth-1 downto 0);
	signal SENDING_HEADER_FIFO_READ_i, SENDING_DATA_FIFO_READ_i                 : std_logic := '0';
	signal SENDING_FIFO_EMPTY_i                : std_logic := '0';
--	signal SelectTarget_i                      : std_logic_vector(FlitWidth-1 downto 0);
	signal TestID_i                            : std_logic_vector(TasksBitWidth-1 downto 0);
	signal BufferingInputValid_i               : std_logic_vector(NbSelections*NbIndexedData-1 downto 0) := (others=>'0');
	signal PacketTypeBits_i                    : std_logic_vector(TypeBitWidth-1 downto 0); -- Encodes modes
	
	signal HeaderConfigInputValid_i            : std_logic_vector(NbIndexedData-1 downto 0) := (others=>'0');
	signal SelectedInputValid_i                : std_logic := '0';
	signal InputBufferStatusInputValid_i            : std_logic := '0';
	
	signal SendRequest_i                       : std_logic := '0';
	signal SelectedOutput_i                    : std_logic_vector(FlitWidth-1 downto 0);
	type DataVector is array(natural range <>) of std_logic_vector(FlitWidth-1 downto 0);
	signal BuffersOutputs_i                    : DataVector(NbSelections*NbIndexedData-1 downto 0);
	
	type HeaderTable is array(natural range <>) of std_logic_vector(FlitWidth-1 downto 0);
	signal SelectionHeaders_i                  : HeaderTable(NbIndexedData-1 downto 0);
	signal SelectedHeader_i                    : std_logic_vector(FlitWidth-1 downto 0);
	signal Selector_i                          : natural := 0;
	signal BufferOutputPointer_i               : natural := 0;
	
	signal ReadyToSelect_i                     : std_logic := '0';
	signal InputStatus_RefIn_i                 : std_logic_vector(IndexedDataBitWidth-1 downto 0);
	signal InputStatus_RefOut_i                : std_logic_vector(IndexedDataBitWidth-1 downto 0);
	signal InputStatusIn_i                     : std_logic_vector(IndexedDataBitWidth-1 downto 0);
	signal InputStatusOut_i                    : std_logic_vector(IndexedDataBitWidth-1 downto 0);
	signal InputStatusWrite_i                  : std_logic;
	signal InputStatus_RefWrite_i              : std_logic;
--	signal SendingCounter_i                    : natural :=0;
	signal SelectionStatus_Input_i             : std_logic_vector(SelectionsBitWidth downto 0);
	signal SelectionStatus_Write_i             : std_logic;
	signal SelectionStatus_Output_i            : std_logic_vector(SelectionsBitWidth downto 0);
	signal Validated_In_i, Validated_Out_i     : std_logic;
	-------------------------------------------------------------------------------
	type Config_Type is (BUFFERING_MODE, VALIDATION_MODE, CONFIG_MODE, READCONF_MODE, SENDING_MODE, RESET_MODE);
	signal CurrentMode_i : Config_Type := CONFIG_MODE;

	signal SendingCounter_i : natural :=0;
	
	signal Transmitted_i : std_logic;

begin  -- RTL

	
	assert TasksBitWidth+IndexedDataBitWidth+SelectionsBitWidth+TypeBitWidth <= (FlitWidth/2) report "TasksBitWidth+IndexedDataBitWidth+SelectionsBitWidth/=FlitWidth/2" severity failure;
	
	------------------------------------------------------------
	-- Network Adapter
	NetworkAdapter: entity work.NetworkAdapter(RTL)
		generic map(
			FlitWidth => FlitWidth
			)
		port map(
			rst => Reset,
			clk => Clock,
			
			DataIn => DataIn,
			Tx     => Tx,
			AckTx  => AckTx,
			
			DataOut => DataOut,
			Rx      => Rx,
			AckRx   => AckRx,
			
			InputData      => NetworkAdapter_InputData_i,
			InputDataValid => NetworkAdapter_InputDataValid_i,
			
			OutputData         => SENDING_DATA_FIFO_OUTPUT_i(FlitWidth-1 downto 0),
			OutputRead         => SENDING_DATA_FIFO_READ_i,
			OutputFifoEmpty    => SENDING_FIFO_EMPTY_i,
			ReadHeaderFifo     => SENDING_HEADER_FIFO_READ_i,
			
			HeaderValid        => NetworkAdapter_HeaderValid_i,
			PayloadValid       => NetworkAdapter_PayloadValid_i,
			
			Transmitted        => Transmitted_i,
			HeaderTransmitted  => SENDING_HEADER_FIFO_OUTPUT_i,
			PayloadTransmitted => STD_LOGIC_VECTOR(TO_UNSIGNED(1, FlitWidth)),
		
			SendBack           => '0', -- when '1', input packets are sent back to output port
			TerminalBusy       => '0' -- when '1', no input packets can be recieved
			);

	-----------------------------------------------------------------------------
	-- Assign payload and TaskID and DataIdx from input flits
	SetRegisters: process (Clock, Reset)
	begin 
		if (Reset = '1') then
			TestID_i   <= (others=>'0');
			BranchID_i <= (others=>'0');
			DataID_i   <= (others=>'0');
			PacketTypeBits_i <= (others=>'0');
		else 
			if rising_edge(Clock) then
				-------------------------------------------------------------
				if NetworkAdapter_HeaderValid_i='1' then
					PacketTypeBits_i<=NetworkAdapter_InputData_i(PacketTypeBits_i'length+FlitWidth/2-1 downto FlitWidth/2);
					TestID_i <= NetworkAdapter_InputData_i(TestID_i'length+DataID_i'length+PacketTypeBits_i'length+FlitWidth/2-1 downto DataID_i'length+PacketTypeBits_i'length+FlitWidth/2);
					BranchID_i <= UNSIGNED(NetworkAdapter_InputData_i(FlitWidth-1 downto FlitWidth-BranchID_i'length));
				end if;
				-------------------------------------------------------------
				if NetworkAdapter_HeaderValid_i='1' then
					DataID_i <= UNSIGNED(NetworkAdapter_InputData_i(DataID_i'length+PacketTypeBits_i'length+FlitWidth/2-1 downto PacketTypeBits_i'length+FlitWidth/2));
				elsif NetworkAdapter_InputDataValid_i='1' then
					DataID_i <= DataID_i+1;
				end if;
				-------------------------------------------------------------
				
			end if;
		end if;
	end process SetRegisters;
	
	OuptutDataIndex_i <= UNSIGNED(SendingBufferIndex_i) when CurrentMode_i=SENDING_MODE or (Validated_Out_i='1' and InputStatusOut_i=InputStatus_RefOut_i) else DataID_i; 
	
	
	-- TODO : RAM for each input branch of the SelectGroup
	-----------------------------------------------------------------------------
	INPUT_STATUS_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => TasksBitWidth,
			SIZE_PORT_MEM  => IndexedDataBitWidth) -- enough to encode numbers up to NbIndexedData
		PORT MAP(
			din    => InputStatusIn_i,
			wen    => InputStatusWrite_i,
			wraddr => TestID_i,
			rdaddr => TestID_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => InputStatusOut_i);
			
	InputStatusIn_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(InputStatusOut_i))+1, InputStatusIn_i'length)) when CurrentMode_i=BUFFERING_MODE and NetworkAdapter_InputDataValid_i='1' else (others=>'0');
	InputStatusWrite_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=BUFFERING_MODE or CurrentMode_i=CONFIG_MODE else 
	                      '1' when CurrentMode_i=SENDING_MODE else 
	                      '0';
	
	-----------------------------------------------------------------------------
	-- SET NUMBER OF DATA TO BE RECEIVED BEFORE TRIGGERING THE SELECTION
	INPUT_REFERENCE_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => TasksBitWidth,
			SIZE_PORT_MEM  => IndexedDataBitWidth) -- enough to encode numbers up to NbIndexedData
		PORT MAP(
			din    => InputStatus_RefIn_i,
			wen    => InputStatus_RefWrite_i,
			wraddr => TestID_i,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => InputStatus_RefOut_i);
			
	InputStatus_RefWrite_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=CONFIG_MODE else '0';
	InputStatus_RefIn_i    <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(InputStatus_RefOut_i))+1, InputStatus_RefIn_i'length)) when CurrentMode_i=CONFIG_MODE else (others=>'1');
	
	-----------------------------------------------------------------------------
	BUFFERS_GENERATE : for i in 0 to NbSelections-1 generate
		-----------------------------------------------------------------------------
		MEMORY_GENERATE: for j in 0 to NbIndexedData-1 generate
			-----------------------------------------------------------------------------
			INPUT_BUFFERS_RAM : entity work.a_sram_param(behavioral)
				GENERIC MAP (
					SIZE_ADDR_MEM  => TasksBitWidth,
					SIZE_PORT_MEM  => FlitWidth)
				PORT MAP(
					din    => NetworkAdapter_InputData_i,
					wen    => BufferingInputValid_i(i*NbIndexedData+j),
					wraddr => TestID_i,
					rdaddr => TestID_i,
					clk    => Clock,
					oclk   => Clock,
					dout   => BuffersOutputs_i(i*NbIndexedData+j));
			BufferingInputValid_i(i*NbIndexedData+j) <= NetworkAdapter_InputDataValid_i when CurrentMode_i=BUFFERING_MODE and TO_INTEGER(DataID_i)=j and TO_INTEGER(BranchID_i)=i else '0';
		end generate;
		-----------------------------------------------------------------------------
--	OutputData <= OutputDataVector((NbIndexedData-Index_i)*DataWidth-1 downto (NbIndexedData-Index_i-1)*DataWidth);
	end generate;
	
	BufferOutputPointer_i <= Selector_i*NbIndexedData+TO_INTEGER(OuptutDataIndex_i);
	SelectedOutput_i <= BuffersOutputs_i(BufferOutputPointer_i);
--	InputBufferIndex_i    <= SendingBufferIndex_i when CurrentMode_i=SENDING_MODE else DataID_i;

	-----------------------------------------------------------------------------
	SELECTION_STATUS_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => TasksBitWidth,
			SIZE_PORT_MEM  => SelectionsBitWidth+1) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => SelectionStatus_Input_i,
			wen    => SelectionStatus_Write_i,
			wraddr => TestID_i,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => SelectionStatus_Output_i);
			
	Validated_Out_i <= SelectionStatus_Output_i(SelectionStatus_Output_i'high);
			
	Validated_In_i <= '1' when CurrentMode_i=VALIDATION_MODE else '0';
	SelectionStatus_Input_i <= (others=>'0') when CurrentMode_i=RESET_MODE else Validated_In_i & NetworkAdapter_InputData_i(SelectionStatus_Input_i'length-2 downto 0);
	SelectionStatus_Write_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=VALIDATION_MODE or CurrentMode_i=CONFIG_MODE else '1' when CurrentMode_i=RESET_MODE else '0';
	
	-------------------------------------------------------------------------------
	ModeAssignmentFSM: process(Clock, Reset)
	begin
		if (Reset = '1') then
			CurrentMode_i <= CONFIG_MODE;
			SendingCounter_i <= 0;
			SendingBufferIndex_i <= (others=>'0');
		else 
			if rising_edge(Clock) then 
				case CurrentMode_i is -- Assignments for FSM ConfigState
					when BUFFERING_MODE =>
						if PacketTypeBits_i = VALIDATION_CODE then
							CurrentMode_i <= VALIDATION_MODE;
						elsif PacketTypeBits_i = CONFIGURATION_CODE then
							CurrentMode_i <= CONFIG_MODE;
						else
							if Validated_Out_i='1' and InputStatusOut_i=InputStatus_RefOut_i then
								SendingBufferIndex_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(SendingCounter_i, SendingBufferIndex_i'length));
								CurrentMode_i <= SENDING_MODE;
							end if;
						end if;
					when VALIDATION_MODE =>
						if PacketTypeBits_i = BUFFERING_CODE then
							CurrentMode_i <= BUFFERING_MODE;
						elsif PacketTypeBits_i = CONFIGURATION_CODE then
							CurrentMode_i <= CONFIG_MODE;
						else
							if Validated_Out_i='1' and InputStatusOut_i=InputStatus_RefOut_i then
								SendingBufferIndex_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(SendingCounter_i, SendingBufferIndex_i'length));
								CurrentMode_i <= SENDING_MODE;
							end if;
						end if;
					when CONFIG_MODE =>
						if PacketTypeBits_i = BUFFERING_CODE then
							CurrentMode_i <= BUFFERING_MODE;
						elsif PacketTypeBits_i = VALIDATION_CODE then
							CurrentMode_i <= VALIDATION_MODE;
						elsif PacketTypeBits_i = READCONFIG_CODE then
							CurrentMode_i <= READCONF_MODE;
						end if;
						SendingCounter_i <= TO_INTEGER(UNSIGNED(InputStatus_RefOut_i));
					when READCONF_MODE =>
						if PacketTypeBits_i = BUFFERING_CODE then
							CurrentMode_i <= BUFFERING_MODE;
						elsif PacketTypeBits_i = VALIDATION_CODE then
							CurrentMode_i <= VALIDATION_MODE;
						elsif PacketTypeBits_i = CONFIGURATION_CODE then
							CurrentMode_i <= CONFIG_MODE;
						end if;
					when SENDING_MODE =>
						SendingBufferIndex_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(SendingCounter_i, SendingBufferIndex_i'length));
						if SendingCounter_i<=1 then
							CurrentMode_i <= RESET_MODE;
						else
							SendingCounter_i <= SendingCounter_i-1;
						end if;
					when RESET_MODE =>
						if PacketTypeBits_i = BUFFERING_CODE then
							CurrentMode_i <= BUFFERING_MODE;
						elsif PacketTypeBits_i = VALIDATION_CODE then
							CurrentMode_i <= VALIDATION_MODE;
						else
							CurrentMode_i <= CONFIG_MODE;
						end if;
					when others => null;
				end case;
			end if;
		end if;
	end process ModeAssignmentFSM;
	
	-----------------------------------------------------------------------------
	Headers_PerSelectedData : for i in 0 to NbIndexedData-1 generate
		-------------------------------------------
		SelectHeader_RAM : entity work.a_sram_param(behavioral)
			GENERIC MAP (
				SIZE_ADDR_MEM  => TasksBitWidth,
				SIZE_PORT_MEM  => FlitWidth) -- enough to encode numbers up to NbDataPerSet
			PORT MAP(
				din    => NetworkAdapter_InputData_i,
				wen    => HeaderConfigInputValid_i(i),
				wraddr => TestID_i,
				rdaddr => TestID_i, -- NextTaskAddr_i,
				clk    => Clock,
				oclk   => Clock,
				dout   => SelectionHeaders_i(i));
		-------------------------------------------
		HeaderConfigInputValid_i(i) <= NetworkAdapter_InputDataValid_i when CurrentMode_i=CONFIG_MODE and TO_INTEGER(DataID_i)=i else '0';
	end generate;
	
	-----------------------------------------------------------------
	SENDING_HEADER_FIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 16,
			largeur => FlitWidth 
			)
		port map(
			ack_rd => open,
			clock_out => Clock,
			wr => SendRequest_i,
			data_in => SENDING_HEADER_FIFO_INPUT_i,
			rd => SENDING_HEADER_FIFO_READ_i,
			data_out => SENDING_HEADER_FIFO_OUTPUT_i,
			IsEmpty => open,
			reset => Reset,
			ack_wr => open,
			clock_in => Clock,
			IsFull => open); -- WARNING !!!! INSURE SAFETY
	
	-----------------------------------------------------------------
	SENDING_DATA_FIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 16,
			largeur => FlitWidth 
			)
		port map(
			ack_rd => open,
			clock_out => Clock,
			wr => SendRequest_i,
			data_in => SENDING_DATA_FIFO_INPUT_i,
			rd => SENDING_DATA_FIFO_READ_i,
			data_out => SENDING_DATA_FIFO_OUTPUT_i,
			IsEmpty => SENDING_FIFO_EMPTY_i,
			reset => Reset,
			ack_wr => open,
			clock_in => Clock,
			IsFull => open); -- WARNING !!!! INSURE SAFETY
	
	Selector_i <= TO_INTEGER(UNSIGNED(SelectionStatus_Output_i(SelectionStatus_Output_i'length-2 downto 0)));
	SelectedHeader_i <= SelectionHeaders_i(TO_INTEGER(OuptutDataIndex_i));
	SENDING_HEADER_FIFO_INPUT_i <= SelectedHeader_i;
	SENDING_DATA_FIFO_INPUT_i   <= SelectedOutput_i;
	

	-----------------------------------------------------------------------------
	-- Set status
--	ReadyToSelect_i <= InputBufferStatusOutput_i(TO_INTEGER(UNSIGNED(DataID_i))) when CurrentMode_i=VALIDATION_MODE else '0';
	
	
	-- WARNING : OVERWRITING OF INPUT VALUE IF BUFFERING WHEREAS STATUS='1' !!!!!
	SendRequest_i <= '1' when CurrentMode_i=SENDING_MODE else '0';
	
--	InputBufferStatusInputValid_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=CONFIG_MODE or CurrentMode_i=BUFFERING_MODE or CurrentMode_i=VALIDATION_MODE else '0';
--	SelectedInputValid_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=VALIDATION_MODE else '0';
	
	-----------------------------------------------------------------------------
--	SendCountProc: process (Clock, Reset)
--	begin 
--		if rising_edge(Clock) then
--			if (Reset = '1') then
--				SendingCounter_i  <= 0; 
--			else 
--				if CurrentMode_i=SENDING_MODE then
--					if SendingCounter_i/=0 then
--						SendingCounter_i <= SendingCounter_i-1; -- UNCOUNT
--					end if;
--				SendingCounter_i <= 0;
--				else
--					SendingCounter_i <= TO_INTEGER(UNSIGNED(InputStatus_RefOut_i));
--				end if;
--			end if;
--		end if;
--	end process SendCountProc;
	
end RTL;




