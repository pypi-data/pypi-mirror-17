
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity DistanceGFC_bench is
end DistanceGFC_bench;

architecture bench of DistanceGFC_bench is


	-- Main component declaration
	
	component DistanceGFC is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		TabEs          : in  std_logic_vector(63 downto 0);
		TabMe          : in  std_logic_vector(63 downto 0);
		--outputs
		dis_gfc        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
    end component;



	signal clk, clk_n : std_logic := '0';

	-- Signals to connect the instantiated multi-match component
	signal rst           : std_logic := '0';
	signal DataRead            : std_logic := '1';
	signal Start            : std_logic := '1';
	
	signal TabEs             : std_logic_vector(63 downto 0) := (others => '0');
	signal TabMe             : std_logic_vector(63 downto 0) := (others => '0');
	signal dis_gfc    : std_logic_vector(63 downto 0) := (others => '0');

begin

	-- Clock generation
	
	clk_n <= not clk;
	clk <= clk_n after 100 ns;


	-- Instantiation of the component to test
	i_comp : DistanceGFC 
		port map (
			rst         => rst,
			clk         => clk,
			Start         => Start,
			
			DataRead              => DataRead ,
			TabEs            => TabEs,
			TabMe            => TabMe,
			dis_gfc     => dis_gfc
		);

	-- Process that generates stimuli
	process
	begin

		rst <= '1';

		wait until rising_edge(clk);
		--wait for 200ns;
		--wait until rising_edge(clk);
		rst <= '0';
		wait until rising_edge(clk);
		TabEs <= X"3FF2147AE147AE14";   -- -1.13
		TabMe <= X"3FF999999999999A";   --1.6
		--wait for 200ns;
		--wait until rising_edge(clk);
		Start <= '0';
		
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
--		wait until rising_edge(clk);
		wait until rising_edge(clk);
		TabEs <= X"3FEBD70A3D70A3D7";   --0.87
		TabMe <= X"3FEBD70A3D70A3D7";   --0.87
	

		-- After that there should be only "02" inside

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
	
	
		

		TabEs <= X"3FF999999999999A";   --1.6
		TabMe <= X"3FF2147AE147AE14";   -- -1.13

		--Start <= '1';
        
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);

		TabEs <= X"3FEBD70A3D70A3D7";   --0.87
		TabMe <= X"3FF999999999999A";   --1.6

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);


		--Start <= '0';
		

		TabEs <= X"3FF2147AE147AE14";   -- -1.13
		TabMe <= X"3FF2147AE147AE14";   -- -1.13

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);



		TabEs<= X"3FEBD70A3D70A3D7";   --0.87
		TabMe<= X"3FEBD70A3D70A3D7";   --0.87

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);


		TabEs <= X"3FF2147AE147AE14";   -- -1.13
		TabMe <= X"3FF2147AE147AE14";   -- -1.13

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);



		TabEs<= X"3FEBD70A3D70A3D7";   --0.87
		TabMe<= X"3FEBD70A3D70A3D7";   --0.87

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);


		TabEs <= X"3FF999999999999A";   --1.6
		TabMe <= X"3FF999999999999A";   --1.6

		
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);
		wait until rising_edge(clk);

		--rst <= '1';
		-- End of simulation
		wait for 1000 ns;
		
		assert false report "*** Test complete ***";
		wait;

	end process;



end architecture;


