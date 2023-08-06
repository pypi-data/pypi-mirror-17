library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;


-------------------------------------------------------------------------------
-- ENTITY: PipelineManager
-------------------------------------------------------------------------------
ENTITY PipelineManager IS

	GENERIC (
		NbTaskBitWidth : natural := 16;
		PipelineLength : natural := 10);

	PORT (
		Reset, Clock   : IN  std_logic;

		BBInputValid   : IN  std_logic;
		BBOutputValid  : OUT std_logic);

--		InputTaskID    : IN  std_logic_vector(NbTaskBitWidth-1 downto 0);
--		OutputTaskID   : OUT std_logic_vector(NbTaskBitWidth-1 downto 0));

END PipelineManager;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of PipelineManager is

	signal PipelineStatus_i : std_logic_vector(PipelineLength-1 downto 0):=(others=>'0');

begin  -- RTL

	LatencyOne : if PipelineLength=1 generate
		-----------------------------------------------------------------------------
		-- Pipeline progress
		PipelineProgress: process (Clock, Reset)
		begin  -- process StateMemory
			if Reset = '1' then            -- asynchronous Reset (active high)
				PipelineStatus_i<=(others=>'0');
		
			elsif rising_edge(Clock) then  -- rising Clock edge
				PipelineStatus_i(0) <= BBInputValid;
		
			end if;
		end process PipelineProgress;
	end generate;
	
	HighLatency : if PipelineLength>1 generate
		-----------------------------------------------------------------------------
		-- Pipeline progress
		PipelineProgress: process (Clock, Reset)
		begin  -- process StateMemory
			if Reset = '1' then            -- asynchronous Reset (active high)
				PipelineStatus_i<=(others=>'0');
		
			elsif rising_edge(Clock) then  -- rising Clock edge
				PipelineStatus_i <= BBInputValid & PipelineStatus_i(PipelineLength-1 downto 1);
		
			end if;
		end process PipelineProgress;
	end generate;

	-----------------------------------------------------------------------------
	BBOutputValid <= PipelineStatus_i(0);
	
--	-----------------------------------------------------------------
--	FIFO: entity work.fifo(RTL)
--		generic map(
--			profondeur => PipelineLength+1,
--			largeur    => NbTaskBitWidth
--			)
--		port map(
--			ack_wr     => open,
--			data_in    => InputTaskID,
--			clock_out  => Clock,
--			IsEmpty    => open,
--			wr         => BBInputValid,
--			clock_in   => Clock,
--			data_out   => OutputTaskID,
--			ack_rd     => open,
--			rd         => PipelineStatus_i(1),
--			IsFull     => open,
--			reset      => Reset
--			);

end RTL;











