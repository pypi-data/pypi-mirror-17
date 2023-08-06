LIBRARY IEEE;
	USE IEEE.STD_LOGIC_1164.ALL;
	USE IEEE.STD_LOGIC_ARITH.ALL;
	USE IEEE.STD_LOGIC_UNSIGNED.ALL;

LIBRARY UNISIM;
	USE UNISIM.VComponents.all;

ENTITY ctrl_096s_096t_000b_100m_mono IS
	PORT (
             sysclk_p	: IN STD_LOGIC;
	     sysclk_n	: IN STD_LOGIC;
             rst_ext_i 	: IN STD_LOGIC;
		--===== Communication Input/Output =====--
             cs_spi   	: IN  STD_LOGIC;
             clk_spi  	: IN  STD_LOGIC;
             di_spi   	: IN  STD_LOGIC;
             do_spi   	: OUT STD_LOGIC;
		--===== Ava-Test Input/Output =====--
--             trce_i 	: IN STD_LOGIC_VECTOR(95 downto 0); 
--             clk_matrix	: OUT STD_LOGIC;
--             stim_o 	: OUT STD_LOGIC_VECTOR(95 downto 0);
             led_rst_o	: OUT STD_LOGIC;
             led_o	: OUT STD_LOGIC_VECTOR(2 downto 0)
             );
END ctrl_096s_096t_000b_100m_mono;
 
ARCHITECTURE fpgaCtrl_spi_behav OF ctrl_096s_096t_000b_100m_mono IS

--========================================================================
-- COMPONENT DECLARATION
--========================================================================
	COMPONENT a_fp0 PORT(
		            clk_ref 		: IN STD_LOGIC;
		            rst_ext_i 		: IN STD_LOGIC;
		            cs_spi   		: IN STD_LOGIC;
                            clk_spi  		: IN STD_LOGIC;
                            di_spi   		: IN STD_LOGIC;
                            do_spi   		: OUT STD_LOGIC;
		            odut_i 		: IN STD_LOGIC_VECTOR(95 downto 0);     
		            clk_user_o 		: OUT STD_LOGIC;
		            idut_o 		: OUT STD_LOGIC_VECTOR(95 downto 0);
	                    led_o 		: OUT STD_LOGIC_VECTOR(10 downto 0)
                            );
	END COMPONENT;
	
	COMPONENT clk_100m_200m_005m port(-- Clock in ports
		          CLK_IN1_P      : IN STD_LOGIC;
		          CLK_IN1_N      : IN STD_LOGIC;
		           -- Clock out ports
		          CLK_OUT1       : OUT STD_LOGIC;
		          CLK_OUT2       : OUT STD_LOGIC;
		          CLK_OUT3       : OUT STD_LOGIC
	                  );
	END COMPONENT;	

--========================================================================
-- INTERNAL SIGNAL DECLARATION
--========================================================================	

	--===================== hor module Inputs/Outputs signals =====================--	
	signal clk_ref_100M		: std_logic;
	signal clk_200M			: std_logic := '0';
	
	--===================== a_fp0 module Inputs/Outputs signals =====================--
	signal a_fp0_stim_o		: std_logic_vector(95 downto 0);	
	signal a_fp0_stim_reg_o 	: std_logic_vector(95 downto 0);	
        signal a_fp0_stim_reg_oa 	: std_logic_vector(95 downto 0);
        signal a_fp0_stim_cnst_o        : std_logic_vector(95 downto 0);
	signal a_fp0_clk_user_o		: std_logic;
	signal a_fp0_led_o 		: std_logic_vector(10 downto 0);

        signal a_fp0_stim_bidir         : std_logic_vector(95 downto 0);
        signal a_fp0_stim_ctrl_bidir    : std_logic_vector(95 downto 0);
        signal trce_bidir               : std_logic_vector(95 downto 0);
        signal trce_cnst_i              : std_logic_vector(95 downto 0);
        signal GestionCtrl              : std_logic                    ;
        signal CtrlAllA                 : std_logic_vector(7  downto 0);
        signal CtrlAll                  : std_logic_vector(15 downto 0);
	--===================== Sampling registers at clk_200M =====================--
	signal trce_reg0		: std_logic_vector(95 downto 0); 
	signal trce_reg1 		: std_logic_vector(95 downto 0);
	signal trce_reg2 		: std_logic_vector(95 downto 0);

	signal trce_i, stim_o           : STD_LOGIC_VECTOR(95 downto 0);

