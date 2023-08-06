library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

entity shift8bit is
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0);
	   b   : in std_logic_vector(7 downto 0);
	   r   : out std_logic_vector(15 downto 0));
end shift8bit;

architecture archi_shift8bit of shift8bit is
signal d : integer range 0 to 8 := 0;
signal c : std_logic_vector(15 downto 0) :=(others =>'0');
attribute keep : boolean;
attribute keep of d : signal is true;
attribute keep of c : signal is true;
begin

process(clk)
begin
if rising_edge(clk) then
	case b is
		when x"00"  => d <= 0;
		when x"01"  => d <= 1;
		when x"02"  => d <= 2;
		when x"03"  => d <= 3;
		when x"04"  => d <= 4;
		when x"05"  => d <= 5;
		when x"06"  => d <= 6;
		when x"07"  => d <= 7;
		when others => d <= 8;
	end case;
		
end if;
end process;

r <= "00000000" & a      when d=0 else
     "0000000"  & a & '0' when d=1 else
	  "000000"   & a & "00" when d=2 else
	  "00000"    & a & "000" when d=3 else
	  "0000"     & a & "0000" when d=4 else
	  "000"      & a & "00000" when d=5 else
	  "00"       & a & "000000" when d=6 else
	  '0'        & a & "0000000" when d=7 else
	               a & "00000000";

c <= "00000000" & a      when d=7 else
     "0000000"  & a & '0' when d=6 else
	  "000000"   & a & "00" when d=5 else
	  "00000"    & a & "000" when d=4 else
	  "0000"     & a & "0000" when d=3 else
	  "000"      & a & "00000" when d=2 else
	  "00"       & a & "000000" when d=1 else
	  '0'        & a & "0000000" when d=0 else
	               a & "00000000";
end archi_shift8bit;