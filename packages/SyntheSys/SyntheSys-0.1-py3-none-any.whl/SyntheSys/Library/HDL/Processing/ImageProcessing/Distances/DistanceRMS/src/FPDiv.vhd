--------------------------------------------------------------------------------
--                            SelFunctionTable_r8
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Maxime Christ, Florent de Dinechin (2015)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
entity SelFunctionTable_r8 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(6 downto 0);
          Y : out  std_logic_vector(3 downto 0)   );
end entity;

architecture arch of SelFunctionTable_r8 is
begin
  with X select  Y <= 
   "0000" when "0000000",
   "0000" when "0000001",
   "0000" when "0000010",
   "0000" when "0000011",
   "0001" when "0000100",
   "0001" when "0000101",
   "0001" when "0000110",
   "0001" when "0000111",
   "0001" when "0001000",
   "0001" when "0001001",
   "0001" when "0001010",
   "0001" when "0001011",
   "0010" when "0001100",
   "0010" when "0001101",
   "0010" when "0001110",
   "0010" when "0001111",
   "0011" when "0010000",
   "0011" when "0010001",
   "0010" when "0010010",
   "0010" when "0010011",
   "0011" when "0010100",
   "0011" when "0010101",
   "0011" when "0010110",
   "0011" when "0010111",
   "0100" when "0011000",
   "0100" when "0011001",
   "0011" when "0011010",
   "0011" when "0011011",
   "0101" when "0011100",
   "0100" when "0011101",
   "0100" when "0011110",
   "0100" when "0011111",
   "0101" when "0100000",
   "0101" when "0100001",
   "0101" when "0100010",
   "0100" when "0100011",
   "0110" when "0100100",
   "0110" when "0100101",
   "0101" when "0100110",
   "0101" when "0100111",
   "0111" when "0101000",
   "0110" when "0101001",
   "0110" when "0101010",
   "0101" when "0101011",
   "0111" when "0101100",
   "0111" when "0101101",
   "0110" when "0101110",
   "0110" when "0101111",
   "0111" when "0110000",
   "0111" when "0110001",
   "0111" when "0110010",
   "0110" when "0110011",
   "0111" when "0110100",
   "0111" when "0110101",
   "0111" when "0110110",
   "0111" when "0110111",
   "0111" when "0111000",
   "0111" when "0111001",
   "0111" when "0111010",
   "0111" when "0111011",
   "0111" when "0111100",
   "0111" when "0111101",
   "0111" when "0111110",
   "0111" when "0111111",
   "1001" when "1000000",
   "1001" when "1000001",
   "1001" when "1000010",
   "1001" when "1000011",
   "1001" when "1000100",
   "1001" when "1000101",
   "1001" when "1000110",
   "1001" when "1000111",
   "1001" when "1001000",
   "1001" when "1001001",
   "1001" when "1001010",
   "1001" when "1001011",
   "1001" when "1001100",
   "1001" when "1001101",
   "1001" when "1001110",
   "1001" when "1001111",
   "1001" when "1010000",
   "1001" when "1010001",
   "1010" when "1010010",
   "1010" when "1010011",
   "1001" when "1010100",
   "1010" when "1010101",
   "1010" when "1010110",
   "1010" when "1010111",
   "1010" when "1011000",
   "1010" when "1011001",
   "1011" when "1011010",
   "1011" when "1011011",
   "1011" when "1011100",
   "1011" when "1011101",
   "1011" when "1011110",
   "1011" when "1011111",
   "1011" when "1100000",
   "1011" when "1100001",
   "1100" when "1100010",
   "1100" when "1100011",
   "1100" when "1100100",
   "1100" when "1100101",
   "1100" when "1100110",
   "1100" when "1100111",
   "1100" when "1101000",
   "1101" when "1101001",
   "1101" when "1101010",
   "1101" when "1101011",
   "1101" when "1101100",
   "1101" when "1101101",
   "1101" when "1101110",
   "1101" when "1101111",
   "1110" when "1110000",
   "1110" when "1110001",
   "1110" when "1110010",
   "1110" when "1110011",
   "1110" when "1110100",
   "1110" when "1110101",
   "1110" when "1110110",
   "1110" when "1110111",
   "1111" when "1111000",
   "1111" when "1111001",
   "1111" when "1111010",
   "1111" when "1111011",
   "1111" when "1111100",
   "1111" when "1111101",
   "1111" when "1111110",
   "1111" when "1111111",
   "----" when others;
end architecture;

--------------------------------------------------------------------------------
--                              FPDiv_11_52_F400
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Maxime Christ, Florent de Dinechin (2015)
--------------------------------------------------------------------------------
-- Pipeline depth: 23 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPDiv_11_52_F400 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end entity;

architecture arch of FPDiv_11_52_F400 is
   component SelFunctionTable_r8 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(6 downto 0);
             Y : out  std_logic_vector(3 downto 0)   );
   end component;

