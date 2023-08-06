

-------------------------------------------------------------------------------
use work.Utilities.ALL;
library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;


-------------------------------------------------------------------------------
-- ENTITY: InputTable
-------------------------------------------------------------------------------
entity InputTable is
	generic (
		FlitWidth          : natural := 16;   -- FlitWidth (in bit)
		NbInputFlit        : natural := 3;    -- FlitWidth (in bit)
		NBTask             : natural := 100;
		InputSerialization : NaturalVector); -- Number of task an operator can manage
	port (
		Rst, Clk           : IN  std_logic;
		
		HeaderConfigMode   : IN  std_logic;
		ConstantConfigMode : IN  std_logic;
		IdleMode           : IN  std_logic;

		TaskID             : IN  std_logic_vector(BitWidth(NBTask)-1 downto 0);
		DataIdx            : IN  std_logic_vector(BitWidth(NbInputFlit)-1 downto 0);
		Serialized         : IN  std_logic;
--		DataID             : IN  std_logic_vector(FlitWidth/2-1 downto 0):=(others=>'0');
--		PayloadReceived    : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
--		PayloadValid       : IN  std_logic;
		HeaderValid        : IN  std_logic;
		
		BufferBusy         : OUT std_logic;
		
		NetworkInputValid     : IN  std_logic;
		NetworkInput          : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		
		PeInputValid    : OUT std_logic;
		PeInput         : OUT std_logic_vector(NbInputFlit*FlitWidth-1 downto 0):=(others=>'0')
		);
end InputTable;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of InputTable is
	
	constant DataIdxBitWidth          : natural := BitWidth(NbInputFlit);
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
	constant PosEncodingBits   : natural := natural(ceil(log2(real(NbInputFlit))));
	constant STATUS_READY      : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'1');
	
--	signal TaskID_i : std_logic_vector(FlitWidth/2-PosEncodingBits-1 downto 0):=(others=>'0');
	
	signal StatusIn_i, StatusOut_i : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'0');
	signal StatusWrite_i : std_logic;
	signal Position_i    : natural;
--	signal ResetStatus_i : std_logic;
	signal DataStatus_i : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'0');
	
	signal Const_StatusIn_i     : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'0'); -- Reset each TaskID if in HEADER_CONFIG_MODE
	signal Const_StatusOut_i    : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'0');
	signal Const_StatusWrite_i  : std_logic;

	signal ConstantInputValid_i : std_logic := '0'; 
	signal ResetConstStatus_i   : std_logic := '0';
	signal NetworkInputValid_i     : std_logic_vector(NbInputFlit-1 downto 0):=(others=>'0');
	signal DataIdx_i : natural :=0;
	signal RcvCnt_i  : unsigned(FlitWidth-1 downto 0):=(others=>'0');
	