BEGIN

clk_inst : clk_100m_200m_005m 
port map(
	-- Clock in ports
	CLK_IN1_P          	=> sysclk_p,
	CLK_IN1_N          	=> sysclk_n,
	-- Clock out ports
	CLK_OUT1           	=> clk_ref_100M,
	CLK_OUT2           	=> clk_200M,
	CLK_OUT3           	=> open
	);


a_fp0_inst : a_fp0 PORT MAP(
		           clk_ref    => clk_ref_100M,
		           rst_ext_i  => rst_ext_i,
		
		           cs_spi     =>	cs_spi,
                           clk_spi    => clk_spi,
                           di_spi     => di_spi,
                           do_spi     => do_spi,

		           clk_user_o => a_fp0_clk_user_o,
		           idut_o     => a_fp0_stim_o,
		           odut_i     => trce_reg2,
		           led_o      => a_fp0_led_o
	                   );

--=================================================================
-- InOut sent to DUT
--=================================================================

a_fp0_stim_ctrl_bidir <= "000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"&"0000000000"; -- A changer pour Bidir les Ctrls

config_inout: for i in 95 downto 0 generate    -- Etant l'emplacement des ios dans la memoire que l'on veux
  IOBUF_inst : IOBUF
               generic map (
                           DRIVE => 24,
                           IOSTANDARD => "DEFAULT",
                           SLEW => "FAST")
               port map (
                        O  => trce_bidir(i),       -- Buffer output VERS La Trace
                        IO => a_fp0_stim_bidir(i), -- Buffer inout port (connect directly to top-level port) Note dans l'ucf il ne faut pas dire que c'est un Inout car le compilateur l'infere automatiquement
                        I  => a_fp0_stim_reg_oa(i),        -- Buffer input  VIENS DES STIMULIs
                        T  => a_fp0_stim_ctrl_bidir(i)  -- 3-state enable input, high=input, low=output VIENS DES STIMULIs ou EXTERIEUR (en fonction du Design)
                        );
end generate config_inout;

--=================================================================
-- Output Clk_User to DUT
--=================================================================
clk_matrix <= a_fp0_clk_user_o ;		

--=================================================================
-- Stimuli sent to DUT
--=================================================================

process(clk_200M)
	begin
		if(rising_edge(clk_200M))then
			a_fp0_stim_reg_o	<= a_fp0_stim_o;
                        a_fp0_stim_reg_oa	<= a_fp0_stim_reg_o;
		end if;
end process;
-- Output Connection --

stim_o	<= a_fp0_stim_bidir; -- Construire pour les Bidirs l'ordonnancement

--=================================================================
-- Trace Sampled from DUT
--=================================================================
--trce_cnst_i <= trce_i(95 downto 78) & trce_bidir(67 downto 52) & trce_i(60 downto 45) & GestionCtrl & trce_i(44 downto 0);

process(clk_200M)
begin
	if (rising_edge(clk_200M)) then
		trce_reg0	<= trce_i    ;
		trce_reg1 	<= trce_reg0 ;
                trce_reg2       <= trce_reg1 ; -- Ajout a ce niveau quand il y a des Bidirs "trce_cnst_i"
	end if;
end process;

--=================================================================
-- Information LEDs
--=================================================================
-- From AVA-TEST --
led_o			<= a_fp0_led_o(1 downto 0) & a_fp0_led_o(9);  
-- Reset Level Visualisation --
led_rst_o	<= rst_ext_i;


trce_i <= stim_o;





END ARCHITECTURE;













