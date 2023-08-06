
library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_unsigned.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: TestSets
-------------------------------------------------------------------------------
entity TestSets is
	generic (
		FlitWidth          : natural := 16; -- FlitWidth (in bit)
		NbTestSets         : natural := 100; -- Number of test set an operator can manage
		NbBranches         : natural := 10);
	port (
		Rst, Clk        : IN  std_logic;
		
		ConfMode        : IN  std_logic; -- for reset of status RAM
		ConfWrite       : IN  std_logic; -- for reset of status RAM
		
		Input           : IN  std_logic_vector(FlitWidth-1 downto 0);
		InputID         : IN  std_logic_vector(natural(ceil(log2(real(NbTestSets))))-1 downto 0);
		InputIdx        : IN  std_logic_vector(natural(ceil(log2(real(NbBranches))))-1 downto 0);
		InputWrite      : IN  std_logic;
		IdxMaxWrite     : IN  std_logic;
--		IdxMaxConf      : IN  std_logic_vector(natural(ceil(log2(real(NbBranches))))-1 downto 0);

		SelectedBranch  : OUT std_logic_vector(natural(ceil(log2(real(NbBranches))))-1 downto 0);
		TakeBranch      : OUT std_logic);
end entity TestSets;
			
-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of TestSets is

--	signal Clk_N                     : std_logic:='0';
	
	constant NbTestBitWidth          : natural :=natural(ceil(log2(real(NbTestSets))));
	constant IdxBitWidth             : natural :=natural(ceil(log2(real(NbBranches))));

	signal TestedResult_i            : std_logic:='0';
--	signal TestReq_i                 : std_logic:='0';
	
	signal Index_i                   : std_logic_vector(IdxBitWidth-1 downto 0);
	signal TestID_i                  : std_logic_vector(NbTestBitWidth-1 downto 0);
	signal TestGroup_CntWrite_i      : std_logic:='0';
	signal TestGroup_CntIn_i         : std_logic_vector(IdxBitWidth-1 downto 0);
	signal TestGroup_CntOut_i        : std_logic_vector(IdxBitWidth-1 downto 0);
	signal IdxMaxOut_i               : std_logic_vector(IdxBitWidth-1 downto 0);
	signal TestGroup_Counter_i, IdxMax_i, SavedTestGroup_Cnt_i : natural :=0;

	signal TestGroup_StatusWrite_i   : std_logic:='0';
	signal TestGroup_StatusIn_i      : std_logic_vector(NbBranches-1 downto 0);
	signal TestGroup_StatusOut_i     : std_logic_vector(NbBranches-1 downto 0);
--	signal TestGroup_DataValidIn_i   : std_logic_vector(NbBranches-1 downto 0);

	signal TestGroup_ResultWrite_i   : std_logic:='0';
	signal TestGroup_ResultIn_i      : std_logic_vector(NbBranches-1 downto 0);
	signal TestGroup_ResultOut_i     : std_logic_vector(NbBranches-1 downto 0);
	signal TakeBranch_i              : std_logic:='0';
	
	signal TestGroup_InvalidWrite_i  : std_logic:='0';
	signal TestGroup_InvalidIn_i     : std_logic_vector(NbBranches-1 downto 0);
	signal TestGroup_InvalidOut_i    : std_logic_vector(NbBranches-1 downto 0);
	
	signal IdxMaxConf_i              : std_logic_vector(IdxBitWidth-1 downto 0);
	signal IdxMaxCounter_i           : natural := 0;
	
	constant AllOnes                 : std_logic_vector(NbBranches-1 downto 0) := (others=>'1');
	constant ZEROS                   : std_logic_vector(FlitWidth-1 downto 0)  := (others=>'0');
	-------------------------------------------------------------------------------
	type FSM_Type is (INCOMING_STATE, UPDATESTATUS_STATE, TEST_STATE, INCCOUNTER_STATE, RESET_STATE);
	signal CurState_i : FSM_Type := INCOMING_STATE;
	-------------------------------------------------------------------------------

