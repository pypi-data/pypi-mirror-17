LIBRARY IEEE;
	USE IEEE.STD_LOGIC_1164.ALL;
--	USE IEEE.STD_LOGIC_ARITH.ALL;
	USE IEEE.STD_LOGIC_UNSIGNED.ALL;
	USE ieee.numeric_std.ALL;

-------------------------------------------------------------------------------
-- ENTITY: Handshake Network Adapter TB
-------------------------------------------------------------------------------
entity ControlVerif_Loopback_96_96_0_TB is
end ControlVerif_Loopback_96_96_0_TB;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture TB of ControlVerif_Loopback_96_96_0_TB is

	-----------------------------------------------------------------------------
	component ControlVerif_Loopback_96_96_0
	PORT (
		Reset       : IN  STD_LOGIC;
		Clock       : IN  STD_LOGIC;
		Inputs      : IN  STD_LOGIC_VECTOR(94 downto 0);
		Outputs     : OUT STD_LOGIC_VECTOR(95 downto 0)
		);
	end component;

	signal Rst, Clk : std_logic := '0';
	signal Inputs   : std_logic_vector(94 downto 0);
	signal Outputs  : std_logic_vector(95 downto 0);
	signal CNT      : natural;

begin  -- TB

	Rst <= '1', '0' after 23 ns;
	Clk <= not Clk after 10 ns;

	-----------------------------------------------------------------------------
	ControlVerif_Loopback_96_96_0_DUT: ControlVerif_Loopback_96_96_0
	port map (
		Reset     => Rst,
		Clock     => Clk,
		Inputs    => Inputs,
		Outputs   => Outputs
		);

	-----------------------------------------------------------------------------
	Inputs <= STD_LOGIC_VECTOR(TO_UNSIGNED(CNT, Inputs'length));
	-----------------------------------------------------------------------------
	
	
	
	------------------------------------------------------------
	-- Configuration modes
	TaskIndexAssignment: process(Clk, Rst)
	begin
		if (Rst = '1') then
			CNT<=0;
		else 
			if rising_edge(Clk) then
				CNT<=CNT+1;
			end if;
		end if;
	end process TaskIndexAssignment;

end TB;








