
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;


-------------------------------------------------------------------------------
-- ENTITY: ReduceStatus
-------------------------------------------------------------------------------
entity ReduceStatus is
	generic (
		FlitWidth          : natural := 16;   -- FlitWidth (in bit)
		NbInputMax         : natural := 63;    -- (in bit)
		NBTask             : natural := 100); -- Number of task an operator can manage
	port (
		Rst, Clk           : IN  std_logic;
		
		HeaderConfigMode   : IN  std_logic;
		ReduceConfigMode   : IN  std_logic;
		ConstantConfigMode : IN  std_logic;
		RunningMode           : IN  std_logic;

		TaskID             : IN  std_logic_vector(BitWidth(NBTask)-1 downto 0);
		DataIdx            : IN  std_logic_vector(BitWidth(NbInputMax)-1 downto 0);		
		BufferBusy         : OUT std_logic;
		
		HeaderValid        : IN  std_logic;
		NetworkInputValid  : IN  std_logic;
		NetworkInput       : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		
		GroupSize          : IN  std_logic_vector(BitWidth(NbInputMax)-1 downto 0);
		SendGroup          : OUT std_logic
		);
end ReduceStatus;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of ReduceStatus is
	
	constant DataIdxBitWidth          : natural := BitWidth(NbInputMax);
	constant NbTaskBitWidth           : natural := BitWidth(NBTask);

	COMPONENT a_sram_param is
		generic (
			SIZE_ADDR_MEM  : integer := 10 ;
			SIZE_PORT_MEM  : integer := 16 );
		Port(
			din    : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0) ;
			wen    : in  STD_LOGIC                                    ;  
			wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
			rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
			clk    : in  STD_LOGIC                                    ;
			oclk   : in  STD_LOGIC                                    ;
			dout   : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0));
	END COMPONENT;

--	signal TaskID_i, TaskID_index_i, HeaderIndex_i, NextID_i, NextIDCnt_i  : natural range 0 to NBTask-1 :=0;
	constant TaskEncodingBits  : natural := BitWidth(NBTask);
	constant PosEncodingBits   : natural := BitWidth(NbInputMax);
	
--	signal TaskID_i : std_logic_vector(FlitWidth/2-PosEncodingBits-1 downto 0):=(others=>'0');
	
	signal StatusIn_i, StatusOut_i : std_logic_vector(NbInputMax-1 downto 0):=(others=>'0');
	signal StatusWrite_i : std_logic;
	signal Position_i    : natural;
--	signal ResetStatus_i : std_logic;
	signal DataStatus_i : std_logic_vector(NbInputMax-1 downto 0):=(others=>'0');
	
	signal Const_StatusIn_i     : std_logic_vector(NbInputMax-1 downto 0):=(others=>'0'); -- Reset each TaskID if in HEADER_CONFIG_MODE
	signal Const_StatusOut_i    : std_logic_vector(NbInputMax-1 downto 0):=(others=>'0');
	signal Const_StatusWrite_i  : std_logic;

	signal ConstantInputValid_i, ReduceInputValid_i : std_logic := '0'; 
	signal ResetConstStatus_i   : std_logic := '0';
	signal NetworkInputValid_i     : std_logic_vector(NbInputMax-1 downto 0):=(others=>'0');
	signal DataIdx_i : natural :=0;
	signal RcvCnt_i  : unsigned(FlitWidth-1 downto 0):=(others=>'0');
	
	signal GroupCntIn_i, GroupCntOut_i : std_logic_vector(DataIdxBitWidth-1 downto 0):=(others=>'0');
	signal IncrementGroupCnt_i : unsigned(DataIdxBitWidth-1 downto 0):=(others=>'0');
	signal SendGroup_i  : std_logic;
	signal GroupCntWr_i : std_logic;
	
begin  -- RTL

	SendGroup <= SendGroup_i;
	------------------------------------------------------------
	-- Configuration modes
