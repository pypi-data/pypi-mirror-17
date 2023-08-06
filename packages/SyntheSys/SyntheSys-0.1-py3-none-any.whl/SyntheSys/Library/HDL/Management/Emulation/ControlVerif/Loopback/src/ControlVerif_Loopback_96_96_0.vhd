LIBRARY IEEE;
	USE IEEE.STD_LOGIC_1164.ALL;
	USE IEEE.STD_LOGIC_ARITH.ALL;
	USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY ControlVerif_Loopback_96_96_0 IS
	PORT (
		Reset       : IN  STD_LOGIC;
		Clock       : IN  STD_LOGIC;
		Inputs      : IN  STD_LOGIC_VECTOR(94 downto 0);
		Outputs     : OUT STD_LOGIC_VECTOR(95 downto 0)
		);
END ControlVerif_Loopback_96_96_0;
 
ARCHITECTURE RTL OF ControlVerif_Loopback_96_96_0 IS

--==================================================================
-- COMPONENT DECLARATION
--==================================================================
	
--============================================================
-- INTERNAL SIGNAL DECLARATION
--============================================================
	
BEGIN

	-- LOOPBACK
	LB_Process : process(Reset, Clock)
	begin
		if Reset='1' then
			Outputs <= x"0123456789ABCDEFFFFFFFFF";
		else
			if rising_edge(Clock) then
				Outputs(94 downto 0) <= Inputs;
				Outputs(95) <= Reset;
			end if;
		end if;
	end process;

END ARCHITECTURE;