begin 

	-------------------------------------------------------------------------------
	-- STORE TEST RESULT
	-----------------------------------------------------------------------------
	TESTGROUP_RESULT_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestBitWidth,
			SIZE_PORT_MEM  => NbBranches) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => TestGroup_ResultIn_i,
			wen    => TestGroup_ResultWrite_i,
			wraddr => TestID_i,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => TestGroup_ResultOut_i);
			
	 -- HERE IS THE TEST : TEST RESULT IS STORED HERE.
	SetupResults : for i in 0 to NbBranches-1 generate
		TestGroup_ResultIn_i(i) <= '1' when ConfMode='0' and TO_INTEGER(UNSIGNED(InputIdx))=i and Input/=ZEROS else 
		                           '0' when (ConfMode='0' and TO_INTEGER(UNSIGNED(InputIdx))=i and Input=ZEROS) or ConfMode='1' else 
		                           TestGroup_ResultOut_i(i);
	end generate;
	
	TestGroup_ResultWrite_i <= '1' when CurState_i=UPDATESTATUS_STATE else ConfWrite;
	TestedResult_i          <= TestGroup_ResultOut_i(TO_INTEGER(UNSIGNED(Index_i)));
			
	Index_i <= TestGroup_CntOut_i; --STD_LOGIC_VECTOR(TO_UNSIGNED(TestGroup_Counter_i, Index_i'length)); -- Test pointer
	
	-----------------------------------------------------------------------------
	TESTGROUP_STATUS_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestBitWidth,
			SIZE_PORT_MEM  => NbBranches) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => TestGroup_StatusIn_i,
			wen    => TestGroup_StatusWrite_i,
			wraddr => InputID,
			rdaddr => InputID, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => TestGroup_StatusOut_i);
			
	TestGroup_StatusWrite_i  <= '1' when CurState_i=UPDATESTATUS_STATE else ConfWrite;
	-----------------------------------------------------------------------------
	-- Set status bit to one for incoming data at index InputIdx
	DataValidation : for i in NbBranches-1 downto 0 generate
		StatValidProc:process(ConfMode, InputIdx, TestGroup_StatusOut_i)
		begin -- warning : take care if datavalid is already 1 (Overwrite ?)
			if ConfMode='0' then
				if TO_INTEGER(UNSIGNED(InputIdx))=i and TestGroup_InvalidOut_i(i)='0' then
					TestGroup_StatusIn_i(i) <= '1';
				else
					TestGroup_StatusIn_i(i) <= TestGroup_StatusOut_i(i);
				end if;
			else
				TestGroup_StatusIn_i(i) <= '0';
			end if;
		end process;
	end generate;
			
	-----------------------------------------------------------------------------
	TESTGROUP_INVALIDATE_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestBitWidth,
			SIZE_PORT_MEM  => NbBranches) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => TestGroup_InvalidIn_i,
			wen    => TestGroup_InvalidWrite_i,
			wraddr => TestID_i,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => TestGroup_InvalidOut_i);
	
