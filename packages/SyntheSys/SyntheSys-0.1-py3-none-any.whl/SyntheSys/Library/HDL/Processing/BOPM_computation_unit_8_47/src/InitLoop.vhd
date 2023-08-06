
--------------------------------------------------------------------------------
--                      IntMultiAdder_48_op1_f400_uid24
--                       (IntCompressorTree_48_1_uid26)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009-2011)
--------------------------------------------------------------------------------
-- Pipeline depth: 0 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntMultiAdder_48_op1_f400_uid24 is
   port ( 
-- OL clk, rst : in std_logic;
          X0 : in  std_logic_vector(47 downto 0);
          R : out  std_logic_vector(47 downto 0)   );
end entity;

architecture arch of IntMultiAdder_48_op1_f400_uid24 is
-- OL signal l_0_s_0 :  std_logic_vector(47 downto 0);
begin
-- OL   process(clk)
-- OL       begin
-- OL         if clk'event and clk = '1' then
-- OL         end if;
-- OL      end process;
-- OL   l_0_s_0 <= X0;
   R <= X0;
end architecture;

--------------------------------------------------------------------------------
--                    IntTruncMultiplier_24_24_48_unsigned
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Sebastian Banescu, Bogdan Pasca, Radu Tudoran (2010-2011)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_signed.all;
library work;
entity IntTruncMultiplier_24_24_48_unsigned is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(23 downto 0);
          Y : in  std_logic_vector(23 downto 0);
          R : out  std_logic_vector(47 downto 0);
          Nc : out  std_logic    );
end entity;

architecture arch of IntTruncMultiplier_24_24_48_unsigned is
   component IntMultiAdder_48_op1_f400_uid24 is
      port ( 
-- OL clk, rst : in std_logic;
             X0 : in  std_logic_vector(47 downto 0);
             R : out  std_logic_vector(47 downto 0));
   end component;

signal x0_0 :  std_logic_vector(17 downto 0);
signal y0_0 :  std_logic_vector(24 downto 0);
signal pxy00, pxy00_d1, pxy00_d2 :  std_logic_vector(42 downto 0);
signal x0_1, x0_1_d1 :  std_logic_vector(17 downto 0);
signal y0_1, y0_1_d1 :  std_logic_vector(24 downto 0);
signal txy01 :  std_logic_vector(42 downto 0);
signal pxy01, pxy01_d1 :  std_logic_vector(42 downto 0);
signal addOpDSP0 :  std_logic_vector(47 downto 0);
signal addRes :  std_logic_vector(47 downto 0);
signal NcA : std_logic;
signal NcB : std_logic;
signal NcC : STD_LOGIC;
constant zero : STD_LOGIC := '0';
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            pxy00_d1 <=  pxy00;
            pxy00_d2 <=  pxy00_d1;
            x0_1_d1 <=  x0_1;
            y0_1_d1 <=  y0_1;
            pxy01_d1 <=  pxy01;
           end if;
         end if;
      end process;
   ----------------Synchro barrier, entering cycle 0----------------
   ----------------Synchro barrier, entering cycle 0----------------
   x0_0 <= zero & X(6 downto 0) & "0000000000";
   y0_0 <= zero & Y(23 downto 0) & "";
-- OF   x0_0 <= "0" & "" & X(6 downto 0) & "0000000000";
-- OF   y0_0 <= "0" & "" & Y(23 downto 0) & "";
   pxy00 <= x0_0(17 downto 0) * y0_0(24 downto 0); --0
   ----------------Synchro barrier, entering cycle 0----------------
   x0_1 <= zero & X(23 downto 7) ;
   y0_1 <= zero & Y(23 downto 0) ;
-- OF   x0_1 <= "0" & "" & X(23 downto 7) & "";
-- OF   y0_1 <= "0" & "" & Y(23 downto 0) & "";
   ----------------Synchro barrier, entering cycle 1----------------
   txy01 <= x0_1_d1(17 downto 0) * y0_1_d1(24 downto 0);
   pxy01 <= (txy01(42 downto 0)) + ("00000000000000000" &pxy00_d1(42 downto 17));
   ----------------Synchro barrier, entering cycle 2----------------
   addOpDSP0 <= "" & pxy01_d1(40 downto 0) & pxy00_d2(16 downto 10) & "" &  "";--3 bpadX 10 bpadY 0
   adder: IntMultiAdder_48_op1_f400_uid24  -- pipelineDepth=0 maxInDelay=4.4472e-10
      port map ( -- clk  => clk,
                 -- rst  => rst,
                 R => addRes,
                 X0 => addOpDSP0);
   R <= addRes(47 downto 0);

NcA <= pxy00_d1(0) and pxy00_d1(1) and pxy00_d1(2) and pxy00_d1(3) and pxy00_d1(4) and pxy00_d1(5) and pxy00_d1(6) and pxy00_d1(7) and pxy00_d1(8) and pxy00_d1(9);
NcB <= pxy01_d1(41) and pxy01_d1(42); 
NcC <= pxy00_d1(0) and pxy00_d1(1) and pxy00_d1(2) and pxy00_d1(3) and pxy00_d1(4) and pxy00_d1(5) and pxy00_d1(6) and pxy00_d1(7) and pxy00_d1(8) and pxy00_d1(9);
Nc <= NcA and NcB and NcC and pxy00_d1(41);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_33_f400_uid28
--                     (IntAdderClassical_33_f400_uid30)
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

entity IntAdder_33_f400_uid28 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(32 downto 0);
          Y : in  std_logic_vector(32 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(32 downto 0)   );
end entity;

architecture arch of IntAdder_33_f400_uid28 is
signal X_d1 :  std_logic_vector(32 downto 0);
signal Y_d1 :  std_logic_vector(32 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                     FPMultiplier_8_23_8_23_8_23_uid21
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin 2008-2011
--------------------------------------------------------------------------------
-- Pipeline depth: 4 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPMultiplier_8_23_8_23_8_23_uid21 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(8+23+2 downto 0);
          Y : in  std_logic_vector(8+23+2 downto 0);
          R : out  std_logic_vector(8+23+2 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of FPMultiplier_8_23_8_23_8_23_uid21 is
   component IntAdder_33_f400_uid28 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(32 downto 0);
             Y : in  std_logic_vector(32 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(32 downto 0)   );
   end component;

   component IntTruncMultiplier_24_24_48_unsigned is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(23 downto 0);
             Y : in  std_logic_vector(23 downto 0);
             R : out  std_logic_vector(47 downto 0);
             Nc : out  std_logic   );
   end component;

signal sign, sign_d1, sign_d2, sign_d3, sign_d4 : std_logic;
signal expX :  std_logic_vector(7 downto 0);
signal expY :  std_logic_vector(7 downto 0);
signal expSumPreSub, expSumPreSub_d1 :  std_logic_vector(9 downto 0);
signal bias, bias_d1 :  std_logic_vector(9 downto 0);
signal expSum, expSum_d1 :  std_logic_vector(9 downto 0);
signal sigX :  std_logic_vector(23 downto 0);
signal sigY :  std_logic_vector(23 downto 0);
signal sigProd :  std_logic_vector(47 downto 0);
signal excSel :  std_logic_vector(3 downto 0);
signal exc, exc_d1, exc_d2, exc_d3, exc_d4 :  std_logic_vector(1 downto 0);
signal norm : std_logic;
signal expPostNorm :  std_logic_vector(9 downto 0);
signal sigProdExt, sigProdExt_d1 :  std_logic_vector(47 downto 0);
signal expSig, expSig_d1 :  std_logic_vector(32 downto 0);
signal sticky, sticky_d1 : std_logic;
signal guard : std_logic;
signal round : std_logic;
signal expSigPostRound :  std_logic_vector(32 downto 0);
signal excPostNorm :  std_logic_vector(1 downto 0);
signal finalExc :  std_logic_vector(1 downto 0);
signal NcA : std_logic ;
constant One : std_logic := '1';

begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            sign_d1 <=  sign;
            sign_d2 <=  sign_d1;
            sign_d3 <=  sign_d2;
            sign_d4 <=  sign_d3;
            expSumPreSub_d1 <=  expSumPreSub;
            bias_d1 <=  bias;
            expSum_d1 <=  expSum;
            exc_d1 <=  exc;
            exc_d2 <=  exc_d1;
            exc_d3 <=  exc_d2;
            exc_d4 <=  exc_d3;
            sigProdExt_d1 <=  sigProdExt;
            expSig_d1 <=  expSig;
            sticky_d1 <=  sticky;
           end if;
         end if;
      end process;
   sign <= X(31) xor Y(31);
   expX <= X(30 downto 23);
   expY <= Y(30 downto 23);
   expSumPreSub <= ("00" & expX) + ("00" & expY);
   bias <= CONV_STD_LOGIC_VECTOR(127,10);
   ----------------Synchro barrier, entering cycle 1----------------
   expSum <= expSumPreSub_d1 - bias_d1;
   ----------------Synchro barrier, entering cycle 0----------------
   sigX <= One & X(22 downto 0);
   sigY <= One & Y(22 downto 0);
-- OF   sigX <= "1" & X(22 downto 0);
-- OF   sigY <= "1" & Y(22 downto 0);
   SignificandMultiplication: IntTruncMultiplier_24_24_48_unsigned  -- pipelineDepth=2 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--                  rst  => rst,
                 R => sigProd,
                 X => sigX,
                 Y => sigY,
                 Nc => NcA);
   ----------------Synchro barrier, entering cycle 2----------------
   ----------------Synchro barrier, entering cycle 0----------------
   excSel <= X(33 downto 32) & Y(33 downto 32);
   with excSel select 
   exc <= "00" when  "0000" | "0001" | "0100", 
          "01" when "0101",
          "10" when "0110" | "1001" | "1010" ,
          "11" when others;
   ----------------Synchro barrier, entering cycle 2----------------
   norm <= sigProd(47);
   -- exponent update
   expPostNorm <= expSum_d1 + ("000000000" & norm);
   ----------------Synchro barrier, entering cycle 2----------------
   -- significand normalization shift
   sigProdExt <= sigProd(46 downto 0) & "0" when norm='1' else
                         sigProd(45 downto 0) & "00";
   expSig <= expPostNorm & sigProdExt(47 downto 25);
   sticky <= sigProdExt(24);
   ----------------Synchro barrier, entering cycle 3----------------
   guard <= '0' when sigProdExt_d1(23 downto 0)="000000000000000000000000" else '1';
   round <= sticky_d1 and ( (guard and not(sigProdExt_d1(25))) or (sigProdExt_d1(25) ))  ;
   RoundingAdder: IntAdder_33_f400_uid28  -- pipelineDepth=1 maxInDelay=1.45844e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                  rst  => rst,
                 Cin => round,
                 R => expSigPostRound   ,
                 X => expSig_d1,
                 Y => "000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 4----------------
   with expSigPostRound(32 downto 31) select
   excPostNorm <=  "01"  when  "00",
                               "10"             when "01", 
                               "00"             when "11"|"10",
                               "11"             when others;
   with exc_d4 select 
   finalExc <= exc_d4 when  "11"|"10"|"00",
                       excPostNorm when others; 
   R <= finalExc & sign_d4 & expSigPostRound(30 downto 0);
   Nc <= NcA and exc_d4(0) and exc_d4(1);
end architecture;

--------------------------------------------------------------------------------
--                       LeftShifter_24_by_max_33_uid35
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2011)
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity LeftShifter_24_by_max_33_uid35 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(23 downto 0);
          S : in  std_logic_vector(5 downto 0);
          R : out  std_logic_vector(56 downto 0)   );
end entity;

