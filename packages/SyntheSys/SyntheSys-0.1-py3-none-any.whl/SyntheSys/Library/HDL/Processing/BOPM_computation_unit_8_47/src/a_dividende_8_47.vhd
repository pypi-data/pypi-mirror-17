--------------------------------------------------------------------------------
-- Create Date:    11/11/2013
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_dividende.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a_dividende is
  port ( 
       Rstn      : in  STD_LOGIC                      ;
       ClkRef    : in  STD_LOGIC                      ; 
       ClkEnCal  : in  STD_LOGIC                      ;
       StartRun  : in  STD_LOGIC                      ;
       DvSend    : in  STD_LOGIC                      ;

       Colonne   : in  STD_LOGIC_VECTOR (15 downto 0) ;
       StartNwCol: in  STD_LOGIC                      ;
       KInit     : in  STD_LOGIC_VECTOR (55 downto 0) ;
       Rinv      : in  STD_LOGIC_VECTOR (55 downto 0) ;
        
       DividendA : in  STD_LOGIC_VECTOR (55 downto 0) ;
       DividendB : in  STD_LOGIC_VECTOR (55 downto 0) ;
       DividendC : in  STD_LOGIC_VECTOR (55 downto 0) ;
       DividendD : in  STD_LOGIC_VECTOR (55 downto 0) ;

       VersTimeA : in  STD_LOGIC_VECTOR (15 downto 0) ;
       VersTimeB : in  STD_LOGIC_VECTOR (15 downto 0) ;
       VersTimeC : in  STD_LOGIC_VECTOR (15 downto 0) ;
       VersTimeD : in  STD_LOGIC_VECTOR (15 downto 0) ;

       KComp     : out STD_LOGIC_VECTOR (57 downto 0) ;
       Nc        : out STD_LOGIC
       );
end a_dividende;

architecture behavioral of a_dividende is

signal CompOutIntA   : STD_LOGIC_VECTOR(3  downto 0) ;
signal CompOutIntB   : STD_LOGIC_VECTOR(3  downto 0) ;
signal CompOutIntC   : STD_LOGIC_VECTOR(3  downto 0) ;
signal CompOutIntD   : STD_LOGIC_VECTOR(3  downto 0) ;

signal CompFin       : STD_LOGIC_VECTOR(3  downto 0) ;
signal PpCompFin     : STD_LOGIC_VECTOR(3  downto 0) ;

signal MxDiv         : STD_LOGIC_VECTOR(55 downto 0) ;
signal SlctDiv       : STD_LOGIC                     ;
signal DivCourant    : STD_LOGIC_VECTOR(57 downto 0) ;

signal CalNorm       : STD_LOGIC_VECTOR(57 downto 0) ;
signal Nc1           : STD_LOGIC                     ;
signal Nc2           : STD_LOGIC                     ;
signal DivCourantInt : STD_LOGIC_VECTOR(57 downto 0) ;
signal PpDivCourantInt : STD_LOGIC_VECTOR(57 downto 0) ;
signal KInitAll      : STD_LOGIC_VECTOR(57 downto 0) ;
signal RinvAll       : STD_LOGIC_VECTOR(57 downto 0) ;
signal SendNwKComp   : STD_LOGIC                     ;
signal SendNorKComp  : STD_LOGIC                     ;
signal SlctMx        : STD_LOGIC                     ;
signal MxDivMemo     : STD_LOGIC_VECTOR(57 downto 0) ;
signal KCompInt      : STD_LOGIC_VECTOR(57 downto 0) ;
signal KCompMemo     : STD_LOGIC_VECTOR(57 downto 0) ;
signal MxInt         : STD_LOGIC_VECTOR(57 downto 0) ;
signal ValDataDvCourant : STD_LOGIC_VECTOR(57 downto 0) ;
signal AddMxDiv      : STD_LOGIC_VECTOR(57 downto 0) ;

signal NwDivVal      : STD_LOGIC_VECTOR(57 downto 0) ;
--signal MemoMxInt     : STD_LOGIC_VECTOR(57 downto 0) ;

component a_comp_param
          generic (SIZE_COMP: integer := 4);
          port(
              dataIn_a    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
              dataIn_b    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
              egalOut     : out STD_LOGIC
              );
end component;

component FPAdderDualPath_8_47_8_47_8_47400 
          port (
               clk    : in  std_logic                        ;
               Enable : in  std_logic                        ;
-- OL          rst    : in  std_logic                        ;
               X      : in  std_logic_vector(8+47+2 downto 0);
               Y      : in  std_logic_vector(8+47+2 downto 0);
               R      : out std_logic_vector(8+47+2 downto 0);
               Nc     : out std_logic
               );
