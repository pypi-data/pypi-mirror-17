--------------------------------------------------------------------------------
--
-- Create Date:    05/16/2012
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_rst_block.vhd
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

entity a_rst_block is
         port (
              clk_ref      : in   STD_LOGIC;
              rst_n_i      : in   STD_LOGIC;

              init_rst_n_o : out   STD_LOGIC
              );
end a_rst_block;

architecture behavioral of a_rst_block is

    signal init_rst_n_int : STD_LOGIC ;
    signal start_cell     : STD_LOGIC ;

  begin

init_rst_n_o <= init_rst_n_int;

GestionRst : process (clk_ref)
  begin
        if rising_edge (clk_ref) then
          if(rst_n_i='1') then
                     init_rst_n_int <= '0' ;
                     start_cell     <= '0' ;

            elsif(start_cell='0') then
                     init_rst_n_int <= '0' ;
                     start_cell     <= '1' ;
  
              elsif(start_cell='1') then
                     init_rst_n_int <= '1' ;
                     start_cell     <= '1' ;

                else
                     init_rst_n_int <= '0' ;
                     start_cell     <= '0' ;
           end if;
        end if;
  end process GestionRst;

end behavioral;
