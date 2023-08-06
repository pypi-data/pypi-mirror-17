--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   10:32:22 05/11/2012
-- Design Name:   
-- Module Name:   /dev/src/HW-common/libraries/cal8_lib/p_sub8bit.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx V6 LX240T 
-- Tool versions: ISE 13.1 
-- Description:  package in personal library example
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


package p_mux8bit is
function mux8bit (a,b :   std_logic_vector) return  std_logic_vector;
end;

package body p_mux8bit is

function mux8bit (a,b :  std_logic_vector) return  std_logic_vector is
  
  begin
  
  return (a * b); 
  
  end function;
end package body;
  
