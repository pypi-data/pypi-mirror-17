
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
entity VectorVectorMult is

	generic(
		DataWidth : natural := 32);

	port (
		--control signals    
		CLK               : in  std_logic;
		RST               : in  std_logic;
		--tree values (k and k-1 values from t+1)
		Vector1           : in  std_logic_vector(DataWidth-1 downto 0);
		Vector2           : in  std_logic_vector(DataWidth-1 downto 0);
		--outputs
		Scalar            : out std_logic_vector(DataWidth-1 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end VectorVectorMult;


----------------------------------------------------------------------------
architecture RTL of VectorVectorMult is

	constant Zeros : std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
	signal   Sum   : natural := 0;

begin
	
	Adder : process (CLK, RST)
	begin  -- process Adder
		if RST = '0' then                   -- asynchronous reset (active HIGH)
			if rising_edge(CLK) then  -- rising clock edge
	--			if Stim1=0 and Stim2=0 then
	--				Sum <= 256;
	--			else
	--				Sum <= 64;
	--			end if;
				Sum <= TO_INTEGER(UNSIGNED(Stim1))+TO_INTEGER(UNSIGNED(Stim2));
			end if;
		else
      Sum <= 0;
			
		end if;
	end process Adder;
	
	Trace1 <= STD_LOGIC_VECTOR(TO_UNSIGNED(Sum, DataWidth));

end RTL;


