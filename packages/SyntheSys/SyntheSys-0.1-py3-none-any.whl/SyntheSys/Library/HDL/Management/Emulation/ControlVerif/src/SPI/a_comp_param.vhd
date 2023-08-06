--------------------------------------------------------------------------------
-- Company: 
-- Engineer: OF
--
-- Create Date:    06/21/2012
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_comp_param.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--        Cellule de comparaison parametrable a 2 Vecteurs d' entrees.
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--                    _______
--          SIZE_COMP|       |
-- dataIn_a ===//===>|\      |
--                   | > (=) |--------> egalOut (actif si (dataIn_a = datAIn_b))
-- dataIn_b ===//===>|/      |
--                   |       |
--                    -------
--
-- Notes: Use all material in this file at your own risk. 
--        makes no claims about any material contained in this file.
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a_comp_param is
  generic (
            SIZE_COMP: integer := 4);
  Port    ( dataIn_a          : in   STD_LOGIC_VECTOR (SIZE_COMP-1  downto 0);
            dataIn_b          : in   STD_LOGIC_VECTOR (SIZE_COMP-1  downto 0);
            egalOut           : out  STD_LOGIC
           );
end a_comp_param;

architecture behavioral of a_comp_param is

  begin

--  Test Egalite des Vecteurs d' entres

          egalOut <= '1' when (dataIn_a = dataIn_b) else '0';

end behavioral;
        

