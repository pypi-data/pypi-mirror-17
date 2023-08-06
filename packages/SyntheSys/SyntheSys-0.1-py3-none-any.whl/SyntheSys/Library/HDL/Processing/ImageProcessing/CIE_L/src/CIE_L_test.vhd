
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity CIE_L_bc is
end CIE_L_bc;

architecture bench of CIE_L_bc is


	-- Main component declaration

	component CIE_L is

	port (
		
		Y                 : in  std_logic_vector(63 downto 0);
		clk, rst          : in std_logic;
		CIE_LValue          	      : out std_logic_vector(63 downto 0));

	end component;


	signal clk, clk_n : std_logic := '0';

	-- Signals to connect the instantiated multi-match component
	signal rst           : std_logic := '0';
	--signal DataRead            : std_logic := '1';
	--signal Start            : std_logic := '1';
	
	signal y             : std_logic_vector(63 downto 0) := (others => '0');
	signal CIE_LValue    : std_logic_vector(63 downto 0) := (others => '0');

begin

	-- Clock generation
	
	clk_n <= not clk;
	clk <= clk_n after 100 ns;


	-- Instantiation of the component to test
	i_comp : CIE_L 
		port map (
			rst         => rst,
			clk         => clk,
			--Start         => Start,
			
			--DataRead              => DataRead ,
			y            => y,
			CIE_LValue     => CIE_LValue
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
		--x <= "01" & X"3FF999999999999A";   --1.6
		--y <= "01" & X"3FEBD70A3D70A3D7";   --0.87
		--wait for 200ns;
		--wait until rising_edge(clk);
		--Start <= '0';
		wait until rising_edge(clk);
		--x <= X"3FF2147AE147AE14";   -- -1.13
		y <= X"3FF2147AE147AE14";   --1.13
	

		-- After that there should be only "02" inside

		wait until rising_edge(clk);

		

		--TabSp <= X"0003";
		--TabRef <= X"0003";

		--Start <= '1';
        wait until rising_edge(clk);
		--TabRef <= X"0000000000000004";
		--TabSp <= X"0000000000000004";

		wait until rising_edge(clk);
		--Start <= '0';
		wait until rising_edge(clk);

		--TabSp <= X"0000000000000001";
		--TabRef <= X"0000000000000001";

		wait until rising_edge(clk);

		--TabRef<= X"0000000000000002";
		--TabSp<= X"0000000000000002";

		wait until rising_edge(clk);

		--rst <= '1';
		-- End of simulation
		wait for 1000 ns;
		
		assert false report "*** Test complete ***";
		wait;

	end process;



end architecture;


