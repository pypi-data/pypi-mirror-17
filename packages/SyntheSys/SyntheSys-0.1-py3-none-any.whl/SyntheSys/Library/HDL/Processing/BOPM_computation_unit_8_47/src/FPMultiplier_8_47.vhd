--------------------------------------------------------------------------------
--                           IntAdder_96_f400_uid9
--                     (IntAdderClassical_96_f400_uid11)
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

entity IntAdder_96_f400_uid9 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL          rst : in std_logic;
          X : in  std_logic_vector(95 downto 0);
          Y : in  std_logic_vector(95 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(95 downto 0)   );
end entity;

architecture arch of IntAdder_96_f400_uid9 is
signal x0 :  std_logic_vector(39 downto 0);
signal y0 :  std_logic_vector(39 downto 0);
signal x1, x1_d1 :  std_logic_vector(41 downto 0);
signal y1, y1_d1 :  std_logic_vector(41 downto 0);
signal x2, x2_d1, x2_d2 :  std_logic_vector(13 downto 0);
signal y2, y2_d1, y2_d2 :  std_logic_vector(13 downto 0);
signal sum0, sum0_d1, sum0_d2 :  std_logic_vector(40 downto 0);
signal sum1, sum1_d1 :  std_logic_vector(42 downto 0);
signal sum2 :  std_logic_vector(14 downto 0);
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
   x0 <= X(39 downto 0);
   y0 <= Y(39 downto 0);
   x1 <= X(81 downto 40);
   y1 <= Y(81 downto 40);
   x2 <= X(95 downto 82);
   y2 <= Y(95 downto 82);
   sum0 <= ( "0" & x0) + ( "0" & y0)  + Cin;
   ----------------Synchro barrier, entering cycle 1----------------
   sum1 <= ( "0" & x1_d1) + ( "0" & y1_d1)  + sum0_d1(40);
   ----------------Synchro barrier, entering cycle 2----------------
   sum2 <= ( "0" & x2_d2) + ( "0" & y2_d2)  + sum1_d1(42);
   R <= sum2(13 downto 0) & sum1_d1(41 downto 0) & sum0_d2(39 downto 0);
end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_96_f400_uid9_oli
--                     (IntAdderClassical_96_f400_uid11)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca, Florent de Dinechin (2008-2010)
--------------------------------------------------------------------------------
-- Pipeline depth: 2 cycles

--library ieee;
--use ieee.std_logic_1164.all;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_unsigned.all;
--library std;
--use std.textio.all;
--library work;


--entity IntAdder_96_f400_uid9_oli is
--       port ( 
--            clk    : in  STD_LOGIC                    ;
--            rst    : in  STD_LOGIC                    ;
--            DvAdd  : in  STD_LOGIC                    ;
--
--            X      : in  STD_LOGIC_VECTOR(95 downto 0);
 --           Y      : in  STD_LOGIC_VECTOR(95 downto 0);
--            Cin    : in  STD_LOGIC                    ;
--            R      : out STD_LOGIC_VECTOR(95 downto 0);
--            Busy_o : out STD_LOGIC
--            );
--end entity;

--architecture arch of IntAdder_96_f400_uid9_oli is

--signal MemoDataX : STD_LOGIC_VECTOR(55 downto 0) ;
--signal MemoDataY : STD_LOGIC_VECTOR(55 downto 0) ;

--signal x0        : STD_LOGIC_VECTOR(39 downto 0) ;
--signal y0        : STD_LOGIC_VECTOR(39 downto 0) ;
--signal x1        : STD_LOGIC_VECTOR(41 downto 0) ;
--signal y1        : STD_LOGIC_VECTOR(41 downto 0) ;
--signal x2        : STD_LOGIC_VECTOR(13 downto 0) ;
--signal y2        : STD_LOGIC_VECTOR(13 downto 0) ;
--signal sum0      : STD_LOGIC_VECTOR(42 downto 0) ;
--signal sum1      : STD_LOGIC_VECTOR(42 downto 0) ;
--signal sum2      : STD_LOGIC_VECTOR(42 downto 0) ;
--signal Slct      : STD_LOGIC_VECTOR(1  downto 0) ;

--signal OpCal     : STD_LOGIC_VECTOR(42 downto 0) ;
--signal Radd      : STD_LOGIC_VECTOR(42 downto 0) ;
--signal CalAdd    : STD_LOGIC                     ;

--signal SumRs0    : STD_LOGIC_VECTOR(39 downto 0) ;
--signal SumRs1    : STD_LOGIC_VECTOR(41 downto 0) ;

--begin