--	Invalidation : for k in 0 to TestGroup_InvalidIn_i'length-1 generate
--		TestGroup_InvalidIn_i(k) <= '1' when CurState_i=RESET_STATE and k>=IdxMax_i else '0';
--	end generate;
	InvalidationInput_generate : for i in NbBranches-1 downto 0 generate
		TestGroup_InvalidIn_i(i) <= '0' when ConfMode='1' or (CurState_i/=RESET_STATE and ConfMode='0' and TO_INTEGER(UNSIGNED(InputIdx))=i) else 
		                            (not TestGroup_StatusOut_i(i)) when CurState_i=RESET_STATE and ConfMode='0' else
		                            TestGroup_InvalidOut_i(i);
	end generate;
	-----------------------------------------------------------------------------
	TestGroup_InvalidWrite_i <= '1' when CurState_i=RESET_STATE or CurState_i=UPDATESTATUS_STATE else ConfWrite;
	-----------------------------------------------------------------------------
	TESTGROUP_COUNTER_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestBitWidth,
			SIZE_PORT_MEM  => IdxBitWidth) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => TestGroup_CntIn_i,
			wen    => TestGroup_CntWrite_i,
			wraddr => InputID,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => TestGroup_CntOut_i);
			
	TestGroup_Counter_i <= TO_INTEGER(UNSIGNED(TestGroup_CntOut_i));
			
	TestGroup_CntWrite_i <= '1' when CurState_i=TEST_STATE else ConfWrite;--InputWrite;
			
	TestGroup_CntIn_i <= (others=>'0') when ConfMode='1' else STD_LOGIC_VECTOR(TO_UNSIGNED(TestGroup_Counter_i+1, TestGroup_CntIn_i'length));
	
	-----------------------------------------------------------------------------
	TESTGROUP_IDXMAX_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTestBitWidth,
			SIZE_PORT_MEM  => IdxBitWidth) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => IdxMaxConf_i,
			wen    => IdxMaxWrite,
			wraddr => InputID,
			rdaddr => TestID_i, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => IdxMaxOut_i);
			
	IdxMax_i    <= TO_INTEGER(UNSIGNED(IdxMaxOut_i));
	IdxMaxConf_i  <= STD_LOGIC_VECTOR(TO_UNSIGNED(IdxMaxCounter_i, IdxMaxConf_i'length));
	-----------------------------------------------------------------------------
	-- Assign payload and TaskID and DataIdx from input flits
	IdxMaxCount: process (Clk, Rst)
	begin 
		if rising_edge(Clk) then
			if Rst='1' then
				IdxMaxCounter_i <= 0;
			else
				-------------------------------------------------------------
				if ConfMode='0' then
					IdxMaxCounter_i <= 0;
				else
					if IdxMaxWrite='1' then
						IdxMaxCounter_i <= 0;
					elsif ConfWrite='1' then
						IdxMaxCounter_i <= IdxMaxCounter_i+1;
					end if;
				end if;
				-------------------------------------------------------------
			
			end if;
		end if;
	end process IdxMaxCount;
	
	-----------------------------------------------------------------------------
	TestList: process (Clk, Rst)
--		variable ProceedTests : boolean :=False;
	begin 
		if (Rst = '1') then
--			TestGroup_Counter_i <= 0;
			CurState_i <= INCOMING_STATE;
		else 
			if rising_edge(Clk) then
				case CurState_i is 
					when INCOMING_STATE => 
						TestID_i <= InputID;
						if InputWrite='1' then
							CurState_i <= UPDATESTATUS_STATE;
						end if;
					when UPDATESTATUS_STATE => 
						if TestGroup_StatusIn_i(TestGroup_Counter_i)='1' then
							CurState_i <= TEST_STATE;
						else
							CurState_i <= INCOMING_STATE;
						end if;
					when TEST_STATE => 
						if TestedResult_i='1' then -- THE TEST !!!!!!!!!
--							-- Start a new test list
							CurState_i <= RESET_STATE;
						else
							CurState_i <= INCCOUNTER_STATE;
						end if;
						
					when INCCOUNTER_STATE => 
						if (TestGroup_Counter_i+1)=IdxMax_i then -- Last test => else condition
							CurState_i <= RESET_STATE;
						else
							if TestGroup_StatusOut_i(TestGroup_Counter_i+1)='1' then -- tested data available
								CurState_i <= TEST_STATE;
							else
								CurState_i <= INCOMING_STATE;
							end if;
						end if;
						
					when RESET_STATE => 
						CurState_i <= INCOMING_STATE;
						
				end case;
			end if;
		end if;
	end process TestList;
	
	
	TakeBranch_i <= '1' when CurState_i=RESET_STATE else '0';
	TakeBranch   <= TakeBranch_i;
	
--	-----------------------------------------------------------------------------
--	Invalidation: process (Clk, Rst)
--		variable ProceedTests : boolean :=False;
--	begin 
--		if (Rst = '1') then
--			TestGroup_InvalidIn_i <= (others=>'0');
--		else 
--			if rising_edge(Clk) then
--				if  then
--				end if;
--			end if;
--		end if;
--	end process Invalidation;
	
	SelectedBranch <= (others=>'0') when TO_INTEGER(UNSIGNED(TestGroup_CntIn_i))=0 else STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(TestGroup_CntIn_i))-1, SelectedBranch'length));

end RTL;










