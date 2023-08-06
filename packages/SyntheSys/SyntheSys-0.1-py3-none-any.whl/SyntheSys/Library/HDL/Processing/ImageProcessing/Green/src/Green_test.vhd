
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity Green_bench is
end Green_bench;

architecture bench of Green_bench is


	-- Main component declaration
	component Green is

	port (
		
		X                 : in  std_logic_vector(63 downto 0);
		Y                 : in  std_logic_vector(63 downto 0);
		Z                 : in  std_logic_vector(63 downto 0);
		clk, rst          : in std_logic;
		GreenValue          	      : out std_logic_vector(63 downto 0));

   end component;



	signal clk, clk_n : std_logic := '0';

	-- Signals to connect the instantiated multi-match component
	signal rst           : std_logic := '0';
	signal x             : std_logic_vector(63 downto 0) := (others => '0');
	signal y             : std_logic_vector(63 downto 0) := (others => '0');
	signal z             : std_logic_vector(63 downto 0) := (others => '0');
	signal GreenValue     : std_logic_vector(63 downto 0) := (others => '0');

begin

	-- Clock generation
	
	clk_n <= not clk;
	clk <= clk_n after 500 ns;


	-- Instantiation of the component to test
	i_comp : Green 
		port map (
			rst         => rst,
			clk           => clk,
			x  	      => x,
			y             => y,
			z             => z,
			GreenValue     => GreenValue
		);

	-- Process that generates stimuli
	process
	begin

		rst <= '1';

		wait until rising_edge(clk);
		rst <= '0';
		x <= X"3FF999999999999A";   --1.6
		--wait until rising_edge(clk);
		y <= X"3FEBD70A3D70A3D7";   --0.87
	

		-- After that there should be only "02" inside

		--wait until rising_edge(clk);

		

		z <= X"3FF2147AE147AE14";   -- -1.13


		wait until rising_edge(clk);

		--x <= X"0000000000000004";
		

		wait until rising_edge(clk);

		--y <= X"0000000000000001";
		

		wait until rising_edge(clk);

		--z <= X"0000000000000002";
	

		wait until rising_edge(clk);


		-- End of simulation
		wait for 1000 ns;
		
		assert false report "*** Test complete ***";
		wait;

	end process;



end architecture;


