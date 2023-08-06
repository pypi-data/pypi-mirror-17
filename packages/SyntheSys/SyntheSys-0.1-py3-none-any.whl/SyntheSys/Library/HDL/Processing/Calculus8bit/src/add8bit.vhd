--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   10:32:22 05/11/2012
-- Design Name:   
-- Module Name:   /dev/src/HW-common/add8bit.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx V6 LX240T 
-- Tool versions: ISE 13.1 
-- Description:  r(15:0) = a(7:0) +  b(7:0)
-- 
-- submodule of calculus8bit
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
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

entity add8bit is
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0);
       b   : in std_logic_vector(7 downto 0);
       r   : out std_logic_vector(15 downto 0));
end add8bit;

architecture archi_add8bit of add8bit is
signal carry : std_logic:='0';
signal rr : std_logic_vector(15 downto 0) :=(others =>'0');
attribute keep : boolean;
attribute keep of carry : signal is true;
attribute keep of rr : signal is true;
begin

process(clk)
begin
if rising_edge(clk) then
rr <= "0000000" & (('0' & a)+ ('0' & b));
end if;
end process;

carry <= rr(8);
r<=rr;

end archi_add8bit;