end component;

component FPMultiplier_8_47_8_47_8_47_uid2 
          port (
               ClkRef : in  std_logic                        ;
               Enable : in  std_logic                        ;
-- OL          rst    : in  std_logic                        ;
               X      : in  std_logic_vector(8+47+2 downto 0);
               Y      : in  std_logic_vector(8+47+2 downto 0);
               R      : out std_logic_vector(8+47+2 downto 0);
               Nc     : out std_logic
               );
end component;

  begin

-- 1ere Comparaison 

GinstA_Comp : for i in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4) 
                       port map    (
                                   dataIn_a   => Colonne  (((i*4)+3) downto i*4),
                                   dataIn_b   => VersTimeA(((i*4)+3) downto i*4),
                                   egalOut    => CompOutIntA(i)
                                   );
end generate GinstA_Comp;

ProcAndA : process(CompOutIntA)
          variable V : STD_LOGIC;
  begin
           V:= CompOutIntA(0);
    for j in 1 to 3 loop
           V:= V AND CompOutIntA(j);
    end loop;

           CompFin(0) <= V;
end process ProcAndA;

-- 2eme Comparaison 

GinstB_Comp : for k in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4) 
                       port map    (
                                   dataIn_a   => Colonne  (((k*4)+3) downto k*4),
                                   dataIn_b   => VersTimeB(((k*4)+3) downto k*4),
                                   egalOut    => CompOutIntB(k)
                                   );
end generate GinstB_Comp;

ProcAndB : process(CompOutIntB)
          variable W : STD_LOGIC;
  begin
           W:= CompOutIntB(0);
    for l in 1 to 3 loop
           W:= W AND CompOutIntB(l);
    end loop;

           CompFin(1) <= W;
end process ProcAndB;

-- 3eme Comparaison 

GinstC_Comp : for m in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4) 
                       port map    (
                                   dataIn_a   => Colonne  (((m*4)+3) downto m*4),
                                   dataIn_b   => VersTimeC(((m*4)+3) downto m*4),
                                   egalOut    => CompOutIntC(m)
                                   );
end generate GinstC_Comp;

ProcAndC : process(CompOutIntC)
          variable X : STD_LOGIC;
  begin
           X:= CompOutIntC(0);
    for n in 1 to 3 loop
           X:= X AND CompOutIntC(n);
    end loop;

           CompFin(2) <= X;
end process ProcAndC;

-- 4eme Comparaison 

GinstD_Comp : for o in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4) 
                       port map    (
                                   dataIn_a   => Colonne  (((o*4)+3) downto o*4),
                                   dataIn_b   => VersTimeD(((o*4)+3) downto o*4),
                                   egalOut    => CompOutIntD(o)
                                   );
end generate GinstD_Comp;

ProcAndD : process(CompOutIntD)
          variable Y : STD_LOGIC;
  begin
           Y:= CompOutIntD(0);
    for p in 1 to 3 loop
           Y:= Y AND CompOutIntD(p);
    end loop;

           CompFin(3) <= Y;
end process ProcAndD;

PipeCompFin : process (ClkRef, Rstn)
  begin
      if Rstn = '0' then
                 PpCompFin <= (others => '0');

        elsif rising_edge (ClkRef) then
         if(ClkEnCal='1') then
                 PpCompFin <= CompFin        ; 
 
         end if;
      end if;
end process PipeCompFin;

-- Selection du Dividende

MuxDividende : process(PpCompFin, DividendA, DividendB, DividendC, DividendD)
           begin
             case PpCompFin is
               when  "0001"  => MxDiv <= DividendA      ;
               when  "0010"  => MxDiv <= DividendB      ;
               when  "0100"  => MxDiv <= DividendC      ;
               when  "1000"  => MxDiv <= DividendD      ;
               when others   => MxDiv <= (others => '0');
             end case;
end process MuxDividende;

MemoDivid : process (ClkRef, Rstn)
  begin
      if Rstn = '0' then
                 MxDivMemo <= (others => '0');

        elsif rising_edge (ClkRef) then
         if(ClkEnCal='1') then
           if(SlctDiv='1') then 
--                 MxDivMemo <= MxDiv          ;
                 MxDivMemo <= NwDivVal       ;

           end if;
         end if;
       end if;
end process MemoDivid;
     
