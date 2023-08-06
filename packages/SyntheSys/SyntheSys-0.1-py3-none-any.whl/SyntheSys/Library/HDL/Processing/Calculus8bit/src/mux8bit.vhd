library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

entity mux8bit is
port ( clk : in std_logic;
       a   : in std_logic_vector(3 downto 0);
	   b   : in std_logic_vector(3 downto 0);
	   r   : out std_logic_vector(7 downto 0));
end mux8bit;

architecture archi_mux8bit of mux8bit is
signal rr : std_logic_vector(9 downto 0);
signal carry : std_logic_vector(1 downto 0);
attribute keep : boolean;
attribute keep of rr : signal is true;
begin

process(clk)
begin
if rising_edge(clk) then
rr <= ('0' & a) *('0' & b);
end if;
end process;

carry <= rr(9 downto 8);
r <= rr(7 downto 0);

end archi_mux8bit;
