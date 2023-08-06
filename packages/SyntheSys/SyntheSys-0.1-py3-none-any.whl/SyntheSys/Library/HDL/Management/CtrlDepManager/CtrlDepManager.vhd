
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_unsigned.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: CtrlDepManager
-------------------------------------------------------------------------------
entity CtrlDepManager is

	generic (
		FlitWidth          : natural := 16; -- FlitWidth (in bit)
		ComHeader          : std_logic_vector;
--		NbTestSets         : natural := 10; -- Number of task an operator can manage
		NbSwitchedData     : natural := 10;
		NbBranches         : natural := 4);

	port (
		Reset, Clock           : IN  std_logic;
		
		Tx                 : OUT  std_logic;
		DataOut            : OUT  std_logic_vector(FlitWidth-1 downto 0);
		AckRx              : OUT  std_logic;
		
		DataIn             : IN std_logic_vector(FlitWidth-1 downto 0);
		Rx                 : IN std_logic;
		AckTx              : IN std_logic);

end CtrlDepManager;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of CtrlDepManager is

	-------------------------------------------------------------------------------
--	constant DATASET_ConfigID          : natural :=0;
--	constant BRANCH_ConfigID           : natural :=1;
--	constant TEST_ConfigID             : natural :=2;
--	constant READ_ConfigID             : natural :=3;
	constant ZEROS_FLIT                : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	-------------------------------------------------------------------------------
	constant TypeBitWidth             : natural := 2;
	constant BranchIdxBitWidth        : natural :=BitWidth(NbBranches);
	constant DataIdxBitWidth          : natural :=BitWidth(NbSwitchedData);
	
	constant MaxTaskNumber            : natural := 64;
	constant NbTestBitWidth           : natural := Minimum(FlitWidth/2-(BranchIdxBitWidth+DataIdxBitWidth+TypeBitWidth), BitWidth(MaxTaskNumber-1));
	constant NbTestSets               : natural := Minimum(2**(NbTestBitWidth)-1, MaxTaskNumber);
	
	
	-------------------------------------------------------------------------------
--	constant BRANCHCONF_CODE          : std_logic_vector(1 downto 0) :="00";
	constant TESTRUN_CODE             : std_logic_vector(1 downto 0) :="01";
	constant DATARUN_CODE             : std_logic_vector(1 downto 0) :="10";
--	constant STOP_CODE                : std_logic_vector(1 downto 0) :="11";
	constant CONFIG_MODE              : std_logic_vector(1 downto 0) :="11";
	
	-------------------------------------------------------------------------------
	type Config_Type is (BRANCHCONF_MODE, DATARUN_MODE, TESTRUN_MODE);
	signal CurrentMode_i : Config_Type := BRANCHCONF_MODE;


	----- MODE CODES - Set up by software 
	constant HEADER_CONFIG_CODE         : std_logic_vector(3 downto 0) :=x"1";
	constant MULTICAST_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"2";
	constant CONSTANTS_CONFIG_CODE      : std_logic_vector(3 downto 0) :=x"3";
	constant READ_HEADER_CONFIG_CODE    : std_logic_vector(3 downto 0) :=x"4";
	constant READ_MULTICAST_CONFIG_CODE : std_logic_vector(3 downto 0) :=x"5";
	constant BRANCHCONF_CONFIG_CODE     : std_logic_vector(3 downto 0) :=x"6";
	
	constant HEADER_CONFIG_MESSAGE         : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(HEADER_CONFIG_CODE), FlitWidth));
	constant MULTICAST_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(MULTICAST_CONFIG_CODE), FlitWidth));
	constant CONSTANTS_CONFIG_MESSAGE      : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(CONSTANTS_CONFIG_CODE), FlitWidth));
	constant READ_HEADER_CONFIG_MESSAGE    : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_HEADER_CONFIG_CODE), FlitWidth));
	constant READ_MULTICAST_CONFIG_MESSAGE : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_MULTICAST_CONFIG_CODE), FlitWidth));
	constant BRANCHCONF_CONFIG_MESSAGE     : std_logic_vector(FlitWidth-1 downto 0) :=STD_LOGIC_VECTOR(resize(UNSIGNED(READ_HEADER_CONFIG_CODE), FlitWidth));
	
	-------------------------------------------------------------------------------
	signal MultiCastConfigMode_i, HeaderConfigMode_i, ConstantConfigMode_i, ConfigMode_i, RunningMode_i : std_logic := '0';
	signal MemoryReadMode_i, HeaderReadMode_i, MultiCastReadMode_i  : std_logic;
	signal HeaderRegister_i    : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	signal ConfigMessage_i     : std_logic_vector(FlitWidth-1 downto 0) :=(others=>'0');
	
	-------------------------------------------------------------------------------