--x0 <= X(39 downto  0);
--y0 <= Y(39 downto  0);
--x1 <= X(41 downto  0);
--y1 <= Y(41 downto  0);
--x2 <= X(55 downto 42);
--y2 <= Y(55 downto 42);

--   sum0  <= ( "000" &    x0) + ( "000" &    y0)  + Cin     ;
--   sum1  <= ( "0"  & MemoDataX(41 downto 0)) + ( "0"  & MemoDataX(41 downto 0))  + Radd(40);
--   sum2  <= ( '0' & X"0000000"  & MemoDataY(55 downto 42)) + ( '0' & X"0000000" & MemoDataY(55 downto 42))  + Radd(42);
--
--   OpCal <= sum1 when (Slct = "01") else
--            sum2 when (Slct = "10") else sum0;
--
--   CalAdd <= DvAdd or Slct(1) or Slct(0);
            
--Additionneur : process(clk, rst)
--  begin
--    if(rst = '0') then 
--              Radd   <= (others => '0') ;
--              Slct   <= (others => '0') ;
--              Busy_o <= '0'             ;
--
--      elsif clk'event and clk = '1' then
--        if(CalAdd = '1') then
--              Radd <= OpCal             ;
--              Slct <= Slct(0) & DvAdd   ;
--              Busy_o <= '1'             ;
--
--          else
--              Radd   <= (others => '0') ;
--              Slct   <= (others => '0') ;
---              Busy_o <= '0'             ;
--
--        end if;
--    end if;
--end process Additionneur;

--Memo : process(clk, rst)
--  begin
--    if(rst = '0') then
--              MemoDataX <= (others => '0') ;
--              MemoDataY <= (others => '0') ;
--
--      elsif clk'event and clk = '1' then
--        if(DvAdd = '1') then
--              MemoDataX <= X(95 downto 40) ;
--              MemoDataY <= Y(95 downto 40) ;
--      
--        end if;
--     end if;
--end process Memo;

--MemResult : process(clk, rst)
--  begin
--    if(rst = '0') then
--              SumRs0 <= (others => '0')   ;
-- -             SumRs1 <= (others => '0')   ;
--
--      elsif clk'event and clk = '1' then
--        if(Slct(0) = '1') then
--              SumRs0 <= Radd(39 downto 0) ;
--              SumRs1 <= (others => '0')   ;
-- 
--          elsif(Slct(1) = '1') then
--              SumRs0 <= SumRs0            ;
--              SumRs1 <= Radd(41 downto 0) ;
--
--        end if;
--     end if;
--end process MemResult;

--   R <= Radd(13 downto 0) & SumRs1 & SumRs0;

--end architecture;

--------------------------------------------------------------------------------
--                       IntMultiAdder_96_op2_f400_uid5
--                       (IntCompressorTree_96_2_uid7)
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Bogdan Pasca (2009-2011)
--------------------------------------------------------------------------------
-- Pipeline depth: 2 cycles

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
library std;
use std.textio.all;
library work;

entity IntMultiAdder_96_op2_f400_uid5 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL         rst : in std_logic;
          X0 : in  std_logic_vector(95 downto 0);
          X1 : in  std_logic_vector(95 downto 0);
          R : out  std_logic_vector(95 downto 0)   );
end entity;

architecture arch of IntMultiAdder_96_op2_f400_uid5 is

--   component IntAdder_96_f400_uid9_oli is
--      port ( clk : in std_logic;
--             rst : in std_logic;
--             DvAdd  : in  STD_LOGIC                    ;
--
--             X : in  std_logic_vector(95 downto 0);
--             Y : in  std_logic_vector(95 downto 0);
--             Cin : in std_logic;
--             R : out  std_logic_vector(95 downto 0);
--             Busy_o : out STD_LOGIC
--             );
--   end component;

   component IntAdder_96_f400_uid9 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL             rst : in std_logic;
             X : in  std_logic_vector(95 downto 0);
             Y : in  std_logic_vector(95 downto 0);
             Cin : in std_logic;
             R : out  std_logic_vector(95 downto 0)   );
   end component;


signal l_0_s_0 :  std_logic_vector(95 downto 0);
signal l_0_s_1 :  std_logic_vector(95 downto 0);
signal myR :  std_logic_vector(95 downto 0);
signal BBB :  std_logic ;
constant Cvar : std_logic := '0' ;