architecture arch of LeftShifter_24_by_max_33_uid35 is
signal level0, level0_d1 :  std_logic_vector(23 downto 0);
signal ps, ps_d1 :  std_logic_vector(5 downto 0);
signal level1 :  std_logic_vector(24 downto 0);
signal level2 :  std_logic_vector(26 downto 0);
signal level3 :  std_logic_vector(30 downto 0);
signal level4 :  std_logic_vector(38 downto 0);
signal level5 :  std_logic_vector(54 downto 0);
signal level6 :  std_logic_vector(86 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            level0_d1 <=  level0;
            ps_d1 <=  ps;
           end if;
         end if;
      end process;
   level0<= X;
   ps<= S;
   ----------------Synchro barrier, entering cycle 1----------------
   level1<= level0_d1 & (0 downto 0 => '0') when ps_d1(0)= '1' else     (0 downto 0 => '0') & level0_d1;
   level2<= level1 & (1 downto 0 => '0') when ps_d1(1)= '1' else     (1 downto 0 => '0') & level1;
   level3<= level2 & (3 downto 0 => '0') when ps_d1(2)= '1' else     (3 downto 0 => '0') & level2;
   level4<= level3 & (7 downto 0 => '0') when ps_d1(3)= '1' else     (7 downto 0 => '0') & level3;
   level5<= level4 & (15 downto 0 => '0') when ps_d1(4)= '1' else     (15 downto 0 => '0') & level4;
   level6<= level5 & (31 downto 0 => '0') when ps_d1(5)= '1' else     (31 downto 0 => '0') & level5;
   R <= level6(56 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_12_f400_uid40
--                     (IntAdderClassical_12_f400_uid42)
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

entity IntAdder_12_f400_uid40 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(11 downto 0);
          Y : in  std_logic_vector(11 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(11 downto 0)   );
end entity;

architecture arch of IntAdder_12_f400_uid40 is
signal X_d1 :  std_logic_vector(11 downto 0);
signal Y_d1 :  std_logic_vector(11 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_34_f400_uid49
--                     (IntAdderClassical_34_f400_uid51)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

-- OL library ieee;
-- OL use ieee.std_logic_1164.all;
-- OL use ieee.std_logic_arith.all;
-- OL use ieee.std_logic_unsigned.all;
-- OL library std;
-- OL use std.textio.all;
-- OL library work;

-- OL entity IntAdder_34_f400_uid49 is
-- OL    port ( clk, rst : in std_logic;
-- OL           X : in  std_logic_vector(33 downto 0);
-- OL           Y : in  std_logic_vector(33 downto 0);
-- OL           Cin : in std_logic;
-- OL           R : out  std_logic_vector(33 downto 0)   );
-- OL end entity;

-- OL architecture arch of IntAdder_34_f400_uid49 is
-- OL signal X_d1 :  std_logic_vector(33 downto 0);
-- OL signal Y_d1 :  std_logic_vector(33 downto 0);
-- OL signal Cin_d1 : std_logic;
-- OL begin
-- OL    process(clk)
-- OL       begin
-- OL          if clk'event and clk = '1' then
-- OL             X_d1 <=  X;
-- OL             Y_d1 <=  Y;
-- OL             Cin_d1 <=  Cin;
-- OL          end if;
-- OL       end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
-- OL     R <= X_d1 + Y_d1 + Cin_d1;
-- OL end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_26_f484_uid55
--                    (IntAdderAlternative_26_f484_uid59)
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

entity IntAdder_26_f484_uid55 is
   port ( clk :  in std_logic;
          Enable : in std_logic;
-- OF     rst : in std_logic;
          X : in  std_logic_vector(25 downto 0);
          Y : in  std_logic_vector(25 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(25 downto 0)   );
end entity;

architecture arch of IntAdder_26_f484_uid55 is
signal s_sum_l0_idx0 :  std_logic_vector(23 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(3 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(22 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
-- OL signal sum_l0_idx1 :  std_logic_vector(2 downto 0);
-- OL signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(3 downto 0);
signal sum_l1_idx1 :  std_logic_vector(2 downto 0);
-- OL signal c_l1_idx1 :  std_logic_vector(0 downto 0);
signal X_d1 :  std_logic_vector(25 downto 0);
signal Y_d1 :  std_logic_vector(25 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            s_sum_l0_idx1_d1 <=  s_sum_l0_idx1;
            sum_l0_idx0_d1 <=  sum_l0_idx0;
            c_l0_idx0_d1 <=  c_l0_idx0;
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   ----------------Synchro barrier, entering cycle 1----------------
   --Alternative
   s_sum_l0_idx0 <= ( "0" & X_d1(22 downto 0)) + ( "0" & Y_d1(22 downto 0)) + Cin_d1;
   s_sum_l0_idx1 <= ( "0" & X_d1(25 downto 23)) + ( "0" & Y_d1(25 downto 23));
   sum_l0_idx0 <= s_sum_l0_idx0(22 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(23 downto 23);
-- OL   sum_l0_idx1 <= s_sum_l0_idx1(2 downto 0);
-- OL   c_l0_idx1 <= s_sum_l0_idx1(3 downto 3);
   ----------------Synchro barrier, entering cycle 2----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(2 downto 0);
-- OL   c_l1_idx1 <= s_sum_l1_idx1(3 downto 3);
   R <= sum_l1_idx1(2 downto 0) & sum_l0_idx0_d1(22 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_18_f400_uid62
--                     (IntAdderClassical_18_f400_uid64)
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

entity IntAdder_18_f400_uid62 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(17 downto 0);
          Y : in  std_logic_vector(17 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(17 downto 0)   );
end entity;

architecture arch of IntAdder_18_f400_uid62 is
signal X_d1 :  std_logic_vector(17 downto 0);
signal Y_d1 :  std_logic_vector(17 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_18_f400_uid68
--                     (IntAdderClassical_18_f400_uid70)
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

entity IntAdder_18_f400_uid68 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(17 downto 0);
          Y : in  std_logic_vector(17 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(17 downto 0)   );
end entity;

architecture arch of IntAdder_18_f400_uid68 is
signal X_d1 :  std_logic_vector(17 downto 0);
signal Y_d1 :  std_logic_vector(17 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                     IntMultiplier_17_18_unsigned_uid74
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Sebastian Banescu (2008-2009)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library work;
entity IntMultiplier_17_18_unsigned_uid74 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL , rst : in std_logic;
          X : in  std_logic_vector(16 downto 0);
          Y : in  std_logic_vector(17 downto 0);
          R : out  std_logic_vector(34 downto 0);
          Nc : out  std_logic    );
end entity;

architecture arch of IntMultiplier_17_18_unsigned_uid74 is
signal sX :  std_logic_vector(16 downto 0);
signal sY :  std_logic_vector(33 downto 0);
signal x0, x0_d1, x0_d2 :  std_logic_vector(16 downto 0);
signal y0, y0_d1 :  std_logic_vector(16 downto 0);
signal y1, y1_d1, y1_d2 :  std_logic_vector(16 downto 0);
signal px0y0, px0y0_d1, px0y0_d2 :  std_logic_vector(33 downto 0);
signal tpx0y1 :  std_logic_vector(33 downto 0);
signal px0y1, px0y1_d1 :  std_logic_vector(34 downto 0);
signal sum0 :  std_logic_vector(50 downto 0);
signal NcA : STD_LOGIC;
signal NcB : STD_LOGIC;
signal NcC : STD_LOGIC;
signal NcD : STD_LOGIC;
signal NcE : STD_LOGIC;
signal NcF : STD_LOGIC;


-- OL signal sum0Low :  std_logic_vector(16 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then 
            x0_d1 <=  x0;
            x0_d2 <=  x0_d1;
            y0_d1 <=  y0;
            y1_d1 <=  y1;
            y1_d2 <=  y1_d1;
            px0y0_d1 <=  px0y0;
            px0y0_d2 <=  px0y0_d1;
            px0y1_d1 <=  px0y1;
           end if;
         end if;
      end process;
   sX <= X & "";
   sY <= Y & "0000000000000000";
   x0 <= sX(16 downto 0);
   y0 <= sY(16 downto 0);
   y1 <= sY(33 downto 17);
   ----------------Synchro barrier, entering cycle 1----------------
   px0y0 <= x0_d1 * y0_d1;
   ----------------Synchro barrier, entering cycle 2----------------
   tpx0y1 <= x0_d2 * y1_d2;
   px0y1 <= ( "0" & tpx0y1) + px0y0_d1(33 downto 17);
   ----------------Synchro barrier, entering cycle 3----------------
   sum0 <= px0y1_d1(33 downto 0) & px0y0_d2(16 downto 0);
-- OL   sum0Low <= sum0(16 downto 0);
   R <= sum0(50 downto 16);

NcA <= px0y0_d1(0) and px0y0_d1(1) and px0y0_d1(2)  and px0y0_d1(3)  and px0y0_d1(4)  and px0y0_d1(5)  and px0y0_d1(6)  and px0y0_d1(7) ;
NcB <= px0y0_d1(8) and px0y0_d1(9) and px0y0_d1(10) and px0y0_d1(11) and px0y0_d1(12) and px0y0_d1(13) and px0y0_d1(14) and px0y0_d1(15);
NcC <= px0y1_d1(0) and px0y1_d1(1) and px0y1_d1(2)  and px0y1_d1(3)  and px0y1_d1(4)  and px0y1_d1(5)  and px0y1_d1(6)  and px0y1_d1(7) ;
NcD <= px0y1_d1(8) and px0y1_d1(9) and px0y1_d1(10) and px0y1_d1(11) and px0y1_d1(12) and px0y1_d1(13) and px0y1_d1(14) and px0y1_d1(34);
NcE <=  px0y0_d2(0) and px0y0_d2(1) and px0y0_d2(2)  and px0y0_d2(3)  and px0y0_d2(4)  and px0y0_d2(5)  and px0y0_d2(6)  and px0y0_d2(7) ;
NcF <= px0y0_d2(8) and px0y0_d2(9) and px0y0_d2(10) and px0y0_d2(11) and px0y0_d2(12) and px0y0_d2(13) and px0y0_d2(14) and px0y0_d2(15);
Nc <= NcA or NcB or NcC or NcD or NcE or NcF or px0y0_d1(16);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_27_f400_uid78
--                     (IntAdderClassical_27_f400_uid80)
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

entity IntAdder_27_f400_uid78 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OF     rst : in std_logic;
          X : in  std_logic_vector(26 downto 0);
          Y : in  std_logic_vector(26 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(26 downto 0)   );
end entity;

architecture arch of IntAdder_27_f400_uid78 is
signal X_d1 :  std_logic_vector(26 downto 0);
signal Y_d1 :  std_logic_vector(26 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_33_f400_uid84
--                    (IntAdderAlternative_33_f400_uid88)
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

entity IntAdder_33_f400_uid84 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OF     rst : in std_logic;
          X : in  std_logic_vector(32 downto 0);
          Y : in  std_logic_vector(32 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(32 downto 0)   );
end entity;

architecture arch of IntAdder_33_f400_uid84 is
signal s_sum_l0_idx0 :  std_logic_vector(25 downto 0);
signal s_sum_l0_idx1, s_sum_l0_idx1_d1 :  std_logic_vector(8 downto 0);
signal sum_l0_idx0, sum_l0_idx0_d1 :  std_logic_vector(24 downto 0);
signal c_l0_idx0, c_l0_idx0_d1 :  std_logic_vector(0 downto 0);
-- OL signal sum_l0_idx1 :  std_logic_vector(7 downto 0);
-- OL signal c_l0_idx1 :  std_logic_vector(0 downto 0);
signal s_sum_l1_idx1 :  std_logic_vector(8 downto 0);
signal sum_l1_idx1 :  std_logic_vector(7 downto 0);
-- OL signal c_l1_idx1 :  std_logic_vector(0 downto 0);
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            s_sum_l0_idx1_d1 <=  s_sum_l0_idx1;
            sum_l0_idx0_d1 <=  sum_l0_idx0;
            c_l0_idx0_d1 <=  c_l0_idx0;
           end if;
         end if;
      end process;
   --Alternative
   s_sum_l0_idx0 <= ( "0" & X(24 downto 0)) + ( "0" & Y(24 downto 0)) + Cin;
   s_sum_l0_idx1 <= ( "0" & X(32 downto 25)) + ( "0" & Y(32 downto 25));
   sum_l0_idx0 <= s_sum_l0_idx0(24 downto 0);
   c_l0_idx0 <= s_sum_l0_idx0(25 downto 25);
-- OL   sum_l0_idx1 <= s_sum_l0_idx1(7 downto 0);
-- OL   c_l0_idx1 <= s_sum_l0_idx1(8 downto 8);
   ----------------Synchro barrier, entering cycle 1----------------
   s_sum_l1_idx1 <=  s_sum_l0_idx1_d1 + c_l0_idx0_d1(0 downto 0);
   sum_l1_idx1 <= s_sum_l1_idx1(7 downto 0);
-- OL   c_l1_idx1 <= s_sum_l1_idx1(8 downto 8);
   R <= sum_l1_idx1(7 downto 0) & sum_l0_idx0_d1(24 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                      IntMultiAdder_48_op1_f400_uid93
--                       (IntCompressorTree_48_1_uid95)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009-2011)
--------------------------------------------------------------------------------
-- Pipeline depth: 0 cycles

-- OF library ieee;
-- OF use ieee.std_logic_1164.all;
-- OF use ieee.std_logic_arith.all;
-- OF use ieee.std_logic_unsigned.all;
-- OF library std;
-- OF use std.textio.all;
-- OF library work;

-- OF entity IntMultiAdder_48_op1_f400_uid93 is
-- OF    port ( clk, rst : in std_logic;
-- OF           X0 : in  std_logic_vector(47 downto 0);
-- OF           R : out  std_logic_vector(47 downto 0)   );
-- OF end entity;

-- OF architecture arch of IntMultiAdder_48_op1_f400_uid93 is
-- OF signal l_0_s_0 :  std_logic_vector(47 downto 0);
-- OF begin
-- OF    process(clk)
-- OF       begin
-- OF          if clk'event and clk = '1' then
-- OF          end if;
-- OF       end process;
-- OF    l_0_s_0 <= X0;
-- OF    R <= X0;
-- OF end architecture;

--------------------------------------------------------------------------------
--                    IntTruncMultiplier_24_24_48_unsigned
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Sebastian Banescu, Bogdan Pasca, Radu Tudoran (2010-2011)
--------------------------------------------------------------------------------
--library ieee; 
--use ieee.std_logic_1164.all;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_signed.all;
--library work;
--
--entity IntTruncMultiplier_24_24_48_unsigned is
--   port ( clk, rst : in std_logic;
--          X : in  std_logic_vector(23 downto 0);
--          Y : in  std_logic_vector(23 downto 0);
--          R : out  std_logic_vector(47 downto 0)   );
--end entity;

--architecture arch of IntTruncMultiplier_24_24_48_unsigned is
--   component IntMultiAdder_48_op1_f400_uid93 is
--      port ( clk, rst : in std_logic;
--             X0 : in  std_logic_vector(47 downto 0);
--             R : out  std_logic_vector(47 downto 0)   );
--   end component;

--signal x0_0 :  std_logic_vector(17 downto 0);
--signal y0_0 :  std_logic_vector(24 downto 0);
--signal pxy00, pxy00_d1, pxy00_d2 :  std_logic_vector(42 downto 0);
--signal x0_1, x0_1_d1 :  std_logic_vector(17 downto 0);
--signal y0_1, y0_1_d1 :  std_logic_vector(24 downto 0);
--signal txy01 :  std_logic_vector(42 downto 0);
--signal pxy01, pxy01_d1 :  std_logic_vector(42 downto 0);
--signal addOpDSP0 :  std_logic_vector(47 downto 0);
--signal addRes :  std_logic_vector(47 downto 0);
--begin
--   process(clk)
--      begin
--         if clk'event and clk = '1' then
--            pxy00_d1 <=  pxy00;
--            pxy00_d2 <=  pxy00_d1;
--            x0_1_d1 <=  x0_1;
--            y0_1_d1 <=  y0_1;
--            pxy01_d1 <=  pxy01;
--         end if;
--      end process;
--   ----------------Synchro barrier, entering cycle 0----------------
--   ----------------Synchro barrier, entering cycle 0----------------
--   x0_0 <= "0" & "" & X(6 downto 0) & "0000000000";
--   y0_0 <= "0" & "" & Y(23 downto 0) & "";
--   pxy00 <= x0_0(17 downto 0) * y0_0(24 downto 0); --0
--   ----------------Synchro barrier, entering cycle 0----------------
--   x0_1 <= "0" & "" & X(23 downto 7) & "";
--   y0_1 <= "0" & "" & Y(23 downto 0) & "";
--   ----------------Synchro barrier, entering cycle 1----------------
--   txy01 <= x0_1_d1(17 downto 0) * y0_1_d1(24 downto 0);
--   pxy01 <= (txy01(42 downto 0)) + ("00000000000000000" &pxy00_d1(42 downto 17));
--   ----------------Synchro barrier, entering cycle 2----------------
--   addOpDSP0 <= "" & pxy01_d1(40 downto 0) & pxy00_d2(16 downto 10) & "" &  "";--3 bpadX 10 bpadY 0
--   adder: IntMultiAdder_48_op1_f400_uid93  -- pipelineDepth=0 maxInDelay=4.4472e-10
--      port map ( clk  => clk,
--                 rst  => rst,
--                 R => addRes,
--                 X0 => addOpDSP0);
--   R <= addRes(47 downto 0);
--end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_33_f400_uid97
--                     (IntAdderClassical_33_f400_uid99)
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

entity IntAdder_33_f400_uid97 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(32 downto 0);
          Y : in  std_logic_vector(32 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(32 downto 0)   );
end entity;

architecture arch of IntAdder_33_f400_uid97 is
signal X_d1 :  std_logic_vector(32 downto 0);
signal Y_d1 :  std_logic_vector(32 downto 0);
signal Cin_d1 : std_logic;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;
   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
end architecture;

--------------------------------------------------------------------------------
--                     FPMultiplier_8_23_8_23_8_23_uid90
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin 2008-2011
--------------------------------------------------------------------------------
-- Pipeline depth: 4 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPMultiplier_8_23_8_23_8_23_uid90 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(8+23+2 downto 0);
          Y : in  std_logic_vector(8+23+2 downto 0);
          R : out  std_logic_vector(8+23+2 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of FPMultiplier_8_23_8_23_8_23_uid90 is
   component IntAdder_33_f400_uid97 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(32 downto 0);
             Y : in  std_logic_vector(32 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(32 downto 0)   );
   end component;

   component IntTruncMultiplier_24_24_48_unsigned is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(23 downto 0);
             Y : in  std_logic_vector(23 downto 0);
             R : out  std_logic_vector(47 downto 0);
             Nc : out  std_logic   );
   end component;

signal sign, sign_d1, sign_d2, sign_d3, sign_d4 : std_logic;
signal expX :  std_logic_vector(7 downto 0);
signal expY :  std_logic_vector(7 downto 0);
signal expSumPreSub, expSumPreSub_d1 :  std_logic_vector(9 downto 0);
signal bias, bias_d1 :  std_logic_vector(9 downto 0);
signal expSum, expSum_d1 :  std_logic_vector(9 downto 0);
signal sigX :  std_logic_vector(23 downto 0);
signal sigY :  std_logic_vector(23 downto 0);
signal sigProd :  std_logic_vector(47 downto 0);
signal excSel :  std_logic_vector(3 downto 0);
signal exc, exc_d1, exc_d2, exc_d3, exc_d4 :  std_logic_vector(1 downto 0);
signal norm : std_logic;
signal expPostNorm :  std_logic_vector(9 downto 0);
signal sigProdExt, sigProdExt_d1 :  std_logic_vector(47 downto 0);
signal expSig, expSig_d1 :  std_logic_vector(32 downto 0);
signal sticky, sticky_d1 : std_logic;
signal guard : std_logic;
signal round : std_logic;
signal expSigPostRound :  std_logic_vector(32 downto 0);
signal excPostNorm :  std_logic_vector(1 downto 0);
signal finalExc :  std_logic_vector(1 downto 0);
signal NcA : STD_LOGIC;
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            sign_d1 <=  sign;
            sign_d2 <=  sign_d1;
            sign_d3 <=  sign_d2;
            sign_d4 <=  sign_d3;
            expSumPreSub_d1 <=  expSumPreSub;
            bias_d1 <=  bias;
            expSum_d1 <=  expSum;
            exc_d1 <=  exc;
            exc_d2 <=  exc_d1;
            exc_d3 <=  exc_d2;
            exc_d4 <=  exc_d3;
            sigProdExt_d1 <=  sigProdExt;
            expSig_d1 <=  expSig;
            sticky_d1 <=  sticky;
           end if;
         end if;
      end process;
   sign <= X(31) xor Y(31);
   expX <= X(30 downto 23);
   expY <= Y(30 downto 23);
   expSumPreSub <= ("00" & expX) + ("00" & expY);
   bias <= CONV_STD_LOGIC_VECTOR(127,10);
   ----------------Synchro barrier, entering cycle 1----------------
   expSum <= expSumPreSub_d1 - bias_d1;
   ----------------Synchro barrier, entering cycle 0----------------
   sigX <= "1" & X(22 downto 0);
   sigY <= "1" & Y(22 downto 0);
   SignificandMultiplication: IntTruncMultiplier_24_24_48_unsigned  -- pipelineDepth=2 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => sigProd,
                 X => sigX,
                 Y => sigY,
                 Nc => NcA);
   ----------------Synchro barrier, entering cycle 2----------------
   ----------------Synchro barrier, entering cycle 0----------------
   excSel <= X(33 downto 32) & Y(33 downto 32);
   with excSel select 
   exc <= "00" when  "0000" | "0001" | "0100", 
          "01" when "0101",
          "10" when "0110" | "1001" | "1010" ,
          "11" when others;
   ----------------Synchro barrier, entering cycle 2----------------
   norm <= sigProd(47);
   -- exponent update
   expPostNorm <= expSum_d1 + ("000000000" & norm);
   ----------------Synchro barrier, entering cycle 2----------------
   -- significand normalization shift
   sigProdExt <= sigProd(46 downto 0) & "0" when norm='1' else
                         sigProd(45 downto 0) & "00";
   expSig <= expPostNorm & sigProdExt(47 downto 25);
   sticky <= sigProdExt(24);
   ----------------Synchro barrier, entering cycle 3----------------
   guard <= '0' when sigProdExt_d1(23 downto 0)="000000000000000000000000" else '1';
   round <= sticky_d1 and ( (guard and not(sigProdExt_d1(25))) or (sigProdExt_d1(25) ))  ;
   RoundingAdder: IntAdder_33_f400_uid97  -- pipelineDepth=1 maxInDelay=1.45844e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 Cin => round,
                 R => expSigPostRound   ,
                 X => expSig_d1,
                 Y => "000000000000000000000000000000000");
   ----------------Synchro barrier, entering cycle 4----------------
   with expSigPostRound(32 downto 31) select
   excPostNorm <=  "01"  when  "00",
                               "10"             when "01", 
                               "00"             when "11"|"10",
                               "11"             when others;
   with exc_d4 select 
   finalExc <= exc_d4 when  "11"|"10"|"00",
                       excPostNorm when others; 
   R <= finalExc & sign_d4 & expSigPostRound(30 downto 0);
   Nc <= NcA;

end architecture;

--------------------------------------------------------------------------------
--                 FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Florent de Dinechin (2007)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
entity FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0 is
   port (-- OL clk, rst : in std_logic;
          X : in  std_logic_vector(5 downto 0);
          Y : out  std_logic_vector(7 downto 0)   );
end entity;

architecture arch of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0 is
begin
  with X select  Y <= 
   "00000000" when "000000",
   "00000011" when "000001",
   "00000110" when "000010",
   "00001001" when "000011",
   "00001100" when "000100",
   "00001110" when "000101",
   "00010001" when "000110",
   "00010100" when "000111",
   "00010111" when "001000",
   "00011010" when "001001",
   "00011101" when "001010",
   "00100000" when "001011",
   "00100011" when "001100",
   "00100110" when "001101",
   "00101000" when "001110",
   "00101011" when "001111",
   "00101110" when "010000",
   "00110001" when "010001",
   "00110100" when "010010",
   "00110111" when "010011",
   "00111010" when "010100",
   "00111101" when "010101",
   "00111111" when "010110",
   "01000010" when "010111",
   "01000101" when "011000",
   "01001000" when "011001",
   "01001011" when "011010",
   "01001110" when "011011",
   "01010001" when "011100",
   "01010100" when "011101",
   "01010111" when "011110",
   "01011001" when "011111",
   "01011100" when "100000",
   "01011111" when "100001",
   "01100010" when "100010",
   "01100101" when "100011",
   "01101000" when "100100",
   "01101011" when "100101",
   "01101110" when "100110",
   "01110001" when "100111",
   "01110011" when "101000",
   "01110110" when "101001",
   "01111001" when "101010",
   "01111100" when "101011",
   "01111111" when "101100",
   "10000010" when "101101",
   "10000101" when "101110",
   "10001000" when "101111",
   "10001010" when "110000",
   "10001101" when "110001",
   "10010000" when "110010",
   "10010011" when "110011",
   "10010110" when "110100",
   "10011001" when "110101",
   "10011100" when "110110",
   "10011111" when "110111",
   "10100010" when "111000",
   "10100100" when "111001",
   "10100111" when "111010",
   "10101010" when "111011",
   "10101101" when "111100",
   "10110000" when "111101",
   "10110011" when "111110",
   "10110110" when "111111",
   "--------" when others;
end architecture;

--------------------------------------------------------------------------------
--                 FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Florent de Dinechin (2007)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
entity FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1 is
   port (-- OL clk, rst : in std_logic;
          X : in  std_logic_vector(3 downto 0);
          Y : out  std_logic_vector(11 downto 0)   );
end entity;

architecture arch of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1 is
begin
  with X select  Y <= 
   "000000001000" when "0000",
   "000011000001" when "0001",
   "000101111001" when "0010",
   "001000110010" when "0011",
   "001011101011" when "0100",
   "001110100011" when "0101",
   "010001011100" when "0110",
   "010100010101" when "0111",
   "010111001101" when "1000",
   "011010000110" when "1001",
   "011100111111" when "1010",
   "011111110111" when "1011",
   "100010110000" when "1100",
   "100101101001" when "1101",
   "101000100001" when "1110",
   "101011011010" when "1111",
   "------------" when others;
end architecture;

--------------------------------------------------------------------------------
--                              MagicSPExpTable
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Radu Tudoran, Florent de Dinechin (2009)
--------------------------------------------------------------------------------
-- combinatorial

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity MagicSPExpTable is
   port ( X1 : in  std_logic_vector(8 downto 0);
          Y1 : out  std_logic_vector(35 downto 0);
          X2 : in  std_logic_vector(8 downto 0);
          Y2 : out  std_logic_vector(35 downto 0)   );
end entity;

architecture arch of MagicSPExpTable is
type ROMContent is array (0 to 511) of std_logic_vector(35 downto 0);
constant memVar: ROMContent :=    ( 
      "100000000000000000000000000000000000",       "100000000100000000010000000000000000",       "100000001000000001000000001000000000",       "100000001100000010010000010000000000", 
      "100000010000000100000000101000000000",       "100000010100000110010001010000000000",       "100000011000001001000010010000000000",       "100000011100001100010011101000000000", 
      "100000100000010000000101011000000000",       "100000100100010100010111101000000000",       "100000101000011001001010100000000000",       "100000101100011110011110000000000000", 
      "100000110000100100010010001000000000",       "100000110100101010100111000000000000",       "100000111000110001011100110000000000",       "100000111100111000110011011000000000", 
      "100001000001000000101011000000000000",       "100001000101001001000011101000000000",       "100001001001010001111101010000000000",       "100001001101011011011000001000000000", 
      "100001010001100101010100001000000000",       "100001010101101111110001100000000000",       "100001011001111010110000001000000000",       "100001011110000110010000001000000000", 
      "100001100010010010010001110000000000",       "100001100110011110110100110000000000",       "100001101010101011111001011000000000",       "100001101110111001011111110000000000", 
      "100001110011000111100111111000000000",       "100001110111010110010001110000000000",       "100001111011100101011101011000000000",       "100001111111110101001011001000000000", 
      "100010000100000101011010110000000001",       "100010001000010110001100100000000001",       "100010001100100111100000010000000001",       "100010010000111001010110011000000001", 
      "100010010101001011101110101000000001",       "100010011001011110101001010000000001",       "100010011101110010000110011000000001",       "100010100010000110000101111000000001", 
      "100010100110011010100111111000000001",       "100010101010101111101100100000000001",       "100010101111000101010011111000000001",       "100010110011011011011101111000000001", 
      "100010110111110010001010110000000001",       "100010111100001001011010100000000001",       "100011000000100001001101001000000001",       "100011000100111001100010110000000001", 
      "100011001001010010011011100000000001",       "100011001101101011110111011000000001",       "100011010010000101110110100000000001",       "100011010110100000011000111000000001", 
      "100011011010111011011110101000000001",       "100011011111010111000111110000000001",       "100011100011110011010100011000000001",       "100011101000010000000100101000000001", 
      "100011101100101101011000100000000010",       "100011110001001011010000000000000010",       "100011110101101001101011010000000010",       "100011111010001000101010100000000010", 
      "100011111110101000001101100000000010",       "100100000011001000010100100000000010",       "100100000111101000111111101000000010",       "100100001100001010001110110000000010", 
      "100100010000101100000010001000000010",       "100100010101001110011001111000000010",       "100100011001110001010101110000000010",       "100100011110010100110110001000000010", 
      "100100100010111000111011000000000010",       "100100100111011101100100100000000010",       "100100101100000010110010100000000010",       "100100110000101000100101001000000010", 
      "100100110101001110111100101000000011",       "100100111001110101111000111000000011",       "100100111110011101011010001000000011",       "100101000011000101100000010000000011", 
      "100101000111101110001011100000000011",       "100101001100010111011011111000000011",       "100101010001000001010001011000000011",       "100101010101101011101100010000000011", 
      "100101011010010110101100011000000011",       "100101011111000010010001111000000011",       "100101100011101110011101000000000011",       "100101101000011011001101100000000011", 
      "100101101101001000100011110000000011",       "100101110001110110011111110000000100",       "100101110110100101000001011000000100",       "100101111011010100001001000000000100", 
      "100110000000000011110110100000000100",       "100110000100110100001010000000000100",       "100110001001100101000011100000000100",       "100110001110010110100011010000000100", 
      "100110010011001000101001010000000100",       "100110010111111011010101100000000100",       "100110011100101110101000001000000100",       "100110100001100010100001001000000100", 
      "100110100110010111000000110000000101",       "100110101011001100000110111000000101",       "100110110000000001110011110000000101",       "100110110100111000000111011000000101", 
      "100110111001101111000001111000000101",       "100110111110100110100011001000000101",       "100111000011011110101011100000000101",       "100111001000010111011010111000000101", 
      "100111001101010000110001011000000101",       "100111010010001010101111001000000101",       "100111010111000101010100001000000101",       "100111011100000000100000011000000110", 
      "100111100000111100010100010000000110",       "100111100101111000101111100000000110",       "100111101010110101110010100000000110",       "100111101111110011011101000000000110", 
      "100111110100110001101111011000000110",       "100111111001110000101001100000000110",       "100111111110110000001011100000000110",       "101000000011110000010101100000000110", 
      "101000001000110001000111101000000111",       "101000001101110010100001111000000111",       "101000010010110100100100010000000111",       "101000010111110111001111000000000111", 
      "101000011100111010100010001000000111",       "101000100001111110011101101000000111",       "101000100111000011000001110000000111",       "101000101100001000001110100000000111", 
      "101000110001001110000011111000001000",       "101000110110010100100010000000001000",       "101000111011011011101001000000001000",       "101001000000100011011001000000001000", 
      "101001000101101011110001111000001000",       "101001001010110100110011111000001000",       "101001001111111110011111001000001000",       "101001010101001000110011100000001000", 
      "101001011010010011110001011000001001",       "101001011111011111011000100000001001",       "101001100100101011101001010000001001",       "101001101001111000100011100000001001", 
      "101001101111000110000111011000001001",       "101001110100010100010101000000001001",       "101001111001100011001100100000001001",       "101001111110110010101101111000001001", 
      "101010000100000010111001010000001010",       "101010001001010011101110101000001010",       "101010001110100101001110001000001010",       "101010010011110111010111111000001010", 
      "101010011001001010001100000000001010",       "101010011110011101101010100000001010",       "101010100011110001110011100000001010",       "101010101001000110100111000000001011", 
      "101010101110011100000101001000001011",       "101010110011110010001110000000001011",       "101010111001001001000001110000001011",       "101010111110100000100000011000001011", 
      "101011000011111000101001111000001011",       "101011001001010001011110100000001011",       "101011001110101010111110010000001100",       "101011010100000101001001010000001100", 
      "101011011001011111111111101000001100",       "101011011110111011100001010000001100",       "101011100100010111101110100000001100",       "101011101001110100100111010000001100", 
      "101011101111010010001011110000001101",       "101011110100110000011011111000001101",       "101011111010001111010111111000001101",       "101011111111101110111111110000001101", 
      "101100000101001111010011101000001101",       "101100001010110000010011101000001101",       "101100010000010001111111110000001101",       "101100010101110100011000001000001110", 
      "101100011011010111011100111000001110",       "101100100000111011001110000000001110",       "101100100110011111101011101000001110",       "101100101100000100110110000000001110", 
      "101100110001101010101100111000001110",       "101100110111010001010000101000001111",       "101100111100111000100001010000001111",       "101101000010100000011110110000001111", 
      "101101001000001001001001011000001111",       "101101001101110010100001001000001111",       "101101010011011100100110000000001111",       "101101011001000111011000010000010000", 
      "101101011110110010110111111000010000",       "101101100100011111000101000000010000",       "101101101010001011111111110000010000",       "101101101111111001101000001000010000", 
      "101101110101100111111110001000010001",       "101101111011010111000010001000010001",       "101110000001000110110100000000010001",       "101110000110110111010011111000010001", 
      "101110001100101000100001111000010001",       "101110010010011010011110000000010001",       "101110011000001101001000100000010010",       "101110011110000000100001010000010010", 
      "101110100011110100101000101000010010",       "101110101001101001011110100000010010",       "101110101111011111000011000000010010",       "101110110101010101010110010000010011", 
      "101110111011001100011000011000010011",       "101111000001000100001001011000010011",       "101111000110111100101001100000010011",       "101111001100110101111000101000010011", 
      "101111010010101111110111000000010100",       "101111011000101010100100101000010100",       "101111011110100110000001101000010100",       "101111100100100010001110001000010100", 
      "101111101010011111001010010000010100",       "101111110000011100110110000000010101",       "101111110110011011010001100000010101",       "101111111100011010011100110000010101", 
      "110000000010011010011000001000010101",       "110000001000011011000011011000010101",       "110000001110011100011110111000010110",       "110000010100011110101010101000010110", 
      "110000011010100001100110101000010110",       "110000100000100101010011000000010110",       "110000100110101001110000000000010110",       "110000101100101110111101100000010111", 
      "110000110010110100111011110000010111",       "110000111000111011101010110000010111",       "110000111111000011001010101000010111",       "110001000101001011011011101000010111", 
      "110001001011010100011101100000011000",       "110001010001011110010000110000011000",       "110001010111101000110101001000011000",       "110001011101110100001011000000011000", 
      "110001100100000000010010010000011001",       "110001101010001101001011001000011001",       "110001110000011010110101100000011001",       "110001110110101001010001110000011001", 
      "110001111100111000011111111000011001",       "110010000011001000100000000000011010",       "110010001001011001010010001000011010",       "110010001111101010110110011000011010", 
      "110010010101111101001100111000011010",       "110010011100010000010101101000011011",       "110010100010100100010000111000011011",       "110010101000111000111110110000011011", 
      "110010101111001110011111010000011011",       "110010110101100100110010011000011011",       "110010111011111011111000100000011100",       "110011000010010011110001011000011100", 
      "110011001000101100011101011000011100",       "110011001111000101111100100000011100",       "110011010101100000001110111000011101",       "110011011011111011010100101000011101", 
      "110011100010010111001101110000011101",       "110011101000110011111010100000011101",       "110011101111010001011010110000011110",       "110011110101101111101110111000011110", 
      "110011111100001110110110110000011110",       "110100000010101110110010101000011110",       "110100001001001111100010100000011111",       "110100001111110001000110100000011111", 
      "110100010110010011011110111000011111",       "110100011100110110101011100000011111",       "110100100011011010101100100000100000",       "110100101001111111100010001000100000", 
      "010011011010001011001100000000100000",       "010011011100100110100111000000100000",       "010011011111000010010101101000100001",       "010011100001011110010111101000100001", 
      "010011100011111010101101010000100001",       "010011100110010111010110011000100001",       "010011101000110100010011001000100010",       "010011101011010001100011011000100010", 
      "010011101101101111000111100000100010",       "010011110000001100111111010000100010",       "010011110010101011001010110000100011",       "010011110101001001101010000000100011", 
      "010011110111101000011101001000100011",       "010011111010000111100100001000100011",       "010011111100100110111111000000100100",       "010011111111000110101101111000100100", 
      "010100000001100110110000110000100100",       "010100000100000111000111101000100100",       "010100000110100111110010100000100101",       "010100001001001000110001101000100101", 
      "010100001011101010000100110000100101",       "010100001110001011101100001000100101",       "010100010000101101100111101000100110",       "010100010011001111110111100000100110", 
      "010100010101110010011011101000100110",       "010100011000010101010100001000100111",       "010100011010111000100001000000100111",       "010100011101011100000010010000100111", 
      "010100011111111111111000000000100111",       "010100100010100100000010010000101000",       "010100100101001000100001000000101000",       "010100100111101101010100011000101000", 
      "010100101010010010011100011000101001",       "010100101100110111111001000000101001",       "010100101111011101101010011000101001",       "010100110010000011110000100000101001", 
      "010100110100101010001011011000101010",       "010100110111010000111011000000101010",       "010100111001110111111111101000101010",       "010100111100011111011001000000101011", 
      "010100111111000111000111100000101011",       "010101000001101111001010111000101011",       "010101000100010111100011010000101011",       "010101000111000000010000110000101100", 
      "010101001001101001010011011000101100",       "010101001100010010101011001000101100",       "010101001110111100011000000000101101",       "010101010001100110011010001000101101", 
      "010101010100010000110001101000101101",       "010101010110111011011110011000101101",       "010101011001100110100000100000101110",       "010101011100010001111000000000101110", 
      "010101011110111101100101000000101110",       "010101100001101001100111011000101111",       "010101100100010101111111011000101111",       "010101100111000010101101000000101111", 
      "010101101001101111110000001000110000",       "010101101100011101001000111000110000",       "010101101111001010110111011000110000",       "010101110001111000111011101000110000", 
      "010101110100100111010101101000110001",       "010101110111010110000101100000110001",       "010101111010000101001011001000110001",       "010101111100110100100110110000110010", 
      "010101111111100100011000011000110010",       "010110000010010100011111111000110010",       "010110000101000100111101100000110011",       "010110000111110101110001001000110011", 
      "010110001010100110111011000000110011",       "010110001101011000011010111000110100",       "010110010000001010010001000000110100",       "010110010010111100011101100000110100", 
      "010110010101101111000000001000110101",       "010110011000100001111001010000110101",       "010110011011010101001000101000110101",       "010110011110001000101110100000110110", 
      "010110100000111100101010111000110110",       "010110100011110000111101110000110110",       "010110100110100101100111001000110110",       "010110101001011010100111001000110111", 
      "010110101100001111111101110000110111",       "010110101111000101101011001000110111",       "010110110001111011101111010000111000",       "010110110100110010001010001000111000", 
      "010110110111101000111011110000111000",       "010110111010100000000100011000111001",       "010110111101010111100011111000111001",       "010111000000001111011010010000111001", 
      "010111000011000111100111101000111010",       "010111000110000000001100001000111010",       "010111001000111001000111110000111010",       "010111001011110010011010100000111011", 
      "010111001110101100000100011000111011",       "010111010001100110000101100000111011",       "010111010100100000011101111000111100",       "010111010111011011001101101000111100", 
      "010111011010010110010100110000111101",       "010111011101010001110011010000111101",       "010111100000001101101001001000111101",       "010111100011001001110110101000111110", 
      "010111100110000110011011101000111110",       "010111101001000011011000010000111110",       "010111101100000000101100100000111111",       "010111101110111110011000100000111111", 
      "010111110001111100011100001000111111",       "010111110100111010110111101001000000",       "010111110111111001101010111001000000",       "010111111010111000110110000001000000", 
      "010111111101111000011001001001000001",       "011000000000111000010100001001000001",       "011000000011111000100111001001000001",       "011000000110111001010010010001000010", 
      "011000001001111010010101100001000010",       "011000001100111011110000111001000011",       "011000001111111101100100100001000011",       "011000010010111111110000010001000011", 
      "011000010110000010010100011001000100",       "011000011001000101010000111001000100",       "011000011100001000100101110001000100",       "011000011111001100010011001001000101", 
      "011000100010010000011000111001000101",       "011000100101010100110111001001000101",       "011000101000011001101110001001000110",       "011000101011011110111101101001000110", 
      "011000101110100100100101111001000111",       "011000110001101010100110110001000111",       "011000110100110001000000100001000111",       "011000110111110111110011000001001000", 
      "011000111010111110111110100001001000",       "011000111110000110100010111001001000",       "011001000001001110100000001001001001",       "011001000100010110110110100001001001", 
      "011001000111011111100101111001001010",       "011001001010101000101110011001001010",       "011001001101110010010000000001001010",       "011001010000111100001011000001001011", 
      "011001010100000110011111001001001011",       "011001010111010001001100101001001011",       "011001011010011100010011011001001100",       "011001011101100111110011101001001100", 
      "011001100000110011101101011001001101",       "011001100100000000000000101001001101",       "011001100111001100101101011001001101",       "011001101010011001110011111001001110", 
      "011001101101100111010011111001001110",       "011001110000110101001101101001001111",       "011001110100000011100001010001001111",       "011001110111010010001110101001001111", 
      "011001111010100001010101110001010000",       "011001111101110000110110111001010000",       "011010000001000000110010000001010001",       "011010000100010001000111001001010001", 
      "011010000111100001110110010001010001",       "011010001010110010111111101001010010",       "011010001110000100100011001001010010",       "011010010001010110100000110001010011", 
      "011010010100101000111000110001010011",       "011010010111111011101011000001010011",       "011010011011001110110111101001010100",       "011010011110100010011110110001010100", 
      "011010100001110110100000010001010101",       "011010100101001010111100011001010101",       "011010101000011111110011000001010101",       "011010101011110101000100011001010110", 
      "011010101111001010110000011001010110",       "011010110010100000110111000001010111",       "011010110101110111011000101001010111",       "011010111001001110010100111001010111", 
      "011010111100100101101100001001011000",       "011010111111111101011110011001011000",       "011011000011010101101011100001011001",       "011011000110101110010011110001011001", 
      "011011001010000111010111001001011001",       "011011001101100000110101101001011010",       "011011010000111010101111011001011010",       "011011010100010101000100011001011011", 
      "011011010111101111110100101001011011",       "011011011011001011000000011001011100",       "011011011110100110100111011001011100",       "011011100010000010101010000001011100", 
      "011011100101011111001000001001011101",       "011011101000111100000001110001011101",       "011011101100011001010111001001011110",       "011011101111110111001000001001011110", 
      "011011110011010101010100111001011111",       "011011110110110011111101100001011111",       "011011111010010011000010000001011111",       "011011111101110010100010010001100000", 
      "011100000001010010011110101001100000",       "011100000100110010110110111001100001",       "011100001000010011101011011001100001",       "011100001011110100111011111001100010", 
      "011100001111010110101000101001100010",       "011100010010111000110001100001100010",       "011100010110011011010110110001100011",       "011100011001111110011000011001100011", 
      "011100011101100001110110011001100100",       "011100100001000101110000111001100100",       "011100100100101010000111111001100101",       "011100101000001110111011011001100101", 
      "011100101011110100001011101001100110",       "011100101111011001111000100001100110",       "011100110011000000000010001001100110",       "011100110110100110101000100001100111", 
      "011100111010001101101011110001100111",       "011100111101110101001100000001101000",       "011101000001011101001001001001101000",       "011101000101000101100011010001101001", 
      "011101001000101110011010100001101001",       "011101001100010111101110111001101010",       "011101010000000001100000100001101010",       "011101010011101011101111010001101011", 
      "011101010111010110011011011001101011",       "011101011011000001100100111001101011",       "011101011110101101001011111001101100",       "011101100010011001010000010001101100", 
      "011101100110000101110010001001101101",       "011101101001110010110001101001101101",       "011101101101100000001110111001101110",       "011101110001001110001001110001101110", 
      "011101110100111100100010011001101111",       "011101111000101011011000111001101111",       "011101111100011010101101010001110000",       "011110000000001010011111101001110000", 
      "011110000011111010101111111001110001",       "011110000111101011011110011001110001",       "011110001011011100101010111001110010",       "011110001111001110010101100001110010", 
      "011110010011000000011110011001110010",       "011110010110110011000101101001110011",       "011110011010100110001011010001110011",       "011110011110011001101111010001110100", 
      "011110100010001101110001101001110100",       "011110100110000010010010101001110101",       "011110101001110111010010010001110101",       "011110101101101100110000100001110110", 
      "011110110001100010101101100001110110",       "011110110101011001001001010001110111",       "011110111001010000000011110001110111",       "011110111101000111011101010001111000", 
      "011111000000111111010101101001111000",       "011111000100110111101101001001111001",       "011111001000110000100011101001111001",       "011111001100101001111001010001111010", 
      "011111010000100011101110001001111010",       "011111010100011110000010010001111011",       "011111011000011000110101101001111011",       "011111011100010100001000100001111100", 
      "011111100000001111111010101001111100",       "011111100100001100001100100001111101",       "011111101000001000111101110001111101",       "011111101100000110001110110001111110", 
      "011111110000000011111111011001111110",       "011111110100000010001111110001111111",       "011111111000000000111111111001111111",       "011111111100000000010000000010000000" 
)
;
begin
          Y1 <= memVar(conv_integer(X1)); 
          Y2 <= memVar(conv_integer(X2)); 
end architecture;

--------------------------------------------------------------------------------
--                     FixRealKCM_M3_6_0_1_log_2_unsigned
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: 
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FixRealKCM_M3_6_0_1_log_2_unsigned is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(9 downto 0);
          R : out  std_logic_vector(7 downto 0)   );
end entity;

architecture arch of FixRealKCM_M3_6_0_1_log_2_unsigned is
   component FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0 is
      port ( -- OL clk, rst : in std_logic;
             X : in  std_logic_vector(5 downto 0);
             Y : out  std_logic_vector(7 downto 0)   );
   end component;

   component FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1 is
      port (-- OL  clk, rst : in std_logic;
             X : in  std_logic_vector(3 downto 0);
             Y : out  std_logic_vector(11 downto 0)   );
   end component;

   component IntAdder_12_f400_uid40 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(11 downto 0);
             Y : in  std_logic_vector(11 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(11 downto 0)   );
   end component;

signal d0 :  std_logic_vector(5 downto 0);
signal pp0 :  std_logic_vector(7 downto 0);
signal addOp0 :  std_logic_vector(11 downto 0);
signal d1 :  std_logic_vector(3 downto 0);
signal pp1 :  std_logic_vector(11 downto 0);
signal addOp1 :  std_logic_vector(11 downto 0);
signal OutRes :  std_logic_vector(11 downto 0);
constant zero : std_logic := '0';
attribute rom_extract: string;
attribute rom_style: string;
attribute rom_extract of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0: component is "yes";
attribute rom_extract of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1: component is "yes";
attribute rom_style of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0: component is "distributed";
attribute rom_style of FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1: component is "distributed";
begin
--   process(clk)
--      begin
--         if clk'event and clk = '1' then
--         end if;
--      end process;
   d0 <= X(5 downto 0);
   KCMTable_0: FixRealKCM_M3_6_0_1_log_2_unsigned_Table_0  -- pipelineDepth=0 maxInDelay=0
      port map (-- OL  clk  => clk,
                -- OL rst  => rst,
                 X => d0,
                 Y => pp0);
   addOp0 <= (11 downto 8 => '0') & pp0;
   d1 <= X(9 downto 6);
   KCMTable_1: FixRealKCM_M3_6_0_1_log_2_unsigned_Table_1  -- pipelineDepth=0 maxInDelay=0
      port map (-- OL clk  => clk,
                -- OL rst  => rst,
                 X => d1,
                 Y => pp1);
   addOp1 <= pp1;
   Result_Adder: IntAdder_12_f400_uid40  -- pipelineDepth=1 maxInDelay=1.80264e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 Cin => zero,
                 R => OutRes,
                 X => addOp0,
                 Y => addOp1);
   ----------------Synchro barrier, entering cycle 1----------------
   R <= OutRes(11 downto 4);
end architecture;

--------------------------------------------------------------------------------
--                 FixRealKCM_0_7_M26_log_2_unsigned_Table_0
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Florent de Dinechin (2007)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
entity FixRealKCM_0_7_M26_log_2_unsigned_Table_0 is
   port (-- OL  clk, rst : in std_logic;
          X : in  std_logic_vector(5 downto 0);
          Y : out  std_logic_vector(31 downto 0)   );
end entity;

architecture arch of FixRealKCM_0_7_M26_log_2_unsigned_Table_0 is
begin
  with X select  Y <= 
   "00000000000000000000000000000000" when "000000",
   "00000010110001011100100001100000" when "000001",
   "00000101100010111001000011000000" when "000010",
   "00001000010100010101100100100000" when "000011",
   "00001011000101110010000101111111" when "000100",
   "00001101110111001110100111011111" when "000101",
   "00010000101000101011001000111111" when "000110",
   "00010011011010000111101010011111" when "000111",
   "00010110001011100100001011111111" when "001000",
   "00011000111101000000101101011111" when "001001",
   "00011011101110011101001110111111" when "001010",
   "00011110011111111001110000011111" when "001011",
   "00100001010001010110010001111110" when "001100",
   "00100100000010110010110011011110" when "001101",
   "00100110110100001111010100111110" when "001110",
   "00101001100101101011110110011110" when "001111",
   "00101100010111001000010111111110" when "010000",
   "00101111001000100100111001011110" when "010001",
   "00110001111010000001011010111110" when "010010",
   "00110100101011011101111100011110" when "010011",
   "00110111011100111010011101111101" when "010100",
   "00111010001110010110111111011101" when "010101",
   "00111100111111110011100000111101" when "010110",
   "00111111110001010000000010011101" when "010111",
   "01000010100010101100100011111101" when "011000",
   "01000101010100001001000101011101" when "011001",
   "01001000000101100101100110111101" when "011010",
   "01001010110111000010001000011101" when "011011",
   "01001101101000011110101001111100" when "011100",
   "01010000011001111011001011011100" when "011101",
   "01010011001011010111101100111100" when "011110",
   "01010101111100110100001110011100" when "011111",
   "01011000101110010000101111111100" when "100000",
   "01011011011111101101010001011100" when "100001",
   "01011110010001001001110010111100" when "100010",
   "01100001000010100110010100011100" when "100011",
   "01100011110100000010110101111011" when "100100",
   "01100110100101011111010111011011" when "100101",
   "01101001010110111011111000111011" when "100110",
   "01101100001000011000011010011011" when "100111",
   "01101110111001110100111011111011" when "101000",
   "01110001101011010001011101011011" when "101001",
   "01110100011100101101111110111011" when "101010",
   "01110111001110001010100000011011" when "101011",
   "01111001111111100111000001111010" when "101100",
   "01111100110001000011100011011010" when "101101",
   "01111111100010100000000100111010" when "101110",
   "10000010010011111100100110011010" when "101111",
   "10000101000101011001000111111010" when "110000",
   "10000111110110110101101001011010" when "110001",
   "10001010101000010010001010111010" when "110010",
   "10001101011001101110101100011001" when "110011",
   "10010000001011001011001101111001" when "110100",
   "10010010111100100111101111011001" when "110101",
   "10010101101110000100010000111001" when "110110",
   "10011000011111100000110010011001" when "110111",
   "10011011010000111101010011111001" when "111000",
   "10011110000010011001110101011001" when "111001",
   "10100000110011110110010110111001" when "111010",
   "10100011100101010010111000011000" when "111011",
   "10100110010110101111011001111000" when "111100",
   "10101001001000001011111011011000" when "111101",
   "10101011111001101000011100111000" when "111110",
   "10101110101011000100111110011000" when "111111",
   "--------------------------------" when others;
end architecture;

--------------------------------------------------------------------------------
--                 FixRealKCM_0_7_M26_log_2_unsigned_Table_1
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Florent de Dinechin (2007)
--------------------------------------------------------------------------------
library ieee; 
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
entity FixRealKCM_0_7_M26_log_2_unsigned_Table_1 is
   port (-- OL clk, rst : in std_logic;
          X : in  std_logic_vector(1 downto 0);
          Y : out  std_logic_vector(33 downto 0)   );
end entity;

architecture arch of FixRealKCM_0_7_M26_log_2_unsigned_Table_1 is
begin
  with X select  Y <= 
   "0000000000000000000000000000000000" when "00",
   "0010110001011100100001011111111000" when "01",
   "0101100010111001000010111111110000" when "10",
   "1000010100010101100100011111100111" when "11",
   "----------------------------------" when others;
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_34_f400_uid49
--                     (IntAdderClassical_34_f400_uid51)
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

entity IntAdder_34_f400_uid49 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(33 downto 0);
          Y : in  std_logic_vector(33 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(33 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of IntAdder_34_f400_uid49 is
signal X_d1 :  std_logic_vector(33 downto 0);
signal Y_d1 :  std_logic_vector(33 downto 0);
signal Cin_d1 : std_logic;
signal NcA : STD_LOGIC;
signal NcB : STD_LOGIC;

begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            X_d1 <=  X;
            Y_d1 <=  Y;
            Cin_d1 <=  Cin;
           end if;
         end if;
      end process;

   --Classical
   ----------------Synchro barrier, entering cycle 1----------------
    R <= X_d1 + Y_d1 + Cin_d1;
NcA <= X_d1(26) and X_d1(27) and X_d1(28) and X_d1(29) and X_d1(30) and X_d1(31);
NcB <= Y_d1(26) and Y_d1(27) and Y_d1(28) and Y_d1(29) and Y_d1(30) and Y_d1(31) and Y_d1(32) and Y_d1(33);
Nc <= NcA and NcB;
end architecture;

--------------------------------------------------------------------------------
--                     FixRealKCM_0_7_M26_log_2_unsigned
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: 
--------------------------------------------------------------------------------
-- Pipeline depth: 1 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FixRealKCM_0_7_M26_log_2_unsigned is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(7 downto 0);
          R : out  std_logic_vector(33 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of FixRealKCM_0_7_M26_log_2_unsigned is
   component FixRealKCM_0_7_M26_log_2_unsigned_Table_0 is
      port (-- OL  clk, rst : in std_logic;
             X : in  std_logic_vector(5 downto 0);
             Y : out  std_logic_vector(31 downto 0)   );
   end component;

   component FixRealKCM_0_7_M26_log_2_unsigned_Table_1 is
      port (-- OL clk, rst : in std_logic;
             X : in  std_logic_vector(1 downto 0);
             Y : out  std_logic_vector(33 downto 0)   );
   end component;

   component IntAdder_34_f400_uid49 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(33 downto 0);
             Y : in  std_logic_vector(33 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(33 downto 0);
             Nc : out  std_logic   );
   end component;

signal d0 :  std_logic_vector(5 downto 0);
signal pp0 :  std_logic_vector(31 downto 0);
signal addOp0 :  std_logic_vector(33 downto 0);
signal d1 :  std_logic_vector(1 downto 0);
signal pp1 :  std_logic_vector(33 downto 0);
signal addOp1 :  std_logic_vector(33 downto 0);
signal OutRes :  std_logic_vector(33 downto 0);
constant zero : std_logic := '0';
attribute rom_extract: string;
attribute rom_style: string;
attribute rom_extract of FixRealKCM_0_7_M26_log_2_unsigned_Table_0: component is "yes";
attribute rom_extract of FixRealKCM_0_7_M26_log_2_unsigned_Table_1: component is "yes";
attribute rom_style of FixRealKCM_0_7_M26_log_2_unsigned_Table_0: component is "distributed";
attribute rom_style of FixRealKCM_0_7_M26_log_2_unsigned_Table_1: component is "distributed";
begin
-- OL   process(clk)
-- OL      begin
-- OL         if clk'event and clk = '1' then
-- OL         end if;
-- OL      end process;
   d0 <= X(5 downto 0);
   KCMTable_0: FixRealKCM_0_7_M26_log_2_unsigned_Table_0  -- pipelineDepth=0 maxInDelay=0
      port map (-- OL clk  => clk,
-- OL                 rst  => rst,
                 X => d0,
                 Y => pp0);
   addOp0 <= (33 downto 32 => '0') & pp0;
   d1 <= X(7 downto 6);
   KCMTable_1: FixRealKCM_0_7_M26_log_2_unsigned_Table_1  -- pipelineDepth=0 maxInDelay=0
      port map (-- OL clk  => clk,
-- OL                 rst  => rst,
                 X => d1,
                 Y => pp1);
   addOp1 <= pp1;
   Result_Adder: IntAdder_34_f400_uid49  -- pipelineDepth=1 maxInDelay=2.13744e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 Cin => zero,
                 R => OutRes,
                 X => addOp0,
                 Y => addOp1,
                 Nc => Nc);
   ----------------Synchro barrier, entering cycle 1----------------
   R <= OutRes(33 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                               FPExp_8_23_400
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: F. de Dinechin, Bogdan Pasca (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 14 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity FPExp_8_23_400 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OF          rst : in std_logic;
          X : in  std_logic_vector(8+23+2 downto 0);
          R : out  std_logic_vector(8+23+2 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of FPExp_8_23_400 is
   component FixRealKCM_0_7_M26_log_2_unsigned is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(7 downto 0);
             R : out  std_logic_vector(33 downto 0);
             Nc : out  std_logic   );
   end component;

   component FixRealKCM_M3_6_0_1_log_2_unsigned is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(9 downto 0);
             R : out  std_logic_vector(7 downto 0)   );
   end component;

   component IntAdder_18_f400_uid62 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(17 downto 0);
             Y : in  std_logic_vector(17 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(17 downto 0)   );
   end component;

   component IntAdder_18_f400_uid68 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(17 downto 0);
             Y : in  std_logic_vector(17 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(17 downto 0)   );
   end component;

   component IntAdder_26_f484_uid55 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OF        rst : in std_logic;
             X : in  std_logic_vector(25 downto 0);
             Y : in  std_logic_vector(25 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(25 downto 0)   );
   end component;

   component IntAdder_27_f400_uid78 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OF        rst : in std_logic;
             X : in  std_logic_vector(26 downto 0);
             Y : in  std_logic_vector(26 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(26 downto 0)   );
   end component;

   component IntAdder_33_f400_uid84 is
      port ( clk :  in std_logic;
             Enable : in std_logic;
-- OF        rst : in std_logic;
             X : in  std_logic_vector(32 downto 0);
             Y : in  std_logic_vector(32 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(32 downto 0)   );
   end component;

   component IntMultiplier_17_18_unsigned_uid74 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL , rst : in std_logic;
             X : in  std_logic_vector(16 downto 0);
             Y : in  std_logic_vector(17 downto 0);
             R : out  std_logic_vector(34 downto 0);
             Nc : out  std_logic   );
   end component;

   component LeftShifter_24_by_max_33_uid35 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(23 downto 0);
             S : in  std_logic_vector(5 downto 0);
             R : out  std_logic_vector(56 downto 0)   );
   end component;

   component MagicSPExpTable is
      port ( X1 : in  std_logic_vector(8 downto 0);
             Y1 : out  std_logic_vector(35 downto 0);
             X2 : in  std_logic_vector(8 downto 0);
             Y2 : out  std_logic_vector(35 downto 0)   );
   end component;

signal Xexn, Xexn_d1, Xexn_d2, Xexn_d3, Xexn_d4, Xexn_d5, Xexn_d6, Xexn_d7, Xexn_d8, Xexn_d9, Xexn_d10, Xexn_d11, Xexn_d12, Xexn_d13, Xexn_d14 :  std_logic_vector(1 downto 0);
signal XSign, XSign_d1, XSign_d2, XSign_d3, XSign_d4, XSign_d5, XSign_d6, XSign_d7, XSign_d8, XSign_d9, XSign_d10, XSign_d11, XSign_d12, XSign_d13, XSign_d14 : std_logic;
signal XexpField :  std_logic_vector(7 downto 0);
signal Xfrac :  std_logic_vector(22 downto 0);
signal e0 :  std_logic_vector(9 downto 0);
signal shiftVal, shiftVal_d1 :  std_logic_vector(9 downto 0);
signal resultWillBeOne, resultWillBeOne_d1, resultWillBeOne_d2 : std_logic;
signal mXu :  std_logic_vector(23 downto 0);
signal oufl0, oufl0_d1, oufl0_d2, oufl0_d3, oufl0_d4, oufl0_d5, oufl0_d6, oufl0_d7, oufl0_d8, oufl0_d9, oufl0_d10, oufl0_d11, oufl0_d12, oufl0_d13 : std_logic;
signal shiftValIn :  std_logic_vector(5 downto 0);
signal fixX0, fixX0_d1 :  std_logic_vector(56 downto 0);
signal fixX, fixX_d1, fixX_d2 :  std_logic_vector(33 downto 0);
signal xMulIn :  std_logic_vector(9 downto 0);
signal absK, absK_d1 :  std_logic_vector(7 downto 0);
signal minusAbsK :  std_logic_vector(8 downto 0);
signal K, K_d1, K_d2, K_d3, K_d4, K_d5, K_d6, K_d7, K_d8, K_d9 :  std_logic_vector(8 downto 0);
signal absKLog2 :  std_logic_vector(33 downto 0);
signal subOp1 :  std_logic_vector(25 downto 0);
signal subOp2 :  std_logic_vector(25 downto 0);
signal Y :  std_logic_vector(25 downto 0);
signal Addr1, Addr1_d1 :  std_logic_vector(8 downto 0);
signal Z, Z_d1 :  std_logic_vector(16 downto 0);
signal Addr2, Addr2_d1 :  std_logic_vector(8 downto 0);
signal lowerTerm0 :  std_logic_vector(35 downto 0);
signal expA0 :  std_logic_vector(35 downto 0);
signal expA, expA_d1, expA_d2, expA_d3, expA_d4 :  std_logic_vector(26 downto 0);
signal expZmZm1_0 :  std_logic_vector(8 downto 0);
signal expZmZm1 :  std_logic_vector(8 downto 0);
signal expZminus1X :  std_logic_vector(17 downto 0);
signal expZminus1Y :  std_logic_vector(17 downto 0);
signal expZminus1 :  std_logic_vector(17 downto 0);
signal expArounded0 :  std_logic_vector(17 downto 0);
signal expArounded :  std_logic_vector(16 downto 0);
signal lowerProduct :  std_logic_vector(34 downto 0);
signal extendedLowerProduct :  std_logic_vector(26 downto 0);
signal expY, expY_d1 :  std_logic_vector(26 downto 0);
signal needNoNorm, needNoNorm_d1 : std_logic;
signal preRoundBiasSig :  std_logic_vector(32 downto 0);
signal roundBit : std_logic;
signal roundNormAddend :  std_logic_vector(32 downto 0);
signal roundedExpSigRes :  std_logic_vector(32 downto 0);
signal roundedExpSig :  std_logic_vector(32 downto 0);
signal ofl1 : std_logic;
signal ofl2 : std_logic;
signal ofl3 : std_logic;
signal ofl : std_logic;
signal ufl1 : std_logic;
signal ufl2 : std_logic;
signal ufl3 : std_logic;
signal ufl : std_logic;
signal Rexn :  std_logic_vector(1 downto 0);

signal Tmp :  std_logic_vector(33 downto 0);
signal NcA : STD_LOGIC;
signal NcB : STD_LOGIC;
signal NcC : STD_LOGIC;

constant g: positive := 3;
constant wE: positive := 8;
constant wF: positive := 23;
constant wFIn: positive := 23;
constant One : STD_LOGIC := '1';
begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            Xexn_d1 <=  Xexn;
            Xexn_d2 <=  Xexn_d1;
            Xexn_d3 <=  Xexn_d2;
            Xexn_d4 <=  Xexn_d3;
            Xexn_d5 <=  Xexn_d4;
            Xexn_d6 <=  Xexn_d5;
            Xexn_d7 <=  Xexn_d6;
            Xexn_d8 <=  Xexn_d7;
            Xexn_d9 <=  Xexn_d8;
            Xexn_d10 <=  Xexn_d9;
            Xexn_d11 <=  Xexn_d10;
            Xexn_d12 <=  Xexn_d11;
            Xexn_d13 <=  Xexn_d12;
            Xexn_d14 <=  Xexn_d13;
            XSign_d1 <=  XSign;
            XSign_d2 <=  XSign_d1;
            XSign_d3 <=  XSign_d2;
            XSign_d4 <=  XSign_d3;
            XSign_d5 <=  XSign_d4;
            XSign_d6 <=  XSign_d5;
            XSign_d7 <=  XSign_d6;
            XSign_d8 <=  XSign_d7;
            XSign_d9 <=  XSign_d8;
            XSign_d10 <=  XSign_d9;
            XSign_d11 <=  XSign_d10;
            XSign_d12 <=  XSign_d11;
            XSign_d13 <=  XSign_d12;
            XSign_d14 <=  XSign_d13;
            shiftVal_d1 <=  shiftVal;
            resultWillBeOne_d1 <=  resultWillBeOne;
            resultWillBeOne_d2 <=  resultWillBeOne_d1;
            oufl0_d1 <=  oufl0;
            oufl0_d2 <=  oufl0_d1;
            oufl0_d3 <=  oufl0_d2;
            oufl0_d4 <=  oufl0_d3;
            oufl0_d5 <=  oufl0_d4;
            oufl0_d6 <=  oufl0_d5;
            oufl0_d7 <=  oufl0_d6;
            oufl0_d8 <=  oufl0_d7;
            oufl0_d9 <=  oufl0_d8;
            oufl0_d10 <=  oufl0_d9;
            oufl0_d11 <=  oufl0_d10;
            oufl0_d12 <=  oufl0_d11;
            oufl0_d13 <=  oufl0_d12;
            fixX0_d1 <=  fixX0;
            fixX_d1 <=  fixX;
            fixX_d2 <=  fixX_d1;
            absK_d1 <=  absK;
            K_d1 <=  K;
            K_d2 <=  K_d1;
            K_d3 <=  K_d2;
            K_d4 <=  K_d3;
            K_d5 <=  K_d4;
            K_d6 <=  K_d5;
            K_d7 <=  K_d6;
            K_d8 <=  K_d7;
            K_d9 <=  K_d8;
            Addr1_d1 <=  Addr1;
            Z_d1 <=  Z;
            Addr2_d1 <=  Addr2;
            expA_d1 <=  expA;
            expA_d2 <=  expA_d1;
            expA_d3 <=  expA_d2;
            expA_d4 <=  expA_d3;
            expY_d1 <=  expY;
            needNoNorm_d1 <=  needNoNorm;
           end if;
         end if;
      end process;
   Xexn <= X(wE+wFIn+2 downto wE+wFIn+1);
   XSign <= X(wE+wFIn);
   XexpField <= X(wE+wFIn-1 downto wFIn);
   Xfrac <= X(wFIn-1 downto 0);
   e0 <= conv_std_logic_vector(101, wE+2);  -- bias - (wF+g)
   shiftVal <= ("00" & XexpField) - e0; -- for a left shift
   -- underflow when input is shifted to zero (shiftval<0), in which case exp = 1
   resultWillBeOne <= shiftVal(wE+1);
   --  mantissa with implicit bit
   mXu <= "1" & Xfrac;
   -- Partial overflow/underflow detection
   ----------------Synchro barrier, entering cycle 1----------------
   oufl0 <= not shiftVal_d1(wE+1) when shiftVal_d1(wE downto 0) >= conv_std_logic_vector(33, wE+1) else '0';
   ---------------- cycle 0----------------
   shiftValIn <= shiftVal(5 downto 0);
   mantissa_shift: LeftShifter_24_by_max_33_uid35  -- pipelineDepth=1 maxInDelay=2.43272e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                  rst  => rst,
                 R => fixX0,
                 S => shiftValIn,
                 X => mXu);
   ----------------Synchro barrier, entering cycle 1----------------
   ----------------Synchro barrier, entering cycle 2----------------
   Tmp  <=  (33 downto 0 => not(resultWillBeOne_d2));
   fixX <=  fixX0_d1(56 downto 23) and Tmp;
--   fixX <=  fixX0_d1(56 downto 23) and (33 downto 0 => not(resultWillBeOne_d2));
   xMulIn <=  fixX(32 downto 23); -- truncation, error 2^-3
   mulInvLog2: FixRealKCM_M3_6_0_1_log_2_unsigned  -- pipelineDepth=1 maxInDelay=1.27192e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => absK,
                 X => xMulIn);
   ----------------Synchro barrier, entering cycle 3----------------
   ----------------Synchro barrier, entering cycle 4----------------
   minusAbsK <= (8 downto 0 => '0') - ('0' & absK_d1);
   K <= minusAbsK when  XSign_d4='1'   else ('0' & absK_d1);
   ---------------- cycle 3----------------
   mulLog2: FixRealKCM_0_7_M26_log_2_unsigned  -- pipelineDepth=1 maxInDelay=1.60672e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => absKLog2,
                 X => absK,
                 Nc => NcC);
   ----------------Synchro barrier, entering cycle 4----------------
   subOp1 <= fixX_d2(25 downto 0) when XSign_d4='0' else not (fixX_d2(25 downto 0));
   subOp2 <= absKLog2(25 downto 0) when XSign_d4='1' else not (absKLog2(25 downto 0));
   theYAdder: IntAdder_26_f484_uid55  -- pipelineDepth=2 maxInDelay=2.42544e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OF                  rst  => rst,
                 Cin => One,
                 R => Y,
                 X => subOp1,
                 Y => subOp2);

   ----------------Synchro barrier, entering cycle 6----------------
   -- Now compute the exp of this fixed-point value
   Addr1 <= Y(25 downto 17);
   Z <= Y(16 downto 0);
   Addr2 <= Z(16 downto 8);
   ----------------Synchro barrier, entering cycle 7----------------
   table: MagicSPExpTable
      port map ( X1 => Addr1_d1,
                 X2 => Addr2_d1,
                 Y1 => expA0,
                 Y2 => lowerTerm0);
   expA <=  expA0(35 downto 9);
   expZmZm1_0 <= lowerTerm0(8 downto 0);
   expZmZm1 <= expZmZm1_0(8 downto 0); 
   -- Computing Z + (exp(Z)-1-Z)
   expZminus1X <= '0' & Z_d1;
   expZminus1Y <= (17 downto 9 => '0') & expZmZm1 ;
   Adder_expZminus1: IntAdder_18_f400_uid62  -- pipelineDepth=1 maxInDelay=2.19472e-09
      port map ( clk  => clk,
                 Enable => Enable,
--                  rst  => rst,
                 Cin =>  '0' ,
                 R => expZminus1,
                 X => expZminus1X,
                 Y => expZminus1Y);
   ----------------Synchro barrier, entering cycle 8----------------
   -- Truncating expA to the same accuracy as expZminus1
   ---------------- cycle 7----------------
   Adder_expArounded0: IntAdder_18_f400_uid68  -- pipelineDepth=1 maxInDelay=2.186e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                  rst  => rst,
                 Cin =>  '1' ,
                 R => expArounded0,
                 X => expA(26 downto 9),
                 Y => "000000000000000000");
   ----------------Synchro barrier, entering cycle 8----------------
   expArounded <= expArounded0(17 downto 1);
   TheLowerProduct: IntMultiplier_17_18_unsigned_uid74  -- pipelineDepth=3 maxInDelay=1.518e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => lowerProduct,
                 X => expArounded,
                 Y => expZminus1,
                 Nc => NcA);

   ----------------Synchro barrier, entering cycle 11----------------
   -- Final addition -- the product MSB bit weight is -k+2 = -7
   extendedLowerProduct <= ((26 downto 19 => '0') & lowerProduct(34 downto 16));
   TheFinalAdder: IntAdder_27_f400_uid78  -- pipelineDepth=1 maxInDelay=1.55172e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OF                 rst  => rst,
                 Cin => '0',
                 R => expY,
                 X => expA_d4,
                 Y => extendedLowerProduct);

   ----------------Synchro barrier, entering cycle 12----------------
   needNoNorm <= expY(26);
   ----------------Synchro barrier, entering cycle 13----------------
   -- Rounding: all this should consume one row of LUTs
   preRoundBiasSig <= conv_std_logic_vector(127, wE+2)  & expY_d1(25 downto 3) when needNoNorm_d1 = '1'
      else conv_std_logic_vector(126, wE+2)  & expY_d1(24 downto 2) ;
   roundBit <= expY_d1(2)  when needNoNorm_d1 = '1'    else expY_d1(1) ;
   roundNormAddend <= K_d9(8) & K_d9 & (22 downto 1 => '0') & roundBit;
   roundedExpSigOperandAdder: IntAdder_33_f400_uid84  -- pipelineDepth=1 maxInDelay=1.25448e-09
      port map ( clk  => clk,
                 Enable => Enable,
-- OF                 rst  => rst,
                 Cin => '0',
                 R => roundedExpSigRes,
                 X => preRoundBiasSig,
                 Y => roundNormAddend);

   ----------------Synchro barrier, entering cycle 14----------------
   -- delay at adder output is 8.52e-10
   roundedExpSig <= roundedExpSigRes when Xexn_d14="01" else  "000" & (wE-2 downto 0 => '1') & (wF-1 downto 0 => '0');
   ofl1 <= not XSign_d14 and oufl0_d13 and (not Xexn_d14(1) and Xexn_d14(0)); -- input positive, normal,  very large
   ofl2 <= not XSign_d14 and (roundedExpSig(wE+wF) and not roundedExpSig(wE+wF+1)) and (not Xexn_d14(1) and Xexn_d14(0)); -- input positive, normal, overflowed
   ofl3 <= not XSign_d14 and Xexn_d14(1) and not Xexn_d14(0);  -- input was -infty
   ofl <= ofl1 or ofl2 or ofl3;
   ufl1 <= (roundedExpSig(wE+wF) and roundedExpSig(wE+wF+1))  and (not Xexn_d14(1) and Xexn_d14(0)); -- input normal
   ufl2 <= XSign_d14 and Xexn_d14(1) and not Xexn_d14(0);  -- input was -infty
   ufl3 <= XSign_d14 and oufl0_d13  and (not Xexn_d14(1) and Xexn_d14(0)); -- input negative, normal,  very large
   ufl <= ufl1 or ufl2 or ufl3;
   Rexn <= "11" when Xexn_d14 = "11"
      else "10" when ofl='1'
      else "00" when ufl='1'
      else "01";
   R <= Rexn & '0' & roundedExpSig(30 downto 0);

NcB <= fixX_d1(26) and fixX_d1(27) and fixX_d1(28) and fixX_d1(29) and fixX_d1(30) and fixX_d1(31) and fixX_d1(32) and fixX_d1(33) and fixX0_d1(56);
Nc <= NcA and NcB and NcC;
end architecture;

--------------------------------------------------------------------------------
--                                  InitLoop
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: ADACSYS Co, 2013
--------------------------------------------------------------------------------
-- Pipeline depth: 41 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity InitLoop is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OF          rst : in std_logic;
          tempvdt : in  std_logic_vector(8+23+2 downto 0);
          S_0 : in  std_logic_vector(8+23+2 downto 0);
          k : in  std_logic_vector(8+23+2 downto 0);
          tempsteps : in  std_logic_vector(8+23+2 downto 0);
          K_min_stim : in  std_logic_vector(8+23+2 downto 0);
          S_k : out  std_logic_vector(8+23+2 downto 0);
          V_k_call : out  std_logic_vector(8+23+2 downto 0);
          V_k_put : out  std_logic_vector(8+23+2 downto 0);
--          Db_resInterm1 : out  std_logic_vector(31 downto 0);
--          Db_resInterm2 : out  std_logic_vector(31 downto 0);
--          Db_resInterm3 : out  std_logic_vector(31 downto 0);
--          Db_S_k_comp   : out  std_logic_vector(31 downto 0)
          Nc : out std_logic
          );
end entity;

architecture arch of InitLoop is
   component FPAdderDualPath_8_23_8_23_8_23400 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OF        rst : in std_logic;
             X : in  std_logic_vector(8+23+2 downto 0);
             Y : in  std_logic_vector(8+23+2 downto 0);
             R : out  std_logic_vector(8+23+2 downto 0);
             Nc : out  std_logic );
   end component;

   component FPExp_8_23_400 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OF             rst : in std_logic;
             X : in  std_logic_vector(8+23+2 downto 0);
             R : out  std_logic_vector(8+23+2 downto 0);
             Nc : out  std_logic   );
   end component;

   component FPMultiplier_8_23_8_23_8_23_uid21 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(8+23+2 downto 0);
             Y : in  std_logic_vector(8+23+2 downto 0);
             R : out  std_logic_vector(8+23+2 downto 0);
             Nc : out  std_logic   );
   end component;

   component FPMultiplier_8_23_8_23_8_23_uid90 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL        rst : in std_logic;
             X : in  std_logic_vector(8+23+2 downto 0);
             Y : in  std_logic_vector(8+23+2 downto 0);
             R : out  std_logic_vector(8+23+2 downto 0);
             Nc : out  std_logic   );
   end component;