--	signal ConfigMode_i      : std_logic := '0';
	signal DataIn_i          : std_logic_vector(FlitWidth-1 downto 0);
	signal DataReq_i, Busy_i : std_logic := '0';

	signal TestID_i          : std_logic_vector(NbTestBitWidth-1 downto 0);
	signal DataIdx_i         : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal BranchIdx_i       : std_logic_vector(BranchIdxBitWidth-1 downto 0);
	signal Type_i            : std_logic_vector(TypeBitWidth-1 downto 0); -- Encodes modes
	signal DataSetID_i       : std_logic_vector(NbTestBitWidth-1 downto 0);
	signal BranchID_i        : std_logic_vector(BranchIdxBitWidth-1 downto 0);
	signal BranchConfig_i    : std_logic := '0';
	signal ConfWrite_i       : std_logic := '0';
	signal ConfigBusy_i      : std_logic := '0';
	signal ConfigReset_i     : std_logic := '0';

	signal NetworkAdapter_InputData_i          : std_logic_vector(FlitWidth-1 downto 0);
	signal NetworkAdapter_InputDataValid_i     : std_logic := '0';

	signal NetworkAdapter_OutputData_i         : std_logic_vector(FlitWidth-1 downto 0);
	signal NetworkAdapter_OutputRead_i         : std_logic := '0';
	signal NetworkAdapter_OutputFifoEmpty_i    : std_logic := '0';
	signal NetworkAdapter_ReadHeaderFifo_i     : std_logic := '0';

	signal NetworkAdapter_HeaderValid_i        : std_logic := '0';
	signal NetworkAdapter_PayloadValid_i       : std_logic := '0';

	signal NetworkAdapter_Transmitted_i        : std_logic := '0';
	signal NetworkAdapter_HeaderTransmitted_i  : std_logic_vector(FlitWidth-1 downto 0);
	signal NetworkAdapter_PayloadTransmitted_i : std_logic_vector(FlitWidth-1 downto 0);

	signal TestMode_i                : std_logic := '0';
	signal SwitchInputMode_i         : std_logic := '0';
	signal TestWrite_i               : std_logic := '0';
	signal IdxMaxWrite_i             : std_logic := '0';
	signal StopSignal_i              : std_logic := '0';

	signal SelectedTestSet_i         : std_logic_vector(NbTestBitWidth-1 downto 0);
	signal SelectedBranch_i, SelectedBranch_mem_i     : std_logic_vector(BranchIdxBitWidth-1 downto 0);
	signal TestFIFO_DataIn_i, TestFIFO_DataOut_i      : std_logic_vector(NbTestBitWidth+BranchIdxBitWidth-1 downto 0);

	signal SelectedFifoWrite_i       : std_logic := '0';
	signal SelectedFifoEmpty_i       : std_logic := '0';
	signal SelectedFifoRead_i        : std_logic := '0';

	signal DataSetInputWrite_i, branchinputwrite_i      : std_logic := '0';

	signal SENDING_DATA_FIFO_OUTPUT_i, SENDING_HEADER_FIFO_OUTPUT_i     : std_logic_vector(FlitWidth-1 downto 0);
	signal SENDING_DATA_FIFO_READ_i, SENDING_HEADER_FIFO_READ_i       : std_logic := '0';
	signal SENDING_FIFO_EMPTY_i      : std_logic := '0';
	signal SENDING_DATA_FIFO_DataIn_i, SENDING_HEADER_FIFO_DataIn_i     : std_logic_vector(FlitWidth-1 downto 0);

	signal SwitchedData_i, switchedheader_i : std_logic_vector(FlitWidth-1 downto 0);
	signal SwitchSendReq_i           : std_logic := '0';

	signal SendingFifo_Write_i       : std_logic := '0';
	signal SendValidation_i          : std_logic := '0';
	signal SelectHeader_i            : std_logic_vector(FlitWidth-1 downto 0);