begin
--   process(clk)
--      begin
--         if clk'event and clk = '1' then
--         end if;
--      end process;
   l_0_s_0 <= X0;
   l_0_s_1 <= X1;
   FinalAdder_CompressorTree: IntAdder_96_f400_uid9  -- pipelineDepth=2 maxInDelay=8.8944e-10
      port map ( clk  => clk,
                 Enable => Enable,
-- OL                 rst  => X1(1),
                 Cin => Cvar,
                 R => myR,
                 X => l_0_s_0,
                 Y => l_0_s_1);

   ----------------Synchro barrier, entering cycle 2----------------
   R <= myR;
 -- delay at adder output 9.9e-10
end architecture;

--------------------------------------------------------------------------------
--                    IntTruncMultiplier_48_48_96_unsigned
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Sebastian Banescu, Bogdan Pasca, Radu Tudoran (2010-2011)
--------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_signed.all;
library work;
entity IntTruncMultiplier_48_48_96_unsigned is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL          rst : in std_logic;
          X : in  std_logic_vector(47 downto 0);
          Y : in  std_logic_vector(47 downto 0);
          R : out  std_logic_vector(95 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of IntTruncMultiplier_48_48_96_unsigned is
   component IntMultiAdder_96_op2_f400_uid5 is
      port ( clk : in std_logic;
             Enable :in std_logic;
-- OL             rst : in std_logic;
             X0 : in  std_logic_vector(95 downto 0);
             X1 : in  std_logic_vector(95 downto 0);
             R : out  std_logic_vector(95 downto 0) );
   end component;

signal x0_0 :  std_logic_vector(17 downto 0);
signal y0_0 :  std_logic_vector(24 downto 0);
signal pxy00, pxy00_d1, pxy00_d2, pxy00_d3 :  std_logic_vector(42 downto 0);
-- OL signal x0_1, x0_1_d1 :  std_logic_vector(17 downto 0);
-- OL signal y0_1, y0_1_d1 :  std_logic_vector(24 downto 0);
signal x0_1, x0_1_d1 :  std_logic_vector(16 downto 0);
signal y0_1, y0_1_d1 :  std_logic_vector(23 downto 0);
signal txy01 :  std_logic_vector(42 downto 0);
signal pxy01, pxy01_d1, pxy01_d2 :  std_logic_vector(42 downto 0);
signal x0_2, x0_2_d1, x0_2_d2 :  std_logic_vector(16 downto 0);
signal y0_2, y0_2_d1, y0_2_d2 :  std_logic_vector(23 downto 0);
signal txy02 :  std_logic_vector(42 downto 0);
signal pxy02, pxy02_d1 :  std_logic_vector(42 downto 0);
signal addOpDSP0 :  std_logic_vector(95 downto 0);
signal x2_0 :  std_logic_vector(16 downto 0);
signal y2_0 :  std_logic_vector(23 downto 0);
signal pxy20, pxy20_d1, pxy20_d2, pxy20_d3 :  std_logic_vector(42 downto 0);
signal x2_1, x2_1_d1 :  std_logic_vector(16 downto 0);
signal y2_1, y2_1_d1 :  std_logic_vector(23 downto 0);
signal txy21 :  std_logic_vector(42 downto 0);
signal pxy21, pxy21_d1, pxy21_d2 :  std_logic_vector(42 downto 0);
signal x2_2, x2_2_d1, x2_2_d2 :  std_logic_vector(16 downto 0);
signal y2_2, y2_2_d1, y2_2_d2 :  std_logic_vector(23 downto 0);
signal txy22 :  std_logic_vector(42 downto 0);
signal pxy22, pxy22_d1 :  std_logic_vector(42 downto 0);
signal addOpDSP1 :  std_logic_vector(95 downto 0);
signal addRes :  std_logic_vector(95 downto 0);

signal NcPxy00_a1 : STD_LOGIC ;
signal NcPxy00_b1 : STD_LOGIC ;
signal NcPxy00_b2 : STD_LOGIC ;
signal NcPxy00_b3 : STD_LOGIC ;
signal NcPxy00_b4 : STD_LOGIC ;
signal NcPxy00_b5 : STD_LOGIC ;
signal NcPxy00    : STD_LOGIC ;
signal NcPxy20_a1 : STD_LOGIC ;
signal NcPxy20_b1 : STD_LOGIC ;
signal NcPxy20_b2 : STD_LOGIC ;
signal NcPxy20_b3 : STD_LOGIC ;
signal NcPxy20_b4 : STD_LOGIC ;
signal NcPxy20_b5 : STD_LOGIC ;
signal NcPxy20    : STD_LOGIC ;
signal NcOther_a1 : STD_LOGIC ;
signal NcOther    : STD_LOGIC ;

constant Var : std_logic := '0' ;

begin
   process(clk)
      begin
         if clk'event and clk = '1' then
           if(Enable='1') then
            pxy00_d1 <=  pxy00;
            pxy00_d2 <=  pxy00_d1;
            pxy00_d3 <=  pxy00_d2;
            x0_1_d1 <=  x0_1;
            y0_1_d1 <=  y0_1;
            pxy01_d1 <=  pxy01;
            pxy01_d2 <=  pxy01_d1;
            x0_2_d1 <=  x0_2;
            x0_2_d2 <=  x0_2_d1;
            y0_2_d1 <=  y0_2;
            y0_2_d2 <=  y0_2_d1;
            pxy02_d1 <=  pxy02;
            pxy20_d1 <=  pxy20;
            pxy20_d2 <=  pxy20_d1;
            pxy20_d3 <=  pxy20_d2;
            x2_1_d1 <=  x2_1;
            y2_1_d1 <=  y2_1;
            pxy21_d1 <=  pxy21;
            pxy21_d2 <=  pxy21_d1;
            x2_2_d1 <=  x2_2;
            x2_2_d2 <=  x2_2_d1;
            y2_2_d1 <=  y2_2;
            y2_2_d2 <=  y2_2_d1;
            pxy22_d1 <=  pxy22;
           end if;
         end if;
      end process;
   ----------------Synchro barrier, entering cycle 0----------------
   ----------------Synchro barrier, entering cycle 0----------------
   x0_0 <= Var & "" & X(13 downto 0) & "000"; -- OL
   y0_0 <= Var & "" & Y(23 downto 0) & "";    -- OL
   pxy00 <= x0_0(17 downto 0) * y0_0(24 downto 0); --0
   ----------------Synchro barrier, entering cycle 0----------------
--   x0_1 <= Var & "" & X(30 downto 14) & "";
--   y0_1 <= Var & "" & Y(23 downto 0) & "";
   x0_1 <= "" & X(30 downto 14) & ""; -- OL
   y0_1 <= "" & Y(23 downto 0) & "";  -- OL
   ----------------Synchro barrier, entering cycle 1----------------
   txy01 <= (Var & x0_1_d1(16 downto 0)) * (Var & y0_1_d1(23 downto 0));
   pxy01 <= (txy01(42 downto 0)) + ("00000000000000000" &pxy00_d1(42 downto 17));
   ----------------Synchro barrier, entering cycle 3----------------
   ----------------Synchro barrier, entering cycle 0----------------
-- OL   x0_2 <= Var & "" & X(47 downto 31) & ""; -- OL
-- OL   y0_2 <= Var & "" & Y(23 downto 0) & "";  -- OL
   x0_2 <= "" & X(47 downto 31) & ""; -- OL
   y0_2 <= "" & Y(23 downto 0) & "";  -- OL
   ----------------Synchro barrier, entering cycle 2----------------
   txy02 <= (Var & x0_2_d2(16 downto 0)) * (Var & y0_2_d2(23 downto 0)); -- OL
   pxy02 <= (txy02(42 downto 0)) + ("00000000000000000" &pxy01_d1(42 downto 17));
   ----------------Synchro barrier, entering cycle 3----------------
   addOpDSP0 <= "000000000000000000000000" & pxy02_d1(40 downto 0) & pxy01_d2(16 downto 0) & pxy00_d3(16 downto 3) & "" &  "";--3 bpadX 3 bpadY 0
   ----------------Synchro barrier, entering cycle 0----------------
   ----------------Synchro barrier, entering cycle 0----------------
-- OL   x2_0 <= "0" & "" & X(13 downto 0) & "000";
-- OL   y2_0 <= "0" & "" & Y(47 downto 24) & "";
-- OL   pxy20 <= x2_0(17 downto 0) * y2_0(24 downto 0); --0
   x2_0 <= "" & X(13 downto 0) & "000";
   y2_0 <= "" & Y(47 downto 24) & "";
   pxy20 <= (Var & x2_0(16 downto 0)) * (Var & y2_0(23 downto 0)); --0
   ----------------Synchro barrier, entering cycle 0----------------
-- OL   x2_1 <= "0" & "" & X(30 downto 14) & "";
-- OL   y2_1 <= "0" & "" & Y(47 downto 24) & "";
   x2_1 <= "" & X(30 downto 14) & "";
   y2_1 <= "" & Y(47 downto 24) & "";
   ----------------Synchro barrier, entering cycle 1----------------
-- OL   txy21 <= x2_1_d1(17 downto 0) * y2_1_d1(24 downto 0);
   txy21 <= (Var & x2_1_d1(16 downto 0)) * (Var & y2_1_d1(23 downto 0));
   pxy21 <= (txy21(42 downto 0)) + ("00000000000000000" &pxy20_d1(42 downto 17));
   ----------------Synchro barrier, entering cycle 3----------------
   ----------------Synchro barrier, entering cycle 0----------------
-- OL   x2_2 <= "0" & "" & X(47 downto 31) & "";
-- OL   y2_2 <= "0" & "" & Y(47 downto 24) & "";
   x2_2 <= "" & X(47 downto 31) & "";
   y2_2 <= "" & Y(47 downto 24) & "";
   ----------------Synchro barrier, entering cycle 2----------------
-- OL   txy22 <= x2_2_d2(17 downto 0) * y2_2_d2(24 downto 0);
   txy22 <= (Var & x2_2_d2(16 downto 0)) * (Var & y2_2_d2(23 downto 0));
   pxy22 <= (txy22(42 downto 0)) + ("00000000000000000" &pxy21_d1(42 downto 17));
   ----------------Synchro barrier, entering cycle 3----------------
   addOpDSP1 <= "" & pxy22_d1(40 downto 0) & pxy21_d2(16 downto 0) & pxy20_d3(16 downto 3) & "000000000000000000000000" &  "";--3 bpadX 3 bpadY 0
   adder: IntMultiAdder_96_op2_f400_uid5  -- pipelineDepth=2 maxInDelay=4.4472e-10
      port map ( clk  => clk,
                 Enable => Enable,
 -- OL                rst  => rst,
                 R => addRes,
                 X0 => addOpDSP0,
                 X1 => addOpDSP1);
   ----------------Synchro barrier, entering cycle 5----------------
   R <= addRes(95 downto 0);

NcPxy00_a1 <= pxy00_d1(0) and pxy00_d1(1) and pxy00_d1(2) and pxy00_d2(0) and pxy00_d2(1) and pxy00_d2(2);
NcPxy00_b1 <= pxy00_d2(17) and pxy00_d2(18) and pxy00_d2(19) and pxy00_d2(20) and pxy00_d2(21);
NcPxy00_b2 <= pxy00_d2(22) and pxy00_d2(23) and pxy00_d2(24) and pxy00_d2(25) and pxy00_d2(26);
NcPxy00_b3 <= pxy00_d2(27) and pxy00_d2(28) and pxy00_d2(29) and pxy00_d2(30) and pxy00_d2(31);
NcPxy00_b4 <= pxy00_d2(32) and pxy00_d2(33) and pxy00_d2(34) and pxy00_d2(35) and pxy00_d2(36);
NcPxy00_b5 <= pxy00_d2(37) and pxy00_d2(38) and pxy00_d2(39) and pxy00_d2(40) and pxy00_d2(41) and pxy00_d2(42);
NcPxy00 <= NcPxy00_a1 and NcPxy00_b1 and NcPxy00_b2 and NcPxy00_b3 and NcPxy00_b4 and NcPxy00_b5 ;

NcPxy20_a1 <= pxy20_d1(0) and pxy20_d1(1) and pxy20_d1(2) and pxy20_d2(0) and pxy20_d2(1) and pxy20_d2(2);
NcPxy20_b1 <= pxy20_d2(17) and pxy20_d2(18) and pxy20_d2(19) and pxy20_d2(20) and pxy20_d2(21);
NcPxy20_b2 <= pxy20_d2(22) and pxy20_d2(23) and pxy20_d2(24) and pxy20_d2(25) and pxy20_d2(26);
NcPxy20_b3 <= pxy20_d2(27) and pxy20_d2(28) and pxy20_d2(29) and pxy20_d2(30) and pxy20_d2(31);
NcPxy20_b4 <= pxy20_d2(32) and pxy20_d2(33) and pxy20_d2(34) and pxy20_d2(35) and pxy20_d2(36);
NcPxy20_b5 <= pxy20_d2(37) and pxy20_d2(38) and pxy20_d2(39) and pxy20_d2(40) and pxy20_d2(41) and pxy20_d2(42);
NcPxy20 <= NcPxy20_a1 and NcPxy20_b1 and NcPxy20_b2 and NcPxy20_b3 and NcPxy20_b4 and NcPxy20_b5 ;

NcOther_a1 <= pxy02_d1(41) and pxy02_d1(42) and pxy22_d1(41) and pxy22_d1(42) ;
NcOther <= NcOther_a1;

Nc <= NcPxy20 and NcPxy00 and NcOther;

end architecture;

--------------------------------------------------------------------------------
--                    IntTruncMultiplier_48_48_96_unsigned_oli
-- This operator is part of the Infinite Virtual Library FloPoCoLib
-- All rights reserved 
-- Authors: Sebastian Banescu, Bogdan Pasca, Radu Tudoran (2010-2011)
--------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_signed.all;
library work;
entity IntTruncMultiplier_48_48_96_unsigned_oli is
       port ( 
            ClkRef : in  STD_LOGIC;
            Rstn   : in  STD_LOGIC;
            Enable : in  STD_LOGIC;

            X      : in  STD_LOGIC_VECTOR(47 downto 0);
            Y      : in  STD_LOGIC_VECTOR(47 downto 0);
            R      : out STD_LOGIC_VECTOR(95 downto 0);
            Nc     : out STD_LOGIC   
            );
end entity;

architecture arch of IntTruncMultiplier_48_48_96_unsigned_oli is
   component IntMultiAdder_96_op2_f400_uid5 is
      port ( clk : in std_logic;
             Enable : in std_logic;

-- OL             rst : in std_logic;
             X0 : in  std_logic_vector(95 downto 0);
             X1 : in  std_logic_vector(95 downto 0);
             R : out  std_logic_vector(95 downto 0) );
   end component;

signal x0_0      : STD_LOGIC_VECTOR(17 downto 0);
signal y0_0      : STD_LOGIC_VECTOR(24 downto 0);
signal x0_1      : STD_LOGIC_VECTOR(17 downto 0);
signal y0_1      : STD_LOGIC_VECTOR(24 downto 0);
signal x0_2      : STD_LOGIC_VECTOR(17 downto 0);
signal y0_2      : STD_LOGIC_VECTOR(24 downto 0);
signal x2_0      : STD_LOGIC_VECTOR(17 downto 0);
signal y2_0      : STD_LOGIC_VECTOR(24 downto 0);
signal x2_1      : STD_LOGIC_VECTOR(17 downto 0);
signal y2_1      : STD_LOGIC_VECTOR(24 downto 0);
signal x2_2      : STD_LOGIC_VECTOR(17 downto 0);
signal y2_2      : STD_LOGIC_VECTOR(24 downto 0);

signal MltIA     : STD_LOGIC_VECTOR(17 downto 0);
signal MltIB1    : STD_LOGIC_VECTOR(17 downto 0);
signal MltIB2    : STD_LOGIC_VECTOR(17 downto 0);
signal MltIC     : STD_LOGIC_VECTOR(17 downto 0);
signal MltID1    : STD_LOGIC_VECTOR(17 downto 0);
signal MltID2    : STD_LOGIC_VECTOR(17 downto 0);

--signal MemoDataX : STD_LOGIC_VECTOR(33 downto 0);
--signal MemoDataY : STD_LOGIC_VECTOR(47 downto 0);
signal CalMult   : STD_LOGIC                    ;

signal Rmult1    : STD_LOGIC_VECTOR(42 downto 0);
signal Rmult2    : STD_LOGIC_VECTOR(42 downto 0);
signal Slct      : STD_LOGIC_VECTOR(1 downto  0);

signal MultRs10  : STD_LOGIC_VECTOR(42 downto 0);
signal MultRs11  : STD_LOGIC_VECTOR(42 downto 0);
signal MultRs20  : STD_LOGIC_VECTOR(42 downto 0);
signal MultRs21  : STD_LOGIC_VECTOR(42 downto 0);

signal pxy01     : STD_LOGIC_VECTOR(42 downto 0);
signal pxy21     : STD_LOGIC_VECTOR(42 downto 0);
signal pxy02     : STD_LOGIC_VECTOR(42 downto 0);
signal pxy22     : STD_LOGIC_VECTOR(42 downto 0);

signal OpCal11   : STD_LOGIC_VECTOR(35 downto 0);
signal OpCal12   : STD_LOGIC_VECTOR(35 downto 0);
signal OpCal21   : STD_LOGIC_VECTOR(35 downto 0);
signal OpCal22   : STD_LOGIC_VECTOR(35 downto 0);

signal add11     : STD_LOGIC_VECTOR(42 downto 0);
signal add12     : STD_LOGIC_VECTOR(42 downto 0);
signal add21     : STD_LOGIC_VECTOR(42 downto 0);
signal add22     : STD_LOGIC_VECTOR(42 downto 0);
signal addOpDSP0 : STD_LOGIC_VECTOR(95 downto 0); 
signal addOpDSP1 : STD_LOGIC_VECTOR(95 downto 0);
signal addRes    : STD_LOGIC_VECTOR(95 downto 0);

signal AddInt0  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt1  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt2  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt3  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt4  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt5  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddInt6  : STD_LOGIC_VECTOR(22 downto 0) ;
signal AddFinal : STD_LOGIC_VECTOR(22 downto 0) ;

signal Addx2  : STD_LOGIC_VECTOR(17 downto 0) ;
signal Addx4  : STD_LOGIC_VECTOR(18 downto 0) ;
signal Addx8  : STD_LOGIC_VECTOR(19 downto 0) ;
signal Addx16 : STD_LOGIC_VECTOR(20 downto 0) ;
signal Addx32 : STD_LOGIC_VECTOR(21 downto 0) ;
signal Addx64 : STD_LOGIC_VECTOR(22 downto 0) ;

signal OpCalNw1 : STD_LOGIC_VECTOR(42 downto 0) ;
signal OpCalNw2 : STD_LOGIC_VECTOR(42 downto 0) ;

constant Var : std_logic := '0' ;

begin

x0_0 <= Var & X(13 downto  0) & "000" ;
y0_0 <= Var & Y(23 downto  0)         ;
x0_1 <= Var & X(30 downto 14)         ;
y0_1 <= Var & Y(23 downto  0)         ;
x0_2 <= Var & X(47 downto 31)         ;
y0_2 <= Var & Y(23 downto  0)         ;

x2_0 <= Var & X(13 downto  0) & "000" ;
y2_0 <= Var & Y(47 downto 24)         ;
x2_1 <= Var & X(30 downto 14)         ;
y2_1 <= Var & Y(47 downto 24)         ;
x2_2 <= Var & X(47 downto 31)         ;
y2_2 <= Var & Y(47 downto 24)         ;

MltIA <= x0_1 when (Slct = "01") else
         x0_2 when (Slct = "10") else x0_0;

MltIB1 <= y0_0(24 downto 7); 

MltIB2 <= "00000000000" & y0_0(6  downto 0); 

MltIC <= x2_1 when (Slct = "01") else
         x2_2 when (Slct = "10") else x2_0;

MltID1 <= y2_0(24 downto 7); 

MltID2 <= "00000000000" & y2_0(6  downto 0);

pxy01 <= Rmult1 + ("00000000000000000" & MultRs10(42 downto 17));
pxy02 <= Rmult1 + ("00000000000000000" & add11   (42 downto 17));
pxy21 <= Rmult2 + ("00000000000000000" & MultRs20(42 downto 17));
pxy22 <= Rmult2 + ("00000000000000000" & add21   (42 downto 17));

CalMult <= Enable or Slct(1) or Slct(0);

OpCal11 <= MltIA * MltIB1;
OpCal12 <= MltIA * MltIB2;
OpCal21 <= MltIC * MltID1;
OpCal22 <= MltIC * MltID2;

OpCalNw1 <= (OpCal11 & "0000000") + ("0000000" & OpCal12) ;
OpCalNw2 <= (OpCal21 & "0000000") + ("0000000" & OpCal22) ;

--MemoData : process(ClkRef, Rstn)
--  begin
--    if(Rstn = '0') then
--              MemoDataX <= (others => '0') ;
--              MemoDataY <= (others => '0') ;
--
--      elsif ClkRef'event and ClkRef = '1' then
--        if(Enable = '1') then               
--              MemoDataX <= X(47 downto 14) ;
--              MemoDataY <= Y(47 downto  0) ; 
--      
--        end if;
--     end if;
--end process MemoData;

Multiplieur : process(ClkRef, Rstn)
  begin
    if(Rstn = '0') then 
              Rmult1 <= (others => '0')  ;
              Rmult2 <= (others => '0')  ;
              Slct   <= (others => '0')  ;

      elsif ClkRef'event and ClkRef = '1' then
        if(CalMult = '1') then
              Rmult1  <= OpCalNw1        ;
              Rmult2  <= OpCalNw2        ;
              Slct   <= Slct(0) & Enable ;

          else
              Rmult1 <= (others => '0')  ;
              Rmult2 <= (others => '0')  ;
              Slct   <= (others => '0')  ;

        end if;
    end if;
end process Multiplieur;

MemResult : process(ClkRef, Rstn)
  begin
    if(Rstn = '0') then
              MultRs10 <= (others => '0')   ;
              MultRs11 <= (others => '0')   ;
              MultRs20 <= (others => '0')   ;
              MultRs21 <= (others => '0')   ;
              Add11    <= (others => '0')   ;
              Add21    <= (others => '0')   ;
              Add12    <= (others => '0')   ;
              Add22    <= (others => '0')   ;

      elsif ClkRef'event and ClkRef = '1' then
        if(Slct(0) = '1') then
              MultRs10 <= Rmult1            ;
              MultRs11 <= MultRs11          ;
              MultRs20 <= Rmult2            ;
              MultRs21 <= MultRs21          ;
              Add11    <= Add11             ;
              Add21    <= Add21             ;
              Add12    <= Add12             ;
              Add22    <= Add22             ;
 
          elsif(Slct(1) = '1') then
              MultRs10 <= MultRs10          ;
              MultRs11 <= Rmult1            ;
              MultRs20 <= MultRs20          ;
              MultRs21 <= Rmult2            ;
              Add11    <= pxy01             ;
              Add21    <= pxy21             ;
              Add12    <= Add12             ;
              Add22    <= Add22             ;
    
            else
              MultRs10 <= MultRs10          ;
              MultRs11 <= MultRs11          ;
              MultRs20 <= MultRs20          ;
              MultRs21 <= MultRs21          ;
              Add11    <= Add11             ;
              Add21    <= Add21             ;
              Add12    <= pxy02             ;
              Add22    <= pxy22             ;

        end if;
     end if;
end process MemResult;

addOpDSP0 <= "000000000000000000000000" & Add12(40 downto 0) &    Add11(16 downto 0) & MultRs10(16 downto 3)     ;
addOpDSP1 <=  Add22(40 downto 0)        & Add21(16 downto 0) & MultRs20(16 downto 3) & "000000000000000000000000";

   adder: IntMultiAdder_96_op2_f400_uid5  -- pipelineDepth=2 maxInDelay=4.4472e-10
      port map ( Clk  => ClkRef,
                 Enable => Enable,
 -- OL                rst  => rst,
                 R => addRes,
                 X0 => addOpDSP0,
                 X1 => addOpDSP1);

Nc <=  Rstn;
   R <= addRes(95 downto 0);

end architecture;

--------------------------------------------------------------------------------
--                           IntAdder_57_f400_uid15
--                     (IntAdderClassical_57_f400_uid17)
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

entity IntAdder_57_f400_uid15 is
   port ( clk : in std_logic;
          Enable : in std_logic;
-- OL         rst : in std_logic;
          X : in  std_logic_vector(56 downto 0);
          Y : in  std_logic_vector(56 downto 0);
          Cin : in std_logic;
          R : out  std_logic_vector(56 downto 0)   );
end entity;
architecture arch of IntAdder_57_f400_uid15 is
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
--                      FPMultiplier_8_47_8_47_8_47_uid2
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

entity FPMultiplier_8_47_8_47_8_47_uid2 is
   port ( ClkRef : in std_logic;
          Enable : in std_logic;
-- OL     rst : in std_logic;
          X : in  std_logic_vector(8+47+2 downto 0);
          Y : in  std_logic_vector(8+47+2 downto 0);
          R : out  std_logic_vector(8+47+2 downto 0);
          Nc : out  std_logic   );
end entity;

architecture arch of FPMultiplier_8_47_8_47_8_47_uid2 is
   component IntAdder_57_f400_uid15 is
      port ( clk : in std_logic;
             Enable : in std_logic;
-- OL             rst : in std_logic;
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
             R : out  std_logic_vector(95 downto 0) ;
             Nc : out  std_logic  );
   end component;

component IntTruncMultiplier_48_48_96_unsigned_oli is
       port ( 
            ClkRef : in  STD_LOGIC;
            Rstn   : in  STD_LOGIC;
            Enable : in  STD_LOGIC;

            X      : in  STD_LOGIC_VECTOR(47 downto 0);
            Y      : in  STD_LOGIC_VECTOR(47 downto 0);
            R      : out STD_LOGIC_VECTOR(95 downto 0);
            Nc     : out STD_LOGIC   
            );
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

signal sigProd_oli :  std_logic_vector(95 downto 0);
signal NcOli    :  std_logic;
begin
   process(ClkRef)
      begin
         if ClkRef'event and ClkRef = '1' then
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
      port map ( clk  => ClkRef,
                 Enable => Enable,
-- OL                 rst  => rst,
                 R => sigProd,
                 X => sigX,
                 Y => sigY,
                 Nc => Nc);

SignificandMultiplication_oli :IntTruncMultiplier_48_48_96_unsigned_oli
                               port map( 
                                       ClkRef => ClkRef,
                                       Rstn   => '1',
                                       Enable => '1',

                                       X      => sigX,
                                       Y      => sigY,
                                       R      => sigProd_oli,
                                       Nc     => NcOli
                                       );

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
   RoundingAdder: IntAdder_57_f400_uid15  -- pipelineDepth=2 maxInDelay=1.55044e-09
      port map ( clk  => ClkRef,
                 Enable => Enable,
-- OL                rst  => rst,
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

