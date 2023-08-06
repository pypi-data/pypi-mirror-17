
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_unsigned.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: BufferedSwitch
-------------------------------------------------------------------------------
entity BufferedSwitch is

	generic(
		FlitWidth          : natural := 16; -- FlitWidth (in bit)
		NbSwitchedData     : natural := 10;
		NbBranches         : natural := 4);

	port(
		Rst, Clk           : IN  std_logic;
		
		InputTestSet       : IN  std_logic_vector;
		DataInput          : IN  std_logic_vector(FlitWidth-1 downto 0);
		DataInputWrite     : IN  std_logic;
		DataInputIdx       : IN  std_logic_vector(BitWidth(NbSwitchedData)-1 downto 0);
		SwitchInputMode    : IN  std_logic;
		TestMode           : IN  std_logic;
--		TestSet            : IN  std_logic_vector(natural(ceil(log2(real(NbTestSets))))-1 downto 0); -- test set 
--		Branch             : IN  std_logic_vector(natural(ceil(log2(real(NbBranches))))-1 downto 0); 
--		SendBusy           : IN  std_logic;
		
--		DataInputBusy      : OUT std_logic;
--		BranchWrite        : IN  std_logic;
		ConfigReset        : IN  std_logic;
		ConfigInput        : IN  std_logic_vector(FlitWidth-1 downto 0);
--		ConfigBranch       : IN  std_logic_vector(natural(ceil(log2(real(NbBranches))))-1 downto 0); -- test set 
--		ConfigDataSelector : IN  std_logic_vector(natural(ceil(log2(real(NbSwitchedData))))-1 downto 0); -- test set 
		ConfigWrite        : IN  std_logic;
		ConfigMode         : IN  std_logic;
		StopSignal         : OUT std_logic;
		
		--From Switch FIFO
		SelectedFifoEmpty  : IN  std_logic;
		SelectedFifoRead   : OUT std_logic;
		SelectedTestSet    : IN  std_logic_vector;
		SelectedBranch     : IN  std_logic_vector(BitWidth(NbBranches)-1 downto 0);
		
		-- to Network Adapter
		SwitchedData       : OUT std_logic_vector(FlitWidth-1 downto 0);
		SwitchedHeader     : OUT std_logic_vector(FlitWidth-1 downto 0);
		SwitchSendReq      : OUT std_logic;
		
		SelectHeader       : OUT std_logic_vector(FlitWidth-1 downto 0);
		SendValidation     : OUT std_logic);

end BufferedSwitch;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of BufferedSwitch is

	signal Clk_N                     : std_logic:='0';
	-------------------------------------------------------------------------------
	constant TypeBitWidth             : natural := 1;
	constant BranchIdxBitWidth      : natural :=BitWidth(NbBranches);
	constant DataIdxBitWidth       : natural :=BitWidth(NbSwitchedData);
	
	constant MaxTaskNumber            : natural := 64;
	constant NbTestSetsBitWidth           : natural := Minimum(FlitWidth/2-(BranchIdxBitWidth+DataIdxBitWidth+TypeBitWidth), BitWidth(MaxTaskNumber-1));
	constant NbTestSets                   : natural := Minimum(2**(NbTestSetsBitWidth)-1, MaxTaskNumber);
	
	-------------------------------------------------------------------------------
	constant STOP_CODE               : std_logic_vector(TypeBitWidth-1 downto 0):=(others=>'1');
	constant NO_MORE_DATA            : std_logic_vector(DataIdxBitWidth-1 downto 0):=(others=>'0');
	-------------------------------------------------------------------------------