begin  -- RTL

	assert (TestID_i'length + BranchIdx_i'length + Type_i'length) <= (FlitWidth/2) report "(TestID_i'length + BranchIdx_i'length + Type_i'length) != (FlitWidth/2)" severity failure;
	
	------------------------------------------------------------
	-- Configuration modes
	NetworkAdapter: entity work.NetworkAdapter(RTL)
		generic map(
			FlitWidth => FlitWidth)
		port map(
			rst                => Reset,
			clk                => Clock,
			
			DataIn             => DataIn,
			Tx                 => Tx,
			AckTx              => AckTx,
			
			DataOut            => DataOut,
			Rx                 => Rx,
			AckRx              => AckRx,
			
			InputData          => NetworkAdapter_InputData_i,
			InputDataValid     => NetworkAdapter_InputDataValid_i,
			
			OutputData         => SENDING_DATA_FIFO_OUTPUT_i,
			OutputRead         => SENDING_DATA_FIFO_READ_i,
			OutputFifoEmpty    => SENDING_FIFO_EMPTY_i,
			ReadHeaderFifo     => SENDING_HEADER_FIFO_READ_i,
			
			HeaderValid        => NetworkAdapter_HeaderValid_i,
			PayloadValid       => NetworkAdapter_PayloadValid_i,
			
			Transmitted        => open,
			HeaderTransmitted  => SENDING_HEADER_FIFO_OUTPUT_i,
			PayloadTransmitted => STD_LOGIC_VECTOR(TO_UNSIGNED(1, FlitWidth)),
		
			SendBack           => '0', -- when '1', input packets are sent back to output port
			TerminalBusy       => '0' -- when '1', no input packets can be recieved
			);
	
	
	CurrentMode_i <= DATARUN_MODE when Type_i=TESTRUN_CODE else 
	                 TESTRUN_MODE when Type_i=DATARUN_CODE else 
	                 BRANCHCONF_MODE;
	
	ConfigModProcess : process(Clock)
	begin
		if rising_edge(Clock) then
			if NetworkAdapter_HeaderValid_i='1' then
				ConfigMessage_i       <= ZEROS_FLIT;
				HeaderConfigMode_i    <= '0';
				MultiCastConfigMode_i <= '0';
				ConstantConfigMode_i  <= '0';
				HeaderReadMode_i      <= '0';
				MultiCastReadMode_i   <= '0';
			else
				if CurrentMode_i=BRANCHCONF_MODE and ConfigMessage_i=ZEROS_FLIT then
					if NetworkAdapter_InputDataValid_i='1' then
						ConfigMessage_i <= NetworkAdapter_InputData_i;
						if NetworkAdapter_InputData_i=HEADER_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '1';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							
						elsif NetworkAdapter_InputData_i=MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '1';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';

						elsif NetworkAdapter_InputData_i=CONSTANTS_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '1';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
							
						elsif NetworkAdapter_InputData_i=READ_HEADER_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '1';
							MultiCastReadMode_i   <= '0';
							
						elsif NetworkAdapter_InputData_i=READ_MULTICAST_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '1';
							
						elsif NetworkAdapter_InputData_i=BRANCHCONF_CONFIG_MESSAGE then
							HeaderConfigMode_i    <= '0';
							MultiCastConfigMode_i <= '0';
							ConstantConfigMode_i  <= '0';
							HeaderReadMode_i      <= '0';
							MultiCastReadMode_i   <= '0';
						end if;
					end if;
				end if;
			end if;
		end if;
	end process ConfigModProcess;
