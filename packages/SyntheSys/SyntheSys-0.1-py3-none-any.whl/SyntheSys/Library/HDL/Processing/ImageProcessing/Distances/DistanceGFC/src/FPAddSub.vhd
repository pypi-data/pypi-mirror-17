--------------------------------------------------------------------------------
--                           IntAdder_66_f400_uid4
--                     (IntAdderAlternative_66_f400_uid8)
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

entity IntAdder_66_f400_uid4 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(65 downto 0);
          Y : in  std_logic_vector(65 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(65 downto 0)   );
end entity;

architecture arch of IntAdder_66_f400_uid4 is
signal s_sum_l0_idx0 :  std_logic_vector(42 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(24 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(41 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
signal sum_l0_idx1 :  std_logic_vector(23 downto 0);
signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(24 downto 0);
signal sum_l1_idx1 :  std_logic_vector(23 downto 0);
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
   s_sum_l0_idx1 <= ( "0" & X(65 downto 42)) + ( "0" & Y(65 downto 42));
   sum_l0_idx0 <= s_sum_l0_idx0(41 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(42 downto 42);
   sum_l0_idx1 <= s_sum_l0_idx1(23 downto 0);
   c_l0_idx1 <= s_sum_l0_idx1(24 downto 24);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(23 downto 0);
   c_l1_idx1 <= s_sum_l1_idx1(24 downto 24);
   R <= sum_l1_idx1(23 downto 0) & sum_l0_idx0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                      FPAddSub_11_52_uid2_RightShifter
--                   (RightShifter_53_by_max_55_F400_uid11)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2011)
--------------------------------------------------------------------------------
-- Pipeline depth: 2 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPAddSub_11_52_uid2_RightShifter is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(52 downto 0);
          S : in  std_logic_vector(5 downto 0);
          R : out  std_logic_vector(107 downto 0)   );
end entity;

architecture arch of FPAddSub_11_52_uid2_RightShifter is
signal level0 :  std_logic_vector(52 downto 0);
signal ps, ps_d1, ps_d2 :  std_logic_vector(5 downto 0);
signal level1 :  std_logic_vector(53 downto 0);
signal level2, level2_d1 :  std_logic_vector(55 downto 0);
signal level3 :  std_logic_vector(59 downto 0);
signal level4, level4_d1 :  std_logic_vector(67 downto 0);
signal level5 :  std_logic_vector(83 downto 0);
signal level6 :  std_logic_vector(115 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            ps_d1 <=  ps;
            ps_d2 <=  ps_d1;
            level2_d1 <=  level2;
            level4_d1 <=  level4;
         end if;
      end process;
   level0<= X;
   ps<= S;
   level1<=  (0 downto 0 => '0') & level0 when ps(0) = '1' else    level0 & (0 downto 0 => '0');
   level2<=  (1 downto 0 => '0') & level1 when ps(1) = '1' else    level1 & (1 downto 0 => '0');
   ----------------Synchro barrier, entering cycle 1----------------
   level3<=  (3 downto 0 => '0') & level2_d1 when ps_d1(2) = '1' else    level2_d1 & (3 downto 0 => '0');
   level4<=  (7 downto 0 => '0') & level3 when ps_d1(3) = '1' else    level3 & (7 downto 0 => '0');
   ----------------Synchro barrier, entering cycle 2----------------
   level5<=  (15 downto 0 => '0') & level4_d1 when ps_d2(4) = '1' else    level4_d1 & (15 downto 0 => '0');
   level6<=  (31 downto 0 => '0') & level5 when ps_d2(5) = '1' else    level5 & (31 downto 0 => '0');
   R <= level6(115 downto 8);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_56_f400_uid14
--                     (IntAdderClassical_56_f400_uid16)
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

entity IntAdder_56_f400_uid14 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(55 downto 0);
          Y : in  std_logic_vector(55 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(55 downto 0)   );
end entity;

architecture arch of IntAdder_56_f400_uid14 is
signal x0 :  std_logic_vector(41 downto 0);
signal y0 :  std_logic_vector(41 downto 0);
signal x1, x1_d1 :  std_logic_vector(13 downto 0);
signal y1, y1_d1 :  std_logic_vector(13 downto 0);
signal sum0, sum0_d1 :  std_logic_vector(42 downto 0);
signal sum1 :  std_logic_vector(14 downto 0);
signal X_d1 :  std_logic_vector(55 downto 0);
signal Y_d1 :  std_logic_vector(55 downto 0);
signal Cin_d1 :  std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            x1_d1 <=  x1;
            y1_d1 <=  y1;
            sum0_d1 <=  sum0;
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
   x0 <= X_d1(41 downto 0);
   y0 <= Y_d1(41 downto 0);
   x1 <= X_d1(55 downto 42);
   y1 <= Y_d1(55 downto 42);
   sum0 <= ( "0" & x0) + ( "0" & y0)  + Cin_d1;
   ----------------Synchro barrier, entering cycle 2----------------
   sum1 <= ( "0" & x1_d1) + ( "0" & y1_d1)  + sum0_d1(42);
   R <= sum1(13 downto 0) & sum0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                 LZCShifter_57_to_57_counting_64_F400_uid22
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Florent de Dinechin, Bogdan Pasca (2007)
--------------------------------------------------------------------------------
-- Pipeline depth: 3 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity LZCShifter_57_to_57_counting_64_F400_uid22 is
   port ( clk, rst : in std_logic;
          I : in  std_logic_vector(56 downto 0);
          Count : out  std_logic_vector(5 downto 0);
          O : out  std_logic_vector(56 downto 0)   );
end entity;

architecture arch of LZCShifter_57_to_57_counting_64_F400_uid22 is
signal level6, level6_d1 :  std_logic_vector(56 downto 0);
signal count5, count5_d1, count5_d2, count5_d3 :  std_logic;
signal level5 :  std_logic_vector(56 downto 0);
signal count4, count4_d1, count4_d2 :  std_logic;
signal level4, level4_d1 :  std_logic_vector(56 downto 0);
signal count3, count3_d1 :  std_logic;
signal level3 :  std_logic_vector(56 downto 0);
signal count2, count2_d1 :  std_logic;
signal level2, level2_d1 :  std_logic_vector(56 downto 0);
signal count1 :  std_logic;
signal level1 :  std_logic_vector(56 downto 0);
signal count0 :  std_logic;
signal level0 :  std_logic_vector(56 downto 0);
signal sCount :  std_logic_vector(5 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            level6_d1 <=  level6;
            count5_d1 <=  count5;
            count5_d2 <=  count5_d1;
            count5_d3 <=  count5_d2;
            count4_d1 <=  count4;
            count4_d2 <=  count4_d1;
            level4_d1 <=  level4;
            count3_d1 <=  count3;
            count2_d1 <=  count2;
            level2_d1 <=  level2;
         end if;
      end process;
   level6 <= I ;
   count5<= '1' when level6(56 downto 25) = (56 downto 25=>'0') else '0';
   ----------------Synchro barrier, entering cycle 1----------------
   level5<= level6_d1(56 downto 0) when count5_d1='0' else level6_d1(24 downto 0) & (31 downto 0 => '0');

   count4<= '1' when level5(56 downto 41) = (56 downto 41=>'0') else '0';
   level4<= level5(56 downto 0) when count4='0' else level5(40 downto 0) & (15 downto 0 => '0');

   ----------------Synchro barrier, entering cycle 2----------------
   count3<= '1' when level4_d1(56 downto 49) = (56 downto 49=>'0') else '0';
   level3<= level4_d1(56 downto 0) when count3='0' else level4_d1(48 downto 0) & (7 downto 0 => '0');

   count2<= '1' when level3(56 downto 53) = (56 downto 53=>'0') else '0';
   level2<= level3(56 downto 0) when count2='0' else level3(52 downto 0) & (3 downto 0 => '0');

   ----------------Synchro barrier, entering cycle 3----------------
   count1<= '1' when level2_d1(56 downto 55) = (56 downto 55=>'0') else '0';
   level1<= level2_d1(56 downto 0) when count1='0' else level2_d1(54 downto 0) & (1 downto 0 => '0');

   count0<= '1' when level1(56 downto 56) = (56 downto 56=>'0') else '0';
   level0<= level1(56 downto 0) when count0='0' else level1(55 downto 0) & (0 downto 0 => '0');

   O <= level0;
   sCount <= count5_d3 & count4_d2 & count3_d1 & count2_d1 & count1 & count0;
   Count <= sCount;
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_66_f400_uid25
--                    (IntAdderAlternative_66_f400_uid29)
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

entity IntAdder_66_f400_uid25 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(65 downto 0);
          Y : in  std_logic_vector(65 downto 0);
          Cin : in  std_logic;
          R : out  std_logic_vector(65 downto 0)   );
end entity;

architecture arch of IntAdder_66_f400_uid25 is
signal s_sum_l0_idx0 :  std_logic_vector(42 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(24 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(41 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
signal sum_l0_idx1 :  std_logic_vector(23 downto 0);
signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(24 downto 0);
signal sum_l1_idx1 :  std_logic_vector(23 downto 0);
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
   s_sum_l0_idx1 <= ( "0" & X(65 downto 42)) + ( "0" & Y(65 downto 42));
   sum_l0_idx0 <= s_sum_l0_idx0(41 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(42 downto 42);
   sum_l0_idx1 <= s_sum_l0_idx1(23 downto 0);
   c_l0_idx1 <= s_sum_l0_idx1(24 downto 24);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(23 downto 0);
   c_l1_idx1 <= s_sum_l1_idx1(24 downto 24);
   R <= sum_l1_idx1(23 downto 0) & sum_l0_idx0_d1(41 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                            FPAddSub_11_52_uid2
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Matei Istoan, Florent de Dinechin (2012)
--------------------------------------------------------------------------------
-- Pipeline depth: 15 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPAddSub_11_52_uid2 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          Radd : out  std_logic_vector(11+52+2 downto 0);
          Rsub : out  std_logic_vector(11+52+2 downto 0)   );
end entity;

architecture arch of FPAddSub_11_52_uid2 is
   component FPAddSub_11_52_uid2_RightShifter is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(52 downto 0);
             S : in  std_logic_vector(5 downto 0);
             R : out  std_logic_vector(107 downto 0)   );
   end component;

   component IntAdder_56_f400_uid14 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(55 downto 0);
             Y : in  std_logic_vector(55 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(55 downto 0)   );
   end component;

   component IntAdder_66_f400_uid25 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(65 downto 0);
             Y : in  std_logic_vector(65 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(65 downto 0)   );
   end component;

   component IntAdder_66_f400_uid4 is
      port ( clk, rst : in std_logic;
             X : in  std_logic_vector(65 downto 0);
             Y : in  std_logic_vector(65 downto 0);
             Cin : in  std_logic;
             R : out  std_logic_vector(65 downto 0)   );
   end component;

   component LZCShifter_57_to_57_counting_64_F400_uid22 is
      port ( clk, rst : in std_logic;
             I : in  std_logic_vector(56 downto 0);
             Count : out  std_logic_vector(5 downto 0);
             O : out  std_logic_vector(56 downto 0)   );
   end component;

signal excExpFracX :  std_logic_vector(64 downto 0);
signal excExpFracY :  std_logic_vector(64 downto 0);
signal eXmeY, eXmeY_d1 :  std_logic_vector(11 downto 0);
signal eYmeX, eYmeX_d1 :  std_logic_vector(11 downto 0);
signal addCmpOp1 :  std_logic_vector(65 downto 0);
signal addCmpOp2 :  std_logic_vector(65 downto 0);
signal cmpRes :  std_logic_vector(65 downto 0);
signal swap, swap_d1, swap_d2 :  std_logic;
signal newX, newX_d1, newX_d2, newX_d3 :  std_logic_vector(65 downto 0);
signal newY :  std_logic_vector(65 downto 0);
signal expX, expX_d1, expX_d2, expX_d3, expX_d4, expX_d5, expX_d6 :  std_logic_vector(10 downto 0);
signal excX :  std_logic_vector(1 downto 0);
signal excY :  std_logic_vector(1 downto 0);
signal signX, signX_d1 :  std_logic;
signal signY :  std_logic;
signal diffSigns, diffSigns_d1, diffSigns_d2, diffSigns_d3, diffSigns_d4, diffSigns_d5, diffSigns_d6, diffSigns_d7, diffSigns_d8, diffSigns_d9, diffSigns_d10, diffSigns_d11, diffSigns_d12, diffSigns_d13 :  std_logic;
signal sXsYExnXY, sXsYExnXY_d1 :  std_logic_vector(5 downto 0);
signal fracY :  std_logic_vector(52 downto 0);
signal excRtRAdd, excRtRAdd_d1, excRtRAdd_d2, excRtRAdd_d3, excRtRAdd_d4, excRtRAdd_d5, excRtRAdd_d6, excRtRAdd_d7, excRtRAdd_d8, excRtRAdd_d9, excRtRAdd_d10, excRtRAdd_d11, excRtRAdd_d12 :  std_logic_vector(1 downto 0);
signal excRtRSub, excRtRSub_d1, excRtRSub_d2, excRtRSub_d3, excRtRSub_d4, excRtRSub_d5, excRtRSub_d6, excRtRSub_d7, excRtRSub_d8, excRtRSub_d9, excRtRSub_d10, excRtRSub_d11, excRtRSub_d12 :  std_logic_vector(1 downto 0);
signal signRAdd, signRAdd_d1, signRAdd_d2, signRAdd_d3, signRAdd_d4, signRAdd_d5, signRAdd_d6, signRAdd_d7, signRAdd_d8 :  std_logic;
signal signRSub, signRSub_d1, signRSub_d2, signRSub_d3, signRSub_d4, signRSub_d5, signRSub_d6, signRSub_d7, signRSub_d8, signRSub_d9, signRSub_d10, signRSub_d11, signRSub_d12 :  std_logic;
signal expDiff, expDiff_d1 :  std_logic_vector(11 downto 0);
signal shiftedOut, shiftedOut_d1 :  std_logic;
signal shiftVal :  std_logic_vector(5 downto 0);
signal shiftedFracY, shiftedFracY_d1 :  std_logic_vector(107 downto 0);
signal sticky, sticky_d1, sticky_d2, sticky_d3 :  std_logic;
signal shiftedFracYext :  std_logic_vector(55 downto 0);
signal fracYAdd :  std_logic_vector(55 downto 0);
signal fracYSub :  std_logic_vector(55 downto 0);
signal fracX :  std_logic_vector(55 downto 0);
signal cInFracAdderSub :  std_logic;
signal fracAdderResultAdd, fracAdderResultAdd_d1 :  std_logic_vector(55 downto 0);
signal fracAdderResultSub, fracAdderResultSub_d1 :  std_logic_vector(55 downto 0);
signal extendedExp :  std_logic_vector(12 downto 0);
signal extendedExpInc, extendedExpInc_d1, extendedExpInc_d2, extendedExpInc_d3, extendedExpInc_d4 :  std_logic_vector(12 downto 0);
signal fracGRSSub :  std_logic_vector(56 downto 0);
signal nZerosNew, nZerosNew_d1 :  std_logic_vector(5 downto 0);
signal shiftedFracSub, shiftedFracSub_d1 :  std_logic_vector(56 downto 0);
signal updatedExpSub :  std_logic_vector(12 downto 0);
signal eqdiffsign, eqdiffsign_d1, eqdiffsign_d2 :  std_logic;
signal expFracSub, expFracSub_d1 :  std_logic_vector(65 downto 0);
signal stkSub :  std_logic;
signal rndSub :  std_logic;
signal grdSub :  std_logic;
signal lsbSub :  std_logic;
signal addToRoundBitSub :  std_logic;
signal RoundedExpFracSub, RoundedExpFracSub_d1 :  std_logic_vector(65 downto 0);
signal upExcSub :  std_logic_vector(1 downto 0);
signal fracRSub, fracRSub_d1 :  std_logic_vector(51 downto 0);
signal expRSub, expRSub_d1 :  std_logic_vector(10 downto 0);
signal excRtEffSub :  std_logic_vector(1 downto 0);
signal exExpExcSub :  std_logic_vector(3 downto 0);
signal excRt2Sub :  std_logic_vector(1 downto 0);
signal excRSub, excRSub_d1 :  std_logic_vector(1 downto 0);
signal computedRSub :  std_logic_vector(62 downto 0);
signal fracGRSAdd, fracGRSAdd_d1 :  std_logic_vector(56 downto 0);
signal updatedFracAdd, updatedFracAdd_d1 :  std_logic_vector(52 downto 0);
signal updatedExpAdd, updatedExpAdd_d1 :  std_logic_vector(12 downto 0);
signal expFracAdd :  std_logic_vector(65 downto 0);
signal stkAdd :  std_logic;
signal rndAdd :  std_logic;
signal grdAdd :  std_logic;
signal lsbAdd :  std_logic;
signal addToRoundBitAdd :  std_logic;
signal RoundedExpFracAdd, RoundedExpFracAdd_d1 :  std_logic_vector(65 downto 0);
signal upExcAdd :  std_logic_vector(1 downto 0);
signal fracRAdd :  std_logic_vector(51 downto 0);
signal expRAdd :  std_logic_vector(10 downto 0);
signal excRtEffAdd :  std_logic_vector(1 downto 0);
signal exExpExcAdd :  std_logic_vector(3 downto 0);
signal excRt2Add :  std_logic_vector(1 downto 0);
signal excRAdd, excRAdd_d1, excRAdd_d2, excRAdd_d3, excRAdd_d4 :  std_logic_vector(1 downto 0);
signal computedRAdd, computedRAdd_d1, computedRAdd_d2, computedRAdd_d3, computedRAdd_d4 :  std_logic_vector(62 downto 0);
signal X_d1, X_d2 :  std_logic_vector(11+52+2 downto 0);
signal Y_d1, Y_d2 :  std_logic_vector(11+52+2 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
            eXmeY_d1 <=  eXmeY;
            eYmeX_d1 <=  eYmeX;
            swap_d1 <=  swap;
            swap_d2 <=  swap_d1;
            newX_d1 <=  newX;
            newX_d2 <=  newX_d1;
            newX_d3 <=  newX_d2;
            expX_d1 <=  expX;
            expX_d2 <=  expX_d1;
            expX_d3 <=  expX_d2;
            expX_d4 <=  expX_d3;
            expX_d5 <=  expX_d4;
            expX_d6 <=  expX_d5;
            signX_d1 <=  signX;
            diffSigns_d1 <=  diffSigns;
            diffSigns_d2 <=  diffSigns_d1;
            diffSigns_d3 <=  diffSigns_d2;
            diffSigns_d4 <=  diffSigns_d3;
            diffSigns_d5 <=  diffSigns_d4;
            diffSigns_d6 <=  diffSigns_d5;
            diffSigns_d7 <=  diffSigns_d6;
            diffSigns_d8 <=  diffSigns_d7;
            diffSigns_d9 <=  diffSigns_d8;
            diffSigns_d10 <=  diffSigns_d9;
            diffSigns_d11 <=  diffSigns_d10;
            diffSigns_d12 <=  diffSigns_d11;
            diffSigns_d13 <=  diffSigns_d12;
            sXsYExnXY_d1 <=  sXsYExnXY;
            excRtRAdd_d1 <=  excRtRAdd;
            excRtRAdd_d2 <=  excRtRAdd_d1;
            excRtRAdd_d3 <=  excRtRAdd_d2;
            excRtRAdd_d4 <=  excRtRAdd_d3;
            excRtRAdd_d5 <=  excRtRAdd_d4;
            excRtRAdd_d6 <=  excRtRAdd_d5;
            excRtRAdd_d7 <=  excRtRAdd_d6;
            excRtRAdd_d8 <=  excRtRAdd_d7;
            excRtRAdd_d9 <=  excRtRAdd_d8;
            excRtRAdd_d10 <=  excRtRAdd_d9;
            excRtRAdd_d11 <=  excRtRAdd_d10;
            excRtRAdd_d12 <=  excRtRAdd_d11;
            excRtRSub_d1 <=  excRtRSub;
            excRtRSub_d2 <=  excRtRSub_d1;
            excRtRSub_d3 <=  excRtRSub_d2;
            excRtRSub_d4 <=  excRtRSub_d3;
            excRtRSub_d5 <=  excRtRSub_d4;
            excRtRSub_d6 <=  excRtRSub_d5;
            excRtRSub_d7 <=  excRtRSub_d6;
            excRtRSub_d8 <=  excRtRSub_d7;
            excRtRSub_d9 <=  excRtRSub_d8;
            excRtRSub_d10 <=  excRtRSub_d9;
            excRtRSub_d11 <=  excRtRSub_d10;
            excRtRSub_d12 <=  excRtRSub_d11;
            signRAdd_d1 <=  signRAdd;
            signRAdd_d2 <=  signRAdd_d1;
            signRAdd_d3 <=  signRAdd_d2;
            signRAdd_d4 <=  signRAdd_d3;
            signRAdd_d5 <=  signRAdd_d4;
            signRAdd_d6 <=  signRAdd_d5;
            signRAdd_d7 <=  signRAdd_d6;
            signRAdd_d8 <=  signRAdd_d7;
            signRSub_d1 <=  signRSub;
            signRSub_d2 <=  signRSub_d1;
            signRSub_d3 <=  signRSub_d2;
            signRSub_d4 <=  signRSub_d3;
            signRSub_d5 <=  signRSub_d4;
            signRSub_d6 <=  signRSub_d5;
            signRSub_d7 <=  signRSub_d6;
            signRSub_d8 <=  signRSub_d7;
            signRSub_d9 <=  signRSub_d8;
            signRSub_d10 <=  signRSub_d9;
            signRSub_d11 <=  signRSub_d10;
            signRSub_d12 <=  signRSub_d11;
            expDiff_d1 <=  expDiff;
            shiftedOut_d1 <=  shiftedOut;
            shiftedFracY_d1 <=  shiftedFracY;
            sticky_d1 <=  sticky;
            sticky_d2 <=  sticky_d1;
            sticky_d3 <=  sticky_d2;
            fracAdderResultAdd_d1 <=  fracAdderResultAdd;
            fracAdderResultSub_d1 <=  fracAdderResultSub;
            extendedExpInc_d1 <=  extendedExpInc;
            extendedExpInc_d2 <=  extendedExpInc_d1;
            extendedExpInc_d3 <=  extendedExpInc_d2;
            extendedExpInc_d4 <=  extendedExpInc_d3;
            nZerosNew_d1 <=  nZerosNew;
            shiftedFracSub_d1 <=  shiftedFracSub;
            eqdiffsign_d1 <=  eqdiffsign;
            eqdiffsign_d2 <=  eqdiffsign_d1;
            expFracSub_d1 <=  expFracSub;
            RoundedExpFracSub_d1 <=  RoundedExpFracSub;
            fracRSub_d1 <=  fracRSub;
            expRSub_d1 <=  expRSub;
            excRSub_d1 <=  excRSub;
            fracGRSAdd_d1 <=  fracGRSAdd;
            updatedFracAdd_d1 <=  updatedFracAdd;
            updatedExpAdd_d1 <=  updatedExpAdd;
            RoundedExpFracAdd_d1 <=  RoundedExpFracAdd;
            excRAdd_d1 <=  excRAdd;
            excRAdd_d2 <=  excRAdd_d1;
            excRAdd_d3 <=  excRAdd_d2;
            excRAdd_d4 <=  excRAdd_d3;
            computedRAdd_d1 <=  computedRAdd;
            computedRAdd_d2 <=  computedRAdd_d1;
            computedRAdd_d3 <=  computedRAdd_d2;
            computedRAdd_d4 <=  computedRAdd_d3;
            X_d1 <=  X;
            X_d2 <=  X_d1;
            Y_d1 <=  Y;
            Y_d2 <=  Y_d1;
         end if;
      end process;
-- Exponent difference and swap  --
   excExpFracX <= X(65 downto 64) & X(62 downto 0);
   excExpFracY <= Y(65 downto 64) & Y(62 downto 0);
   eXmeY <= ("0" & X(62 downto 52)) - ("0" & Y(62 downto 52));
   eYmeX <= ("0" & Y(62 downto 52)) - ("0" & X(62 downto 52));
   addCmpOp1<= "0" & excExpFracX;
   addCmpOp2<= "1" & not(excExpFracY);
   cmpAdder: IntAdder_66_f400_uid4  -- pipelineDepth=1 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => '1',
                 R => cmpRes,
                 X => addCmpOp1,
                 Y => addCmpOp2);

   ----------------Synchro barrier, entering cycle 1----------------
   swap <= cmpRes(65);
   ----------------Synchro barrier, entering cycle 2----------------
   newX <= X_d2     when swap_d1 = '0' else Y_d2;
   newY <= Y_d2     when swap_d1 = '0' else X_d2;
   expX<= newX(62 downto 52);
   excX<= newX(65 downto 64);
   excY<= newY(65 downto 64);
   signX<= newX(63);
   signY<= newY(63);
   diffSigns <= signX xor signY;
   sXsYExnXY <= signX & signY & excX & excY;
   fracY <= "00000000000000000000000000000000000000000000000000000" when excY="00" else ('1' & newY(51 downto 0));
   with sXsYExnXY select 
   excRtRAdd <= "00" when "000000"|"010000"|"100000"|"110000",
      "01" when "000101"|"010101"|"100101"|"110101"|"000100"|"010100"|"100100"|"110100"|"000001"|"010001"|"100001"|"110001",
      "10" when "111010"|"001010"|"001000"|"011000"|"101000"|"111000"|"000010"|"010010"|"100010"|"110010"|"001001"|"011001"|"101001"|"111001"|"000110"|"010110"|"100110"|"110110", 
      "11" when others;
   with sXsYExnXY select 
   excRtRSub <= "00" when "000000"|"010000"|"100000"|"110000",
      "01" when "000101"|"010101"|"100101"|"110101"|"000100"|"010100"|"100100"|"110100"|"000001"|"010001"|"100001"|"110001",
      "10" when "001000"|"011000"|"101000"|"111000"|"000010"|"010010"|"100010"|"110010"|"001001"|"011001"|"101001"|"111001"|"000110"|"010110"|"100110"|"110110"|"101010"|"011010", 
      "11" when others;
   ----------------Synchro barrier, entering cycle 3----------------
   signRAdd<= '0' when (sXsYExnXY_d1="100000" or sXsYExnXY_d1="010000") else signX_d1;
   signRSub<= '0' when (sXsYExnXY_d1="000000" or sXsYExnXY_d1="110000") else (signX_d1 and (not swap_d2)) or ((not signX_d1) and swap_d2);
   ---------------- cycle 1----------------
   expDiff <= eXmeY_d1 when (swap = '0') else eYmeX_d1;
   shiftedOut <= '1' when (expDiff >= 54) else '0';
   ----------------Synchro barrier, entering cycle 2----------------
   shiftVal <= expDiff_d1(5 downto 0) when shiftedOut_d1='0' else CONV_STD_LOGIC_VECTOR(55,6);
   RightShifterComponent: FPAddSub_11_52_uid2_RightShifter  -- pipelineDepth=2 maxInDelay=9.8416e-10
      port map ( clk  => clk,
                 rst  => rst,
                 R => shiftedFracY,
                 S => shiftVal,
                 X => fracY);
   ----------------Synchro barrier, entering cycle 4----------------
   ----------------Synchro barrier, entering cycle 5----------------
   sticky <= '0' when (shiftedFracY_d1(52 downto 0)=CONV_STD_LOGIC_VECTOR(0,52)) else '1';
   ---------------- cycle 4----------------
   ----------------Synchro barrier, entering cycle 5----------------
   shiftedFracYext <= "0" & shiftedFracY_d1(107 downto 53);
   fracYAdd <= shiftedFracYext;
   fracYSub <= shiftedFracYext xor ( 55 downto 0 => '1');
   fracX <= "01" & (newX_d3(51 downto 0)) & "00";
   cInFracAdderSub <= not sticky;
   fracAdderAdd: IntAdder_56_f400_uid14  -- pipelineDepth=2 maxInDelay=2.06176e-09
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => '0',
                 R => fracAdderResultAdd,
                 X => fracX,
                 Y => fracYAdd);
   fracAdderSub: IntAdder_56_f400_uid14  -- pipelineDepth=2 maxInDelay=2.06176e-09
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => cInFracAdderSub,
                 R => fracAdderResultSub,
                 X => fracX,
                 Y => fracYSub);
   ---------------- cycle 7----------------
   ----------------Synchro barrier, entering cycle 8----------------
   extendedExp<= "00" & expX_d6;
   extendedExpInc<= ("00" & expX_d6) + '1';
   fracGRSSub<= fracAdderResultSub_d1 & sticky_d3; 
   LZC_component: LZCShifter_57_to_57_counting_64_F400_uid22  -- pipelineDepth=3 maxInDelay=1.01904e-09
      port map ( clk  => clk,
                 rst  => rst,
                 Count => nZerosNew,
                 I => fracGRSSub,
                 O => shiftedFracSub);
   ----------------Synchro barrier, entering cycle 11----------------
   ----------------Synchro barrier, entering cycle 12----------------
   updatedExpSub <= extendedExpInc_d4 - ("0000000" & nZerosNew_d1);
   eqdiffsign <= '1' when nZerosNew_d1="111111" else '0';
   ---------------- cycle 11----------------
   expFracSub<= updatedExpSub & shiftedFracSub(55 downto 3);
   ---------------- cycle 11----------------
   ----------------Synchro barrier, entering cycle 12----------------
   stkSub<= shiftedFracSub_d1(1) or shiftedFracSub_d1(0);
   rndSub<= shiftedFracSub_d1(2);
   grdSub<= shiftedFracSub_d1(3);
   lsbSub<= shiftedFracSub_d1(4);
   ---------------- cycle 11----------------
   ----------------Synchro barrier, entering cycle 12----------------
   addToRoundBitSub<= '0' when (lsbSub='0' and grdSub='1' and rndSub='0' and stkSub='0')  else '1';
   roundingAdderSub: IntAdder_66_f400_uid25  -- pipelineDepth=1 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => addToRoundBitSub,
                 R => RoundedExpFracSub,
                 X => expFracSub_d1,
                 Y => "000000000000000000000000000000000000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 13----------------
   ----------------Synchro barrier, entering cycle 14----------------
   upExcSub <= RoundedExpFracSub_d1(65 downto 64);
   fracRSub <= RoundedExpFracSub_d1(52 downto 1);
   expRSub <= RoundedExpFracSub_d1(63 downto 53);
   excRtEffSub <= excRtRAdd_d12 when (diffSigns_d12='1') else excRtRSub_d12;
   exExpExcSub <= upExcSub & excRtEffSub;
   with (exExpExcSub) select 
   excRt2Sub<= "00" when "0000"|"0100"|"1000"|"1100"|"1001"|"1101",
      "01" when "0001",
      "10" when "0010"|"0110"|"0101",
      "11" when others;
   excRSub <= "00" when (eqdiffsign_d2='1') else excRt2Sub;
   ----------------Synchro barrier, entering cycle 15----------------
   computedRSub <= expRSub_d1 & fracRSub_d1;
   Rsub <= excRSub_d1 & signRSub_d12 & computedRSub when (diffSigns_d13='0') else excRAdd_d4 & signRSub_d12 & computedRAdd_d4;
   ---------------- cycle 8----------------
   fracGRSAdd<= fracAdderResultAdd_d1 & sticky_d3; 
   updatedFracAdd <= fracGRSAdd(55 downto 3) when (fracAdderResultAdd_d1(55)='1') else fracGRSAdd(54 downto 2);
   updatedExpAdd <= extendedExpInc when (fracAdderResultAdd_d1(55)='1') else extendedExp;
   ----------------Synchro barrier, entering cycle 9----------------
   expFracAdd<= updatedExpAdd_d1 & updatedFracAdd_d1;
   ---------------- cycle 8----------------
   ----------------Synchro barrier, entering cycle 9----------------
   stkAdd<= fracGRSAdd_d1(1) or fracGRSAdd_d1(0);
   rndAdd<= fracGRSAdd_d1(2);
   grdAdd<= fracGRSAdd_d1(3);
   lsbAdd<= fracGRSAdd_d1(4);
   addToRoundBitAdd<= (grdAdd and rndAdd) or (grdAdd and (not rndAdd) and lsbAdd) or ((not grdAdd) and rndAdd and stkAdd) or (grdAdd and (not rndAdd) and stkAdd);
   roundingAdderAdd: IntAdder_66_f400_uid25  -- pipelineDepth=1 maxInDelay=0
      port map ( clk  => clk,
                 rst  => rst,
                 Cin => addToRoundBitAdd,
                 R => RoundedExpFracAdd,
                 X => expFracAdd,
                 Y => "000000000000000000000000000000000000000000000000000000000000000000");
   ---------------- cycle 10----------------
   ----------------Synchro barrier, entering cycle 11----------------
   upExcAdd <= RoundedExpFracAdd_d1(65 downto 64);
   fracRAdd <= RoundedExpFracAdd_d1(52 downto 1);
   expRAdd <= RoundedExpFracAdd_d1(63 downto 53);
   excRtEffAdd <= excRtRAdd_d9 when (diffSigns_d9='0') else excRtRSub_d9;
   exExpExcAdd <= upExcAdd & excRtEffAdd;
   with (exExpExcAdd) select 
   excRt2Add<= "00" when "0000"|"0100"|"1000"|"1100"|"1001",
      "01" when "0001",
      "10" when "0010"|"0110"|"0101",
      "11" when others;
   excRAdd <=  excRt2Add;
   computedRAdd <= expRAdd & fracRAdd;
   Radd <= excRAdd & signRAdd_d8 & computedRAdd when (diffSigns_d9='0') else excRSub & signRAdd_d8 & computedRSub;
   ----------------Synchro barrier, entering cycle 15----------------
end architecture;

