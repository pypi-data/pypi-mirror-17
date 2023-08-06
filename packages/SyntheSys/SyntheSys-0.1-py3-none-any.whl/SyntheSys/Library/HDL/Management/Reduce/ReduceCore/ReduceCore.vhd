
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: ReduceCore
-------------------------------------------------------------------------------
entity ReduceCore is
	generic(
		FlitWidth  : natural                       := 16;
--		NBTask     : natural                       := 5;
		NbInputMax : natural                       := 63;
		ComHeader  : std_logic_vector);
	port (
		Reset, Clock       : IN  std_logic;

		InputData          : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');   -- Input data flit
		InputDataValid     : IN  std_logic;

		HeaderValid        : IN  std_logic;
		PayloadValid       : IN  std_logic;

		HeaderTransmitted  : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		PayloadTransmitted : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');

		Transmitted        : IN  std_logic; -- Request

		TerminalBusy       : OUT std_logic; -- when '1', no input packets can be recieved
		
		OutputData         : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		------------------------------------------
		ReadHeaderFifo     : IN  std_logic;
		OutputRead         : IN  std_logic;
		OutputFifoEmpty    : OUT std_logic;--;
		SendBack           : OUT std_logic
--		DebugVector        : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0')
		);

end ReduceCore;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of ReduceCore is


	constant TypeBitWidth             : natural := 1;
	constant DataIdxBitWidth          : natural := BitWidth(NbInputMax);
	
	constant MaxTaskNumber            : natural := 16;
	constant NbTaskBitWidth           : natural := Minimum(FlitWidth/2-(DataIdxBitWidth+TypeBitWidth), BitWidth(MaxTaskNumber-1));
	constant NBTask                   : natural := 2**(NbTaskBitWidth)-1;
	
	constant DataMemBitWidth          : natural := BitWidth(NBTask*NbInputMax);
	---------------------------
	
	----- MODE CODES - Set up by software 
	constant HEADER_CONFIG_CODE         : std_logic_vector(3 downto 0) :=x"1";
	constant MULTICAST_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"2";
	constant CONSTANTS_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"3";
	constant READ_HEADER_CONFIG_CODE    : std_logic_vector(3 downto 0) :=x"4";
	constant READ_MULTICAST_CONFIG_CODE : std_logic_vector(3 downto 0) :=x"5";
	constant REDUCE_CONFIG_CODE         : std_logic_vector(3 downto 0) :=x"6";
	
	constant HEADER_CONFIG_MESSAGE         : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(HEADER_CONFIG_CODE), FlitWidth));
	constant MULTICAST_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(MULTICAST_CONFIG_CODE), FlitWidth));
	constant CONSTANTS_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(CONSTANTS_CONFIG_CODE), FlitWidth));
	constant READ_HEADER_CONFIG_MESSAGE    : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_HEADER_CONFIG_CODE), FlitWidth));
	constant READ_MULTICAST_CONFIG_MESSAGE : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_MULTICAST_CONFIG_CODE), FlitWidth));
	constant REDUCE_CONFIG_MESSAGE : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(REDUCE_CONFIG_CODE), FlitWidth));
	
