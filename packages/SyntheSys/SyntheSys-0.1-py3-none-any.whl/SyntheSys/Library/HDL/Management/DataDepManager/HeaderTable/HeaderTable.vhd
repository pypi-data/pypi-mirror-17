
library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;


-------------------------------------------------------------------------------
-- ENTITY: HeaderTable
-------------------------------------------------------------------------------
entity HeaderTable is

	generic (
		FlitWidth        : natural := 16; -- FlitWidth (in bit)
		NbInputs         : natural := 16; -- FlitWidth (in bit)
		NBTask           : natural := 100); -- Number of task an operator can manage

	port (
		Rst, Clk         : IN  std_logic;

		TaskAddr         : IN  std_logic_vector(natural(ceil(log2(real(NBTask))))-1 downto 0):=(others=>'0');
		
		HeaderInputWrite : IN  std_logic;
		HeaderInput      : IN  std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		HeaderOutput     : OUT std_logic_vector(FlitWidth-1 downto 0):=(others=>'0');
		
		HeaderConfigMode    : IN  std_logic;
		MultiCastConfigMode : IN  std_logic;
		
		NextTarget       : IN  std_logic;
		NewTask          : IN  std_logic;
		
		NbTargetsWrite   : IN  std_logic;
		NbTargetsInput   : IN  unsigned(FlitWidth/2-1 downto 0);
		--NextIDOutput     : OUT natural := 0;
		NbTargetsOutput  : OUT unsigned(FlitWidth/2-1 downto 0)
		);

end HeaderTable;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of HeaderTable is


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

--	signal TaskAddr_i, TaskAddr_index_i, HeaderIndex_i, NextID_i, NextIDCnt_i  : natural range 0 to NBTask-1 :=0;
--	constant NbConfigModes  : natural := 1;
--	constant PosBitWidth    : natural := natural(ceil(log2(real(NbInputs))));
--	constant TaskAddrBitWidth : natural := natural(ceil(log2(real(NBTask))));
--	constant NO_NEXT_ID     : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');

	signal MultiCastCounter_i : unsigned(natural(ceil(log2(real(NBTask))))-1 downto 0) := (others=>'0');
--	signal   NextTaskAddr_i : std_logic_vector(natural(ceil(log2(real(NBTask))))-1 downto 0);
--	signal   HeaderInputWrite_i : std_logic := '0';
	signal TaskAddr_i     : std_logic_vector(natural(ceil(log2(real(NBTask))))-1 downto 0):=(others=>'0');
	
	signal NbTargetsInput_i   : std_logic_vector(FlitWidth/2-1 downto 0);
	--NextIDOutput     : OUT natural := 0;
	signal NbTargetsOutput_i  : std_logic_vector(FlitWidth/2-1 downto 0);

begin  -- RTL


	HEADER_TABLE_RAM : a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => natural(ceil(log2(real(NBTask)))),
			SIZE_PORT_MEM  => FlitWidth)
		PORT MAP(
			din    => HeaderInput,
			wen    => HeaderInputWrite,
			wraddr => TaskAddr_i,
			rdaddr => TaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => HeaderOutput);

	NBTARGET_TABLE_RAM : a_sram_param
		GENERIC MAP (
			SIZE_ADDR_MEM  => natural(ceil(log2(real(NBTask)))),
			SIZE_PORT_MEM  => FlitWidth/2)
		PORT MAP(
			din    => NbTargetsInput_i,
			wen    => NbTargetsWrite,
			wraddr => TaskAddr_i,
			rdaddr => TaskAddr_i, --NextTaskAddr_i,
			clk    => Clk,
			oclk   => Clk,
			dout   => NbTargetsOutput_i);

	NbTargetsOutput  <= UNSIGNED(NbTargetsOutput_i);
	NbTargetsInput_i <= STD_LOGIC_VECTOR(NbTargetsInput);
	
	MultiCastSetup : process(Rst, Clk) is 
	begin
		if Rst='1'then 
			MultiCastCounter_i <= (others=>'0');
		else
			if rising_edge(Clk) then
				-- MultiCastSetup
				if (ConfigMode='0' and NewTask='0') then
					if NextTarget='1' then 
						MultiCastCounter_i <= MultiCastCounter_i+1;
					end if;
				else
					MultiCastCounter_i <= UNSIGNED(TaskAddr);
				end if;
			end if;
		end if;
	end process MultiCastSetup;

	
	TaskAddr_i <= TaskAddr when (ConfigMode='1' or NewTask='1') else STD_LOGIC_VECTOR(MultiCastCounter_i);

end RTL;