--	PacketSendBack: process(Clk, Rst)
--	begin
--		if (Rst = '1') then
--			BufferBusy <= '0';
--		else 
--			if rising_edge(Clk) then 
--				if HeaderValid='1' then
--					if DataStatus_i(DataIdx_i)='1' then
--						BufferBusy <= '1';
--					else
--						BufferBusy <= '0';
--					end if;
--				else
--					BufferBusy <= '0';
--				end if;
--			end if;
--		end if;
--	END PROCESS;
	BufferBusy <= '0';

	------------------------------------------------------------
	ConstantInputValid_i <= NetworkInputValid when ConstantConfigMode='1' else '0';
	ReduceInputValid_i   <= NetworkInputValid when ReduceConfigMode='1' else '0';
	
	-----------------------------------------------------------------------------
	GROUP_CNT_RAM : a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => TaskEncodingBits,
			SIZE_PORT_MEM  => DataIdxBitWidth)
		PORT MAP(
			din    => GroupCntIn_i,
			wen    => GroupCntWr_i,
			wraddr => TaskID,
			rdaddr => TaskID,
			clk    => Clk,
			oclk   => Clk,
			dout   => GroupCntOut_i);
	
	IncrementGroupCnt_i <= UNSIGNED(GroupCntOut_i)+1 when ReduceConfigMode='0' else (others=>'0');
	GroupCntIn_i <= STD_LOGIC_VECTOR(IncrementGroupCnt_i) when SendGroup_i='0' else (others=>'0');
	GroupCntWr_i <= StatusWrite_i or Const_StatusWrite_i or ReduceInputValid_i;
	SendGroup_i  <= '1' when GroupCntOut_i=GroupSize and RunningMode='1' else '0';
	
	-----------------------------------------------------------------------------
	STATUS_TABLE_RAM : a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => TaskEncodingBits,
			SIZE_PORT_MEM  => NbInputMax)
		PORT MAP(
			din    => StatusIn_i,
			wen    => StatusWrite_i,
			wraddr => TaskID,
			rdaddr => TaskID,
			clk    => Clk,
			oclk   => Clk,
			dout   => StatusOut_i);
	
	StatusWrite_i <= '1' when SendGroup_i='1' or (NetworkInputValid='1' and (HeaderConfigMode='1' or RunningMode='1')) else '0';
	
	-----------------------------------------------------------
	STATUS_SETUP : FOR i IN 0 TO NbInputMax-1 GENERATE
		StatSetupProcess: process(DataStatus_i, RunningMode, DataIdx_i, StatusOut_i)
		begin
			if RunningMode='0' then
				StatusIn_i(i) <= '0';
			else
				if SendGroup_i='1' then
					StatusIn_i(i) <= '0';
				else
					if DataIdx_i=i then
						StatusIn_i(i) <= '1';
					else
						StatusIn_i(i) <= StatusOut_i(i);
					end if;
				end if;
			end if;
		end process StatSetupProcess;
	END GENERATE;

	-----------------------------------------------------------------------------
	CONSTANT_STATUS_RAM : entity work.a_sram_param(behavioral)
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => NbInputMax) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => Const_StatusIn_i, -- Reset each TaskID if in HEADER_CONFIG_MODE
			wen    => Const_StatusWrite_i,
			wraddr => TaskID,
			rdaddr => TaskID, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => Const_StatusOut_i);

	-- RESET each Task constant status if in HEADER_CONFIG_MODE elsif in CONSTANT_CONFIG_MODE set bit to 1
	ConstConfig : for k in 0 to NbInputMax-1 generate
		Const_StatusIn_i(k) <= '0' when HeaderConfigMode='1' else 
		                       '1' when (k=DataIdx_i and ConstantConfigMode='1') else 
		                       Const_StatusOut_i(k);
	end generate;

	-----------------------------------------------------------------------------
--	Delay1cycle: process (Clk, Rst)
--	begin  -- process StateMemory
--		if rising_edge(Clk) then
	Const_StatusWrite_i <= ResetConstStatus_i or ConstantInputValid_i;
--		end if;
--	end process Delay1cycle;

--	TaskID_i   <= DataID(FlitWidth/2-1 downto BitWidth(NbInputMax));

	DataIdx_i       <= TO_INTEGER(UNSIGNED(DataIdx));
	DataStatus_i    <= StatusOut_i or Const_StatusOut_i;
	
	
end RTL;











