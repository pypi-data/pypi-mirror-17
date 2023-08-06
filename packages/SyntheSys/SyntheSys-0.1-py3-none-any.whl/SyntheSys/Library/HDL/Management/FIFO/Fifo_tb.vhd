LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;
USE work.profondeur.ALL;
 
ENTITY testbench IS
END testbench;
 
ARCHITECTURE tb OF testbench IS 
 
  COMPONENT fifos
  
  PORT (
    clock_ins  : IN std_logic;
    clock_outs : IN logique;
    resets     : IN std_logic;
    data_ins   : IN dataio;
    wrs        : IN logique;
    rds        : IN logique;
    ack_rds    : OUT logique;
    ack_wrs    : OUT logique;
    data_outs  : OUT dataio
    );
  END COMPONENT;
    
   --Inputs
			signal clock_ins  : STD_LOGIC;
			signal clock_outs : logique; 
			signal resets     : STD_LOGIC := '0'; 
			signal data_ins   : dataio;   
      signal wrs        : logique;
			signal rds        : logique;
   
 	--Outputs
 			signal ack_rds   : logique;
			signal ack_wrs   : logique;
			signal data_outs : dataio;

   -- Clock period definitions
      constant clk_period0 : time := 20 ns;
      constant clk_period1 : time := 31 ns;
      constant clk_period2 : time := 55 ns;
      constant clk_period3 : time := 87 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: fifos

   PORT MAP (
      clock_ins  => clock_ins,
      clock_outs => clock_outs,
      resets     => resets,
      data_ins   => data_ins,
      wrs        => wrs,
      rds        => rds,
      ack_rds    => ack_rds,
      ack_wrs    => ack_wrs,
      data_outs  => data_outs
        );

   -- Clock process definitions
   
    clk0_process :process
    begin
		clock_ins <= '0';
		wait for clk_period0/2;
		clock_ins <= '1';
		wait for clk_period0/2;
    end process;
    
    clk1_process :process
    begin
		clock_outs(0) <= '0';
		wait for clk_period1/2;
		clock_outs(0) <= '1';
		wait for clk_period1/2;
    end process;
   
    clk2_process :process
    begin
		clock_outs(1) <= '0';
		wait for clk_period2/2;
		clock_outs(1) <= '1';
		wait for clk_period2/2;
    end process;
    
    clk3_process :process
    begin
		clock_outs(2) <= '0';
		wait for clk_period3/2;
		clock_outs(2) <= '1';
		wait for clk_period3/2;
    end process; 
   
    data_ins1_process :process
    begin
    data_ins(0) <= "0000000000000000";
    wait for 10 ns;
    data_ins(0) <= "0000000000000001";
    wait for 20 ns;
    data_ins(0) <= "0000000000000010";
    wait for 20 ns;
    data_ins(0) <= "0000000000000011";
    wait for 20 ns;
    data_ins(0) <= "0000000000000100";
    wait for 20 ns;
    data_ins(0) <= "0000000000000101";
    wait for 20 ns;
    end process;
 
    data_ins2_process :process
    begin
    data_ins(1) <= "0000000000000110";
    wait for 10 ns;
    data_ins(1) <= "0000000000000111";
    wait for 20 ns;
    data_ins(1) <= "0000000000001000";
    wait for 20 ns;
    data_ins(1) <= "0000000000001001";
    wait for 20 ns;
    data_ins(1) <= "0000000000001010";
    wait for 20 ns;
    data_ins(1) <= "0000000000001011";
    wait for 20 ns;
    end process;
    
    data_ins3_process :process
    begin
    data_ins(2) <= "0000000000001100";
    wait for 10 ns;
    data_ins(2) <= "0000000000001101";
    wait for 20 ns;
    data_ins(2) <= "0000000000001110";
    wait for 20 ns;
    data_ins(2) <= "0000000000001111";
    wait for 20 ns;
    data_ins(2) <= "0000000000010000";
    wait for 20 ns;
    data_ins(2) <= "0000000000010001";
    wait for 20 ns;
    end process;
 
    wr1_process :process
    begin
    wrs(0) <= '1';
    wait for 100 ns;
    wrs(0) <= '0';
    wait for 100 ns;
    end process;
    
    wr2_process :process
    begin
    wrs(1) <= '1';
    wait for 120 ns;
    wrs(1) <= '0';
    wait for 120 ns;
    end process;
    
    wr3_process :process
    begin
    wrs(2) <= '1';
    wait for 90 ns;
    wrs(2) <= '0';
    wait for 90 ns;
    end process;

    rd1_process :process
    begin
    rds(0) <= '0';
    wait for 100 ns;
    rds(0) <= '1';
    wait for 100 ns;
    end process;
    
    rd2_process :process
    begin
    rds(1) <= '0';
    wait for 120 ns;
    rds(1) <= '1';
    wait for 120 ns;
    end process;
    
    rd3_process :process
    begin
    rds(2) <= '0';
    wait for 90 ns;
    rds(2) <= '1';
    wait for 90 ns;
    end process;

END;
