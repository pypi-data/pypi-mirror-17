

use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: TaskManager
-------------------------------------------------------------------------------
entity TaskManager is
	generic (
		FlitWidth           : natural := 16; -- FlitWidth (in bit)
		BBOutputWidth       : natural := 16; -- Output width (in bit)
		BBInputWidth        : natural := 16; -- Basic block Width (in bit)
		ComHeader           : std_logic_vector;
		PipelineLength      : natural := 2;
		OutputSerialization : NaturalVector;
		InputSerialization  : NaturalVector); -- Number of task an operator can manage
	port (
		Reset, Clock       : IN  std_logic;

		InputData          : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');   -- Input data flit
		InputDataValid     : IN  std_logic;
		
		Start              : OUT std_logic;
		DataRead           : IN  std_logic;
		
		HeaderValid        : IN  std_logic;
		
		PayloadValid       : IN  std_logic;

		Transmitted        : IN  std_logic; -- Request

		HeaderTransmitted  : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		PayloadTransmitted : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');

		BBInputs           : OUT std_logic_vector(BBInputWidth-1 downto 0):=(others=>'0');
--		BBInputValid       : OUT std_logic;
		
		ReadProgram        : OUT std_logic;
		BBOutput           : IN  std_logic_vector(BBOutputWidth-1 downto 0):=(others=>'0');
		
		SendBack           : OUT std_logic; -- when '1', input packets are sent back to output port
		TerminalBusy       : OUT std_logic; -- when '1', no input packets can be recieved
		
		OutputData         : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		------------------------------------------
		ReadHeaderFifo     : IN  std_logic;
		OutputRead         : IN  std_logic;
		OutputFifoEmpty    : OUT std_logic--;
--		DebugVector        : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0')
		);

end TaskManager;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of TaskManager is

	constant NbInputFlits             : natural := BBInputWidth/FlitWidth;
	constant NbOutputFlits            : natural := BBOutputWidth/FlitWidth;
	
	constant TypeBitWidth             : natural := 1;
	constant DataIdxBitWidth          : natural := BitWidth(NbInputFlits);
	
	constant MaxTaskNumber            : natural := 256;
	constant NbTaskBitWidth           : natural := Minimum(FlitWidth/2-(DataIdxBitWidth+TypeBitWidth), BitWidth(MaxTaskNumber-1));
	constant NBTask                   : natural := Minimum(2**(NbTaskBitWidth)-1, MaxTaskNumber);
	
	constant OutputAddrBitWidth       : natural := BitWidth(Maximum(OutputSerialization));
	
	-------------------------------------------------------------------------------
	
	----- MODE CODES - Set up by software 
	constant HEADER_CONFIG_CODE         : std_logic_vector(3 downto 0) :=x"1";
	constant MULTICAST_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"2";
	constant CONSTANTS_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"3";
	constant READ_HEADER_CONFIG_CODE    : std_logic_vector(3 downto 0) :=x"4";
	constant READ_MULTICAST_CONFIG_CODE : std_logic_vector(3 downto 0) :=x"5";
	
	constant HEADER_CONFIG_MESSAGE         : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(HEADER_CONFIG_CODE), FlitWidth));
	constant MULTICAST_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(MULTICAST_CONFIG_CODE), FlitWidth));
	constant CONSTANTS_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(CONSTANTS_CONFIG_CODE), FlitWidth));
	constant READ_HEADER_CONFIG_MESSAGE    : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_HEADER_CONFIG_CODE), FlitWidth));
	constant READ_MULTICAST_CONFIG_MESSAGE : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_MULTICAST_CONFIG_CODE), FlitWidth));
	
	
--	constant HeaderConfigCode          : std_logic_vector(TypeBitWidth-1 downto 0) :="00";
--	constant MulticastConfigCode       : std_logic_vector(TypeBitWidth-1 downto 0) :="01";
--	constant RunningCode               : std_logic_vector(TypeBitWidth-1 downto 0) :="10";
--	constant ConstantConfigCode        : std_logic_vector(TypeBitWidth-1 downto 0) :="11";
	constant CONFIG_CODE_ZERO          : std_logic_vector(DataIdxBitWidth-1 downto 0) :=(others=>'0');
	constant ZEROS_HALF_FLIT           : std_logic_vector(FlitWidth/2-1 downto 0) :=(others=>'0');
	constant ZEROS_FLIT                : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	