--	
--	signal Idx_i                     : std_logic_vector(BranchIdxBitWidth-1 downto 0);
	signal DataSetReadID_i           : std_logic_vector(NbTestSetsBitWidth-1 downto 0);
	signal BranchAddr_i              : std_logic_vector(NbTestSetsBitWidth-1 downto 0);
	signal DataSelector_i            : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal SendingCounter_i          : natural := 0;

	signal ConfigWriteAddr_i         : std_logic_vector(NbTestSetsBitWidth-1 downto 0);
	signal ConfAddrCounter_i         : natural;
	signal DataSet_RefIn_i           : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal DataSet_StatusIn_i        : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal DataSet_RefOut_i          : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal DataSet_StatusOut_i       : std_logic_vector(DataIdxBitWidth-1 downto 0);
	signal DataSet_StatusWrite_i     : std_logic;
	signal RefWrite_i, RefReset_Reg_i: std_logic;
	signal StopSignal_i              : std_logic;
	signal ConfigWrite_i             : std_logic;
	
	signal SelectHeader_Write_i      : std_logic;
	signal SelectHeader_i            : std_logic_vector(FlitWidth-1 downto 0);
	
	signal SetAddr_i                 : std_logic_vector(NbTestSetsBitWidth-1 downto 0);
	signal DataSetStatus_input_i, DataSetStatus_output_i : std_logic_vector(2*BranchIdxBitWidth-1 downto 0);
	
	signal ConfigWrites_i            : std_logic_vector(NbTestSets-1 downto 0);
	signal RefReset_i                : std_logic := '0';
	type HEADER_ARRAY is array (natural range <> ) of std_logic_vector(FlitWidth-1 downto 0);
	signal SwitchedHeaders_i         : HEADER_ARRAY(NbTestSets-1 downto 0) := (others=>(others=>'0'));
	
	signal DataCounter_i, DataSel_i  : natural := 0;
	signal BranchIdx_i               : std_logic_vector(BranchIdxBitWidth-1 downto 0);
	signal ConfIdxCounter_i          : natural := 0;
	
	type SwitchBufferStateType is (IDLE_STATE, SELECT_STATE, SENDING_STATE, VALIDATION_STATE, BUFFERING_STATE, BUFFERING_SELECTED_STATE);
	signal CurrentState_i : SwitchBufferStateType := IDLE_STATE;
	
