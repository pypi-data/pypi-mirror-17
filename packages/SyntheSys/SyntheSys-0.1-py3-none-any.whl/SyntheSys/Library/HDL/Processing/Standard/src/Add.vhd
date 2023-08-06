
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


entity Add is
	generic(
		DataWidth : natural := 64);
	port (
		Clk           : in  std_logic;
		Rst           : in  std_logic;
		A             : in  std_logic_vector(DataWidth-1 downto 0);
		B             : in  std_logic_vector(DataWidth-1 downto 0);
		R             : out std_logic_vector(DataWidth-1 downto 0));

end Add;

architecture RTL of Add is

	constant Zeros : std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
	signal   R_i   : natural := 0;

begin
	
	Add : process (CLK, RST)
	begin  -- process Add
		if RST = '0' then                   -- asynchronous reset (active HIGH)
			if rising_edge(CLK) then  -- rising clock edge
				R_i <= TO_INTEGER(UNSIGNED(A))+TO_INTEGER(UNSIGNED(B));
			end if;
		else
			R_i <= 0;
			
		end if;
	end process Add;
	
	R <= STD_LOGIC_VECTOR(TO_UNSIGNED(R_i, DataWidth));

end RTL;