signal partialFX :  std_logic_vector(52 downto 0);
signal partialFY :  std_logic_vector(52 downto 0);
signal expR0, expR0_d1, expR0_d2, expR0_d3, expR0_d4, expR0_d5, expR0_d6, expR0_d7, expR0_d8, expR0_d9, expR0_d10, expR0_d11, expR0_d12, expR0_d13, expR0_d14, expR0_d15, expR0_d16, expR0_d17, expR0_d18, expR0_d19, expR0_d20, expR0_d21, expR0_d22 :  std_logic_vector(12 downto 0);
signal sR, sR_d1, sR_d2, sR_d3, sR_d4, sR_d5, sR_d6, sR_d7, sR_d8, sR_d9, sR_d10, sR_d11, sR_d12, sR_d13, sR_d14, sR_d15, sR_d16, sR_d17, sR_d18, sR_d19, sR_d20, sR_d21, sR_d22, sR_d23 :  std_logic;
signal exnXY :  std_logic_vector(3 downto 0);
signal exnR0, exnR0_d1, exnR0_d2, exnR0_d3, exnR0_d4, exnR0_d5, exnR0_d6, exnR0_d7, exnR0_d8, exnR0_d9, exnR0_d10, exnR0_d11, exnR0_d12, exnR0_d13, exnR0_d14, exnR0_d15, exnR0_d16, exnR0_d17, exnR0_d18, exnR0_d19, exnR0_d20, exnR0_d21, exnR0_d22, exnR0_d23 :  std_logic_vector(1 downto 0);
signal fY, fY_d1, fY_d2, fY_d3, fY_d4, fY_d5, fY_d6, fY_d7, fY_d8, fY_d9, fY_d10, fY_d11, fY_d12, fY_d13, fY_d14, fY_d15, fY_d16, fY_d17, fY_d18, fY_d19, fY_d20 :  std_logic_vector(54 downto 0);
signal fX :  std_logic_vector(55 downto 0);
signal w19, w19_d1, w19_d2 :  std_logic_vector(57 downto 0);
signal sel19 :  std_logic_vector(6 downto 0);
signal q19, q19_d1, q19_d2, q19_d3, q19_d4, q19_d5, q19_d6, q19_d7, q19_d8, q19_d9, q19_d10, q19_d11, q19_d12, q19_d13, q19_d14, q19_d15, q19_d16, q19_d17, q19_d18, q19_d19 :  std_logic_vector(3 downto 0);
signal w19pad :  std_logic_vector(58 downto 0);
signal w18fulla :  std_logic_vector(58 downto 0);
signal fYdec18 :  std_logic_vector(58 downto 0);
signal w18full :  std_logic_vector(58 downto 0);
signal w18, w18_d1 :  std_logic_vector(57 downto 0);
signal sel18 :  std_logic_vector(6 downto 0);
signal q18, q18_d1, q18_d2, q18_d3, q18_d4, q18_d5, q18_d6, q18_d7, q18_d8, q18_d9, q18_d10, q18_d11, q18_d12, q18_d13, q18_d14, q18_d15, q18_d16, q18_d17, q18_d18 :  std_logic_vector(3 downto 0);
signal w18pad :  std_logic_vector(58 downto 0);
signal w17fulla :  std_logic_vector(58 downto 0);
signal fYdec17 :  std_logic_vector(58 downto 0);
signal w17full :  std_logic_vector(58 downto 0);
signal w17, w17_d1 :  std_logic_vector(57 downto 0);
signal sel17 :  std_logic_vector(6 downto 0);
signal q17, q17_d1, q17_d2, q17_d3, q17_d4, q17_d5, q17_d6, q17_d7, q17_d8, q17_d9, q17_d10, q17_d11, q17_d12, q17_d13, q17_d14, q17_d15, q17_d16, q17_d17 :  std_logic_vector(3 downto 0);
signal w17pad :  std_logic_vector(58 downto 0);
signal w16fulla :  std_logic_vector(58 downto 0);
signal fYdec16 :  std_logic_vector(58 downto 0);
signal w16full :  std_logic_vector(58 downto 0);
signal w16, w16_d1 :  std_logic_vector(57 downto 0);
signal sel16 :  std_logic_vector(6 downto 0);
signal q16, q16_d1, q16_d2, q16_d3, q16_d4, q16_d5, q16_d6, q16_d7, q16_d8, q16_d9, q16_d10, q16_d11, q16_d12, q16_d13, q16_d14, q16_d15, q16_d16 :  std_logic_vector(3 downto 0);
signal w16pad :  std_logic_vector(58 downto 0);
signal w15fulla :  std_logic_vector(58 downto 0);
signal fYdec15 :  std_logic_vector(58 downto 0);
signal w15full :  std_logic_vector(58 downto 0);
signal w15, w15_d1 :  std_logic_vector(57 downto 0);
signal sel15 :  std_logic_vector(6 downto 0);
signal q15, q15_d1, q15_d2, q15_d3, q15_d4, q15_d5, q15_d6, q15_d7, q15_d8, q15_d9, q15_d10, q15_d11, q15_d12, q15_d13, q15_d14, q15_d15 :  std_logic_vector(3 downto 0);
signal w15pad :  std_logic_vector(58 downto 0);
signal w14fulla :  std_logic_vector(58 downto 0);
signal fYdec14 :  std_logic_vector(58 downto 0);
signal w14full :  std_logic_vector(58 downto 0);
signal w14, w14_d1 :  std_logic_vector(57 downto 0);
signal sel14 :  std_logic_vector(6 downto 0);
signal q14, q14_d1, q14_d2, q14_d3, q14_d4, q14_d5, q14_d6, q14_d7, q14_d8, q14_d9, q14_d10, q14_d11, q14_d12, q14_d13, q14_d14 :  std_logic_vector(3 downto 0);
signal w14pad :  std_logic_vector(58 downto 0);
signal w13fulla :  std_logic_vector(58 downto 0);
signal fYdec13 :  std_logic_vector(58 downto 0);
signal w13full :  std_logic_vector(58 downto 0);
signal w13, w13_d1 :  std_logic_vector(57 downto 0);
signal sel13 :  std_logic_vector(6 downto 0);
signal q13, q13_d1, q13_d2, q13_d3, q13_d4, q13_d5, q13_d6, q13_d7, q13_d8, q13_d9, q13_d10, q13_d11, q13_d12, q13_d13 :  std_logic_vector(3 downto 0);
signal w13pad :  std_logic_vector(58 downto 0);
signal w12fulla :  std_logic_vector(58 downto 0);
signal fYdec12 :  std_logic_vector(58 downto 0);
signal w12full :  std_logic_vector(58 downto 0);
signal w12, w12_d1 :  std_logic_vector(57 downto 0);
signal sel12 :  std_logic_vector(6 downto 0);
signal q12, q12_d1, q12_d2, q12_d3, q12_d4, q12_d5, q12_d6, q12_d7, q12_d8, q12_d9, q12_d10, q12_d11, q12_d12 :  std_logic_vector(3 downto 0);
signal w12pad :  std_logic_vector(58 downto 0);
signal w11fulla :  std_logic_vector(58 downto 0);
signal fYdec11 :  std_logic_vector(58 downto 0);
signal w11full :  std_logic_vector(58 downto 0);
signal w11, w11_d1 :  std_logic_vector(57 downto 0);
signal sel11 :  std_logic_vector(6 downto 0);
signal q11, q11_d1, q11_d2, q11_d3, q11_d4, q11_d5, q11_d6, q11_d7, q11_d8, q11_d9, q11_d10, q11_d11 :  std_logic_vector(3 downto 0);
signal w11pad :  std_logic_vector(58 downto 0);
signal w10fulla :  std_logic_vector(58 downto 0);
signal fYdec10 :  std_logic_vector(58 downto 0);
signal w10full :  std_logic_vector(58 downto 0);
signal w10, w10_d1 :  std_logic_vector(57 downto 0);
signal sel10 :  std_logic_vector(6 downto 0);
signal q10, q10_d1, q10_d2, q10_d3, q10_d4, q10_d5, q10_d6, q10_d7, q10_d8, q10_d9, q10_d10 :  std_logic_vector(3 downto 0);
signal w10pad :  std_logic_vector(58 downto 0);
signal w9fulla :  std_logic_vector(58 downto 0);
signal fYdec9 :  std_logic_vector(58 downto 0);
signal w9full :  std_logic_vector(58 downto 0);
signal w9, w9_d1 :  std_logic_vector(57 downto 0);
signal sel9 :  std_logic_vector(6 downto 0);
signal q9, q9_d1, q9_d2, q9_d3, q9_d4, q9_d5, q9_d6, q9_d7, q9_d8, q9_d9 :  std_logic_vector(3 downto 0);
signal w9pad :  std_logic_vector(58 downto 0);
signal w8fulla :  std_logic_vector(58 downto 0);
signal fYdec8 :  std_logic_vector(58 downto 0);
signal w8full :  std_logic_vector(58 downto 0);
signal w8, w8_d1 :  std_logic_vector(57 downto 0);
signal sel8 :  std_logic_vector(6 downto 0);
signal q8, q8_d1, q8_d2, q8_d3, q8_d4, q8_d5, q8_d6, q8_d7, q8_d8 :  std_logic_vector(3 downto 0);
signal w8pad :  std_logic_vector(58 downto 0);
signal w7fulla :  std_logic_vector(58 downto 0);
signal fYdec7 :  std_logic_vector(58 downto 0);
signal w7full :  std_logic_vector(58 downto 0);
signal w7, w7_d1 :  std_logic_vector(57 downto 0);
signal sel7 :  std_logic_vector(6 downto 0);
signal q7, q7_d1, q7_d2, q7_d3, q7_d4, q7_d5, q7_d6, q7_d7 :  std_logic_vector(3 downto 0);
signal w7pad :  std_logic_vector(58 downto 0);
signal w6fulla :  std_logic_vector(58 downto 0);
signal fYdec6 :  std_logic_vector(58 downto 0);
signal w6full :  std_logic_vector(58 downto 0);
signal w6, w6_d1 :  std_logic_vector(57 downto 0);
signal sel6 :  std_logic_vector(6 downto 0);
signal q6, q6_d1, q6_d2, q6_d3, q6_d4, q6_d5, q6_d6 :  std_logic_vector(3 downto 0);
signal w6pad :  std_logic_vector(58 downto 0);
signal w5fulla :  std_logic_vector(58 downto 0);
signal fYdec5 :  std_logic_vector(58 downto 0);
signal w5full :  std_logic_vector(58 downto 0);
signal w5, w5_d1 :  std_logic_vector(57 downto 0);
signal sel5 :  std_logic_vector(6 downto 0);
signal q5, q5_d1, q5_d2, q5_d3, q5_d4, q5_d5 :  std_logic_vector(3 downto 0);
signal w5pad :  std_logic_vector(58 downto 0);
signal w4fulla :  std_logic_vector(58 downto 0);
signal fYdec4 :  std_logic_vector(58 downto 0);
signal w4full :  std_logic_vector(58 downto 0);
signal w4, w4_d1 :  std_logic_vector(57 downto 0);
signal sel4 :  std_logic_vector(6 downto 0);
signal q4, q4_d1, q4_d2, q4_d3, q4_d4 :  std_logic_vector(3 downto 0);
signal w4pad :  std_logic_vector(58 downto 0);
signal w3fulla :  std_logic_vector(58 downto 0);
signal fYdec3 :  std_logic_vector(58 downto 0);
signal w3full :  std_logic_vector(58 downto 0);
signal w3, w3_d1 :  std_logic_vector(57 downto 0);
signal sel3 :  std_logic_vector(6 downto 0);
signal q3, q3_d1, q3_d2, q3_d3 :  std_logic_vector(3 downto 0);
signal w3pad :  std_logic_vector(58 downto 0);
signal w2fulla :  std_logic_vector(58 downto 0);
signal fYdec2 :  std_logic_vector(58 downto 0);
signal w2full :  std_logic_vector(58 downto 0);
signal w2, w2_d1 :  std_logic_vector(57 downto 0);
signal sel2 :  std_logic_vector(6 downto 0);
signal q2, q2_d1, q2_d2 :  std_logic_vector(3 downto 0);
signal w2pad :  std_logic_vector(58 downto 0);
signal w1fulla :  std_logic_vector(58 downto 0);
signal fYdec1 :  std_logic_vector(58 downto 0);
signal w1full :  std_logic_vector(58 downto 0);
signal w1, w1_d1 :  std_logic_vector(57 downto 0);
signal sel1 :  std_logic_vector(6 downto 0);
signal q1, q1_d1 :  std_logic_vector(3 downto 0);
signal w1pad :  std_logic_vector(58 downto 0);
signal w0fulla :  std_logic_vector(58 downto 0);
signal fYdec0 :  std_logic_vector(58 downto 0);
signal w0full :  std_logic_vector(58 downto 0);
signal w0, w0_d1 :  std_logic_vector(57 downto 0);
signal q0 :  std_logic_vector(3 downto 0);
signal qP19 :  std_logic_vector(2 downto 0);
signal qM19 :  std_logic_vector(2 downto 0);
signal qP18 :  std_logic_vector(2 downto 0);
signal qM18 :  std_logic_vector(2 downto 0);
signal qP17 :  std_logic_vector(2 downto 0);
signal qM17 :  std_logic_vector(2 downto 0);
signal qP16 :  std_logic_vector(2 downto 0);
signal qM16 :  std_logic_vector(2 downto 0);
signal qP15 :  std_logic_vector(2 downto 0);
signal qM15 :  std_logic_vector(2 downto 0);
signal qP14 :  std_logic_vector(2 downto 0);
signal qM14 :  std_logic_vector(2 downto 0);
signal qP13 :  std_logic_vector(2 downto 0);
signal qM13 :  std_logic_vector(2 downto 0);
signal qP12 :  std_logic_vector(2 downto 0);
signal qM12 :  std_logic_vector(2 downto 0);
signal qP11 :  std_logic_vector(2 downto 0);
signal qM11 :  std_logic_vector(2 downto 0);
signal qP10 :  std_logic_vector(2 downto 0);
signal qM10 :  std_logic_vector(2 downto 0);
signal qP9 :  std_logic_vector(2 downto 0);
signal qM9 :  std_logic_vector(2 downto 0);
signal qP8 :  std_logic_vector(2 downto 0);
signal qM8 :  std_logic_vector(2 downto 0);
signal qP7 :  std_logic_vector(2 downto 0);
signal qM7 :  std_logic_vector(2 downto 0);
signal qP6 :  std_logic_vector(2 downto 0);
signal qM6 :  std_logic_vector(2 downto 0);
signal qP5 :  std_logic_vector(2 downto 0);
signal qM5 :  std_logic_vector(2 downto 0);
signal qP4 :  std_logic_vector(2 downto 0);
signal qM4 :  std_logic_vector(2 downto 0);
signal qP3 :  std_logic_vector(2 downto 0);
signal qM3 :  std_logic_vector(2 downto 0);
signal qP2 :  std_logic_vector(2 downto 0);
signal qM2 :  std_logic_vector(2 downto 0);
signal qP1 :  std_logic_vector(2 downto 0);
signal qM1 :  std_logic_vector(2 downto 0);
signal qP0 :  std_logic_vector(2 downto 0);
signal qM0 :  std_logic_vector(2 downto 0);
signal qP :  std_logic_vector(59 downto 0);
signal qM :  std_logic_vector(59 downto 0);
signal fR0, fR0_d1 :  std_logic_vector(59 downto 0);
signal fR :  std_logic_vector(57 downto 0);
signal fRn1, fRn1_d1 :  std_logic_vector(55 downto 0);
signal expR1, expR1_d1 :  std_logic_vector(12 downto 0);
signal round, round_d1 :  std_logic;
signal expfrac :  std_logic_vector(64 downto 0);
signal expfracR :  std_logic_vector(64 downto 0);
signal exnR :  std_logic_vector(1 downto 0);
signal exnRfinal :  std_logic_vector(1 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            expR0_d1 <=  expR0;
            expR0_d2 <=  expR0_d1;
            expR0_d3 <=  expR0_d2;
            expR0_d4 <=  expR0_d3;
            expR0_d5 <=  expR0_d4;
            expR0_d6 <=  expR0_d5;
            expR0_d7 <=  expR0_d6;
            expR0_d8 <=  expR0_d7;
            expR0_d9 <=  expR0_d8;
            expR0_d10 <=  expR0_d9;
            expR0_d11 <=  expR0_d10;
            expR0_d12 <=  expR0_d11;
            expR0_d13 <=  expR0_d12;
            expR0_d14 <=  expR0_d13;
            expR0_d15 <=  expR0_d14;
            expR0_d16 <=  expR0_d15;
            expR0_d17 <=  expR0_d16;
            expR0_d18 <=  expR0_d17;
            expR0_d19 <=  expR0_d18;
            expR0_d20 <=  expR0_d19;
            expR0_d21 <=  expR0_d20;
            expR0_d22 <=  expR0_d21;
            sR_d1 <=  sR;
            sR_d2 <=  sR_d1;
            sR_d3 <=  sR_d2;
            sR_d4 <=  sR_d3;
            sR_d5 <=  sR_d4;
            sR_d6 <=  sR_d5;
            sR_d7 <=  sR_d6;
            sR_d8 <=  sR_d7;
            sR_d9 <=  sR_d8;
            sR_d10 <=  sR_d9;
            sR_d11 <=  sR_d10;
            sR_d12 <=  sR_d11;
            sR_d13 <=  sR_d12;
            sR_d14 <=  sR_d13;
            sR_d15 <=  sR_d14;
            sR_d16 <=  sR_d15;
            sR_d17 <=  sR_d16;
            sR_d18 <=  sR_d17;
            sR_d19 <=  sR_d18;
            sR_d20 <=  sR_d19;
            sR_d21 <=  sR_d20;
            sR_d22 <=  sR_d21;
            sR_d23 <=  sR_d22;
            exnR0_d1 <=  exnR0;
            exnR0_d2 <=  exnR0_d1;
            exnR0_d3 <=  exnR0_d2;
            exnR0_d4 <=  exnR0_d3;
            exnR0_d5 <=  exnR0_d4;
            exnR0_d6 <=  exnR0_d5;
            exnR0_d7 <=  exnR0_d6;
            exnR0_d8 <=  exnR0_d7;
            exnR0_d9 <=  exnR0_d8;
            exnR0_d10 <=  exnR0_d9;
            exnR0_d11 <=  exnR0_d10;
            exnR0_d12 <=  exnR0_d11;
            exnR0_d13 <=  exnR0_d12;
            exnR0_d14 <=  exnR0_d13;
            exnR0_d15 <=  exnR0_d14;
            exnR0_d16 <=  exnR0_d15;
            exnR0_d17 <=  exnR0_d16;
            exnR0_d18 <=  exnR0_d17;
            exnR0_d19 <=  exnR0_d18;
            exnR0_d20 <=  exnR0_d19;
            exnR0_d21 <=  exnR0_d20;
            exnR0_d22 <=  exnR0_d21;
            exnR0_d23 <=  exnR0_d22;
            fY_d1 <=  fY;
            fY_d2 <=  fY_d1;
            fY_d3 <=  fY_d2;
            fY_d4 <=  fY_d3;
            fY_d5 <=  fY_d4;
            fY_d6 <=  fY_d5;
            fY_d7 <=  fY_d6;
            fY_d8 <=  fY_d7;
            fY_d9 <=  fY_d8;
            fY_d10 <=  fY_d9;
            fY_d11 <=  fY_d10;
            fY_d12 <=  fY_d11;
            fY_d13 <=  fY_d12;
            fY_d14 <=  fY_d13;
            fY_d15 <=  fY_d14;
            fY_d16 <=  fY_d15;
            fY_d17 <=  fY_d16;
            fY_d18 <=  fY_d17;
            fY_d19 <=  fY_d18;
            fY_d20 <=  fY_d19;
            w19_d1 <=  w19;
            w19_d2 <=  w19_d1;
            q19_d1 <=  q19;
            q19_d2 <=  q19_d1;
            q19_d3 <=  q19_d2;
            q19_d4 <=  q19_d3;
            q19_d5 <=  q19_d4;
            q19_d6 <=  q19_d5;
            q19_d7 <=  q19_d6;
            q19_d8 <=  q19_d7;
            q19_d9 <=  q19_d8;
            q19_d10 <=  q19_d9;
            q19_d11 <=  q19_d10;
            q19_d12 <=  q19_d11;
            q19_d13 <=  q19_d12;
            q19_d14 <=  q19_d13;
            q19_d15 <=  q19_d14;
            q19_d16 <=  q19_d15;
            q19_d17 <=  q19_d16;
            q19_d18 <=  q19_d17;
            q19_d19 <=  q19_d18;
            w18_d1 <=  w18;
            q18_d1 <=  q18;
            q18_d2 <=  q18_d1;
            q18_d3 <=  q18_d2;
            q18_d4 <=  q18_d3;
            q18_d5 <=  q18_d4;
            q18_d6 <=  q18_d5;
            q18_d7 <=  q18_d6;
            q18_d8 <=  q18_d7;
            q18_d9 <=  q18_d8;
            q18_d10 <=  q18_d9;
            q18_d11 <=  q18_d10;
            q18_d12 <=  q18_d11;
            q18_d13 <=  q18_d12;
            q18_d14 <=  q18_d13;
            q18_d15 <=  q18_d14;
            q18_d16 <=  q18_d15;
            q18_d17 <=  q18_d16;
            q18_d18 <=  q18_d17;
            w17_d1 <=  w17;
            q17_d1 <=  q17;
            q17_d2 <=  q17_d1;
            q17_d3 <=  q17_d2;
            q17_d4 <=  q17_d3;
            q17_d5 <=  q17_d4;
            q17_d6 <=  q17_d5;
            q17_d7 <=  q17_d6;
            q17_d8 <=  q17_d7;
            q17_d9 <=  q17_d8;
            q17_d10 <=  q17_d9;
            q17_d11 <=  q17_d10;
            q17_d12 <=  q17_d11;
            q17_d13 <=  q17_d12;
            q17_d14 <=  q17_d13;
            q17_d15 <=  q17_d14;
            q17_d16 <=  q17_d15;
            q17_d17 <=  q17_d16;
            w16_d1 <=  w16;
            q16_d1 <=  q16;
            q16_d2 <=  q16_d1;
            q16_d3 <=  q16_d2;
            q16_d4 <=  q16_d3;
            q16_d5 <=  q16_d4;
            q16_d6 <=  q16_d5;
            q16_d7 <=  q16_d6;
            q16_d8 <=  q16_d7;
            q16_d9 <=  q16_d8;
            q16_d10 <=  q16_d9;
            q16_d11 <=  q16_d10;
            q16_d12 <=  q16_d11;
            q16_d13 <=  q16_d12;
            q16_d14 <=  q16_d13;
            q16_d15 <=  q16_d14;
            q16_d16 <=  q16_d15;
            w15_d1 <=  w15;
            q15_d1 <=  q15;
            q15_d2 <=  q15_d1;
            q15_d3 <=  q15_d2;
            q15_d4 <=  q15_d3;
            q15_d5 <=  q15_d4;
            q15_d6 <=  q15_d5;
            q15_d7 <=  q15_d6;
            q15_d8 <=  q15_d7;
            q15_d9 <=  q15_d8;
            q15_d10 <=  q15_d9;
            q15_d11 <=  q15_d10;
            q15_d12 <=  q15_d11;
            q15_d13 <=  q15_d12;
            q15_d14 <=  q15_d13;
            q15_d15 <=  q15_d14;
            w14_d1 <=  w14;
            q14_d1 <=  q14;
            q14_d2 <=  q14_d1;
            q14_d3 <=  q14_d2;
            q14_d4 <=  q14_d3;
            q14_d5 <=  q14_d4;
            q14_d6 <=  q14_d5;
            q14_d7 <=  q14_d6;
            q14_d8 <=  q14_d7;
            q14_d9 <=  q14_d8;
            q14_d10 <=  q14_d9;
            q14_d11 <=  q14_d10;
            q14_d12 <=  q14_d11;
            q14_d13 <=  q14_d12;
            q14_d14 <=  q14_d13;
            w13_d1 <=  w13;
            q13_d1 <=  q13;
            q13_d2 <=  q13_d1;
            q13_d3 <=  q13_d2;
            q13_d4 <=  q13_d3;
            q13_d5 <=  q13_d4;
            q13_d6 <=  q13_d5;
            q13_d7 <=  q13_d6;
            q13_d8 <=  q13_d7;
            q13_d9 <=  q13_d8;
            q13_d10 <=  q13_d9;
            q13_d11 <=  q13_d10;
            q13_d12 <=  q13_d11;
            q13_d13 <=  q13_d12;
            w12_d1 <=  w12;
            q12_d1 <=  q12;
            q12_d2 <=  q12_d1;
            q12_d3 <=  q12_d2;
            q12_d4 <=  q12_d3;
            q12_d5 <=  q12_d4;
            q12_d6 <=  q12_d5;
            q12_d7 <=  q12_d6;
            q12_d8 <=  q12_d7;
            q12_d9 <=  q12_d8;
            q12_d10 <=  q12_d9;
            q12_d11 <=  q12_d10;
            q12_d12 <=  q12_d11;
            w11_d1 <=  w11;
            q11_d1 <=  q11;
            q11_d2 <=  q11_d1;
            q11_d3 <=  q11_d2;
            q11_d4 <=  q11_d3;
            q11_d5 <=  q11_d4;
            q11_d6 <=  q11_d5;
            q11_d7 <=  q11_d6;
            q11_d8 <=  q11_d7;
            q11_d9 <=  q11_d8;
            q11_d10 <=  q11_d9;
            q11_d11 <=  q11_d10;
            w10_d1 <=  w10;
            q10_d1 <=  q10;
            q10_d2 <=  q10_d1;
            q10_d3 <=  q10_d2;
            q10_d4 <=  q10_d3;
            q10_d5 <=  q10_d4;
            q10_d6 <=  q10_d5;
            q10_d7 <=  q10_d6;
            q10_d8 <=  q10_d7;
            q10_d9 <=  q10_d8;
            q10_d10 <=  q10_d9;
            w9_d1 <=  w9;
            q9_d1 <=  q9;
            q9_d2 <=  q9_d1;
            q9_d3 <=  q9_d2;
            q9_d4 <=  q9_d3;
            q9_d5 <=  q9_d4;
            q9_d6 <=  q9_d5;
            q9_d7 <=  q9_d6;
            q9_d8 <=  q9_d7;
            q9_d9 <=  q9_d8;
            w8_d1 <=  w8;
            q8_d1 <=  q8;
            q8_d2 <=  q8_d1;
            q8_d3 <=  q8_d2;
            q8_d4 <=  q8_d3;
            q8_d5 <=  q8_d4;
            q8_d6 <=  q8_d5;
            q8_d7 <=  q8_d6;
            q8_d8 <=  q8_d7;
            w7_d1 <=  w7;
            q7_d1 <=  q7;
            q7_d2 <=  q7_d1;
            q7_d3 <=  q7_d2;
            q7_d4 <=  q7_d3;
            q7_d5 <=  q7_d4;
            q7_d6 <=  q7_d5;
            q7_d7 <=  q7_d6;
            w6_d1 <=  w6;
            q6_d1 <=  q6;
            q6_d2 <=  q6_d1;
            q6_d3 <=  q6_d2;
            q6_d4 <=  q6_d3;
            q6_d5 <=  q6_d4;
            q6_d6 <=  q6_d5;
            w5_d1 <=  w5;
            q5_d1 <=  q5;
            q5_d2 <=  q5_d1;
            q5_d3 <=  q5_d2;
            q5_d4 <=  q5_d3;
            q5_d5 <=  q5_d4;
            w4_d1 <=  w4;
            q4_d1 <=  q4;
            q4_d2 <=  q4_d1;
            q4_d3 <=  q4_d2;
            q4_d4 <=  q4_d3;
            w3_d1 <=  w3;
            q3_d1 <=  q3;
            q3_d2 <=  q3_d1;
            q3_d3 <=  q3_d2;
            w2_d1 <=  w2;
            q2_d1 <=  q2;
            q2_d2 <=  q2_d1;
            w1_d1 <=  w1;
            q1_d1 <=  q1;
            w0_d1 <=  w0;
            fR0_d1 <=  fR0;
            fRn1_d1 <=  fRn1;
            expR1_d1 <=  expR1;
            round_d1 <=  round;
         end if;
      end process;
   partialFX <= "1" & X(51 downto 0);
   partialFY <= "1" & Y(51 downto 0);
   -- exponent difference, sign and exception combination computed early, to have less bits to pipeline
   expR0 <= ("00" & X(62 downto 52)) - ("00" & Y(62 downto 52));
   sR <= X(63) xor Y(63);
   -- early exception handling 
   exnXY <= X(65 downto 64) & Y(65 downto 64);
   with exnXY select
      exnR0 <= 
         "01"  when "0101",                   -- normal
         "00"  when "0001" | "0010" | "0110", -- zero
         "10"  when "0100" | "1000" | "1001", -- overflow
         "11"  when others;                   -- NaN
    -- Prescaling
   with partialFY (51 downto 50) select
      fY <= 
         ("0" & partialFY & "0") + (partialFY & "00") when "00",
         ("00" & partialFY) + (partialFY & "00") when "01",
         partialFY &"00" when others;
   with partialFY (51 downto 50) select
      fX <= 
         ("00" & partialFX & "0") + ("0" & partialFX & "00") when "00",
         ("000" & partialFX) + ("0" & partialFX & "00") when "01",
         "0" & partialFX &"00" when others;
   w19 <=  "00" & fX;
   ----------------Synchro barrier, entering cycle 1----------------
   ----------------Synchro barrier, entering cycle 2----------------
   sel19 <= w19_d2(57 downto 53) & fY_d2(52 downto 51);
   SelFunctionTable19: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel19,
                 Y => q19);
   w19pad <= w19_d2 & '0';
   with q19(1 downto 0) select 
   w18fulla <= 
      w19pad - ("0000" & fY_d2)			when "01",
      w19pad + ("0000" & fY_d2)			when "11",
      w19pad + ("000" & fY_d2 & "0")	  when "10",
      w19pad 			   		  when others;
   with q19(3 downto 1) select 
   fYdec18 <= 
      ("00" & fY_d2 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d2 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q19(3) select
   w18full <= 
      w18fulla - fYdec18			when '0',
      w18fulla + fYdec18			when others;
   w18 <= w18full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 3----------------
   sel18 <= w18_d1(57 downto 53) & fY_d3(52 downto 51);
   SelFunctionTable18: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel18,
                 Y => q18);
   w18pad <= w18_d1 & '0';
   with q18(1 downto 0) select 
   w17fulla <= 
      w18pad - ("0000" & fY_d3)			when "01",
      w18pad + ("0000" & fY_d3)			when "11",
      w18pad + ("000" & fY_d3 & "0")	  when "10",
      w18pad 			   		  when others;
   with q18(3 downto 1) select 
   fYdec17 <= 
      ("00" & fY_d3 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d3 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q18(3) select
   w17full <= 
      w17fulla - fYdec17			when '0',
      w17fulla + fYdec17			when others;
   w17 <= w17full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 4----------------
   sel17 <= w17_d1(57 downto 53) & fY_d4(52 downto 51);
   SelFunctionTable17: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel17,
                 Y => q17);
   w17pad <= w17_d1 & '0';
   with q17(1 downto 0) select 
   w16fulla <= 
      w17pad - ("0000" & fY_d4)			when "01",
      w17pad + ("0000" & fY_d4)			when "11",
      w17pad + ("000" & fY_d4 & "0")	  when "10",
      w17pad 			   		  when others;
   with q17(3 downto 1) select 
   fYdec16 <= 
      ("00" & fY_d4 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d4 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q17(3) select
   w16full <= 
      w16fulla - fYdec16			when '0',
      w16fulla + fYdec16			when others;
   w16 <= w16full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 5----------------
   sel16 <= w16_d1(57 downto 53) & fY_d5(52 downto 51);
   SelFunctionTable16: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel16,
                 Y => q16);
   w16pad <= w16_d1 & '0';
   with q16(1 downto 0) select 
   w15fulla <= 
      w16pad - ("0000" & fY_d5)			when "01",
      w16pad + ("0000" & fY_d5)			when "11",
      w16pad + ("000" & fY_d5 & "0")	  when "10",
      w16pad 			   		  when others;
   with q16(3 downto 1) select 
   fYdec15 <= 
      ("00" & fY_d5 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d5 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q16(3) select
   w15full <= 
      w15fulla - fYdec15			when '0',
      w15fulla + fYdec15			when others;
   w15 <= w15full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 6----------------
   sel15 <= w15_d1(57 downto 53) & fY_d6(52 downto 51);
   SelFunctionTable15: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel15,
                 Y => q15);
   w15pad <= w15_d1 & '0';
   with q15(1 downto 0) select 
   w14fulla <= 
      w15pad - ("0000" & fY_d6)			when "01",
      w15pad + ("0000" & fY_d6)			when "11",
      w15pad + ("000" & fY_d6 & "0")	  when "10",
      w15pad 			   		  when others;
   with q15(3 downto 1) select 
   fYdec14 <= 
      ("00" & fY_d6 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d6 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q15(3) select
   w14full <= 
      w14fulla - fYdec14			when '0',
      w14fulla + fYdec14			when others;
   w14 <= w14full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 7----------------
   sel14 <= w14_d1(57 downto 53) & fY_d7(52 downto 51);
   SelFunctionTable14: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel14,
                 Y => q14);
   w14pad <= w14_d1 & '0';
   with q14(1 downto 0) select 
   w13fulla <= 
      w14pad - ("0000" & fY_d7)			when "01",
      w14pad + ("0000" & fY_d7)			when "11",
      w14pad + ("000" & fY_d7 & "0")	  when "10",
      w14pad 			   		  when others;
   with q14(3 downto 1) select 
   fYdec13 <= 
      ("00" & fY_d7 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d7 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q14(3) select
   w13full <= 
      w13fulla - fYdec13			when '0',
      w13fulla + fYdec13			when others;
   w13 <= w13full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 8----------------
   sel13 <= w13_d1(57 downto 53) & fY_d8(52 downto 51);
   SelFunctionTable13: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel13,
                 Y => q13);
   w13pad <= w13_d1 & '0';
   with q13(1 downto 0) select 
   w12fulla <= 
      w13pad - ("0000" & fY_d8)			when "01",
      w13pad + ("0000" & fY_d8)			when "11",
      w13pad + ("000" & fY_d8 & "0")	  when "10",
      w13pad 			   		  when others;
   with q13(3 downto 1) select 
   fYdec12 <= 
      ("00" & fY_d8 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d8 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q13(3) select
   w12full <= 
      w12fulla - fYdec12			when '0',
      w12fulla + fYdec12			when others;
   w12 <= w12full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 9----------------
   sel12 <= w12_d1(57 downto 53) & fY_d9(52 downto 51);
   SelFunctionTable12: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel12,
                 Y => q12);
   w12pad <= w12_d1 & '0';
   with q12(1 downto 0) select 
   w11fulla <= 
      w12pad - ("0000" & fY_d9)			when "01",
      w12pad + ("0000" & fY_d9)			when "11",
      w12pad + ("000" & fY_d9 & "0")	  when "10",
      w12pad 			   		  when others;
   with q12(3 downto 1) select 
   fYdec11 <= 
      ("00" & fY_d9 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d9 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q12(3) select
   w11full <= 
      w11fulla - fYdec11			when '0',
      w11fulla + fYdec11			when others;
   w11 <= w11full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 10----------------
   sel11 <= w11_d1(57 downto 53) & fY_d10(52 downto 51);
   SelFunctionTable11: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel11,
                 Y => q11);
   w11pad <= w11_d1 & '0';
   with q11(1 downto 0) select 
   w10fulla <= 
      w11pad - ("0000" & fY_d10)			when "01",
      w11pad + ("0000" & fY_d10)			when "11",
      w11pad + ("000" & fY_d10 & "0")	  when "10",
      w11pad 			   		  when others;
   with q11(3 downto 1) select 
   fYdec10 <= 
      ("00" & fY_d10 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d10 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q11(3) select
   w10full <= 
      w10fulla - fYdec10			when '0',
      w10fulla + fYdec10			when others;
   w10 <= w10full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 11----------------
   sel10 <= w10_d1(57 downto 53) & fY_d11(52 downto 51);
   SelFunctionTable10: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel10,
                 Y => q10);
   w10pad <= w10_d1 & '0';
   with q10(1 downto 0) select 
   w9fulla <= 
      w10pad - ("0000" & fY_d11)			when "01",
      w10pad + ("0000" & fY_d11)			when "11",
      w10pad + ("000" & fY_d11 & "0")	  when "10",
      w10pad 			   		  when others;
   with q10(3 downto 1) select 
   fYdec9 <= 
      ("00" & fY_d11 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d11 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q10(3) select
   w9full <= 
      w9fulla - fYdec9			when '0',
      w9fulla + fYdec9			when others;
   w9 <= w9full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 12----------------
   sel9 <= w9_d1(57 downto 53) & fY_d12(52 downto 51);
   SelFunctionTable9: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel9,
                 Y => q9);
   w9pad <= w9_d1 & '0';
   with q9(1 downto 0) select 
   w8fulla <= 
      w9pad - ("0000" & fY_d12)			when "01",
      w9pad + ("0000" & fY_d12)			when "11",
      w9pad + ("000" & fY_d12 & "0")	  when "10",
      w9pad 			   		  when others;
   with q9(3 downto 1) select 
   fYdec8 <= 
      ("00" & fY_d12 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d12 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q9(3) select
   w8full <= 
      w8fulla - fYdec8			when '0',
      w8fulla + fYdec8			when others;
   w8 <= w8full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 13----------------
   sel8 <= w8_d1(57 downto 53) & fY_d13(52 downto 51);
   SelFunctionTable8: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel8,
                 Y => q8);
   w8pad <= w8_d1 & '0';
   with q8(1 downto 0) select 
   w7fulla <= 
      w8pad - ("0000" & fY_d13)			when "01",
      w8pad + ("0000" & fY_d13)			when "11",
      w8pad + ("000" & fY_d13 & "0")	  when "10",
      w8pad 			   		  when others;
   with q8(3 downto 1) select 
   fYdec7 <= 
      ("00" & fY_d13 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d13 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q8(3) select
   w7full <= 
      w7fulla - fYdec7			when '0',
      w7fulla + fYdec7			when others;
   w7 <= w7full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 14----------------
   sel7 <= w7_d1(57 downto 53) & fY_d14(52 downto 51);
   SelFunctionTable7: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel7,
                 Y => q7);
   w7pad <= w7_d1 & '0';
   with q7(1 downto 0) select 
   w6fulla <= 
      w7pad - ("0000" & fY_d14)			when "01",
      w7pad + ("0000" & fY_d14)			when "11",
      w7pad + ("000" & fY_d14 & "0")	  when "10",
      w7pad 			   		  when others;
   with q7(3 downto 1) select 
   fYdec6 <= 
      ("00" & fY_d14 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d14 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q7(3) select
   w6full <= 
      w6fulla - fYdec6			when '0',
      w6fulla + fYdec6			when others;
   w6 <= w6full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 15----------------
   sel6 <= w6_d1(57 downto 53) & fY_d15(52 downto 51);
   SelFunctionTable6: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel6,
                 Y => q6);
   w6pad <= w6_d1 & '0';
   with q6(1 downto 0) select 
   w5fulla <= 
      w6pad - ("0000" & fY_d15)			when "01",
      w6pad + ("0000" & fY_d15)			when "11",
      w6pad + ("000" & fY_d15 & "0")	  when "10",
      w6pad 			   		  when others;
   with q6(3 downto 1) select 
   fYdec5 <= 
      ("00" & fY_d15 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d15 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q6(3) select
   w5full <= 
      w5fulla - fYdec5			when '0',
      w5fulla + fYdec5			when others;
   w5 <= w5full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 16----------------
   sel5 <= w5_d1(57 downto 53) & fY_d16(52 downto 51);
   SelFunctionTable5: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel5,
                 Y => q5);
   w5pad <= w5_d1 & '0';
   with q5(1 downto 0) select 
   w4fulla <= 
      w5pad - ("0000" & fY_d16)			when "01",
      w5pad + ("0000" & fY_d16)			when "11",
      w5pad + ("000" & fY_d16 & "0")	  when "10",
      w5pad 			   		  when others;
   with q5(3 downto 1) select 
   fYdec4 <= 
      ("00" & fY_d16 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d16 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q5(3) select
   w4full <= 
      w4fulla - fYdec4			when '0',
      w4fulla + fYdec4			when others;
   w4 <= w4full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 17----------------
   sel4 <= w4_d1(57 downto 53) & fY_d17(52 downto 51);
   SelFunctionTable4: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel4,
                 Y => q4);
   w4pad <= w4_d1 & '0';
   with q4(1 downto 0) select 
   w3fulla <= 
      w4pad - ("0000" & fY_d17)			when "01",
      w4pad + ("0000" & fY_d17)			when "11",
      w4pad + ("000" & fY_d17 & "0")	  when "10",
      w4pad 			   		  when others;
   with q4(3 downto 1) select 
   fYdec3 <= 
      ("00" & fY_d17 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d17 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q4(3) select
   w3full <= 
      w3fulla - fYdec3			when '0',
      w3fulla + fYdec3			when others;
   w3 <= w3full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 18----------------
   sel3 <= w3_d1(57 downto 53) & fY_d18(52 downto 51);
   SelFunctionTable3: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel3,
                 Y => q3);
   w3pad <= w3_d1 & '0';
   with q3(1 downto 0) select 
   w2fulla <= 
      w3pad - ("0000" & fY_d18)			when "01",
      w3pad + ("0000" & fY_d18)			when "11",
      w3pad + ("000" & fY_d18 & "0")	  when "10",
      w3pad 			   		  when others;
   with q3(3 downto 1) select 
   fYdec2 <= 
      ("00" & fY_d18 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d18 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q3(3) select
   w2full <= 
      w2fulla - fYdec2			when '0',
      w2fulla + fYdec2			when others;
   w2 <= w2full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 19----------------
   sel2 <= w2_d1(57 downto 53) & fY_d19(52 downto 51);
   SelFunctionTable2: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel2,
                 Y => q2);
   w2pad <= w2_d1 & '0';
   with q2(1 downto 0) select 
   w1fulla <= 
      w2pad - ("0000" & fY_d19)			when "01",
      w2pad + ("0000" & fY_d19)			when "11",
      w2pad + ("000" & fY_d19 & "0")	  when "10",
      w2pad 			   		  when others;
   with q2(3 downto 1) select 
   fYdec1 <= 
      ("00" & fY_d19 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d19 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q2(3) select
   w1full <= 
      w1fulla - fYdec1			when '0',
      w1fulla + fYdec1			when others;
   w1 <= w1full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 20----------------
   sel1 <= w1_d1(57 downto 53) & fY_d20(52 downto 51);
   SelFunctionTable1: SelFunctionTable_r8  -- pipelineDepth=0 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 X => sel1,
                 Y => q1);
   w1pad <= w1_d1 & '0';
   with q1(1 downto 0) select 
   w0fulla <= 
      w1pad - ("0000" & fY_d20)			when "01",
      w1pad + ("0000" & fY_d20)			when "11",
      w1pad + ("000" & fY_d20 & "0")	  when "10",
      w1pad 			   		  when others;
   with q1(3 downto 1) select 
   fYdec0 <= 
      ("00" & fY_d20 & "00")			when "001" | "010" | "110"| "101",
      ("0" & fY_d20 & "000")			when "011"| "100",
      (58 downto 0 => '0')when others;
   with q1(3) select
   w0full <= 
      w0fulla - fYdec0			when '0',
      w0fulla + fYdec0			when others;
   w0 <= w0full(55 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 21----------------
   q0(3 downto 0) <= "0000" when  w0_d1 = (57 downto 0 => '0')
                else w0_d1(57) & "010";
   qP19 <=      q19_d19(2 downto 0);
   qM19 <=      q19_d19(3) & "00";
   qP18 <=      q18_d18(2 downto 0);
   qM18 <=      q18_d18(3) & "00";
   qP17 <=      q17_d17(2 downto 0);
   qM17 <=      q17_d17(3) & "00";
   qP16 <=      q16_d16(2 downto 0);
   qM16 <=      q16_d16(3) & "00";
   qP15 <=      q15_d15(2 downto 0);
   qM15 <=      q15_d15(3) & "00";
   qP14 <=      q14_d14(2 downto 0);
   qM14 <=      q14_d14(3) & "00";
   qP13 <=      q13_d13(2 downto 0);
   qM13 <=      q13_d13(3) & "00";
   qP12 <=      q12_d12(2 downto 0);
   qM12 <=      q12_d12(3) & "00";
   qP11 <=      q11_d11(2 downto 0);
   qM11 <=      q11_d11(3) & "00";
   qP10 <=      q10_d10(2 downto 0);
   qM10 <=      q10_d10(3) & "00";
   qP9 <=      q9_d9(2 downto 0);
   qM9 <=      q9_d9(3) & "00";
   qP8 <=      q8_d8(2 downto 0);
   qM8 <=      q8_d8(3) & "00";
   qP7 <=      q7_d7(2 downto 0);
   qM7 <=      q7_d7(3) & "00";
   qP6 <=      q6_d6(2 downto 0);
   qM6 <=      q6_d6(3) & "00";
   qP5 <=      q5_d5(2 downto 0);
   qM5 <=      q5_d5(3) & "00";
   qP4 <=      q4_d4(2 downto 0);
   qM4 <=      q4_d4(3) & "00";
   qP3 <=      q3_d3(2 downto 0);
   qM3 <=      q3_d3(3) & "00";
   qP2 <=      q2_d2(2 downto 0);
   qM2 <=      q2_d2(3) & "00";
   qP1 <=      q1_d1(2 downto 0);
   qM1 <=      q1_d1(3) & "00";
   qP0 <= q0(2 downto 0);
   qM0 <= q0(3)  & "00";
   qP <= qP19 & qP18 & qP17 & qP16 & qP15 & qP14 & qP13 & qP12 & qP11 & qP10 & qP9 & qP8 & qP7 & qP6 & qP5 & qP4 & qP3 & qP2 & qP1 & qP0;
   qM <= qM19(1 downto 0) & qM18 & qM17 & qM16 & qM15 & qM14 & qM13 & qM12 & qM11 & qM10 & qM9 & qM8 & qM7 & qM6 & qM5 & qM4 & qM3 & qM2 & qM1 & qM0 & "0";
   fR0 <= qP - qM;
   ----------------Synchro barrier, entering cycle 22----------------
   fR <= fR0_d1(59 downto 3) & (fR0_d1(0) or fR0_d1(1) or fR0_d1(2)); 
   -- normalisation
   with fR(56) select
      fRn1 <= fR(56 downto 2) & (fR(0) or fR(1)) when '1',
              fR(55 downto 0)          when others;
   expR1 <= expR0_d22 + ("000" & (9 downto 1 => '1') & fR(56)); -- add back bias
   round <= fRn1(2) and (fRn1(0) or fRn1(1) or fRn1(3)); -- fRn1(0) is the sticky bit
   ----------------Synchro barrier, entering cycle 23----------------
   -- final rounding
   expfrac <= expR1_d1 & fRn1_d1(54 downto 3) ;
   expfracR <= expfrac + ((64 downto 1 => '0') & round_d1);
   exnR <=      "00"  when expfracR(64) = '1'   -- underflow
           else "10"  when  expfracR(64 downto 63) =  "01" -- overflow
           else "01";      -- 00, normal case
   with exnR0_d23 select
      exnRfinal <= 
         exnR   when "01", -- normal
         exnR0_d23  when others;
   R <= exnRfinal & sR_d23 & expfracR(62 downto 0);
end architecture;

