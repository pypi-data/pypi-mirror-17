library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

entity sub8bit is
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0);
	   b   : in std_logic_vector(7 downto 0);
	   r   : out std_logic_vector(15 downto 0));
end sub8bit;

architecture archi_sub8bit of sub8bit is
signal point_neg: std_logic:='0';
signal rr : std_logic_vector(15 downto 0) :=(others =>'0');
attribute keep : boolean;
attribute keep of point_neg : signal is true;
attribute keep of rr : signal is true;
begin

process(clk)
begin
if rising_edge(clk) then
	if a>= b then
	rr <= "00000000" & (a-b);
	else rr <= "00000000" & (b-a);
	end if;
end if;
end process;
point_neg <= rr(8);
r <= rr;
end archi_sub8bit;