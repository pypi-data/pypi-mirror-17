--------------------------------------------------------------------------------
--                           IntAdder_84_f400_uid8
--                    (IntAdderAlternative_84_f400_uid12)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntAdder_84_f400_uid8 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(83 downto 0);
          Y : in  std_logic_vector(83 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(83 downto 0)   );
end entity;

architecture arch of IntAdder_84_f400_uid8 is
signal s_sum_l0_idx0 :  std_logic_vector(42 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(42 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(41 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
signal sum_l0_idx1 :  std_logic_vector(41 downto 0);
signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(42 downto 0);
signal sum_l1_idx1 :  std_logic_vector(41 downto 0);
signal c_l1_idx1 :  std_logic_vector(0 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            s_sum_l0_idx1_d1 <=  s_sum_l0_idx1;
            sum_l0_idx0_d1 <=  sum_l0_idx0;
            c_l0_idx0_d1 <=  c_l0_idx0;
         end if;
      end process;
   --Alternative
   s_sum_l0_idx0 <= ( "0" & X(41 downto 0)) + ( "0" & Y(41 downto 0)) + Cin;
   s_sum_l0_idx1 <= ( "0" & X(83 downto 42)) + ( "0" & Y(83 downto 42));
   sum_l0_idx0 <= s_sum_l0_idx0(41 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(42 downto 42);
   sum_l0_idx1 <= s_sum_l0_idx1(41 downto 0);
   c_l0_idx1 <= s_sum_l0_idx1(42 downto 42);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(41 downto 0);
   c_l1_idx1 <= s_sum_l1_idx1(42 downto 42);
   R <= sum_l1_idx1(41 downto 0) & sum_l0_idx0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                             IntSquarer_51_uid6
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009)
--------------------------------------------------------------------------------
-- Pipeline depth: 4 cycles

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library work;
entity IntSquarer_51_uid6 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(50 downto 0);
          R : out  std_logic_vector(101 downto 0)   );
end entity;

architecture arch of IntSquarer_51_uid6 is
   component IntAdder_84_f400_uid8 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(83 downto 0);
             Y : in  std_logic_vector(83 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(83 downto 0)   );
   end component;

signal sigX, sigX_d1, sigX_d2 :  std_logic_vector(50 downto 0);
signal x0_16_sqr, x0_16_sqr_d1, x0_16_sqr_d2, x0_16_sqr_d3 :  std_logic_vector(33 downto 0);
signal x17_33_sqr, x17_33_sqr_d1, x17_33_sqr_d2 :  std_logic_vector(33 downto 0);
signal x34_50_sqr, x34_50_sqr_d1, x34_50_sqr_d2 :  std_logic_vector(33 downto 0);
signal x0_16_x17_33, x0_16_x17_33_d1, x0_16_x17_33_d2 :  std_logic_vector(33 downto 0);
signal x0_16_x34_50_prod, x0_16_x34_50_prod_d1 :  std_logic_vector(33 downto 0);
signal x0_16_x34_50, x0_16_x34_50_d1 :  std_logic_vector(33 downto 0);
signal x17_33_x34_50_prod, x17_33_x34_50_prod_d1 :  std_logic_vector(33 downto 0);
signal x17_33_x34_50 :  std_logic_vector(33 downto 0);
signal op1 :  std_logic_vector(83 downto 0);
signal op2 :  std_logic_vector(83 downto 0);
signal adderOutput :  std_logic_vector(83 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            sigX_d1 <=  sigX;
            sigX_d2 <=  sigX_d1;
            x0_16_sqr_d1 <=  x0_16_sqr;
            x0_16_sqr_d2 <=  x0_16_sqr_d1;
            x0_16_sqr_d3 <=  x0_16_sqr_d2;
            x17_33_sqr_d1 <=  x17_33_sqr;
            x17_33_sqr_d2 <=  x17_33_sqr_d1;
            x34_50_sqr_d1 <=  x34_50_sqr;
            x34_50_sqr_d2 <=  x34_50_sqr_d1;
            x0_16_x17_33_d1 <=  x0_16_x17_33;
            x0_16_x17_33_d2 <=  x0_16_x17_33_d1;
            x0_16_x34_50_prod_d1 <=  x0_16_x34_50_prod;
            x0_16_x34_50_d1 <=  x0_16_x34_50;
            x17_33_x34_50_prod_d1 <=  x17_33_x34_50_prod;
         end if;
      end process;
   sigX<= X;
   ----------------Synchro barrier, entering cycle 1----------------
   x0_16_sqr<= sigX_d1(16 downto 0) * sigX_d1(16 downto 0);
   x17_33_sqr<= sigX_d1(33 downto 17) * sigX_d1(33 downto 17);
   x34_50_sqr<= sigX_d1(50 downto 34) * sigX_d1(50 downto 34);
   x0_16_x17_33<= sigX_d1(16 downto 0) * sigX_d1(33 downto 17);
   x0_16_x34_50_prod<= sigX_d1(16 downto 0) * sigX_d1(50 downto 34);
   ----------------Synchro barrier, entering cycle 2----------------
   x0_16_x34_50<= x0_16_x17_33_d1(33 downto 17) + x0_16_x34_50_prod_d1;
   x17_33_x34_50_prod<= sigX_d2(33 downto 17) * sigX_d2(50 downto 34);
   ----------------Synchro barrier, entering cycle 3----------------
   x17_33_x34_50<= x0_16_x34_50_d1(33 downto 17) + x17_33_x34_50_prod_d1;
   op1<= x34_50_sqr_d2 & x17_33_sqr_d2 & x0_16_sqr_d2(33 downto 18);
   op2<= "0000000000000000" & x17_33_x34_50 & x0_16_x34_50_d1(16 downto 0) & x0_16_x17_33_d2(16 downto 0);
   ADDER1: IntAdder_84_f400_uid8  -- pipelineDepth=1 maxInDelay=4.36e-10
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => '0',
                 R => adderOutput   ,
                 X => op1,
                 Y => op2);
   R <= adderOutput(83 downto 0) & x0_16_sqr_d3(17 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_54_f400_uid15
--                    (IntAdderAlternative_54_f400_uid19)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntAdder_54_f400_uid15 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(53 downto 0);
          Y : in  std_logic_vector(53 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(53 downto 0)   );
end entity;

architecture arch of IntAdder_54_f400_uid15 is
signal s_sum_l0_idx0 :  std_logic_vector(42 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(12 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(41 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
signal sum_l0_idx1 :  std_logic_vector(11 downto 0);
signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(12 downto 0);
signal sum_l1_idx1 :  std_logic_vector(11 downto 0);
signal c_l1_idx1 :  std_logic_vector(0 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            s_sum_l0_idx1_d1 <=  s_sum_l0_idx1;
            sum_l0_idx0_d1 <=  sum_l0_idx0;
            c_l0_idx0_d1 <=  c_l0_idx0;
         end if;
      end process;
   --Alternative
   s_sum_l0_idx0 <= ( "0" & X(41 downto 0)) + ( "0" & Y(41 downto 0)) + Cin;
   s_sum_l0_idx1 <= ( "0" & X(53 downto 42)) + ( "0" & Y(53 downto 42));
   sum_l0_idx0 <= s_sum_l0_idx0(41 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(42 downto 42);
   sum_l0_idx1 <= s_sum_l0_idx1(11 downto 0);
   c_l0_idx1 <= s_sum_l0_idx1(12 downto 12);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(11 downto 0);
   c_l1_idx1 <= s_sum_l1_idx1(12 downto 12);
   R <= sum_l1_idx1(11 downto 0) & sum_l0_idx0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_53_f400_uid21
--                    (IntAdderAlternative_53_f400_uid25)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntAdder_53_f400_uid21 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(52 downto 0);
          Y : in  std_logic_vector(52 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(52 downto 0)   );
end entity;

architecture arch of IntAdder_53_f400_uid21 is
signal s_sum_l0_idx0 :  std_logic_vector(42 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(11 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(41 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
signal sum_l0_idx1 :  std_logic_vector(10 downto 0);
signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(11 downto 0);
signal sum_l1_idx1 :  std_logic_vector(10 downto 0);
signal c_l1_idx1 :  std_logic_vector(0 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            s_sum_l0_idx1_d1 <=  s_sum_l0_idx1;
            sum_l0_idx0_d1 <=  sum_l0_idx0;
            c_l0_idx0_d1 <=  c_l0_idx0;
         end if;
      end process;
   --Alternative
   s_sum_l0_idx0 <= ( "0" & X(41 downto 0)) + ( "0" & Y(41 downto 0)) + Cin;
   s_sum_l0_idx1 <= ( "0" & X(52 downto 42)) + ( "0" & Y(52 downto 42));
   sum_l0_idx0 <= s_sum_l0_idx0(41 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(42 downto 42);
   sum_l0_idx1 <= s_sum_l0_idx1(10 downto 0);
   c_l0_idx1 <= s_sum_l0_idx1(11 downto 11);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(10 downto 0);
   c_l1_idx1 <= s_sum_l1_idx1(11 downto 11);
   R <= sum_l1_idx1(10 downto 0) & sum_l0_idx0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                             IntSquarer_53_uid4
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009)
--------------------------------------------------------------------------------
-- Pipeline depth: 6 cycles

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library work;
entity IntSquarer_53_uid4 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(52 downto 0);
          R : out  std_logic_vector(105 downto 0)   );
end entity;

architecture arch of IntSquarer_53_uid4 is
   component IntAdder_53_f400_uid21 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(52 downto 0);
             Y : in  std_logic_vector(52 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(52 downto 0)   );
   end component;

   component IntAdder_54_f400_uid15 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(53 downto 0);
             Y : in  std_logic_vector(53 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(53 downto 0)   );
   end component;

   component IntSquarer_51_uid6 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(50 downto 0);
             R : out  std_logic_vector(101 downto 0)   );
   end component;

signal sigX, sigX_d1, sigX_d2, sigX_d3, sigX_d4 :  std_logic_vector(52 downto 0);
signal out_Squarer_51, out_Squarer_51_d1, out_Squarer_51_d2 :  std_logic_vector(101 downto 0);
signal op1mul2, op1mul2_d1 :  std_logic_vector(52 downto 0);
signal op2mul2, op2mul2_d1 :  std_logic_vector(52 downto 0);
signal x51_52_times_x_0_50, x51_52_times_x_0_50_d1, x51_52_times_x_0_50_d2, x51_52_times_x_0_50_d3 :  std_logic_vector(52 downto 0);
signal x51_52_sqr, x51_52_sqr_d1 :  std_logic_vector(3 downto 0);
signal op1 :  std_logic_vector(53 downto 0);
signal op2 :  std_logic_vector(53 downto 0);
signal adderOutput :  std_logic_vector(53 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            sigX_d1 <=  sigX;
            sigX_d2 <=  sigX_d1;
            sigX_d3 <=  sigX_d2;
            sigX_d4 <=  sigX_d3;
            out_Squarer_51_d1 <=  out_Squarer_51;
            out_Squarer_51_d2 <=  out_Squarer_51_d1;
            op1mul2_d1 <=  op1mul2;
            op2mul2_d1 <=  op2mul2;
            x51_52_times_x_0_50_d1 <=  x51_52_times_x_0_50;
            x51_52_times_x_0_50_d2 <=  x51_52_times_x_0_50_d1;
            x51_52_times_x_0_50_d3 <=  x51_52_times_x_0_50_d2;
            x51_52_sqr_d1 <=  x51_52_sqr;
         end if;
      end process;
   sigX<= X;
   SQUARER51: IntSquarer_51_uid6  -- pipelineDepth=4 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 R => out_Squarer_51   ,
                 X => sigX(50 downto 0));
   op1mul2<= ("00" & sigX(50 downto 0)) when sigX(51)='1' else "00000000000000000000000000000000000000000000000000000";
   op2mul2<= ("0" & sigX(50 downto 0) & "0") when sigX(52)='1' else "00000000000000000000000000000000000000000000000000000";
   ----------------Synchro barrier, entering cycle 1----------------
   MULT2: IntAdder_53_f400_uid21  -- pipelineDepth=1 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => '0',
                 R => x51_52_times_x_0_50   ,
                 X => op1mul2_d1,
                 Y => op2mul2_d1);
   ----------------Synchro barrier, entering cycle 4----------------
   x51_52_sqr <= sigX_d4(52 downto 51) * sigX_d4(52 downto 51);
   ----------------Synchro barrier, entering cycle 5----------------
   op1<= x51_52_sqr_d1 & out_Squarer_51_d1(101 downto 52);
   op2<="0" & x51_52_times_x_0_50_d3;
   ADDER54: IntAdder_54_f400_uid15  -- pipelineDepth=1 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => '0',
                 R => adderOutput   ,
                 X => op1,
                 Y => op2);
   R <= adderOutput & out_Squarer_51_d2(51 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_65_f400_uid31
--                     (IntAdderClassical_65_f400_uid33)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 2 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntAdder_65_f400_uid31 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(64 downto 0);
          Y : in  std_logic_vector(64 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(64 downto 0)   );
end entity;

architecture arch of IntAdder_65_f400_uid31 is
signal x0 :  std_logic_vector(13 downto 0);
signal y0 :  std_logic_vector(13 downto 0);
signal x1, x1_d1 :  std_logic_vector(41 downto 0);
signal y1, y1_d1 :  std_logic_vector(41 downto 0);
signal x2, x2_d1, x2_d2 :  std_logic_vector(8 downto 0);
signal y2, y2_d1, y2_d2 :  std_logic_vector(8 downto 0);
signal sum0, sum0_d1, sum0_d2 :  std_logic_vector(14 downto 0);
signal sum1, sum1_d1 :  std_logic_vector(42 downto 0);
signal sum2 :  std_logic_vector(9 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            x1_d1 <=  x1;
            y1_d1 <=  y1;
            x2_d1 <=  x2;
            x2_d2 <=  x2_d1;
            y2_d1 <=  y2;
            y2_d2 <=  y2_d1;
            sum0_d1 <=  sum0;
            sum0_d2 <=  sum0_d1;
            sum1_d1 <=  sum1;
         end if;
      end process;
   --Classical
   x0 <= X(13 downto 0);
   y0 <= Y(13 downto 0);
   x1 <= X(55 downto 14);
   y1 <= Y(55 downto 14);
   x2 <= X(64 downto 56);
   y2 <= Y(64 downto 56);
   sum0 <= ( "0" & x0) + ( "0" & y0)  + Cin;
   ----------------Synchro barrier, entering cycle 1----------------
   sum1 <= ( "0" & x1_d1) + ( "0" & y1_d1)  + sum0_d1(14);
   ----------------Synchro barrier, entering cycle 2----------------
   sum2 <= ( "0" & x2_d2) + ( "0" & y2_d2)  + sum1_d1(42);
   R <= sum2(8 downto 0) & sum1_d1(41 downto 0) & sum0_d2(13 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           FPSquare_11_52_52_uid2
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009)
--------------------------------------------------------------------------------
-- Pipeline depth: 9 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPSquare_11_52_52_uid2 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end entity;

architecture arch of FPSquare_11_52_52_uid2 is
   component IntAdder_65_f400_uid31 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(64 downto 0);
             Y : in  std_logic_vector(64 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(64 downto 0)   );
   end component;

   component IntSquarer_53_uid4 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(52 downto 0);
             R : out  std_logic_vector(105 downto 0)   );
   end component;

signal exc, exc_d1, exc_d2, exc_d3, exc_d4, exc_d5, exc_d6, exc_d7, exc_d8, exc_d9 :  std_logic_vector(1 downto 0);
signal exp :  std_logic_vector(10 downto 0);
signal frac :  std_logic_vector(52 downto 0);
signal extExponent :  std_logic_vector(12 downto 0);
signal negBias :  std_logic_vector(12 downto 0);
signal extExpPostBiasSub, extExpPostBiasSub_d1, extExpPostBiasSub_d2, extExpPostBiasSub_d3, extExpPostBiasSub_d4, extExpPostBiasSub_d5, extExpPostBiasSub_d6, extExpPostBiasSub_d7 :  std_logic_vector(12 downto 0);
signal sqrFrac, sqrFrac_d1 :  std_logic_vector(105 downto 0);
signal sticky :  std_logic;
signal guard :  std_logic;
signal fracULP :  std_logic;
signal extExp :  std_logic_vector(12 downto 0);
signal finalFrac :  std_logic_vector(51 downto 0);
signal concatExpFrac :  std_logic_vector(64 downto 0);
signal addCin :  std_logic;
signal postRound :  std_logic_vector(64 downto 0);
signal excConcat :  std_logic_vector(3 downto 0);
signal excR :  std_logic_vector(1 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            exc_d1 <=  exc;
            exc_d2 <=  exc_d1;
            exc_d3 <=  exc_d2;
            exc_d4 <=  exc_d3;
            exc_d5 <=  exc_d4;
            exc_d6 <=  exc_d5;
            exc_d7 <=  exc_d6;
            exc_d8 <=  exc_d7;
            exc_d9 <=  exc_d8;
            extExpPostBiasSub_d1 <=  extExpPostBiasSub;
            extExpPostBiasSub_d2 <=  extExpPostBiasSub_d1;
            extExpPostBiasSub_d3 <=  extExpPostBiasSub_d2;
            extExpPostBiasSub_d4 <=  extExpPostBiasSub_d3;
            extExpPostBiasSub_d5 <=  extExpPostBiasSub_d4;
            extExpPostBiasSub_d6 <=  extExpPostBiasSub_d5;
            extExpPostBiasSub_d7 <=  extExpPostBiasSub_d6;
            sqrFrac_d1 <=  sqrFrac;
         end if;
      end process;
   exc <= X(65 downto 64);
   exp <= X(62 downto 52);
   frac <= "1" & X(51 downto 0);
   extExponent<="0" & exp & "0";
   negBias<=CONV_STD_LOGIC_VECTOR(7168,13);
   extExpPostBiasSub <= extExponent + negBias + '1';
   FractionSquarer: IntSquarer_53_uid4  -- pipelineDepth=6 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 R => sqrFrac   ,
                 X => frac);
   ----------------Synchro barrier, entering cycle 6----------------
   ----------------Synchro barrier, entering cycle 7----------------
   sticky<='0' when sqrFrac_d1(50 downto 0)="000000000000000000000000000000000000000000000000000"else '1';
   guard <= sqrFrac_d1(51) when sqrFrac_d1(105)='0' else sqrFrac_d1(52);
   fracULP<=sqrFrac_d1(52) when sqrFrac_d1(105)='0' else sqrFrac_d1(53);
   extExp <= extExpPostBiasSub_d7 + sqrFrac_d1(105);
   finalFrac<= sqrFrac_d1(104 downto 53) when sqrFrac_d1(105)='1' else 
      sqrFrac_d1(103 downto 52);
   concatExpFrac <= extExp & finalFrac;
   addCin <= (guard and sticky) or (fracULP and guard and not(sticky));
   Rounding_Instance: IntAdder_65_f400_uid31  -- pipelineDepth=2 maxInDelay=1.48744e-09
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => addCin,
                 R => postRound,
                 X => concatExpFrac,
                 Y => "00000000000000000000000000000000000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 9----------------
   excConcat <= exc_d9 & postRound(64 downto 63);
   with excConcat select 
   excR<="00" when "0000",
      "00" when "0001",
      "00" when "0010",
      "00" when "0011",
      "01" when "0100",
      "10" when "0101",
      "00" when "0110",
      "00" when "0111",
      "10" when "1000",
      "10" when "1001",
      "10" when "1010",
      "10" when "1011",
      "11" when "1100",
      "11" when "1101",
      "11" when "1110",
      "11" when "1111",
      "11" when others;
   R <= excR &  "0"  & postRound(62 downto 52) & postRound(51 downto 0);
end architecture;