--	constant OutputSerializationFactor : natural :=BBOutputWidth/FlitWidth;
	constant PosBitWidth               : natural := DataIdxBitWidth;

	---------------------------------------------------------------------------
	signal TaskID_i            : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal DataIdx_i           : std_logic_vector(DataIdxBitWidth-1 downto 0);
--	signal PacketType_i        : std_logic_vector(TypeBitWidth-1 downto 0); -- Encodes modes
	signal DataID_i            : std_logic_vector(FlitWidth/2-1 downto 0) :=(others=>'0');
	signal ConfigCode_i        : std_logic_vector(DataIdxBitWidth-1 downto 0);

	signal MultiCastConfigMode_i, HeaderConfigMode_i, ConstantConfigMode_i, ConfigMode_i, RunningMode_i : std_logic := '0';
	signal MemoryReadMode_i, HeaderReadMode_i, MultiCastReadMode_i  : std_logic;
	signal HeaderRegister_i    : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	signal ConfigMessage_i     : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	
	---------------------------------------------------------------------------
	constant TaskStartAddr     : unsigned(NbTaskBitWidth-1 downto 0) := (others=>'0');
	constant ZEROS             : unsigned(FlitWidth/2-1 downto 0):=(others=>'0');
	
	---------------------------------------------------------------------------
	signal BBInputValid_i      : std_logic :='0';
	signal PeInputValid_i      : std_logic :='0';
	signal DataIdxCounter_i    : unsigned(DataIdxBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal InputCounter_i      : unsigned(NbTaskBitWidth-1 downto 0);
	signal OutputCounter_i     : unsigned(OutputAddrBitWidth-1 downto 0) := (others=>'0');
	
	---------------------------------------------------------------------------
	signal HeaderInputWrite_i  : std_logic;
	signal HeaderOutput_i      : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderInput_i       : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderAddrWr_i, HeaderAddrRd_i : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal HeaderAddr_Output_i : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal MemReadAddr_i       : std_logic_vector(NbTaskBitWidth-1 downto 0);
	
	signal OutputTaskID_i      : std_logic_vector(NbTaskBitWidth-1 downto 0);
	---------------------------------------------------------------------------
	signal MultiCastWrite_i    : std_logic;
	signal MultiCastInput_i    : std_logic_vector(FlitWidth/2-1 downto 0);
	signal MultiCastOutput_i   : std_logic_vector(FlitWidth/2-1 downto 0);
	signal MultiCastAddrWr_i, MultiCastAddrRd_i    : std_logic_vector(NbTaskBitWidth-1 downto 0);
--	signal MultiCastCounter_i : unsigned(NbTaskBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal BBOutputValid_i     : std_logic;
	signal PeInput_i           : std_logic_vector(BBInputWidth-1 downto 0);
	
	signal OutputDataMemIn_i   : std_logic_vector(FlitWidth-1 downto 0);
	signal MemoryOutput_i      : std_logic_vector(FlitWidth-1 downto 0);
	signal OutputDataMemWr_i   : std_logic;
	
	signal ReceivedDataIdx_i          : unsigned(DataIdxBitWidth-1 downto 0);
	type ADDRESSES is array(natural range <>) of std_logic_vector(BitWidth(NbTask*Maximum(InputSerialization))-1 downto 0);
	signal StructWrAddr_i, StructRdAddr_i : ADDRESSES(NbInputFlits-1 downto 0);
	signal StructuredDataWrite_i       : std_logic_vector(NbInputFlits-1 downto 0);
--	signal StructuredDataRamOutput_i   : std_logic_vector(InputSerialization'length*FlitWidth-1 downto 0);

	type COUNTERS is array(natural range <>) of unsigned(BitWidth(NbTask*Maximum(InputSerialization))-1 downto 0);
	signal WrCnt_i, RdCnt_i : COUNTERS(NbInputFlits-1 downto 0);
	
	signal ConstOrVariableValid_i : std_logic;
	signal Serialized_i : std_logic;
	signal InputSerialized_i : natural;
	
	signal OutputWrOffset_i, OutputRdOffset_i : std_logic_vector(OutputAddrBitWidth-1 downto 0);
	signal OutputData_i : std_logic_vector(FlitWidth-1 downto 0);

	signal DataAvailable_i        : std_logic;
	
	signal BaseStructAddr_i : unsigned(BitWidth(NbTask*Maximum(InputSerialization))-1 downto 0); 
	
begin  -- RTL

	ReadProgram <= '0';

--####################################################################
--         STATUS REGISTERS
--####################################################################
	-----------------------------------------------------------------------------
	-- Select which header to read or write
	HeaderRegisterLock: process (Clock, Reset)
	begin  -- process StateMemory
		if (Reset = '1') then
			HeaderRegister_i <= (others=>'0');
		else 
			if rising_edge(Clock) then
				-------------------------------------------------------------
				if HeaderValid='1' then
					HeaderRegister_i <= InputData;
				end if;
				
			end if;
		end if;
	end process HeaderRegisterLock;
	
	ConfigMode_i <= HeaderRegister_i(FlitWidth/2);
	ConfigCode_i <= HeaderRegister_i(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2);
	TaskID_i     <= HeaderRegister_i(NbTaskBitWidth+DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto DataIdxBitWidth+TypeBitWidth+FlitWidth/2) when HeaderValid='0' else InputData(NbTaskBitWidth+DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto DataIdxBitWidth+TypeBitWidth+FlitWidth/2);
	RunningMode_i <= not ConfigMode_i;
	
	
--	HeaderConfigMode_i    <= '1' when PacketType_i=HeaderConfigCode and ConfigCode_i=CONFIG_CODE_ZERO else '0';
--	MultiCastConfigMode_i <= '1' when PacketType_i=MulticastConfigCode and ConfigCode_i=CONFIG_CODE_ZERO else '0';
--	ConstantConfigMode_i  <= '1' when PacketType_i=ConstantConfigCode else '0'; -- Constant config mode can be considered as normal data input. The only difference is that constant status is set.
--	HeaderReadMode_i      <= '1' when (PacketType_i=HeaderConfigCode) and ConfigCode_i/=CONFIG_CODE_ZERO else '0';
--	MultiCastReadMode_i   <= '1' when (PacketType_i=MulticastConfigCode) and ConfigCode_i/=CONFIG_CODE_ZERO else '0';
	
	ConfigModProcess : process(Clock)
	begin
		if rising_edge(Clock) then
			if HeaderValid='1' then
				ConfigMessage_i       <= ZEROS_FLIT;
				HeaderConfigMode_i    <= '0';
				MultiCastConfigMode_i <= '0';
				ConstantConfigMode_i  <= '0';
				HeaderReadMode_i      <= '0';
				MultiCastReadMode_i   <= '0';
			else
				if ConfigMode_i='1' and ConfigMessage_i=ZEROS_FLIT then
					if InputDataValid='1' then
						ConfigMessage_i <= InputData;
						if InputData=HEADER_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '1';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							
						elsif InputData=MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '1';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';

						elsif InputData=CONSTANTS_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '1';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							
						elsif InputData=READ_HEADER_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '1';
							MultiCastReadMode_i   <= '0';
							
						elsif InputData=READ_MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '1';
						end if;
					end if;
				end if;
			end if;
		end if;
	end process ConfigModProcess;
	
	MemoryReadMode_i <= HeaderReadMode_i or MultiCastReadMode_i;
	
--####################################################################
--         INPUT TABLE
--####################################################################
	-------------------------------------------------------------------------------
	InputTable: entity work.InputTable(RTL)
		GENERIC MAP(
			FlitWidth          => FlitWidth,   -- FlitWidth (in bit)
			NbInputFlit        => NbInputFlits,    -- Flits number
			NBTask             => NBTask,
			InputSerialization => InputSerialization) -- Number of task an operator can manage
		PORT MAP(
			Rst                => Reset,
			Clk                => Clock,
			
			HeaderConfigMode   => HeaderConfigMode_i,
			ConstantConfigMode => ConstantConfigMode_i,
			IdleMode           => RunningMode_i,

			DataIdx           => DataIdx_i,
			Serialized        => Serialized_i,
			TaskID            => TaskID_i,
--			DataID            => DataID_i,
--			PayloadReceived   => PayloadReceived_i,
--			PayloadValid      => PayloadValid,
			HeaderValid       => HeaderValid,
			
			BufferBusy        => SendBack,
		
			NetworkInputValid => InputDataValid,
			NetworkInput      => InputData,
		
			PeInputValid      => PeInputValid_i,
			PeInput           => PeInput_i);
			
	Start <= PeInputValid_i;
	
	Serialized_i <= '0' when InputSerialized_i=1 else '1';
	InputSerialized_i <= InputSerialization(TO_INTEGER(ReceivedDataIdx_i));
	
	BBInputValid_i <= PeInputValid_i;

	-----------------------------------------------------------------------------	
	BBInput_Feeder: for i in 0 to InputSerialization'length-1 generate
	
		--%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		DirectFeed : if InputSerialization(i)=1 generate
			BBInputs(FlitWidth*i+FlitWidth-1 downto FlitWidth*i) <= PeInput_i(FlitWidth*i+FlitWidth-1 downto FlitWidth*i);
--			StructuredDataRamOutput_i(FlitWidth*i+FlitWidth-1 downto FlitWidth*i) <= (others=>'0');
			StructuredDataWrite_i(i) <= '0';
		end generate DirectFeed;
		
		--%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		RamFeed : if InputSerialization(i)>1 generate
		
			StructuredDataWrite_i(i) <= InputDataValid when TO_INTEGER(ReceivedDataIdx_i)=i else '0';
			---------------------------------------
			STRUCTURED_DATA_RAM : entity work.a_sram_param
				GENERIC MAP (
					SIZE_ADDR_MEM  => BitWidth(NbTask*Maximum(InputSerialization)),
					SIZE_PORT_MEM  => FlitWidth)
				PORT MAP(
					din    => InputData,
					wen    => StructuredDataWrite_i(i),
					wraddr => StructWrAddr_i(i),
					rdaddr => StructRdAddr_i(i),
					clk    => Clock,
					oclk   => Clock,
					dout   => BBInputs(FlitWidth*i+FlitWidth-1 downto FlitWidth*i));
			
			BaseStructAddr_i <= resize(UNSIGNED(TaskID_i)*Maximum(InputSerialization), BaseStructAddr_i'length);
			---------------------------------------
			STRUCT_WRCOUNTER_PROC : process(Clock) is 
			begin
				if rising_edge(Clock) then
					if HeaderValid='1' or Reset='1' then 
						WrCnt_i(i) <= (others=>'0');
					else
						if InputDataValid='1' and TO_INTEGER(ReceivedDataIdx_i)=i then
							WrCnt_i(i) <= WrCnt_i(i)+1;
						end if;
					end if;
				end if;
			end process STRUCT_WRCOUNTER_PROC;
			
			StructWrAddr_i(i) <= STD_LOGIC_VECTOR(BaseStructAddr_i + WrCnt_i(i));
			
			---------------------------------------
			STRUCT_RDCOUNTER_PROC : process(Clock) is 
			begin
				if rising_edge(Clock) then
					if RdCnt_i(i)=InputSerialization(i) or Reset='1' then 
						RdCnt_i(i) <= (others=>'0');
					else
						if PeInputValid_i='1' and TO_INTEGER(ReceivedDataIdx_i)=i then
							RdCnt_i(i) <= (others=>'0');
						else
							if DataRead='1' then
								RdCnt_i(i) <= RdCnt_i(i)+1;
							end if;
						end if;
					end if;
				end if;
			end process STRUCT_RDCOUNTER_PROC;
			
			StructRdAddr_i(i) <= STD_LOGIC_VECTOR(BaseStructAddr_i + RdCnt_i(i));
			
		end generate RamFeed;
	end generate;
	
	-----------------------------------------------------------------------------
	DataIdx_i <= InputData(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2) when HeaderValid='1' else STD_LOGIC_VECTOR(DataIdxCounter_i);
	ConstOrVariableValid_i <= (InputDataValid and RunningMode_i) or (InputDataValid and ConstantConfigMode_i);
	
	-----------------------------------------------------------------------------
	DATA_INDEX_PROC : process(Reset, Clock) is 
	begin
		if (Reset = '1') then
			DataIdxCounter_i <= (others=>'0');
			ReceivedDataIdx_i   <= (others=>'0');
		else 
			if rising_edge(Clock) then
				if HeaderValid='1' then
					ReceivedDataIdx_i <= UNSIGNED(InputData(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2));
					DataIdxCounter_i <= UNSIGNED(InputData(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2));
				else
					if ConstOrVariableValid_i='1' and Serialized_i='0' then --MultiCastConfigMode='1' or HeaderConfigMode_i='1' or ConstantConfigMode_i='1' then
						DataIdxCounter_i <= DataIdxCounter_i+1;
					end if;
				end if;
			end if;
		end if;
	end process DATA_INDEX_PROC;

	-----------------------------------------------------------------------------
	PayloadTransmitted <= STD_LOGIC_VECTOR(TO_UNSIGNED(NbTask, PayloadTransmitted'length)) when MemoryReadMode_i='1' else
	                      STD_LOGIC_VECTOR(TO_UNSIGNED(OutputSerialization(0), PayloadTransmitted'length));
	-----------------------------------------------------------------------------

	
--####################################################################
--         OUTPUT MEMORY BUFFER
--####################################################################
	RESULTS_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => OutputAddrBitWidth,
			SIZE_PORT_MEM  => FlitWidth)
		PORT MAP(
			din    => OutputDataMemIn_i,
			wen    => OutputDataMemWr_i,
			wraddr => OutputWrOffset_i,
			rdaddr => OutputRdOffset_i, --NextTaskAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => OutputData_i);
			
	OutputWrOffset_i  <= STD_LOGIC_VECTOR(OutputCounter_i);
	OutputDataMemWr_i <= '1' when BBOutputValid_i='1' or OutputCounter_i/=TO_UNSIGNED(0, OutputCounter_i'length) else '0';
	OutputDataMemIn_i <= MemoryOutput_i when MemoryReadMode_i='1' else BBOutput;
	MemoryOutput_i    <= HeaderOutput_i when HeaderReadMode_i='1' else 
	                     ZEROS_HALF_FLIT & MultiCastOutput_i when MultiCastReadMode_i='1' else 
	                     (others=>'1');

--####################################################################
--         INPUT COUNTER
--####################################################################

	-----------------------------------------------------------------------------
	CONFIG_COUNTER_PROC : process(Reset, Clock) is 
	begin
		if rising_edge(Clock) then
			if HeaderValid='1' then
				InputCounter_i <= (others=>'0');
			else
				if InputDataValid='1' and (HeaderConfigMode_i='1' or MultiCastConfigMode_i='1') then --MultiCastConfigMode='1' or HeaderConfigMode_i='1' or ConstantConfigMode_i='1' then
					InputCounter_i <= InputCounter_i+1;
				end if;
			end if;
		end if;
	end process CONFIG_COUNTER_PROC;

--####################################################################
--         OUTPUT COUNTER
--####################################################################

	SerializedOutput : if Maximum(OutputSerialization)>1 generate
		-----------------------------------------------------------------------------
		OUTPUT_COUNTER_PROC : process(Reset, Clock) is 
		begin
			if rising_edge(Clock) then
				if (OutputCounter_i=TO_UNSIGNED(0, OutputCounter_i'length) and BBOutputValid_i='1') or OutputCounter_i/=TO_UNSIGNED(OutputSerialization(0), OutputCounter_i'length) then
					OutputCounter_i <= OutputCounter_i+1;
				else
					OutputCounter_i <= (others=>'0');
				end if;
			end if;
		end process OUTPUT_COUNTER_PROC;
	end generate;
	
	ParallelOutput : if Maximum(OutputSerialization)=1 generate
		OutputCounter_i <= (others=>'0');
	end generate;
	
--####################################################################
--         HEADER TABLE
--####################################################################

	HEADER_TABLE_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => FlitWidth)
		PORT MAP(
			din    => HeaderInput_i,
			wen    => HeaderInputWrite_i,
			wraddr => HeaderAddrWr_i,
			rdaddr => HeaderAddrRd_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => HeaderOutput_i);

	HeaderInput_i  <= InputData(FlitWidth-1 downto 0);
	HeaderAddrWr_i <= STD_LOGIC_VECTOR(InputCounter_i);
	HeaderAddrRd_i <= MemReadAddr_i when HeaderReadMode_i='1' else 
	                  STD_LOGIC_VECTOR(HeaderAddr_Output_i);
	
	HeaderInputWrite_i <= '1' when (InputDataValid='1' and HeaderConfigMode_i='1') else '0';


--####################################################################
--         MULTI-CAST MANAGEMENT
--####################################################################
	MULTICAST_TABLE_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => FlitWidth/2)
		PORT MAP(
			din    => MultiCastInput_i,
			wen    => MultiCastWrite_i,
			wraddr => MultiCastAddrWr_i,
			rdaddr => MultiCastAddrRd_i, --NextTaskAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => MultiCastOutput_i);

	MultiCastInput_i <= InputData(FlitWidth/2-1 downto 0);
	MultiCastWrite_i <= '1' when (InputDataValid='1' and MultiCastConfigMode_i='1') else '0';
	
	MultiCastAddrWr_i <= STD_LOGIC_VECTOR(InputCounter_i);
	MultiCastAddrRd_i <= MemReadAddr_i when MultiCastReadMode_i='1' else 
	                     STD_LOGIC_VECTOR(resize(UNSIGNED(TaskID_i), MultiCastAddrRd_i'length));

--####################################################################
--         PIPELINE MANAGER
--####################################################################
	-----------------------------------------------------------------
	PipelineManager: entity work.PipelineManager(RTL)
		generic map(
			NbTaskBitWidth => NbTaskBitWidth,
			PipelineLength => PipelineLength
			)
		port map(
			clock         => Clock,
			reset         => Reset,
			BBInputValid  => BBInputValid_i,
--			InputTaskID   => TaskID_i,
			BBOutputValid => BBOutputValid_i--,
--			OutputTaskID  => OutputTaskID_i
			);
			
			
--####################################################################
--         OUTPUT CONTROLLER
--####################################################################
	OutputCtrl_0 : entity work.OutputCtrl(RTL)
		GENERIC MAP(
			FlitWidth       => FlitWidth,
			NbInputFlit     => NbInputFlits,
			NbTask          => NbTask,
			ResultSizes     => OutputSerialization, -- TODO : support more than one output vector
			ComHeader       => ComHeader) -- Number of task an operator can manage
		PORT MAP(
			Rst             => Reset, 
			Clk             => Clock,

			HeaderReadMode    => HeaderReadMode_i,
			MultiCastReadMode => MultiCastReadMode_i,
			InputDataValid    => InputDataValid,
			MemReadAddr       => MemReadAddr_i,

			Start           => PeInputValid_i,
			SendResult      => BBOutputValid_i,
			MultiCast       => MultiCastOutput_i,

			DataIn          => OutputData_i,
			DataInRead      => OutputRead,
			DataInAddr      => OutputRdOffset_i,

			TaskID          => TaskID_i,
			HeaderIn        => HeaderOutput_i,
			HeaderAddr      => HeaderAddr_Output_i,

			DataAvailable   => DataAvailable_i,
			DataOut         => OutputData,
			HeaderOut       => HeaderTransmitted,
			TerminalBusy    => TerminalBusy);
	
	OutputFifoEmpty <= not DataAvailable_i;

end RTL;











