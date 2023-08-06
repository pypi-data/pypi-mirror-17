--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   19:52:22 05/11/2012
-- Design Name:   
-- Module Name:   /dev/src/HW_common/ChooseResult.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx Spartan 6 
-- Tool versions:  
-- Description:  mux in vhdl for choosing the output result
-- 
-- 
-- 
-- Dependencies:
-- 
-- Revision: 0.5
-- Revision 0.01 - File Created
-- Additional Comments:
--                      
--
-- Notes: Use all material in this file at your own risk. ADACSYS SAS
--        makes no claims about any material contained in this file.
-- 
----------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

entity ChooseResult is
port ( clk : in std_logic;
       radd : in std_logic_vector (15 downto 0);
       rsub : in std_logic_vector (15 downto 0);
       rshift : in std_logic_vector (15 downto 0);
       rmux : in std_logic_vector (15 downto 0);
       sel : in std_logic_vector (1 downto 0);
       r : out std_logic_vector(15 downto 0)
       );
end entity ChooseResult;

architecture archi_ChooseResult of ChooseResult is
begin

process(clk)
begin
 if clk'event and clk='1' then
  case sel is
   when "00" => r <= radd;
   when "01" => r <= rsub;
   when "10" => r <= rmux;
   when "11" => r <= rshift;
   when others => r <= (others =>'0');
   end case;
 end if;
end process;

end architecture archi_ChooseResult;