begin  -- RTL
	
	Clk_N <= not Clk;
	
	-------------------------------------------------
	Headers_PerDataAndBranch : for i in 0 to NbTestSets-1 generate
		-------------------------------------------
		Headers : entity work.DataBuffers(RTL)
			GENERIC MAP(
				DataWidth        => FlitWidth,    -- FlitWidth (in bit)
				NbIndexedData    => NbBranches, 
				NbAddr           => NbSwitchedData)-- Number of Headers the table can manage
			PORT MAP(
				Rst              => Rst,
				Clk              => Clk,

				ReadID           => DataSelector_i,
				Index            => BranchIdx_i,
				-- Configuration port
				WriteID          => DataSelector_i,
				InputWrite       => ConfigWrites_i(i),
				InputData        => ConfigInput,

				-- Running port
				OutputData       => SwitchedHeaders_i(i));
	end generate;
	
	SwitchedHeader <= SwitchedHeaders_i(TO_INTEGER(UNSIGNED(SelectedTestSet)));
	BranchIdx_i    <= STD_LOGIC_VECTOR(TO_UNSIGNED(ConfIdxCounter_i, BranchIdx_i'length)) when ConfigMode='1' else SelectedBranch;
	
	-------------------------------------------------
	ConfigWriteDemux : for i in 0 to NbTestSets-1 generate
		ConfigWrites_i(i) <= ConfigWrite when TO_INTEGER(UNSIGNED(InputTestSet))=i and StopSignal_i='0' else '0';
	end generate;
	RefReset_i   <= '1' when ConfigReset='1' or (ConfigWrite='1' and StopSignal_i='1') else '0';
	StopSignal_i <= '1' when ConfigInput(TypeBitWidth+FlitWidth/2-1 downto FlitWidth/2)=STOP_CODE else '0';
	StopSignal   <= StopSignal_i and ConfigWrite;
	-----------------------------------------------------------------------------
	RegRefResetProcess: process (Clk_N)
	begin 
		if rising_edge(Clk_N) then
			RefReset_Reg_i <= RefReset_i;
		end if;
	end process RegRefResetProcess;
	-----------------------------------------------------------------------------
--	RegConfigWriteProcess: process (Clk)
--	begin 
--		if rising_edge(Clk) then
			ConfigWrite_i <= ConfigWrite;
--		end if;
--	end process RegConfigWriteProcess;
	
	ConfigWriteAddr_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(ConfAddrCounter_i, ConfigWriteAddr_i'length));
	-----------------------------------------------------------------------------
	ConfigAddressProcess: process (Clk, ConfigMode)
	begin 
		if rising_edge(Clk) then
			if (ConfigMode = '0') then
				ConfAddrCounter_i <= 0; --DataSelector
				ConfIdxCounter_i  <= 0; --Branch
			else 
				-------------------------------------------------------------
				if StopSignal_i='1' then
					-- TASKSET STOP CODE
					if ConfigWrite='1' and ConfigReset='0' then
						ConfAddrCounter_i <= ConfAddrCounter_i+1;-- Jump to next test set
					end if;
					ConfIdxCounter_i  <= 0;-- Jump to next test set
				else
					if ConfigWrite='1' and ConfigReset='0' then
						ConfIdxCounter_i <= ConfIdxCounter_i+1;
					end if;
				end if;
				-------------------------------------------------------------
			end if;
		end if;
	end process ConfigAddressProcess;
	-------------------------------------------------------------------------------
	-------------------------------------------------------------------------------

	-------------------------------------------------------------------------------
	-- SWITCH BUFFER
	-------------------------------------------------------------------------------
	DataSets : entity work.DataBuffers(RTL)
		GENERIC MAP(
			DataWidth        => FlitWidth,    -- FlitWidth (in bit)
			NbIndexedData    => NbSwitchedData, 
			NbAddr           => NbTestSets)-- Number of set the table can manage
		PORT MAP(
			Rst              => Rst,
			Clk              => Clk,

			Index            => DataSelector_i,
			ReadID           => DataSetReadID_i,
			WriteID          => InputTestSet,
			
			-- Configuration port
			InputWrite       => DataInputWrite,
			InputData        => DataInput,

			-- Running port
			OutputData       => SwitchedData);
			
	DataSetReadID_i <= InputTestSet when SwitchInputMode='1' else SelectedTestSet;
	-- DataSetReadID_i <= SelectedTestSet;
	-----------------------------------------------------------------------------
	DATASET_STATUS_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestSetsBitWidth,
			SIZE_PORT_MEM  => DataIdxBitWidth) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => DataSet_StatusIn_i,
			wen    => DataSet_StatusWrite_i,
			wraddr => SetAddr_i,
			rdaddr => SetAddr_i, --NextTaskAddr_i,
			clk    => Clk_N,
			oclk   => Clk_N,
			dout   => DataSet_StatusOut_i);
			
	-----------------------------------------------------------------------------
	SendCountProc: process (Clk, Rst)
	begin 
		if rising_edge(Clk) then
			if (Rst = '1') then
				SendingCounter_i  <= 0; 
			else 
				CASE CurrentState_i is
					when SENDING_STATE =>
						if SendingCounter_i/=0 then
							SendingCounter_i <= SendingCounter_i-1; -- UNCOUNT
						end if;
					when others =>
						if TO_INTEGER(UNSIGNED(DataSet_StatusOut_i))=0 then
							SendingCounter_i <= 0;
						else
							SendingCounter_i <= TO_INTEGER(UNSIGNED(DataSet_StatusOut_i))-1;
						end if;
				END CASE;
			end if;
		end if;
	end process SendCountProc;
	
	-----------------------------------------------------------------------------
	DataSet_StatusIn_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(DataSet_StatusOut_i))+1, DataSet_StatusOut_i'length)) when (CurrentState_i=BUFFERING_STATE or CurrentState_i=BUFFERING_SELECTED_STATE) and DataInputWrite='1' else (others=>'0');
	
	DataSet_StatusWrite_i <= DataInputWrite when (CurrentState_i=BUFFERING_STATE or CurrentState_i=BUFFERING_SELECTED_STATE) and ConfigMode='0' else 
	                         '1' when CurrentState_i=SENDING_STATE and ConfigMode='0' else 
	                         ConfigWrite when ConfigMode='1' else 
	                         '0';
	
	-----------------------------------------------------------------------------
	DATASET_REFERENCE_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestSetsBitWidth,
			SIZE_PORT_MEM  => DataIdxBitWidth) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => DataSet_RefIn_i,
			wen    => RefWrite_i,
			wraddr => SetAddr_i,
			rdaddr => SetAddr_i, --NextTaskAddr_i,
			clk    => Clk_N,
			oclk   => Clk_N,
			dout   => DataSet_RefOut_i);
			
	RefWrite_i <= ConfigWrite or RefReset_Reg_i when StopSignal_i='0' else RefReset_Reg_i;
	-- TODO : RESET ALL THE MEMORIES
