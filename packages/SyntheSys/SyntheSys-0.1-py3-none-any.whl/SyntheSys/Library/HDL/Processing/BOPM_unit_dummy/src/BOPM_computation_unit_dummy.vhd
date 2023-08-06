
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_unsigned.all;
--use ieee.numeric_std.all;
--library std;
--use std.textio.all;
--library work;


entity BOPM_computation_unit_dummy is

	-- computation block at step t, position k
	-- Vt,k[call]= max{d * St+1,k - K ; rp * Vt+1,k + r(1-p) * Vt+1,k-1 }
	-- Vt,k[put] = max{K - d * St+1,k ; rp * Vt+1,k + r(1-p) * Vt+1,k-1 }

	-- WARNING : some internal operators (flopoco generated) do not actually
	-- reset to a known state. The output of BOPM_computation_unit is thus stable and
	-- meaningful only after [PIPELINE_LENGTH] clock cycles.
	generic(
		DataWidth : natural := 16
		);

	port (
		--control signals    
		CLK               : in  std_logic;
		RST               : in  std_logic;
		--tree values (k and k-1 values from t+1)
		Stim1             : in  std_logic_vector(DataWidth-1 downto 0);
		Stim2             : in  std_logic_vector(DataWidth-1 downto 0);
		--outputs
		Trace1            : out std_logic_vector(DataWidth-1 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)

  );

end BOPM_computation_unit_dummy;

architecture RTL of BOPM_computation_unit_dummy is

	constant Zeros : std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
	signal   Sum, Sum1, Sum2, Sum3, Sum4, Sum5, Sum6, Sum7, Sum8 : UNSIGNED(DataWidth-1 downto 0) := (others=>'0');

begin
	
	Adder : process (CLK, RST)
	begin  -- process Adder
		if RST = '0' then                   -- asynchronous reset (active HIGH)
			if rising_edge(CLK) then  -- rising clock edge
				Sum <= UNSIGNED(Stim1)+UNSIGNED(Stim2);
				Sum1 <= Sum;
				Sum2 <= Sum1;
				Sum3 <= Sum2;
				Sum4 <= Sum3;
				Sum5 <= Sum4;
				Sum6 <= Sum5;
				Sum7 <= Sum6;
				Sum8 <= Sum7;
			end if;
		else
			Sum  <= (others=>'0');
			Sum1 <= (others=>'0');
			Sum2 <= (others=>'0');
			Sum3 <= (others=>'0');
			Sum4 <= (others=>'0');
			Sum5 <= (others=>'0');
			Sum6 <= (others=>'0');
			Sum7 <= (others=>'0');
			Sum8 <= (others=>'0');
			
		end if;
	end process Adder;
	
	Trace1 <= STD_LOGIC_VECTOR(Sum8);

end RTL;


