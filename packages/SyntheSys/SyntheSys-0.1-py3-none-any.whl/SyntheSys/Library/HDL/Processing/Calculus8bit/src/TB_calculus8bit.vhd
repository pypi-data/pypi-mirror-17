--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   19:52:22 05/04/2012
-- Design Name:   
-- Module Name:   /dev/TB/global/TB_calculus8bit.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx V6 LX240T 
-- Tool versions:  
-- Description:  simple testbench to demonstrate how to import stimuli to AVA
-- 
-- VHDL Test Bench Created by ISE for module: calculus8bit
-- 
-- Dependencies:
-- 
-- Revision: 0.5
-- Revision 0.01 - File Created
-- Additional Comments:
--                      Add end of simulation
--
-- Notes: Use all material in this file at your own risk. ADACSYS SAS
--        makes no claims about any material contained in this file.
-- 
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY TB_calculus8bit IS
END TB_calculus8bit;
 
ARCHITECTURE behavior OF TB_calculus8bit IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT calculus8bit
    PORT(
         clk : IN  std_logic;
         a : IN  std_logic_vector(7 downto 0);
         b : IN  std_logic_vector(7 downto 0);
         sel : IN  std_logic_vector(1 downto 0);
         r : OUT  std_logic_vector(15 downto 0)
        );
    END COMPONENT;
    

   --Inputs stimuli
   signal clk      : std_logic := '0';
   signal a_stim   : std_logic_vector(7 downto 0) := (others => '0');
   signal b_stim   : std_logic_vector(7 downto 0) := (others => '0');
   signal sel_stim : std_logic_vector(1 downto 0) := (others => '0');

  --Outputs traces
   signal r_trace : std_logic_vector(15 downto 0);

   -- Clock period definitions
   constant clk_period : time := 10 ns;
   


BEGIN

 
 -- Instantiate the Unit Under Test (UUT)
   uut: calculus8bit PORT MAP (
          clk => clk,
          a => a_stim,
          b => b_stim,
          sel => sel_stim,
          r => r_trace
        );

   -- Clock process definitions
   clk_process :process
   begin
    clk <= '0';
    wait for clk_period/2;
    clk <= '1';
    wait for clk_period/2;
   end process clk_process;
 

   -- Stimulus process
   stim_proc: process
   begin
      -- hold reset state for 100 ns.
      wait for 10*clk_period;	

     wait for clk_period*10;

     for sel_value in (2**(sel_stim'length)-1) downto 0 loop
      for a_value in 0 to (2**(a_stim'length)-1) loop
       for b_value in 0 to (2**(b_stim'length)-1) loop
         wait until rising_edge(clk);
       a_stim <= std_logic_vector(ieee.numeric_std.to_unsigned(a_value,a_stim'length));
       b_stim <= std_logic_vector(ieee.numeric_std.to_unsigned(b_value,b_stim'length));
       sel_stim <= std_logic_vector(ieee.numeric_std.to_unsigned(sel_value,sel_stim'length));
       end loop;
      end loop;
     end loop;

--get all results		
     wait until rising_edge(clk);
     wait until rising_edge(clk);
     wait until rising_edge(clk);

     report "Test completed";		
     assert false report "NONE. End of simulation." severity failure;

   end process stim_proc;

END;