--	DataID_i <= TO_INTEGER(UNSIGNED(BranchIdx_i)) when TestID_i=STD_LOGIC_VECTOR(TO_UNSIGNED(0, TestID_i'length)) else STD_LOGIC_VECTOR(TO_UNSIGNED(0, BranchIdx_i'length));

	-------------------------------------------------------------------------------
	TestSets_0 : ENTITY work.TestSets(RTL)
		GENERIC MAP(
			FlitWidth        => FlitWidth,
			NbTestSets       => NbTestSets, -- Number of test sets 
			NbBranches       => NbBranches) -- Number of tested data per Tests
		PORT MAP(
			Rst              => Reset,
			Clk              => Clock,
		
			ConfMode         => BranchConfig_i, -- for the reset of status RAM
			ConfWrite        => ConfWrite_i, -- for the reset of status RAM

			Input            => NetworkAdapter_InputData_i,
			InputID          => TestID_i,
			InputIdx         => BranchIdx_i,
			InputWrite       => TestWrite_i,
			IdxMaxWrite      => IdxMaxWrite_i,
--			IdxMaxConf       => IdxMaxConf_i,

			SelectedBranch   => SelectedBranch_mem_i,
			TakeBranch       => SelectedFifoWrite_i);
	
	
	ConfWrite_i   <= NetworkAdapter_InputDataValid_i when CurrentMode_i=BRANCHCONF_MODE else '0'; 
	IdxMaxWrite_i <= StopSignal_i;--NetworkAdapter_InputDataValid_i when StopSignal_i='1' else '0';
	
	TestFIFO_DataIn_i <= TestID_i & SelectedBranch_mem_i;
	SelectedTestSet_i <= TestFIFO_DataOut_i(TestID_i'length+SelectedBranch_i'length-1 downto SelectedBranch_i'length);
	SelectedBranch_i  <= TestFIFO_DataOut_i(SelectedBranch_i'length-1 downto 0);
	-----------------------------------------------------------------
	TestFIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 16,
			largeur => TestFIFO_DataIn_i'length 
			)
		port map(
			reset => Reset,
			clock_in => Clock,
			data_in => TestFIFO_DataIn_i,
			rd => SelectedFifoRead_i,
			ack_rd => open,
			clock_out => Clock,
			data_out => TestFIFO_DataOut_i,
			wr => SelectedFifoWrite_i,
			ack_wr => open,
			IsEmpty => SelectedFifoEmpty_i,
			IsFull => open); -- WARNING !!!! INSURE SAFETY
			
	-----------------------------------------------------------------------------
	-- Assign payload and TaskID and DataIdx from input flits
	Set_ID_Idx: process (Clock, Reset)
	begin 
		if rising_edge(Clock) then
			if (Reset = '1') then
				TestID_i    <= (others=>'0');
				BranchIdx_i <= (others=>'0');
				DataIdx_i   <= (others=>'0');
--				Type_i      <= (others=>'0');
			else 
				-------------------------------------------------------------
				if NetworkAdapter_HeaderValid_i='1' then
					TestID_i    <= NetworkAdapter_InputData_i(TestID_i'length+BranchIdx_i'length+Type_i'length+FlitWidth/2-1 downto BranchIdx_i'length+Type_i'length+FlitWidth/2);
					BranchIdx_i <= NetworkAdapter_InputData_i(BranchIdx_i'length+Type_i'length+FlitWidth/2-1 downto Type_i'length+FlitWidth/2);
					DataIdx_i   <= NetworkAdapter_InputData_i(DataIdx_i'length+Type_i'length+FlitWidth/2-1 downto Type_i'length+FlitWidth/2);
				elsif NetworkAdapter_InputDataValid_i='1' then
					DataIdx_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(DataIdx_i))+1, DataIdx_i'length));
				end if;
				-------------------------------------------------------------
				
			end if;
		end if;
	end process Set_ID_Idx;
	
	Type_i   <= NetworkAdapter_InputData_i(Type_i'length+FlitWidth/2-1 downto FlitWidth/2);
	------------------------------------------------------------


	-------------------------------------------------------------------------------
	BufferedSwitch : ENTITY work.BufferedSwitch(RTL)
		GENERIC MAP (
			FlitWidth         => FlitWidth,
			NbSwitchedData    => NbSwitchedData,
--			NbTestSets        => NbTestSets,
			NbBranches        => NbBranches)

		PORT MAP (
			Rst               => Reset, 
			Clk               => Clock,
		
			InputTestSet      => TestID_i,
			DataInput         => NetworkAdapter_InputData_i,
			DataInputIdx      => DataIdx_i,
			DataInputWrite    => DataSetInputWrite_i,
			SwitchInputMode   => SwitchInputMode_i,
			TestMode          => TestMode_i,
--			DataInputBusy     => ,-- 
			
			ConfigInput       => NetworkAdapter_InputData_i,
--			ConfigBranch      =>,
			ConfigWrite       => BranchInputWrite_i,
			ConfigMode        => BranchConfig_i,
			ConfigReset       => ConfigReset_i,
			StopSignal        => StopSignal_i,
			
			SelectedFifoEmpty => SelectedFifoEmpty_i,
			SelectedFifoRead  => SelectedFifoRead_i,
			SelectedTestSet   => SelectedTestSet_i,
			SelectedBranch    => SelectedBranch_i,
		
			SwitchedData      => SwitchedData_i,
			SwitchedHeader    => SwitchedHeader_i,
			SwitchSendReq     => SwitchSendReq_i,
			
			SelectHeader      => SelectHeader_i,
			SendValidation    => SendValidation_i);
			
	ConfigReset_i <= BranchConfig_i and NetworkAdapter_HeaderValid_i;
			
	SENDING_HEADER_FIFO_DataIn_i <= SelectHeader_i when SendValidation_i='1' else SwitchedHeader_i;
	SENDING_DATA_FIFO_DataIn_i   <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(SelectedBranch_i)), SwitchedData_i'length)) when SendValidation_i='1' else SwitchedData_i;
	
	-----------------------------------------------------------------
	SENDING_HEADER_FIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 16,
			largeur => FlitWidth 
			)
		port map(
			reset     => Reset,
			clock_out => Clock,
			clock_in  => Clock,
			data_in   => SENDING_HEADER_FIFO_DataIn_i,
			wr        => SendingFifo_Write_i,
			IsEmpty   => open, -- use SENDING_DATA_FIFO's signal instead
			rd        => SENDING_HEADER_FIFO_READ_i,
			data_out  => SENDING_HEADER_FIFO_OUTPUT_i,
			ack_wr    => open,
			ack_rd    => open,
			IsFull    => open); -- WARNING !!!! INSURE SAFETY
	
	SendingFifo_Write_i <= SwitchSendReq_i or SendValidation_i;
	-----------------------------------------------------------------
	SENDING_DATA_FIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 16,
			largeur => FlitWidth 
			)
		port map(
			reset     => Reset,
			clock_out => Clock,
			clock_in  => Clock,
			data_in   => SENDING_DATA_FIFO_DataIn_i,
			wr        => SendingFifo_Write_i,
			IsEmpty   => SENDING_FIFO_EMPTY_i,
			rd        => SENDING_DATA_FIFO_READ_i,
			data_out  => SENDING_DATA_FIFO_OUTPUT_i,
			ack_wr    => open,
			ack_rd    => open,
			IsFull    => open); -- WARNING !!!! INSURE SAFETY
			
			
	BranchConfig_i <= '1' when CurrentMode_i=BRANCHCONF_MODE else '0';
	-----------------------------------------------------------------------------
	-- Assign tables configuration inputs
	BranchInputWrite_i  <= NetworkAdapter_InputDataValid_i when CurrentMode_i=BRANCHCONF_MODE else '0';
	DataSetInputWrite_i <= NetworkAdapter_InputDataValid_i when CurrentMode_i=DATARUN_MODE else '0';
	TestWrite_i         <= NetworkAdapter_InputDataValid_i when CurrentMode_i=TESTRUN_MODE else '0';
	SwitchInputMode_i   <= '1' when CurrentMode_i=DATARUN_MODE else '0';
	TestMode_i          <= '1' when CurrentMode_i=TESTRUN_MODE else '0';
	
end RTL;











