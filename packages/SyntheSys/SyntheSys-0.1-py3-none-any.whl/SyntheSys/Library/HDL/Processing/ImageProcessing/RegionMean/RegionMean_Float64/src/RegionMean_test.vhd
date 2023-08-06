
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity RegionMean_bench is
end RegionMean_bench;

architecture bench of RegionMean_bench is


	-- Main component declaration
	
	component RegionMean is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		NbElement         : in  std_logic_vector(15 downto 0);
		DataList          : in  std_logic_vector(63 downto 0);
		--outputs
		RegionMeanValue        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
    end component;



	signal clk, clk_n : std_logic := '0';

	-- Signals to connect the instantiated multi-match component
	signal rst           : std_logic := '0';
	signal DataRead            : std_logic := '1';
	signal Start            : std_logic := '1';
	
	signal NbElement             : std_logic_vector(15 downto 0) := (others => '0');
	signal DataList             : std_logic_vector(63 downto 0) := (others => '0');
	signal RegionMeanValue    : std_logic_vector(63 downto 0) := (others => '0');

begin

	-- Clock generation
	
	clk_n <= not clk;
	clk <= clk_n after 100 ns;


	-- Instantiation of the component to test
	i_comp : RegionMean 
		port map (
			rst         => rst,
			clk         => clk,
			Start         => Start,
			
			DataRead              => DataRead ,
			NbElement            => NbElement,
			DataList            => DataList,
			RegionMeanValue     => RegionMeanValue
		);

	-- Process that generates stimuli
	process
	
	begin
		NbElement  <= X"0009"; 
		rst <= '1';

		wait until rising_edge(clk);
		--wait for 200ns;
		--wait until rising_edge(clk);
		rst <= '0';
		wait until rising_edge(clk);
		DataList <= X"3FF2147AE147AE14";   -- -1.13
		
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
		wait until rising_edge(clk);

		DataList <= X"3FEBD70A3D70A3D7";   --0.87
		--TabSp <= X"3FEBD70A3D70A3D7";   --0.87
	

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
		wait until rising_edge(clk);    --12
	
	
		

		DataList <= X"3FF999999999999A";   --1.6
		--TabRef <= X"3FF2147AE147AE14";   -- -1.13

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

		DataList <= X"3FEBD70A3D70A3D7";   --0.87
		--TabSp <= X"3FF999999999999A";   --1.6

		
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
		

		DataList <= X"3FF2147AE147AE14";   -- -1.13
		--TabRef <= X"3FF2147AE147AE14";   -- -1.13

		
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



		DataList<= X"3FEBD70A3D70A3D7";   --0.87
		--TabSp<= X"3FEBD70A3D70A3D7";   --0.87

		
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


		DataList <= X"3FF2147AE147AE14";   -- -1.13
		--TabRef <= X"3FF2147AE147AE14";   -- -1.13

		
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



		DataList<= X"3FEBD70A3D70A3D7";   --0.87
		--TabSp<= X"3FEBD70A3D70A3D7";   --0.87

		
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


		DataList <= X"3FF999999999999A";   --1.6
		--TabSp <= X"3FF999999999999A";   --1.6

		
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