signal resInterm1 :  std_logic_vector(33 downto 0);
signal resInterm2 :  std_logic_vector(33 downto 0);
signal resInterm3, resInterm3_d1 :  std_logic_vector(33 downto 0);
signal S_k_comp, S_k_comp_d1, S_k_comp_d2, S_k_comp_d3, S_k_comp_d4, S_k_comp_d5, S_k_comp_d6, S_k_comp_d7, S_k_comp_d8, S_k_comp_d9 :  std_logic_vector(33 downto 0);
signal unmaxed_value_call :  std_logic_vector(33 downto 0);
signal S_0_d1, S_0_d2, S_0_d3, S_0_d4, S_0_d5, S_0_d6, S_0_d7, S_0_d8, S_0_d9, S_0_d10, S_0_d11, S_0_d12, S_0_d13, S_0_d14, S_0_d15, S_0_d16, S_0_d17, S_0_d18, S_0_d19, S_0_d20, S_0_d21, S_0_d22, S_0_d23, S_0_d24, S_0_d25, S_0_d26, S_0_d27, S_0_d28 :  std_logic_vector(8+23+2 downto 0);
-- OL signal k_d1, k_d2, k_d3, k_d4, k_d5, k_d6, k_d7, k_d8, k_d9 :  std_logic_vector(8+23+2 downto 0);
signal K_min_stim_d1, K_min_stim_d2, K_min_stim_d3, K_min_stim_d4, K_min_stim_d5, K_min_stim_d6, K_min_stim_d7, K_min_stim_d8, K_min_stim_d9, K_min_stim_d10, K_min_stim_d11, K_min_stim_d12, K_min_stim_d13, K_min_stim_d14, K_min_stim_d15, K_min_stim_d16, K_min_stim_d17, K_min_stim_d18, K_min_stim_d19, K_min_stim_d20, K_min_stim_d21, K_min_stim_d22, K_min_stim_d23, K_min_stim_d24, K_min_stim_d25, K_min_stim_d26, K_min_stim_d27, K_min_stim_d28, K_min_stim_d29, K_min_stim_d30, K_min_stim_d31, K_min_stim_d32 :  std_logic_vector(8+23+2 downto 0);

