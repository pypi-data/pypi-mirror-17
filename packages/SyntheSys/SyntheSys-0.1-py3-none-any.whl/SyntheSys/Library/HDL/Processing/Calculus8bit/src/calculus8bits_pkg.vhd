--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   10:32:22 05/11/2012
-- Design Name:   
-- Module Name:   /dev/src/HW-common/packages/cal8_pkg.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx V6 LX240T 
-- Tool versions: ISE 13.1 
-- Description:  package example
-- 
-- package of calculus8bit
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
--------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

package calculus8bits_pkg is
 
 subtype stdlv8 is std_logic_vector (7 downto 0);
 subtype stdlv16 is std_logic_vector (15 downto 0);
 
end calculus8bits_pkg;