--	ConfigRef : for k in 0 to NbBranches-1 generate
--		DataSet_RefIn_i(k) <= '0' when RefReset_Reg_i='1' else '1' when k=ConfIdxCounter_i else DataSet_RefOut_i(k);
--	end generate;
	DataSet_RefIn_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(DataSet_RefOut_i))+1, DataSet_RefIn_i'length)) when ConfigMode='1' and RefReset_Reg_i='0' else (others=>'1');
	
	-----------------------------------------------------------------------------
	-- Internal states : IDLE_STATE, SELECT_STATE, SENDING_STATE, BUFFERING_STATE, BUFFERING_SELECTED_STATE
	StateAssignmentFSM: process(Clk, Rst)
	begin
		if (Rst = '1') then
			CurrentState_i <= IDLE_STATE;
		else 
			if rising_edge(Clk) then 
				case CurrentState_i is -- Assignments for FSM ConfigState
					when IDLE_STATE => 
						if SelectedFifoEmpty='0' and ConfigMode='0' then
							CurrentState_i <= SELECT_STATE;
						else
							if SwitchInputMode='1' then
								CurrentState_i <= BUFFERING_STATE;
							else
								CurrentState_i <= IDLE_STATE;
							end if;
						end if;
					when SELECT_STATE => 
						if DataSet_RefOut_i = DataSet_StatusOut_i then
							CurrentState_i <= SENDING_STATE; -- Every data is buffered
						else -- waiting for data to be sent
							if SwitchInputMode='1' then
								CurrentState_i <= BUFFERING_SELECTED_STATE;
							else
								CurrentState_i <= SELECT_STATE;
							end if;
						end if;
					when SENDING_STATE => -- Send every data
						if SendingCounter_i=0 then 
							CurrentState_i <= VALIDATION_STATE;
						else
							CurrentState_i <= SENDING_STATE;
						end if;
					when VALIDATION_STATE =>
						CurrentState_i <= IDLE_STATE;
					when BUFFERING_STATE => 
						if SwitchInputMode='0' then
							CurrentState_i <= IDLE_STATE;
						else
							if SelectedFifoEmpty='0' and ConfigMode='0' then
								CurrentState_i <= SELECT_STATE;
							else
								CurrentState_i <= BUFFERING_STATE;
							end if;
						end if;
					when BUFFERING_SELECTED_STATE => 
						if SwitchInputMode='0' then
							CurrentState_i <= SELECT_STATE;
						elsif DataSet_RefOut_i = DataSet_StatusOut_i then
							CurrentState_i <= SENDING_STATE; -- Every data is buffered
						else
							CurrentState_i <= BUFFERING_SELECTED_STATE;
						end if;
					when others => null;
				end case;
				
			end if;
		end if;
	
	end process StateAssignmentFSM;
	
	-----------------------------------------------------------------------------
	-- Output assignments
	ModeAssignmentFSM: process(CurrentState_i, SelectedFifoEmpty, SelectedTestSet, InputTestSet, DataCounter_i, ConfigWriteAddr_i)
	begin
		if Rst='1' then
			SetAddr_i        <= (others=>'0');