signal NcA : STD_LOGIC;
signal NcB : STD_LOGIC;
signal NcC : STD_LOGIC;
signal NcD : STD_LOGIC;
signal NcE : STD_LOGIC;
--signal NcSupA : STD_LOGIC;

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
-- OL           k_d1 <=  k;
-- OL           k_d2 <=  k_d1;
-- OL           k_d3 <=  k_d2;
-- OL           k_d4 <=  k_d3;
-- OL           k_d5 <=  k_d4;
-- OL           k_d6 <=  k_d5;
-- OL           k_d7 <=  k_d6;
-- OL           k_d8 <=  k_d7;
-- OL           k_d9 <=  k_d8;
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
           end if;
         end if;
      end process;
   fAdd: FPAdderDualPath_8_23_8_23_8_23400  -- pipelineDepth=9 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OF                 rst  => rst,
                 R => resInterm1,
                 X => k,
                 Y => tempsteps,
                 Nc => NcB);
   ----------------Synchro barrier, entering cycle 9----------------
   multDt: FPMultiplier_8_23_8_23_8_23_uid21  -- pipelineDepth=4 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                  rst  => rst,
                 R => resInterm2,
                 X => resInterm1,
                 Y => tempvdt,
                 Nc => NcA);
--                 Y => k_d9);
   ----------------Synchro barrier, entering cycle 13----------------
   Inst_resInterm3: FPExp_8_23_400  -- pipelineDepth=14 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