begin  -- RTL

	------------------------------------------------------------
	-- Configuration modes
	PacketSendBack: process(Clk, Rst)
	begin
		if (Rst = '1') then
			BufferBusy <= '0';
		else 
			if rising_edge(Clk) then 
				if HeaderValid='1' then
					if StatusOut_i(DataIdx_i)='1' then
						BufferBusy <= '1';
					end if;
				else
					BufferBusy <= '0';
				end if;
			end if;
		end if;
	END PROCESS;

	------------------------------------------------------------
	ResetConstStatus_i   <= NetworkInputValid when HeaderConfigMode='1' else '0';
	ConstantInputValid_i <= NetworkInputValid when ConstantConfigMode='1' else '0';
	
	InputValidLoop: for i in 0 to NbInputFlit-1 generate
		NetworkInputValid_i(i) <= NetworkInputValid when (IdleMode='1' or ConstantConfigMode='1') and (i=DataIdx_i) else '0';
	end generate;
	-----------------------------------------------------------------------------
	InputLoop: for i in 0 to NbInputFlit-1 generate
		InputBuffer : if InputSerialization(i)=1 generate
			INPUT_TABLE_RAM : a_sram_param
				GENERIC MAP (
					SIZE_ADDR_MEM  => NbTaskBitWidth,
					SIZE_PORT_MEM  => FlitWidth)
				PORT MAP(
					din    => NetworkInput,
					wen    => NetworkInputValid_i(i),
					wraddr => TaskID(NbTaskBitWidth-1 downto 0),
					rdaddr => TaskID(NbTaskBitWidth-1 downto 0),
					clk    => Clk,
					oclk   => Clk,
					dout   => PeInput((i+1)*FlitWidth-1 downto i*FlitWidth));
		end generate InputBuffer;
		InputConstant : if InputSerialization(i)>1 generate
			PeInput((i+1)*FlitWidth-1 downto i*FlitWidth) <= STD_LOGIC_VECTOR(TO_UNSIGNED(TO_INTEGER(UNSIGNED(TaskID))*InputSerialization(i), FlitWidth));
		end generate InputConstant;
	end generate InputLoop;
	
	-----------------------------------------------------------------------------
	STATUS_TABLE_RAM : a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => NbTaskBitWidth,
			SIZE_PORT_MEM  => NbInputFlit)
		PORT MAP(
			din    => StatusIn_i,
			wen    => StatusWrite_i,
			wraddr => TaskID(NbTaskBitWidth-1 downto 0),
			rdaddr => TaskID(NbTaskBitWidth-1 downto 0),
			clk    => Clk,
			oclk   => Clk,
			dout   => StatusOut_i);
	
	StatusWrite_i <= '1' when DataStatus_i=STATUS_READY or (Serialized='0' and NetworkInputValid='1' and (HeaderConfigMode='1' or IdleMode='1')) or RcvCnt_i=TO_UNSIGNED(InputSerialization(DataIdx_i), RcvCnt_i'length) else '0';
	
	------------------------------------------------------------
	-- Configuration modes
	SerializeCnt: process(Clk, Rst)
	begin
		if (Rst = '1') then
			RcvCnt_i <= (others=>'0');
		else 
			if rising_edge(Clk) then 
				if HeaderValid='1' or RcvCnt_i=TO_UNSIGNED(InputSerialization(DataIdx_i), FlitWidth) then
					RcvCnt_i <= (others=>'0');
				else
					if Serialized='1' and NetworkInputValid='1' then
						RcvCnt_i <= RcvCnt_i+1;
					end if;
				end if;
			end if;
		end if;
	END PROCESS SerializeCnt;
	-----------------------------------------------------------
	STATUS_SETUP : FOR i IN 0 TO NbInputFlit-1 GENERATE
		StatSetupProcess: process(DataStatus_i, IdleMode, DataIdx_i, StatusOut_i)
		begin
			if IdleMode='0' then
				StatusIn_i(i) <= '0';
			else
				if DataStatus_i=STATUS_READY then
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
			SIZE_PORT_MEM  => NbInputFlit) -- enough to encode numbers up to NbDataPerSet
		PORT MAP(
			din    => Const_StatusIn_i, -- Reset each TaskID if in HEADER_CONFIG_MODE
			wen    => Const_StatusWrite_i,
			wraddr => TaskID(NbTaskBitWidth-1 downto 0),
			rdaddr => TaskID(NbTaskBitWidth-1 downto 0), --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => Const_StatusOut_i);

	-- RESET each Task constant status if in HEADER_CONFIG_MODE elsif in CONSTANT_CONFIG_MODE set bit to 1
	ConstConfig : for k in 0 to NbInputFlit-1 generate
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

--	TaskID_i   <= DataID(FlitWidth/2-1 downto natural(ceil(log2(real(NbInputFlit)))));
	DataIdx_i       <= TO_INTEGER(UNSIGNED(DataIdx)) when TO_INTEGER(UNSIGNED(DataIdx))<InputSerialization'length else 0;
	DataStatus_i    <= StatusOut_i or Const_StatusOut_i;
	PeInputValid    <= '1' when DataStatus_i=STATUS_READY else '0';


end RTL;