--			DataInputBusy    <= '0';
			SelectedFifoRead <= '0';
			SwitchSendReq    <= '0';
--			Idx_i            <= (others=>'0');
		else
			case CurrentState_i is -- Assignments for FSM ConfigState
				when IDLE_STATE =>
					SetAddr_i <= ConfigWriteAddr_i;
--					DataInputBusy <= '0';
					if SelectedFifoEmpty='0' and ConfigMode='0' then
						SelectedFifoRead <= '1';
					else
						SelectedFifoRead <= '0';
					end if;
					SwitchSendReq <= '0';
					SendValidation   <= '0';
--					Idx_i <= DataInputIdx;
				when SELECT_STATE =>
					SetAddr_i <= SelectedTestSet;
--					DataInputBusy <= '0';
					SelectedFifoRead <= '0';
--					Idx_i <= DataInputIdx;
					SwitchSendReq <= '0';
					SendValidation   <= '0';
				when SENDING_STATE =>
					SetAddr_i <= SelectedTestSet;
--					DataInputBusy <= '0';
					SelectedFifoRead <= '0';
					if DataSet_RefOut_i = DataSet_StatusOut_i then
						SwitchSendReq <= '1'; -- Every data is buffered / TRANSITION TO SELECT_STATE
					else -- waiting for data to be sent
						SwitchSendReq <= '0';
					end if;
					SendValidation   <= '0';
				when VALIDATION_STATE => 
					SetAddr_i        <= InputTestSet;
					SelectedFifoRead <= '0';
					SwitchSendReq    <= '1';
					SendValidation   <= '1';
				when BUFFERING_STATE =>
					SetAddr_i <= InputTestSet;
--					DataInputBusy <= '1';
					SelectedFifoRead <= '0';
					SwitchSendReq    <= '0';
					SendValidation   <= '0';
--					Idx_i <= DataInputIdx;
				when BUFFERING_SELECTED_STATE =>
					SetAddr_i <= InputTestSet;
					SelectedFifoRead <= '0';
					if DataSet_RefOut_i = DataSet_StatusOut_i and SwitchInputMode='1' then
						SwitchSendReq <= '1'; -- Every data is buffered / TRANSITION TO SELECT_STATE
					else -- waiting for data to be sent
						SwitchSendReq <= '0';
					end if;
					SendValidation   <= '0';
				when others => 
					SetAddr_i        <= InputTestSet;
					SelectedFifoRead <= '0';
					SwitchSendReq    <= '0';
					SendValidation   <= '0';
			end case;
		end if;
	
	end process ModeAssignmentFSM;
			
	-----------------------------------------------------------------------------
	DataSelector_i <= STD_LOGIC_VECTOR(TO_UNSIGNED(SendingCounter_i, DataSelector_i'length)) when CurrentState_i=SENDING_STATE else DataInputIdx;--STD_LOGIC_VECTOR(TO_UNSIGNED(DataSel_i, DataSelector_i'length));
	DataSel_i <= TO_INTEGER(UNSIGNED(DataInputIdx));--TO_INTEGER(UNSIGNED(DataSet_StatusOut_i)) when TestMode='1' else 
	
	-----------------------------------------------------------------------------

	-----------------------------------------------------------------------------
	SELECT_HEADER_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestSetsBitWidth,
			SIZE_PORT_MEM  => FlitWidth) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => ConfigInput,
			wen    => SelectHeader_Write_i,
			wraddr => InputTestSet,
			rdaddr => InputTestSet, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => SelectHeader);
			
	SelectHeader_Write_i <= ConfigWrite when StopSignal_i='1' else '0';
	
end RTL;