--	constant HeaderConfigCode          : std_logic_vector(TypeBitWidth-1 downto 0) :="00";
--	constant MulticastConfigCode       : std_logic_vector(TypeBitWidth-1 downto 0) :="01";
--	constant RunningCode               : std_logic_vector(TypeBitWidth-1 downto 0) :="10";
--	constant ConstantConfigCode        : std_logic_vector(TypeBitWidth-1 downto 0) :="11";
	constant CONFIG_CODE_ZERO          : std_logic_vector(DataIdxBitWidth-1 downto 0) :=(others=>'0');
	constant GROUP_SIZE_CODE           : unsigned(DataIdxBitWidth-1 downto 0) := (others=>'1');
	constant ZEROS_FLIT                : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	
	constant PosBitWidth               : natural := DataIdxBitWidth;

	---------------------------------------------------------------------------
	signal TaskID_i          : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal DataIdx_i         : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal PacketType_i      : std_logic_vector(TypeBitWidth-1 downto 0); -- Encodes modes
	signal DataID_i          : std_logic_vector(FlitWidth/2-1 downto 0) :=(others=>'0');
	signal ConfigCode_i      : std_logic_vector(DataIdxBitWidth-1 downto 0);

	signal MultiCastConfigMode_i, HeaderConfigMode_i, ConstantConfigMode_i, RunningMode_i, ConfigMode_i, ReduceConfigMode_i : std_logic := '0';
	signal HeaderReadMode_i, MultiCastReadMode_i, MemoryReadMode_i  : std_logic;
	signal HeaderRegister_i  : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	signal ConfigMessage_i   : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	
	---------------------------------------------------------------------------
	constant TaskStartAddr    : unsigned(NbTaskBitWidth-1 downto 0) := (others=>'0');
	constant ZEROS            : std_logic_vector(FlitWidth/2-1 downto 0):=(others=>'0');
	
	---------------------------------------------------------------------------
	signal DataIdxCounter_i   : unsigned(DataIdxBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal InputCounter_i     : unsigned(NbTaskBitWidth-1 downto 0);
	signal OutputCnt_i        : unsigned(FlitWidth/2-1 downto 0);
	signal MemReadAddr_i      : std_logic_vector(NbTaskBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal HeaderInputWrite_i : std_logic;
	signal HeaderOutput_i     : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderInput_i      : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderAddr_i       : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal HeaderCounter_i    : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal TaskID_Received_i  : unsigned(NbTaskBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal MultiCastWrite_i   : std_logic;
	signal MultiCastInput_i   : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal MultiCastOutput_i  : std_logic_vector(NbTaskBitWidth-1 downto 0);
	signal MultiCastAddr_i    : std_logic_vector(NbTaskBitWidth-1 downto 0);
--	signal MultiCastCounter_i : unsigned(NbTaskBitWidth-1 downto 0);
	
	---------------------------------------------------------------------------
	signal PipelineManager_OutputHeader_i : std_logic_vector(FlitWidth-1 downto 0);
	signal OutputFifoFull_i : std_logic;
	
	signal OutputDataFIFO_DataIn_i     : std_logic_vector(FlitWidth-1 downto 0);
	signal MemoryOutput_i              : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderOutputFIFO_DataIn_i   : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderOutputFIFO_Write_i    : std_logic;
	signal OutputDataFIFO_Write_i      : std_logic;
	
	signal ReceivedDataIdx_i          : unsigned(DataIdxBitWidth-1 downto 0);
	
	signal OutputOffset_i         : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal WrAddr_i               : std_logic_vector(DataMemBitWidth-1 downto 0);
	signal RdAddr_i               : std_logic_vector(DataMemBitWidth-1 downto 0);
	signal InputDataWrite_i       : std_logic;
	
	signal GroupSize_DataWrite_i  : std_logic;
	signal GroupSize_i            : std_logic_vector(BitWidth(NbInputMax)-1 downto 0);
	
	signal HeaderNext_i           : std_logic;
	signal DataAvailable_i        : std_logic;
	signal OutputData_i           : std_logic_vector(FlitWidth-1 downto 0);
	signal SendGroup_i            : std_logic;
	signal ConstOrVariableValid_i : std_logic;
	
	signal Task_Offset_i, DataIdxCounter_Resized_i, OutputOffset_Resized_i : unsigned(DataMemBitWidth-1 downto 0);

begin  -- RTL

--	RunningMode_i         <= '1' when PacketType_i=RunningCode else '0';
--	HeaderConfigMode_i    <= '1' when PacketType_i=HeaderConfigCode and ConfigCode_i=CONFIG_CODE_ZERO else '0';
--	MultiCastConfigMode_i <= '1' when PacketType_i=MulticastConfigCode and ConfigCode_i=CONFIG_CODE_ZERO else '0';
--	ConstantConfigMode_i  <= '1' when PacketType_i=ConstantConfigCode else '0'; -- Constant config mode can be considered as normal data input. The only difference is that constant status is set.
--	HeaderReadMode_i      <= '1' when (PacketType_i=HeaderConfigCode) and ConfigCode_i/=CONFIG_CODE_ZERO else '0';
--	MultiCastReadMode_i   <= '1' when (PacketType_i=MulticastConfigCode) and ConfigCode_i/=CONFIG_CODE_ZERO else '0';

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
	PacketType_i <= HeaderRegister_i(TypeBitWidth+FlitWidth/2-1 downto FlitWidth/2);
	ConfigCode_i <= HeaderRegister_i(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2);
	TaskID_i     <= HeaderRegister_i(NbTaskBitWidth+DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto DataIdxBitWidth+TypeBitWidth+FlitWidth/2);
	RunningMode_i <= not ConfigMode_i;
	
	
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
				ReduceConfigMode_i    <= '0';
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
							ReduceConfigMode_i    <= '0';
							
						elsif InputData=MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '1';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							ReduceConfigMode_i    <= '0';

						elsif InputData=CONSTANTS_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '1';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							ReduceConfigMode_i    <= '0';
							
						elsif InputData=READ_HEADER_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '1';
							MultiCastReadMode_i   <= '0';
							ReduceConfigMode_i    <= '0';
							
						elsif InputData=READ_MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '1';
							ReduceConfigMode_i    <= '0';
							
						elsif InputData=REDUCE_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							ReduceConfigMode_i    <= '1';
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
	ReduceStatus_0: entity work.ReduceStatus(RTL)
		GENERIC MAP(
			FlitWidth        => FlitWidth,   -- FlitWidth (in bit)
			NbInputMax       => NbInputMax,  -- Flits number
			NBTask           => NBTask)      -- Number of task an operator can manage
		PORT MAP(
			Rst              => Reset,
			Clk              => Clock,
			
			HeaderConfigMode   => HeaderConfigMode_i,
			ReduceConfigMode   => ReduceConfigMode_i,
			ConstantConfigMode => ConstantConfigMode_i,
			RunningMode        => RunningMode_i,

			DataIdx           => DataIdx_i,
			TaskID            => TaskID_i,
--			DataID            => DataID_i,
--			PayloadReceived   => PayloadReceived_i,
--			PayloadValid      => PayloadValid,
			HeaderValid       => HeaderValid,
			
			BufferBusy        => SendBack,
		
			NetworkInputValid => ConstOrVariableValid_i,
			NetworkInput      => InputData,
		
			GroupSize         => GroupSize_i,
			SendGroup         => SendGroup_i);
	
	-----------------------------------------------------------------------------
	DataIdx_i <= STD_LOGIC_VECTOR(DataIdxCounter_i);
	
	---------------------------------------
	GROUP_SIZE_DATA_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => BitWidth(NbInputMax))
		PORT MAP(
			din    => InputData(BitWidth(NbInputMax)-1 downto 0),
			wen    => GroupSize_DataWrite_i,
			wraddr => TaskID_i,
			rdaddr => TaskID_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => GroupSize_i);
	
	GroupSize_DataWrite_i <= '1' when ReduceConfigMode_i='1' and InputDataValid='1' else '0';

	PayloadTransmitted <= STD_LOGIC_VECTOR(resize(UNSIGNED(GroupSize_i), FlitWidth));

	---------------------------------------
	INPUT_DATA_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => DataMemBitWidth,
			SIZE_PORT_MEM  => FlitWidth)
		PORT MAP(
			din    => InputData,
			wen    => InputDataWrite_i,
			wraddr => WrAddr_i,
			rdaddr => RdAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => OutputData_i);

	InputDataWrite_i <= InputDataValid when RunningMode_i='1' else '0';
	
	Task_Offset_i            <= resize(resize(UNSIGNED(TaskID_i), DataMemBitWidth)*NbInputMax, DataMemBitWidth);
	DataIdxCounter_Resized_i <= resize(DataIdxCounter_i, DataMemBitWidth);
	OutputOffset_Resized_i   <= resize(UNSIGNED(OutputOffset_i), DataMemBitWidth);
	
	WrAddr_i <= STD_LOGIC_VECTOR(DataIdxCounter_Resized_i+Task_Offset_i);
	RdAddr_i <= STD_LOGIC_VECTOR(OutputOffset_Resized_i+Task_Offset_i);

	ConstOrVariableValid_i <= InputDataValid and (RunningMode_i or ConstantConfigMode_i or ReduceConfigMode_i);
	-----------------------------------------------------------------------------
	DATA_INDEX_PROC : process(Reset, Clock) is 
	begin
		if (Reset = '1') then
			DataIdxCounter_i  <= (others=>'0');
			ReceivedDataIdx_i <= (others=>'0');
			TaskID_Received_i <= (others=>'0');
		else 
			if rising_edge(Clock) then
				if HeaderValid='1' then
					ReceivedDataIdx_i <= UNSIGNED(InputData(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2));
					DataIdxCounter_i <= UNSIGNED(InputData(DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto TypeBitWidth+FlitWidth/2));
					TaskID_Received_i <= UNSIGNED(InputData(NbTaskBitWidth+DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto DataIdxBitWidth+TypeBitWidth+FlitWidth/2));
				else
					if ConstOrVariableValid_i='1' then --MultiCastConfigMode='1' or HeaderConfigMode_i='1' or ConstantConfigMode_i='1' then
						DataIdxCounter_i <= DataIdxCounter_i+1;
					end if;
				end if;
			end if;
		end if;
	end process DATA_INDEX_PROC;

	-----------------------------------------------------------------------------


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
--         MEMORY READ COUNTER
--####################################################################
	
	
--	DebugVector <= STD_LOGIC_VECTOR(resize(MemReadCounter_i, FlitWidth));
	
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
			wraddr => HeaderAddr_i,
			rdaddr => HeaderAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => HeaderOutput_i);

	HeaderInput_i <= InputData(FlitWidth-1 downto 0);
	HeaderAddr_i  <= STD_LOGIC_VECTOR(TaskID_Received_i + UNSIGNED(HeaderCounter_i) - 1) when RunningMode_i='1' else
	                 STD_LOGIC_VECTOR(InputCounter_i)   when HeaderConfigMode_i='1' else 
	                 MemReadAddr_i                      when HeaderReadMode_i='1' else 
	                 (others=>'0');
	
	HeaderInputWrite_i <= '1' when (InputDataValid='1' and HeaderConfigMode_i='1') else '0';
	
	-----------------------------------------------------------------------------
	-- Select which header to read or write in running mode