SlctDiv      <= PpCompFin(3) or      PpCompFin(2) or PpCompFin(1) or PpCompFin(0);
SendNwKComp  <= StartNwCol and     SlctDiv                               ;
SendNorKComp <= StartNwCol and not SlctDiv                               ;

GstSlctMx : process (ClkRef, Rstn)
  begin
      if Rstn = '0' then
                  SlctMx <= '0'  ;
                  DivCourant <= "0100000000000000000000000000000000000000000000000000000000";
                  KCompMemo  <= "0100000000000000000000000000000000000000000000000000000000";
                  ValDataDvCourant <= "0100000000000000000000000000000000000000000000000000000000";
--                  MemoMxInt  <= "0100000000000000000000000000000000000000000000000000000000";

        elsif rising_edge (ClkRef) then
         if(ClkEnCal='1') then
           if(DvSend='1') then
                  SlctMx <= '0'  ;
                  DivCourant <= "0100000000000000000000000000000000000000000000000000000000";
                  KCompMemo  <= "0100000000000000000000000000000000000000000000000000000000";
                  ValDataDvCourant <= "0100000000000000000000000000000000000000000000000000000000";
--                  MemoMxInt  <= "0100000000000000000000000000000000000000000000000000000000";

           elsif(SendNwKComp='1') then
                  SlctMx <= '1'  ;
                  DivCourant <=  PpDivCourantInt      ;
                  KCompMemo <= KCompInt       ;
--                  KCompMemo <= "01"&MxDivMemo      ;
                  ValDataDvCourant <= MxInt         ;
--                  MemoMxInt  <= MxInt         ;

             elsif(SendNorKComp='1') then
                  SlctMx <= '0'  ;
                  DivCourant <=  PpDivCourantInt      ;
                  KCompMemo <= KCompInt       ;
                  ValDataDvCourant <= MxInt         ;
--                  MemoMxInt  <= MxInt         ;
      
               elsif(StartRun='1') then
                  SlctMx <= '0'  ;
                  DivCourant <= "0100000000000000000000000000000000000000000000000000000000";
                  KCompMemo  <= "01"&KInit;
                  ValDataDvCourant <= "0100000000000000000000000000000000000000000000000000000000";

           end if;
         end if;
      end if;
end process GstSlctMx;

-- Partie Multiplication 

RinvAll <= "01"&Rinv;

FPMultiplier_8_47_1 : FPMultiplier_8_47_8_47_8_47_uid2
                      port map (
                               ClkRef => ClkRef     ,
                               Enable => ClkEnCal   ,
-- OL                          rst    => RST        ,
                               X      => RinvAll    , 
                               Y      => PpDivCourantInt ,
                               R      => CalNorm    ,
                               Nc     => Nc1
                               );

-- Multiplexeur entre Data Dividende et Calcul Normal

--MxInt <= "01"&MxDivMemo when(SlctDiv='1') else CalNorm ;
MxInt <= MxDivMemo when(SlctDiv='1') else CalNorm ;

--DivCourantInt <= "01"&MxDivMemo when(SlctMx='1') else ValDataDvCourant;
DivCourantInt <= MxDivMemo when(SlctMx='1') else ValDataDvCourant;

PipeDvCourant : process (ClkRef, Rstn)
  begin
      if Rstn = '0' then
                 PpDivCourantInt <= (others => '0');

        elsif rising_edge (ClkRef) then
         if(ClkEnCal='1') then
                 PpDivCourantInt <= DivCourantInt        ; 
 
         end if;
      end if;
end process PipeDvCourant;

KInitAll <= "01"&KInit;

FPAdderDualPath_8_47_1 : FPAdderDualPath_8_47_8_47_8_47400
                         port map (
                                  clk    => ClkRef        ,
                                  Enable => ClkEnCal      ,
-- OL                             rst => RST,
                                  X      => KInitAll      ,
--                                  Y      => DivCourantInt ,
                                  Y      => MxInt ,
                                  R      => KCompInt      ,
                                  Nc     => Nc2
                                  );

-- Preparation de la valeur suivant 

AddMxDiv <= "01"&MxDiv;

FPAdderDualPath_8_47_2 : FPAdderDualPath_8_47_8_47_8_47400
                         port map (
                                  clk    => ClkRef        ,
                                  Enable => ClkEnCal      ,
-- OL                             rst => RST,
                                  X      => PpDivCourantInt ,
--                                  Y      => DivCourantInt ,
                                  Y      => AddMxDiv    ,
                                  R      => NwDivVal      ,
                                  Nc     => Nc2
                                  );

KComp <= KCompMemo ;

end behavioral;
        