--  OF                 rst  => rst,
                 R => resInterm3,
                 X => resInterm2,
                 Nc => NcD);
   ----------------Synchro barrier, entering cycle 27----------------
   ----------------Synchro barrier, entering cycle 28----------------
   multExp: FPMultiplier_8_23_8_23_8_23_uid90  -- pipelineDepth=4 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                  rst  => rst,
                 R => S_k_comp,
                 X => resInterm3_d1,
                 Y => S_0_d28,
                 Nc => NcE);
   ----------------Synchro barrier, entering cycle 32----------------
   fAdd2: FPAdderDualPath_8_23_8_23_8_23400  -- pipelineDepth=9 maxInDelay=0
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => unmaxed_value_call,
                 X => K_min_stim_d32,
                 Y => S_k_comp,
                 Nc => NcC);
   ----------------Synchro barrier, entering cycle 41----------------
S_k <= S_k_comp_d9;
V_k_call <= unmaxed_value_call when unmaxed_value_call(31)='0'
                               else (others=>'0');
V_k_put <= "000"&unmaxed_value_call(30 downto 0) when unmaxed_value_call(31)='1'
                               else (others=>'0');

--NcSupA <= exc_d4(0) and exc_d4(1);
Nc <= ((NcA or NcB or NcC or NcE) xor NcD) and resInterm2(32) and resInterm2(33); -- and NcSupA;
--Db_resInterm1 <= resInterm1(31 downto 0) ;
--Db_resInterm2 <= resInterm2(31 downto 0) ;
--Db_resInterm3 <= resInterm3(31 downto 0) ;
--Db_S_k_comp   <= S_k_comp(31 downto 0)   ;
end architecture;

