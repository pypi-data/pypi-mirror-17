
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_unsigned.all;
--use ieee.numeric_std.all;
--library std;
--use std.textio.all;
--library work;


----------------------------------------------------------------------------
entity VectorVectorAdd is

	generic(
		DataWidth : natural := 32);

	port (
		--control signals    
		CLK               : in  std_logic;
		RST               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		DataWrite         : out std_logic;
		--tree values (k and k-1 values from t+1)
		InputSize         : in  std_logic_vector(DataWidth-1 downto 0);
		OuptutSize        : in  std_logic_vector(DataWidth-1 downto 0);
		
		Vector1           : in  std_logic_vector(DataWidth-1 downto 0);
		Vector2           : in  std_logic_vector(DataWidth-1 downto 0);
		--outputs
		VectorResult      : out std_logic_vector(DataWidth-1 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end VectorVectorAdd;


----------------------------------------------------------------------------
architecture RTL of VectorVectorAdd is

	constant Zeros : std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
	signal   Sum_i   : unsigned := (others=>'0');

begin

	AddVect : process (Clk, Rst)
	begin  -- process Adder
		if rising_edge(Clk) then  -- rising clock edge
			if Rst = '1' then -- synchronous reset (active HIGH)
				Sum_i      <= (others=>'0');
				Cnt_i      <= (others=>'0');
				RegionMean <= (others=>'0');
			else
				if Start = '1' then 
					Sum_i <= UNSIGNED(Vector1)+UNSIGNED(Vector2);
					Cnt_i <= (others=>'0');
				else
					Accu  <= UNSIGNED(DataList)+Accu;
					Cnt_i <=Cnt_i+1;
				end if;
				if Cnt_i=(NbElement_i) then
					Sum <= UNSIGNED(Vector1)+UNSIGNED(Vector2);
				end if;
			end if;
		end if;
	end process AddVect;
	
	VectorResult <= STD_LOGIC_VECTOR(Sum_i, DataWidth);

end RTL;


