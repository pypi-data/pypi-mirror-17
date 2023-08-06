--------------------------------------------------------------------------------
-- Company: ADACSYS
-- Engineer:
--
-- Create Date:   10:32:22 05/11/2012
-- Design Name:   
-- Module Name:   /dev/src/HW-common/calculus8bit.vhd
-- Project Name:  calculus8bit
-- Target Device: Xilinx V6 LX240T 
-- Tool versions: ISE 13.1 
-- Description:  top file example
-- 
-- top entity of calculus8bit
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
use work.calculus8bits_pkg.all;

library calculus8bits_lib;
use calculus8bits_lib.p_mux8bit.all;


entity calculus8bit is
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0); 
       b   : in std_logic_vector(7 downto 0);
       sel : in std_logic_vector(1 downto 0);
       r   : out std_logic_vector(15 downto 0));
end calculus8bit;

architecture archi_calculus8bit of calculus8bit is

signal radd: std_logic_vector(15 downto 0) :=(others =>'0');
signal rsub: std_logic_vector(15 downto 0) :=(others =>'0');
signal rshift: std_logic_vector(15 downto 0) :=(others =>'0');
signal rmux: std_logic_vector(15 downto 0) :=(others =>'0');

attribute keep : boolean;
attribute keep of radd : signal is true;
attribute keep of rsub : signal is true;
attribute keep of rshift : signal is true;
attribute keep of rmux : signal is true;

component add8bit  
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0);
       b   : in std_logic_vector(7 downto 0);
       r   : out std_logic_vector(15 downto 0));
end component;

component sub8bit  
port ( clk : in std_logic;
       a   : in std_logic_vector(7 downto 0);
	   b   : in std_logic_vector(7 downto 0);
	   r   : out std_logic_vector(15 downto 0));
end component;

component shift8bit  
port ( clk : in std_logic;
       a   : in stdlv8;
       b   : in stdlv8;
       r   : out stdlv16);
end component;

component ChooseResult
port ( clk : in std_logic;
       radd   : in std_logic_vector(15 downto 0);
       rsub   : in std_logic_vector(15 downto 0);
       rshift : in std_logic_vector(15 downto 0);
       rmux   : in std_logic_vector(15 downto 0);
       r      : out std_logic_vector(15 downto 0);
       sel    : in std_logic_vector(1 downto 0));
end component;
begin

U_add: add8bit port map(clk, a, b, radd);
U_sub: sub8bit port map(clk, a, b, rsub);
rmux <= mux8bit(a, b);
U_shift : shift8bit port map(clk, a, b, rshift);

U_ChooseResult: ChooseResult port map (clk, radd, rsub, rshift, rmux, r, sel);

end archi_calculus8bit;
