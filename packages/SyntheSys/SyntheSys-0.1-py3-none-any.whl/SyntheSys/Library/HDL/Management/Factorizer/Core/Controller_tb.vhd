--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   19:52:22 05/04/2012
-- Design Name:   
-- Module Name:   /dev/TB/global/Controller_tb.vhd
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

ENTITY Controller_tb IS
END Controller_tb;
 
ARCHITECTURE behavior OF Controller_tb IS 
 
   constant DATAWIDTH  : natural := 16;
   constant ADDRWIDTH  : natural := 14;
   constant NBDEP      : natural := 2;
   -- Clock period definitions
   constant clk_period : time := 10 ns;
   
    -- Component Declaration for the Unit Under Test (UUT)
    COMPONENT Controller
    generic (
         DATAWIDTH : natural := 16;
         ADDRWIDTH : natural := 16;
         NBDEP  : natural := 2);
    PORT(
         Rst : IN  std_logic;
         Clk : IN  std_logic;
         Debug_Idle  : out  std_logic;
    
         InReq    : in  std_logic;
         OutReq   : out std_logic;
         Busy     : out std_logic;
         DataIn   : in  std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
         DataOut  : out std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
    
    -- RAM interface
         RAM_din    : out STD_LOGIC_VECTOR (NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
         RAM_wen    : out STD_LOGIC;
         RAM_wraddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
         RAM_rdaddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
         RAM_dout   : in  STD_LOGIC_VECTOR (NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0)   
    );
    END COMPONENT;
    
   --Inputs stimuli
   signal Rst        : std_logic := '0';
   signal Clk        : std_logic := '0';
   signal Debug_Idle : std_logic := '0';
  
   signal InReq      : std_logic;
   signal OutReq     : std_logic;
   signal Busy       : std_logic;
   signal DataIn     : std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
   signal DataOut    : std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
   signal RAM_din    : std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);
   signal RAM_wen    : std_logic;
   signal RAM_wraddr : std_logic_vector(ADDRWIDTH-1 downto 0);
   signal RAM_rdaddr : std_logic_vector(ADDRWIDTH-1 downto 0);
   signal RAM_dout   : std_logic_vector(NBDEP+NBDEP*ADDRWIDTH+DATAWIDTH downto 0);

BEGIN

 -- Instantiate the Unit Under Test (UUT)
   Controller_1: Controller 
   GENERIC MAP (
         DATAWIDTH   => DATAWIDTH,
         ADDRWIDTH   => ADDRWIDTH,
         NBDEP       => NBDEP
        )
   PORT MAP (
         Rst        => Rst,
         Clk        => Clk,
         Debug_Idle => Debug_Idle,
    
         InReq      => InReq,
         OutReq     => OutReq,
         Busy       => Busy,
         DataIn     => DataIn,
         DataOut    => DataOut,
    
    -- RAM interface
         RAM_din    => RAM_din,
         RAM_wen    => RAM_wen,
         RAM_wraddr => RAM_wraddr,
         RAM_rdaddr => RAM_rdaddr,
         RAM_dout   => RAM_dout
        );

   -- Clock process definitions
   clk_process :process
   begin
    Clk <= '0';
    wait for clk_period/2;
    Clk <= '1';
    wait for clk_period/2;
   end process clk_process;

   ------------------------------------------------------
   -- Stimulus process
   stim_proc: process
   begin
     ----------------------------------
     Rst      <= '1';
     InReq    <= '0';
     DataIn   <= (others=>'0');
    -- RAM interface
     RAM_dout <= (others=>'0');
     
     ----------------------------------
     -- hold reset state for 50 ns.
     wait for clk_period*50;
     Rst      <= '0';
    
     ----------------------------------
     wait for 30 ns;
     InReq    <= '1', '0' after clk_period;
     DataIn   <= "000"&X"000"&X"0000"&X"0001"; -- Cmd : config
    -- RAM interface
     RAM_dout <= "000"&X"000"&X"0000"&X"0000";
     
     ----------------------------------
     wait for 30 ns;
     InReq    <= '1', '0' after clk_period;
     DataIn   <= "000"&X"000"&X"0000"&X"0002"; -- Cmd : config
    -- RAM interface
     RAM_dout <= "000"&X"000"&X"0000"&X"0000";
     
     ----------------------------------
     wait for 30 ns;
     InReq    <= '1', '0' after clk_period;
     DataIn   <= "000"&X"000"&X"0000"&X"0002"; -- Cmd : config
    -- RAM interface
     RAM_dout <= "000"&X"000"&X"0000"&X"0000";

    --get all results		
     wait until rising_edge(clk);
     wait until rising_edge(clk);
     wait until rising_edge(clk);

     report "Test completed";		
     assert false report "NONE. End of simulation." severity failure;

   end process stim_proc;

END;
