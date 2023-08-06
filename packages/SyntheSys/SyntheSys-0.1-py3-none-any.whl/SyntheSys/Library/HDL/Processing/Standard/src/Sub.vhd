
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


entity Sub is
	generic(
		DataWidth : natural := 64);
	port (
		Clk           : in  std_logic;
		Rst           : in  std_logic;
		A             : in  std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
		B             : in  std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
		R             : out std_logic_vector(DataWidth-1 downto 0) := (others=>'0'));

end Sub;

architecture RTL of Sub is

	constant Zeros : STD_LOGIC_VECTOR(DataWidth-1 downto 0) := (others=>'0');
	signal   R_i   : SIGNED(DataWidth-1 downto 0) := (others=>'0');

begin
	
	Sub : process (CLK, RST)
	begin  -- process Sub
		if RST = '0' then                   -- asynchronous reset (active HIGH)
			if rising_edge(CLK) then  -- rising clock edge
				R_i <= SIGNED(A) - SIGNED(B);
			end if;
		else
			R_i <= (others=>'0');
			
		end if;
	end process Sub;
	
	R <= STD_LOGIC_VECTOR(R_i);

end RTL;


