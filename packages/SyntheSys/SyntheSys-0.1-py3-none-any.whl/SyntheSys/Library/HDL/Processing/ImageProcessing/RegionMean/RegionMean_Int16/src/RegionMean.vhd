
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity RegionMean is

	generic(
		DataWidth : natural := 16);
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		NbElement         : in  std_logic_vector(DataWidth-1 downto 0);
		DataList          : in  std_logic_vector(DataWidth-1 downto 0);
		--outputs
		RegionMean        : out std_logic_vector(DataWidth-1 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end RegionMean;


----------------------------------------------------------------------------
architecture RTL of RegionMean is

	signal Accu   : unsigned(DataWidth-1 downto 0) := (others=>'0');
	signal Cnt_i  : unsigned(DataWidth-1 downto 0) := (others=>'0');
	signal NbElement_i: unsigned(DataWidth-1 downto 0) := (others=>'0');

begin

	NbElement_i <= UNSIGNED(NbElement);

	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if rising_edge(Clk) then  -- rising clock edge
			if Rst = '1' then -- synchronous reset (active HIGH)
				Accu       <= (others=>'0');
				Cnt_i      <=(others=>'0');
				RegionMean <= (others=>'0');
			else
				if Start = '1' then 
					Accu <= UNSIGNED(DataList);
					Cnt_i<=(others=>'0');
				else
					Accu <= UNSIGNED(DataList)+Accu;
					Cnt_i<=Cnt_i+1;
				end if;
				if Cnt_i=(NbElement_i) then
					RegionMean <= STD_LOGIC_VECTOR(Accu/NbElement_i);
				end if;
			end if;
		end if;
	end process Accumulator;

	DataRead <= '1' when Cnt_i<UNSIGNED(NbElement) else '0';

end RTL;


