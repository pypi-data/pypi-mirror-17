
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.all;

entity DistanceRGB_bc is
end DistanceRGB_bc;

architecture bench of DistanceRGB_bc is


	-- Main component declaration
	component DistanceRGB is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		--Start             : in  std_logic;
		--DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		R1          : in  std_logic_vector(63 downto 0);
		G1          : in  std_logic_vector(63 downto 0);
		B1          : in  std_logic_vector(63 downto 0);
		R2          : in  std_logic_vector(63 downto 0);
		G2          : in  std_logic_vector(63 downto 0);
		B2          : in  std_logic_vector(63 downto 0);
		--outputs
		deta_E        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
    end component;



	signal clk, clk_n : std_logic := '0';

	-- Signals to connect the instantiated multi-match component
	signal rst           : std_logic := '0';
	--signal DataRead            : std_logic := '1';
	--signal Start            : std_logic := '1';
	
	signal R1             : std_logic_vector(63 downto 0) := (others => '0');
	signal G1             : std_logic_vector(63 downto 0) := (others => '0');
	signal B1             : std_logic_vector(63 downto 0) := (others => '0');
	signal R2             : std_logic_vector(63 downto 0) := (others => '0');
	signal G2             : std_logic_vector(63 downto 0) := (others => '0');
	signal B2             : std_logic_vector(63 downto 0) := (others => '0');
	signal deta_E             : std_logic_vector(63 downto 0) := (others => '0');
	
begin

	-- Clock generation
	
	clk_n <= not clk;
	clk <= clk_n after 100 ns;


	-- Instantiation of the component to test
	i_comp : DistanceRGB 
		port map (
			rst         => rst,
			clk         => clk,
			--Start         => Start,
			
			--DataRead              => DataRead ,
			R1            => R1,
			G1            => G1,
			B1            => B1,
			R2            => R2,
			G2            => G2,
			B2            => B2,
			deta_E     => deta_E
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
		R1 <= X"3FF999999999999A";   --1.6
		G1 <= X"3FEBD70A3D70A3D7";   --0.87
		--wait for 200ns;
		--wait until rising_edge(clk);
		--Start <= '0';
		--wait until rising_edge(clk);
		B1 <= X"3FF2147AE147AE14";   -- -1.13
		R2 <= X"3FF2147AE147AE14";   --1.13
		G2 <= X"3FF999999999999A";   --1.6
		B2 <= X"3FEBD70A3D70A3D7";   --0.87

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


