
use work.Utilities.ALL;

library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;
-------------------------------------------------------------------------------
-- ENTITY: DataBuffers
-------------------------------------------------------------------------------
entity DataBuffers is

	generic (
		DataWidth          : natural := 16; -- FlitWidth (in bit)
		NbIndexedData      : natural := 10; -- Number of indexed data managed per address
		NbAddr             : natural := 10); -- Number of addresses an operator can manage

	port (
		Rst, Clk     : IN  std_logic;
	
		WriteID      : IN  std_logic_vector(BitWidth(NbAddr)-1 downto 0);
		ReadID       : IN  std_logic_vector(BitWidth(NbAddr)-1 downto 0);
		Index        : IN  std_logic_vector(BitWidth(NbIndexedData)-1 downto 0);
		
		InputWrite   : IN  std_logic := '0';
		InputData    : IN  std_logic_vector(DataWidth-1 downto 0);

		OutputData   : OUT std_logic_vector(DataWidth-1 downto 0));

end DataBuffers;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of DataBuffers is

	constant AddrBitWidth             : natural :=BitWidth(NbAddr);
	constant IdxBitWidth              : natural :=BitWidth(NbIndexedData);
	
	signal OutputDataVector : std_logic_vector(NbIndexedData*DataWidth-1 downto 0):=(others=>'0');
	signal InputWriteVector : std_logic_vector(NbIndexedData-1 downto 0):=(others=>'0');
	signal Index_i          : natural := 0;
	
begin

	Index_i <= TO_INTEGER(UNSIGNED(Index));
	-----------------------------------------------------------------------------
	WriteMemLoop: for n in 0 to NbIndexedData-1 generate
		InputWriteProcess : process(InputWrite, Index_i)
		begin
			if n=Index_i then
				InputWriteVector(n)<=InputWrite;
			else
				InputWriteVector(n)<='0';
			end if;
		end process;
	end generate;

	-----------------------------------------------------------------------------
	MEMORYLoop: for i in 0 to NbIndexedData-1 generate
		DATASET_RAM : entity work.a_sram_param(behavioral)
			GENERIC MAP (
				SIZE_ADDR_MEM  => AddrBitWidth,
				SIZE_PORT_MEM  => DataWidth)
			PORT MAP(
				din    => InputData,
				wen    => InputWriteVector(i),
				wraddr => WriteID,
				rdaddr => ReadID,
				clk    => Clk,
				oclk   => Clk,
				dout   => OutputDataVector((NbIndexedData-i)*DataWidth-1 downto (NbIndexedData-i-1)*DataWidth));
	end generate;
	-----------------------------------------------------------------------------
	
	OutputData <= OutputDataVector((NbIndexedData-Index_i)*DataWidth-1 downto (NbIndexedData-Index_i-1)*DataWidth);
	
	
	
end RTL;




