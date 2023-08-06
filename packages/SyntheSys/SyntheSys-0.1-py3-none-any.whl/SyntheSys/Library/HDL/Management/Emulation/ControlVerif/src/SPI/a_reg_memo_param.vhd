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

entity a_reg_memo_param is
  generic (
         SIZE_IN : integer := 32);
  Port ( 
        enable            : in   STD_LOGIC                              ;
        dataIn            : in   STD_LOGIC_VECTOR (SIZE_IN-1  downto 0) ;
        samplingClk       : in   STD_LOGIC                              ;
        resetn            : in   STD_LOGIC                              ;
        syncDataOut       : out  STD_LOGIC_VECTOR (SIZE_IN-1  downto 0)
       );
end a_reg_memo_param;

architecture behavioral of a_reg_memo_param is

  begin

-- synchronize inputs on fast sampling clk

  sampling : process (samplingClk, resetn)
    
  begin
      if resetn = '0' then
          syncDataOut <= (others => '0');
      elsif rising_edge (samplingClk) then
        if(enable='1') then
          syncDataOut <= dataIn;
        end if;
      end if;
  end process sampling;

end behavioral;
        