--	HEADER_COUNTER_PROC: process (Clock, Reset)
--	begin 
--		if (Reset = '1') then
--			HeaderCounter_i <= (others=>'0');
--		else 
--			if rising_edge(Clock) then 
--				if HeaderValid='1' then
--					HeaderCounter_i <= UNSIGNED(InputData(NbTaskBitWidth+DataIdxBitWidth+TypeBitWidth+FlitWidth/2-1 downto DataIdxBitWidth+TypeBitWidth+FlitWidth/2));
--				else
--					if HeaderNext_i='1' then 
--						HeaderCounter_i <= HeaderCounter_i+1;
--					end if;
--				end if;
--			end if;
--		end if;
--	end process HEADER_COUNTER_PROC;

--####################################################################
--         MULTI-CAST MANAGEMENT
--####################################################################
	MULTICAST_TABLE_RAM : entity work.a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => NbTaskBitWidth)
		PORT MAP(
			din    => MultiCastInput_i,
			wen    => MultiCastWrite_i,
			wraddr => MultiCastAddr_i,
			rdaddr => MultiCastAddr_i, --NextTaskAddr_i,
			clk    => Clock,
			oclk   => Clock,
			dout   => MultiCastOutput_i);

	MultiCastInput_i <= InputData(NbTaskBitWidth-1 downto 0);
	MultiCastWrite_i <= '1' when (InputDataValid='1' and MultiCastConfigMode_i='1') else '0';
	
	MultiCastAddr_i  <= STD_LOGIC_VECTOR(TaskID_Received_i + UNSIGNED(HeaderCounter_i)) when RunningMode_i='1' else
	                    STD_LOGIC_VECTOR(InputCounter_i)   when MultiCastConfigMode_i='1' else 
	                    MemReadAddr_i                      when MultiCastReadMode_i='1' else 
	                    (others=>'0');

	ReduceOutputCtrl_0 : entity work.ReduceOutputCtrl(RTL)
		GENERIC MAP(
			FlitWidth       => FlitWidth,
			NbInputMax      => NbInputMax,
			NbTask          => NbTask,
			ComHeader       => ComHeader) -- Number of task an operator can manage
		PORT MAP(
			Rst             => Reset, 
			Clk             => Clock,

			HeaderReadMode    => HeaderReadMode_i,
			MultiCastReadMode => MultiCastReadMode_i,
			InputDataValid    => InputDataValid,
			MemReadAddr       => MemReadAddr_i,

			SendGroup       => SendGroup_i,
			MultiCast       => MultiCastOutput_i,
			GroupSize       => GroupSize_i,

			DataIn          => OutputData_i,
			DataInRead      => OutputRead,
			DataInAddr      => OutputOffset_i,

			HeaderIn        => HeaderOutput_i,
			HeaderCounter   => HeaderCounter_i,

			DataAvailable   => DataAvailable_i,
			DataOut         => OutputData,
			HeaderOut       => HeaderTransmitted,
			
			TerminalBusy    => TerminalBusy);
	
	OutputFifoEmpty <= not DataAvailable_i;

end RTL;











