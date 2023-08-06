
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.math_real.all;
USE ieee.numeric_std.ALL;

-------------------------------------------------------------------------------
-- ENTITY: Arbiter that 
-------------------------------------------------------------------------------
entity Arbiter is

	generic (
		NbInputs : natural := 5); -- North, South, East, West, Local

	port (
		Clk             : in  std_logic;
		Rst             : in std_logic;

		RequestTable    : in  std_logic_vector(NbInputs-1 downto 0);
		ConnectionTable : in  std_logic_vector(NbInputs-1 downto 0);
		SelectedPort    : out natural
		);

end Arbiter;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of Arbiter is

	signal Selected, Cnt : natural range 0 to natural(2**ceil(log2(real(NbInputs))))-1 := 0; -- UPPER VALUE= DISCONNECTED
	constant Allones : natural := natural(2**ceil(log2(real(NbInputs))))-1;

begin  -- RTL

	SelectedPort <= Selected;
	-----------------------------------------------------------------------------
	PortSelection: process (Clk, Rst)
	begin  -- process PortSelection
		if Clk'event and Clk='1' then  -- rising clock edge
			if Rst = '1' then      -- synchronous reset (active high)
				Cnt <= 0;

			else
				if Cnt<(NbInputs-1) then
					Cnt<=Cnt+1;
				else
					Cnt<=0;
				end if;
			end if;
		end if;
	end process PortSelection;

	-----------------------------------------------------------------------------
	Selected <= Cnt when (RequestTable(Cnt)='1' and ConnectionTable(Cnt)='0') else
	            Allones;

end RTL;


