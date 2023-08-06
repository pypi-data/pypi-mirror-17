
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;



entity Equal is
	generic(
		DataWidth : natural := 64);
	port (
		Clk           : in  std_logic;
		Rst           : in  std_logic;
		A             : in  std_logic_vector(DataWidth-1 downto 0);
		B             : in  std_logic_vector(DataWidth-1 downto 0);
		R             : out std_logic_vector(DataWidth-1 downto 0));

end Equal;

architecture RTL of Equal is

begin
	
	Equal : process (CLK, RST)
	begin  -- process Equal_
		if RST = '0' then                   -- asynchronous reset (active HIGH)
			if rising_edge(CLK) then  -- rising clock edge
				if A=B then
					R <= STD_LOGIC_VECTOR(TO_UNSIGNED(1, DataWidth));
				else
					R <= STD_LOGIC_VECTOR(TO_UNSIGNED(0, DataWidth));
				end if;
			end if;
		else
			R <= STD_LOGIC_VECTOR(TO_UNSIGNED(0, DataWidth));
			
		end if;
	end process Equal;

end RTL;


