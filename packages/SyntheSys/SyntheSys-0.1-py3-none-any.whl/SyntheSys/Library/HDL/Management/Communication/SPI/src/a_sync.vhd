--------------------------------------------------------------------------------
--
-- Create Date:    05/16/2012
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_sync.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--  syncronized input signals from a clock domaine to fast sampling clock
--  this is the first step of embedded logic analyser on FPGA
--
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
-- Revision 0.02 - Add Asynchrone Reset and Parameter for the Data I/O Sizing 
--                 By OF:w
--
--
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a_sync is
  generic (
         SIZE_IN : integer := 32);
  Port ( dataIn            : in   STD_LOGIC_VECTOR (SIZE_IN-1  downto 0);
         samplingClk       : in   STD_LOGIC;
         resetn            : in   STD_LOGIC;
         syncDataOut       : out  STD_LOGIC_VECTOR (SIZE_IN-1  downto 0)
  );
end a_sync;

architecture behavioral of a_sync is

  begin

-- synchronize inputs on fast sampling clk

  sampling : process (samplingClk, resetn)
    
  begin
      if resetn = '0' then
          syncDataOut <= (others => '0');
      elsif rising_edge (samplingClk) then
          syncDataOut <= dataIn;
      end if;
  end process sampling;

end behavioral;
        

