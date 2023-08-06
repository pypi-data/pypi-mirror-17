--------------------------------------------------------------------------------
--                          IntAdder_57_f400_uid158
--                     (IntAdderClassical_57_f400_uid160)
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

entity IntAdder_57_f400_uid158 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL , rst : in std_logic;
          X : in  std_logic_vector(56 downto 0);
          Y : in  std_logic_vector(56 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(56 downto 0)   );
end entity;

architecture arch of IntAdder_57_f400_uid158 is
signal x0 :  std_logic_vector(11 downto 0);
signal y0 :  std_logic_vector(11 downto 0);
signal x1, x1_d1 :  std_logic_vector(41 downto 0);
signal y1, y1_d1 :  std_logic_vector(41 downto 0);
signal x2, x2_d1, x2_d2 :  std_logic_vector(2 downto 0);
signal y2, y2_d1, y2_d2 :  std_logic_vector(2 downto 0);
signal sum0, sum0_d1, sum0_d2 :  std_logic_vector(12 downto 0);
signal sum1, sum1_d1 :  std_logic_vector(42 downto 0);
signal sum2 :  std_logic_vector(3 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
          if(Enable='1') then
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
         end if;
      end process;
   --Classical
   x0 <= X(11 downto 0);
   y0 <= Y(11 downto 0);
   x1 <= X(53 downto 12);
   y1 <= Y(53 downto 12);
   x2 <= X(56 downto 54);
   y2 <= Y(56 downto 54);
   sum0 <= ( "0" & x0) + ( "0" & y0)  + Cin;
   ----------------Synchro barrier, entering cycle 1----------------
   sum1 <= ( "0" & x1_d1) + ( "0" & y1_d1)  + sum0_d1(12);
   ----------------Synchro barrier, entering cycle 2----------------
   sum2 <= ( "0" & x2_d2) + ( "0" & y2_d2)  + sum1_d1(42);
   R <= sum2(2 downto 0) & sum1_d1(41 downto 0) & sum0_d2(11 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                     FPMultiplier_8_47_8_47_8_47_uid145
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin 2008-2011
--------------------------------------------------------------------------------
-- Pipeline depth: 9 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPMultiplier_8_47_8_47_8_47_uid145 is
   port ( clk: in std_logic;
          Enable : in std_logic;
-- OL ,, rst : in std_logic;
          X : in  std_logic_vector(8+47+2 downto 0);
          Y : in  std_logic_vector(8+47+2 downto 0);
          R : out  std_logic_vector(8+47+2 downto 0)   );
end entity;

architecture arch of FPMultiplier_8_47_8_47_8_47_uid145 is
   component IntAdder_57_f400_uid158 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL , rst : in std_logic;
             X : in  std_logic_vector(56 downto 0);
             Y : in  std_logic_vector(56 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(56 downto 0)   );
   end component;

   component IntTruncMultiplier_48_48_96_unsigned is
      port ( clk: in std_logic;
             Enable : in std_logic;
-- OL ,, rst : in std_logic;
             X : in  std_logic_vector(47 downto 0);
             Y : in  std_logic_vector(47 downto 0);
             R : out  std_logic_vector(95 downto 0)   );
   end component;

signal sign, sign_d1, sign_d2, sign_d3, sign_d4, sign_d5, sign_d6, sign_d7, sign_d8, sign_d9 : std_logic;
signal expX :  std_logic_vector(7 downto 0);
signal expY :  std_logic_vector(7 downto 0);
signal expSumPreSub, expSumPreSub_d1 :  std_logic_vector(9 downto 0);
signal bias, bias_d1 :  std_logic_vector(9 downto 0);
signal expSum, expSum_d1, expSum_d2, expSum_d3, expSum_d4, expSum_d5 :  std_logic_vector(9 downto 0);
signal sigX :  std_logic_vector(47 downto 0);
signal sigY :  std_logic_vector(47 downto 0);
signal sigProd :  std_logic_vector(95 downto 0);
signal excSel :  std_logic_vector(3 downto 0);
signal exc, exc_d1, exc_d2, exc_d3, exc_d4, exc_d5, exc_d6, exc_d7, exc_d8, exc_d9 :  std_logic_vector(1 downto 0);
signal norm, norm_d1 : std_logic;
signal expPostNorm :  std_logic_vector(9 downto 0);
signal sigProdExt, sigProdExt_d1, sigProdExt_d2 :  std_logic_vector(95 downto 0);
signal expSig, expSig_d1 :  std_logic_vector(56 downto 0);
signal sticky, sticky_d1 : std_logic;
signal guard : std_logic;
signal round : std_logic;
signal expSigPostRound :  std_logic_vector(56 downto 0);
signal excPostNorm :  std_logic_vector(1 downto 0);
signal finalExc :  std_logic_vector(1 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
          if(Enable='1') then
            sign_d1 <=  sign;
            sign_d2 <=  sign_d1;
            sign_d3 <=  sign_d2;
            sign_d4 <=  sign_d3;
            sign_d5 <=  sign_d4;
            sign_d6 <=  sign_d5;
            sign_d7 <=  sign_d6;
            sign_d8 <=  sign_d7;
            sign_d9 <=  sign_d8;
            expSumPreSub_d1 <=  expSumPreSub;
            bias_d1 <=  bias;
            expSum_d1 <=  expSum;
            expSum_d2 <=  expSum_d1;
            expSum_d3 <=  expSum_d2;
            expSum_d4 <=  expSum_d3;
            expSum_d5 <=  expSum_d4;
            exc_d1 <=  exc;
            exc_d2 <=  exc_d1;
            exc_d3 <=  exc_d2;
            exc_d4 <=  exc_d3;
            exc_d5 <=  exc_d4;
            exc_d6 <=  exc_d5;
            exc_d7 <=  exc_d6;
            exc_d8 <=  exc_d7;
            exc_d9 <=  exc_d8;
            norm_d1 <=  norm;
            sigProdExt_d1 <=  sigProdExt;
            sigProdExt_d2 <=  sigProdExt_d1;
            expSig_d1 <=  expSig;
            sticky_d1 <=  sticky;
          end if;
         end if;
      end process;
   sign <= X(55) xor Y(55);
   expX <= X(54 downto 47);
   expY <= Y(54 downto 47);
   expSumPreSub <= ("00" & expX) + ("00" & expY);
   bias <= CONV_STD_LOGIC_VECTOR(127,10);
   ----------------Synchro barrier, entering cycle 1----------------
   expSum <= expSumPreSub_d1 - bias_d1;
   ----------------Synchro barrier, entering cycle 0----------------
   sigX <= "1" & X(46 downto 0);
   sigY <= "1" & Y(46 downto 0);
   SignificandMultiplication: IntTruncMultiplier_48_48_96_unsigned  -- pipelineDepth=5 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => sigProd,
                 X => sigX,
                 Y => sigY);
   ----------------Synchro barrier, entering cycle 5----------------
   ----------------Synchro barrier, entering cycle 0----------------
   excSel <= X(57 downto 56) & Y(57 downto 56);
   with excSel select
   exc <= "00" when  "0000" | "0001" | "0100",
          "01" when "0101",
          "10" when "0110" | "1001" | "1010" ,
          "11" when others;
   ----------------Synchro barrier, entering cycle 5----------------
   norm <= sigProd(95);
   ----------------Synchro barrier, entering cycle 6----------------
   -- exponent update
   expPostNorm <= expSum_d5 + ("000000000" & norm_d1);
   ----------------Synchro barrier, entering cycle 5----------------
   -- significand normalization shift
   sigProdExt <= sigProd(94 downto 0) & "0" when norm='1' else
                         sigProd(93 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 6----------------
   expSig <= expPostNorm & sigProdExt_d1(95 downto 49);
   sticky <= sigProdExt_d1(48);
   ----------------Synchro barrier, entering cycle 7----------------
   guard <= '0' when sigProdExt_d2(47 downto 0)="000000000000000000000000000000000000000000000000" else '1';
   round <= sticky_d1 and ( (guard and not(sigProdExt_d2(49))) or (sigProdExt_d2(49) ))  ;
   RoundingAdder: IntAdder_57_f400_uid158  -- pipelineDepth=2 maxInDelay=1.55044e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL            rst  => rst,
                 Cin => round,
                 R => expSigPostRound   ,
                 X => expSig_d1,
                 Y => "000000000000000000000000000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 9----------------
   with expSigPostRound(56 downto 55) select
   excPostNorm <=  "01"  when  "00",
                               "10"             when "01",
                               "00"             when "11"|"10",
                               "11"             when others;
   with exc_d9 select
   finalExc <= exc_d9 when  "11"|"10"|"00",
                       excPostNorm when others;
   R <= finalExc & sign_d9 & expSigPostRound(54 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_57_f400_uid34
--                     (IntAdderClassical_57_f400_uid36)
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

entity IntAdder_57_f400_uid34 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL, rst : in std_logic;
          X : in  std_logic_vector(56 downto 0);
          Y : in  std_logic_vector(56 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(56 downto 0)   );
end entity;

architecture arch of IntAdder_57_f400_uid34 is
signal x0 :  std_logic_vector(11 downto 0);
signal y0 :  std_logic_vector(11 downto 0);
signal x1, x1_d1 :  std_logic_vector(41 downto 0);
signal y1, y1_d1 :  std_logic_vector(41 downto 0);
signal x2, x2_d1, x2_d2 :  std_logic_vector(2 downto 0);
signal y2, y2_d1, y2_d2 :  std_logic_vector(2 downto 0);
signal sum0, sum0_d1, sum0_d2 :  std_logic_vector(12 downto 0);
signal sum1, sum1_d1 :  std_logic_vector(42 downto 0);
signal sum2 :  std_logic_vector(3 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
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
         end if;
      end process;
   --Classical
   x0 <= X(11 downto 0);
   y0 <= Y(11 downto 0);
   x1 <= X(53 downto 12);
   y1 <= Y(53 downto 12);
   x2 <= X(56 downto 54);
   y2 <= Y(56 downto 54);
   sum0 <= ( "0" & x0) + ( "0" & y0)  + Cin;
   ----------------Synchro barrier, entering cycle 1----------------
   sum1 <= ( "0" & x1_d1) + ( "0" & y1_d1)  + sum0_d1(12);
   ----------------Synchro barrier, entering cycle 2----------------
   sum2 <= ( "0" & x2_d2) + ( "0" & y2_d2)  + sum1_d1(42);
   R <= sum2(2 downto 0) & sum1_d1(41 downto 0) & sum0_d2(11 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                     FPMultiplier_8_47_8_47_8_47_uid21
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin 2008-2011
--------------------------------------------------------------------------------
-- Pipeline depth: 9 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPMultiplier_8_47_8_47_8_47_uid21 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL , rst : in std_logic;
          X : in  std_logic_vector(8+47+2 downto 0);
          Y : in  std_logic_vector(8+47+2 downto 0);
          R : out  std_logic_vector(8+47+2 downto 0)   );
end entity;

architecture arch of FPMultiplier_8_47_8_47_8_47_uid21 is
   component IntAdder_57_f400_uid34 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL, rst : in std_logic;
             X : in  std_logic_vector(56 downto 0);
             Y : in  std_logic_vector(56 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(56 downto 0)   );
   end component;

   component IntTruncMultiplier_48_48_96_unsigned is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(47 downto 0);
             Y : in  std_logic_vector(47 downto 0);
             R : out  std_logic_vector(95 downto 0)   );
   end component;

signal sign, sign_d1, sign_d2, sign_d3, sign_d4, sign_d5, sign_d6, sign_d7, sign_d8, sign_d9 : std_logic;
signal expX :  std_logic_vector(7 downto 0);
signal expY :  std_logic_vector(7 downto 0);
signal expSumPreSub, expSumPreSub_d1 :  std_logic_vector(9 downto 0);
signal bias, bias_d1 :  std_logic_vector(9 downto 0);
signal expSum, expSum_d1, expSum_d2, expSum_d3, expSum_d4, expSum_d5 :  std_logic_vector(9 downto 0);
signal sigX :  std_logic_vector(47 downto 0);
signal sigY :  std_logic_vector(47 downto 0);
signal sigProd :  std_logic_vector(95 downto 0);
signal excSel :  std_logic_vector(3 downto 0);
signal exc, exc_d1, exc_d2, exc_d3, exc_d4, exc_d5, exc_d6, exc_d7, exc_d8, exc_d9 :  std_logic_vector(1 downto 0);
signal norm, norm_d1 : std_logic;
signal expPostNorm :  std_logic_vector(9 downto 0);
signal sigProdExt, sigProdExt_d1, sigProdExt_d2 :  std_logic_vector(95 downto 0);
signal expSig, expSig_d1 :  std_logic_vector(56 downto 0);
signal sticky, sticky_d1 : std_logic;
signal guard : std_logic;
signal round : std_logic;
signal expSigPostRound :  std_logic_vector(56 downto 0);
signal excPostNorm :  std_logic_vector(1 downto 0);
signal finalExc :  std_logic_vector(1 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            sign_d1 <=  sign;
            sign_d2 <=  sign_d1;
            sign_d3 <=  sign_d2;
            sign_d4 <=  sign_d3;
            sign_d5 <=  sign_d4;
            sign_d6 <=  sign_d5;
            sign_d7 <=  sign_d6;
            sign_d8 <=  sign_d7;
            sign_d9 <=  sign_d8;
            expSumPreSub_d1 <=  expSumPreSub;
            bias_d1 <=  bias;
            expSum_d1 <=  expSum;
            expSum_d2 <=  expSum_d1;
            expSum_d3 <=  expSum_d2;
            expSum_d4 <=  expSum_d3;
            expSum_d5 <=  expSum_d4;
            exc_d1 <=  exc;
            exc_d2 <=  exc_d1;
            exc_d3 <=  exc_d2;
            exc_d4 <=  exc_d3;
            exc_d5 <=  exc_d4;
            exc_d6 <=  exc_d5;
            exc_d7 <=  exc_d6;
            exc_d8 <=  exc_d7;
            exc_d9 <=  exc_d8;
            norm_d1 <=  norm;
            sigProdExt_d1 <=  sigProdExt;
            sigProdExt_d2 <=  sigProdExt_d1;
            expSig_d1 <=  expSig;
            sticky_d1 <=  sticky;
          end if;
         end if;
      end process;
   sign <= X(55) xor Y(55);
   expX <= X(54 downto 47);
   expY <= Y(54 downto 47);
   expSumPreSub <= ("00" & expX) + ("00" & expY);
   bias <= CONV_STD_LOGIC_VECTOR(127,10);
   ----------------Synchro barrier, entering cycle 1----------------
   expSum <= expSumPreSub_d1 - bias_d1;
   ----------------Synchro barrier, entering cycle 0----------------
   sigX <= "1" & X(46 downto 0);
   sigY <= "1" & Y(46 downto 0);
   SignificandMultiplication: IntTruncMultiplier_48_48_96_unsigned  -- pipelineDepth=5 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => sigProd,
                 X => sigX,
                 Y => sigY);
   ----------------Synchro barrier, entering cycle 5----------------
   ----------------Synchro barrier, entering cycle 0----------------
   excSel <= X(57 downto 56) & Y(57 downto 56);
   with excSel select 
   exc <= "00" when  "0000" | "0001" | "0100", 
          "01" when "0101",
          "10" when "0110" | "1001" | "1010" ,
          "11" when others;
   ----------------Synchro barrier, entering cycle 5----------------
   norm <= sigProd(95);
   ----------------Synchro barrier, entering cycle 6----------------
   -- exponent update
   expPostNorm <= expSum_d5 + ("000000000" & norm_d1);
   ----------------Synchro barrier, entering cycle 5----------------
   -- significand normalization shift
   sigProdExt <= sigProd(94 downto 0) & "0" when norm='1' else
                         sigProd(93 downto 0) & "00";
   ----------------Synchro barrier, entering cycle 6----------------
   expSig <= expPostNorm & sigProdExt_d1(95 downto 49);
   sticky <= sigProdExt_d1(48);
   ----------------Synchro barrier, entering cycle 7----------------
   guard <= '0' when sigProdExt_d2(47 downto 0)="000000000000000000000000000000000000000000000000" else '1';
   round <= sticky_d1 and ( (guard and not(sigProdExt_d2(49))) or (sigProdExt_d2(49) ))  ;
   RoundingAdder: IntAdder_57_f400_uid34  -- pipelineDepth=2 maxInDelay=1.55044e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 Cin => round,
                 R => expSigPostRound   ,
                 X => expSig_d1,
                 Y => "000000000000000000000000000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 9----------------
   with expSigPostRound(56 downto 55) select
   excPostNorm <=  "01"  when  "00",
                               "10"             when "01", 
                               "00"             when "11"|"10",
                               "11"             when others;
   with exc_d9 select 
   finalExc <= exc_d9 when  "11"|"10"|"00",
                       excPostNorm when others; 
   R <= finalExc & sign_d9 & expSigPostRound(54 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                                  InitLoop_8_47
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: ADACSYS Co, 2013
--------------------------------------------------------------------------------
-- Pipeline depth: 73 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity InitLoop_8_47 is
   port ( 
        clk        : in std_logic;
        Enable     : in std_logic;
-- OL         rst : in std_logic;
        tempvdt    : in  std_logic_vector(8+47+2 downto 0);
        S_0        : in  std_logic_vector(8+47+2 downto 0);
        k          : in  std_logic_vector(8+47+2 downto 0);
        tempsteps  : in  std_logic_vector(8+47+2 downto 0);
        K_min_stim : in  std_logic_vector(8+47+2 downto 0);
        S_k        : out  std_logic_vector(8+47+2 downto 0);
        V_k_call   : out  std_logic_vector(8+47+2 downto 0);
        V_k_put    : out  std_logic_vector(8+47+2 downto 0);
        Nc         : out std_logic
        );
end entity;

architecture arch of InitLoop_8_47 is
   component FPAdderDualPath_8_47_8_47_8_47400 is
      port ( clk    : in std_logic;
             Enable : in std_logic;
-- OL             rst : in std_logic;
             X      : in  std_logic_vector(8+47+2 downto 0);
             Y      : in  std_logic_vector(8+47+2 downto 0);
             R      : out  std_logic_vector(8+47+2 downto 0)   );
   end component;

   component FPExp_8_47_400 is
      port ( clk    : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X      : in  std_logic_vector(8+47+2 downto 0);
             R      : out  std_logic_vector(8+47+2 downto 0)   );
   end component;

   component FPMultiplier_8_47_8_47_8_47_uid145 is
      port ( clk    : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X      : in  std_logic_vector(8+47+2 downto 0);
             Y      : in  std_logic_vector(8+47+2 downto 0);
             R      : out  std_logic_vector(8+47+2 downto 0)   );
   end component;

   component FPMultiplier_8_47_8_47_8_47_uid21 is
      port ( clk    : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X      : in  std_logic_vector(8+47+2 downto 0);
             Y      : in  std_logic_vector(8+47+2 downto 0);
             R      : out  std_logic_vector(8+47+2 downto 0)   );
   end component;

signal resInterm1 :  std_logic_vector(57 downto 0);
signal resInterm2 :  std_logic_vector(57 downto 0);
signal resInterm3, resInterm3_d1 :  std_logic_vector(57 downto 0);
signal S_k_comp, S_k_comp_d1, S_k_comp_d2, S_k_comp_d3, S_k_comp_d4, S_k_comp_d5, S_k_comp_d6, S_k_comp_d7, S_k_comp_d8, S_k_comp_d9, S_k_comp_d10, S_k_comp_d11 :  std_logic_vector(57 downto 0);
signal unmaxed_value_call :  std_logic_vector(57 downto 0);
signal tempvdt_d1, tempvdt_d2, tempvdt_d3, tempvdt_d4, tempvdt_d5, tempvdt_d6, tempvdt_d7, tempvdt_d8, tempvdt_d9, tempvdt_d10, tempvdt_d11 :  std_logic_vector(8+47+2 downto 0);
signal S_0_d1, S_0_d2, S_0_d3, S_0_d4, S_0_d5, S_0_d6, S_0_d7, S_0_d8, S_0_d9, S_0_d10, S_0_d11, S_0_d12, S_0_d13, S_0_d14, S_0_d15, S_0_d16, S_0_d17, S_0_d18, S_0_d19, S_0_d20, S_0_d21, S_0_d22, S_0_d23, S_0_d24, S_0_d25, S_0_d26, S_0_d27, S_0_d28, S_0_d29, S_0_d30, S_0_d31, S_0_d32, S_0_d33, S_0_d34, S_0_d35, S_0_d36, S_0_d37, S_0_d38, S_0_d39, S_0_d40, S_0_d41, S_0_d42, S_0_d43, S_0_d44, S_0_d45, S_0_d46, S_0_d47, S_0_d48, S_0_d49, S_0_d50, S_0_d51, S_0_d52, S_0_d53 :  std_logic_vector(8+47+2 downto 0);
signal K_min_stim_d1, K_min_stim_d2, K_min_stim_d3, K_min_stim_d4, K_min_stim_d5, K_min_stim_d6, K_min_stim_d7, K_min_stim_d8, K_min_stim_d9, K_min_stim_d10, K_min_stim_d11, K_min_stim_d12, K_min_stim_d13, K_min_stim_d14, K_min_stim_d15, K_min_stim_d16, K_min_stim_d17, K_min_stim_d18, K_min_stim_d19, K_min_stim_d20, K_min_stim_d21, K_min_stim_d22, K_min_stim_d23, K_min_stim_d24, K_min_stim_d25, K_min_stim_d26, K_min_stim_d27, K_min_stim_d28, K_min_stim_d29, K_min_stim_d30, K_min_stim_d31, K_min_stim_d32, K_min_stim_d33, K_min_stim_d34, K_min_stim_d35, K_min_stim_d36, K_min_stim_d37, K_min_stim_d38, K_min_stim_d39, K_min_stim_d40, K_min_stim_d41, K_min_stim_d42, K_min_stim_d43, K_min_stim_d44, K_min_stim_d45, K_min_stim_d46, K_min_stim_d47, K_min_stim_d48, K_min_stim_d49, K_min_stim_d50, K_min_stim_d51, K_min_stim_d52, K_min_stim_d53, K_min_stim_d54, K_min_stim_d55, K_min_stim_d56, K_min_stim_d57, K_min_stim_d58, K_min_stim_d59, K_min_stim_d60, K_min_stim_d61, K_min_stim_d62 :  std_logic_vector(8+47+2 downto 0);


signal foobar, barfoo : std_logic_vector(8+47 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            resInterm3_d1 <=  resInterm3;
            S_k_comp_d1 <=  S_k_comp;
            S_k_comp_d2 <=  S_k_comp_d1;
            S_k_comp_d3 <=  S_k_comp_d2;
            S_k_comp_d4 <=  S_k_comp_d3;
            S_k_comp_d5 <=  S_k_comp_d4;
            S_k_comp_d6 <=  S_k_comp_d5;
            S_k_comp_d7 <=  S_k_comp_d6;
            S_k_comp_d8 <=  S_k_comp_d7;
            S_k_comp_d9 <=  S_k_comp_d8;
            S_k_comp_d10 <=  S_k_comp_d9;
            S_k_comp_d11 <=  S_k_comp_d10;
            tempvdt_d1 <=  tempvdt;
            tempvdt_d2 <=  tempvdt_d1;
            tempvdt_d3 <=  tempvdt_d2;
            tempvdt_d4 <=  tempvdt_d3;
            tempvdt_d5 <=  tempvdt_d4;
            tempvdt_d6 <=  tempvdt_d5;
            tempvdt_d7 <=  tempvdt_d6;
            tempvdt_d8 <=  tempvdt_d7;
            tempvdt_d9 <=  tempvdt_d8;
            tempvdt_d10 <=  tempvdt_d9;
            tempvdt_d11 <=  tempvdt_d10;
            S_0_d1 <=  S_0;
            S_0_d2 <=  S_0_d1;
            S_0_d3 <=  S_0_d2;
            S_0_d4 <=  S_0_d3;
            S_0_d5 <=  S_0_d4;
            S_0_d6 <=  S_0_d5;
            S_0_d7 <=  S_0_d6;
            S_0_d8 <=  S_0_d7;
            S_0_d9 <=  S_0_d8;
            S_0_d10 <=  S_0_d9;
            S_0_d11 <=  S_0_d10;
            S_0_d12 <=  S_0_d11;
            S_0_d13 <=  S_0_d12;
            S_0_d14 <=  S_0_d13;
            S_0_d15 <=  S_0_d14;
            S_0_d16 <=  S_0_d15;
            S_0_d17 <=  S_0_d16;
            S_0_d18 <=  S_0_d17;
            S_0_d19 <=  S_0_d18;
            S_0_d20 <=  S_0_d19;
            S_0_d21 <=  S_0_d20;
            S_0_d22 <=  S_0_d21;
            S_0_d23 <=  S_0_d22;
            S_0_d24 <=  S_0_d23;
            S_0_d25 <=  S_0_d24;
            S_0_d26 <=  S_0_d25;
            S_0_d27 <=  S_0_d26;
            S_0_d28 <=  S_0_d27;
            S_0_d29 <=  S_0_d28;
            S_0_d30 <=  S_0_d29;
            S_0_d31 <=  S_0_d30;
            S_0_d32 <=  S_0_d31;
            S_0_d33 <=  S_0_d32;
            S_0_d34 <=  S_0_d33;
            S_0_d35 <=  S_0_d34;
            S_0_d36 <=  S_0_d35;
            S_0_d37 <=  S_0_d36;
            S_0_d38 <=  S_0_d37;
            S_0_d39 <=  S_0_d38;
            S_0_d40 <=  S_0_d39;
            S_0_d41 <=  S_0_d40;
            S_0_d42 <=  S_0_d41;
            S_0_d43 <=  S_0_d42;
            S_0_d44 <=  S_0_d43;
            S_0_d45 <=  S_0_d44;
            S_0_d46 <=  S_0_d45;
            S_0_d47 <=  S_0_d46;
            S_0_d48 <=  S_0_d47;
            S_0_d49 <=  S_0_d48;
            S_0_d50 <=  S_0_d49;
            S_0_d51 <=  S_0_d50;
            S_0_d52 <=  S_0_d51;
            S_0_d53 <=  S_0_d52;
            K_min_stim_d1 <=  K_min_stim;
            K_min_stim_d2 <=  K_min_stim_d1;
            K_min_stim_d3 <=  K_min_stim_d2;
            K_min_stim_d4 <=  K_min_stim_d3;
            K_min_stim_d5 <=  K_min_stim_d4;
            K_min_stim_d6 <=  K_min_stim_d5;
            K_min_stim_d7 <=  K_min_stim_d6;
            K_min_stim_d8 <=  K_min_stim_d7;
            K_min_stim_d9 <=  K_min_stim_d8;
            K_min_stim_d10 <=  K_min_stim_d9;
            K_min_stim_d11 <=  K_min_stim_d10;
            K_min_stim_d12 <=  K_min_stim_d11;
            K_min_stim_d13 <=  K_min_stim_d12;
            K_min_stim_d14 <=  K_min_stim_d13;
            K_min_stim_d15 <=  K_min_stim_d14;
            K_min_stim_d16 <=  K_min_stim_d15;
            K_min_stim_d17 <=  K_min_stim_d16;
            K_min_stim_d18 <=  K_min_stim_d17;
            K_min_stim_d19 <=  K_min_stim_d18;
            K_min_stim_d20 <=  K_min_stim_d19;
            K_min_stim_d21 <=  K_min_stim_d20;
            K_min_stim_d22 <=  K_min_stim_d21;
            K_min_stim_d23 <=  K_min_stim_d22;
            K_min_stim_d24 <=  K_min_stim_d23;
            K_min_stim_d25 <=  K_min_stim_d24;
            K_min_stim_d26 <=  K_min_stim_d25;
            K_min_stim_d27 <=  K_min_stim_d26;
            K_min_stim_d28 <=  K_min_stim_d27;
            K_min_stim_d29 <=  K_min_stim_d28;
            K_min_stim_d30 <=  K_min_stim_d29;
            K_min_stim_d31 <=  K_min_stim_d30;
            K_min_stim_d32 <=  K_min_stim_d31;
            K_min_stim_d33 <=  K_min_stim_d32;
            K_min_stim_d34 <=  K_min_stim_d33;
            K_min_stim_d35 <=  K_min_stim_d34;
            K_min_stim_d36 <=  K_min_stim_d35;
            K_min_stim_d37 <=  K_min_stim_d36;
            K_min_stim_d38 <=  K_min_stim_d37;
            K_min_stim_d39 <=  K_min_stim_d38;
            K_min_stim_d40 <=  K_min_stim_d39;
            K_min_stim_d41 <=  K_min_stim_d40;
            K_min_stim_d42 <=  K_min_stim_d41;
            K_min_stim_d43 <=  K_min_stim_d42;
            K_min_stim_d44 <=  K_min_stim_d43;
            K_min_stim_d45 <=  K_min_stim_d44;
            K_min_stim_d46 <=  K_min_stim_d45;
            K_min_stim_d47 <=  K_min_stim_d46;
            K_min_stim_d48 <=  K_min_stim_d47;
            K_min_stim_d49 <=  K_min_stim_d48;
            K_min_stim_d50 <=  K_min_stim_d49;
            K_min_stim_d51 <=  K_min_stim_d50;
            K_min_stim_d52 <=  K_min_stim_d51;
            K_min_stim_d53 <=  K_min_stim_d52;
            K_min_stim_d54 <=  K_min_stim_d53;
            K_min_stim_d55 <=  K_min_stim_d54;
            K_min_stim_d56 <=  K_min_stim_d55;
            K_min_stim_d57 <=  K_min_stim_d56;
            K_min_stim_d58 <=  K_min_stim_d57;
            K_min_stim_d59 <=  K_min_stim_d58;
            K_min_stim_d60 <=  K_min_stim_d59;
            K_min_stim_d61 <=  K_min_stim_d60;
            K_min_stim_d62 <=  K_min_stim_d61;
           end if;
         end if;
      end process;
   fAdd: FPAdderDualPath_8_47_8_47_8_47400  -- pipelineDepth=11 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                 rst  => rst,
                 R => resInterm1,
                 X => k,
                 Y => tempsteps);
   ----------------Synchro barrier, entering cycle 11----------------
   multDt: FPMultiplier_8_47_8_47_8_47_uid21  -- pipelineDepth=9 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                 rst  => rst,
                 R => resInterm2,
                 X => resInterm1,
                 Y => tempvdt_d11);
   ----------------Synchro barrier, entering cycle 20----------------
   resInterm3_8_47: FPExp_8_47_400  -- pipelineDepth=32 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                 rst  => rst,
                 R => resInterm3,
                 X => resInterm2);
   ----------------Synchro barrier, entering cycle 52----------------
   ----------------Synchro barrier, entering cycle 53----------------
   multExp: FPMultiplier_8_47_8_47_8_47_uid145  -- pipelineDepth=9 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                 rst  => rst,
                 R => S_k_comp,
                 X => resInterm3_d1,
                 Y => S_0_d53);
   ----------------Synchro barrier, entering cycle 62----------------
   fAdd2: FPAdderDualPath_8_47_8_47_8_47400  -- pipelineDepth=11 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                 rst  => rst,
                 R => unmaxed_value_call,
                 X => K_min_stim_d62,
                 Y => S_k_comp);
   ----------------Synchro barrier, entering cycle 73----------------
S_k <= S_k_comp_d11;
--V_k_call <= unmaxed_value_call when unmaxed_value_call(63)='0'
--                               else (others=>'0')
--V_k_put <= '0'&unmaxed_value_call(62 downto 0) when unmaxed_value_call(63)='1'
--                               else (others=>'0');
							 
foobar <= '0'&unmaxed_value_call(54 downto 0);
barfoo <= (others=>'0');
V_k_call <= unmaxed_value_call when unmaxed_value_call(55)='0'
                               else "01"&barfoo;
V_k_put <= "01"&foobar when unmaxed_value_call(55)='1'
                               else "01"&barfoo;
end architecture;

