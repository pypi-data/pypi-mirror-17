--------------------------------------------------------------------------------
-- Company:       ADACSYS
-- Engineer: 
--
-- Create Date:    08/05/2013
-- Design Name:
-- Module Name:    a_DeSerialSpi.vhd
-- Project Name:
-- Target Device:  None
-- Tool versions:
-- Description:
--      
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--
-- Connection Effectue :
--
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity a_DeSerialSpi is
  Port(
--- Control Signals
      resetn    : in  STD_LOGIC                     ; -- Actif niveau Bas
      clkRef    : in  STD_LOGIC                     ; -- Clock Reference
      ClkEnCom  : in  STD_LOGIC                     ;

      cs        : in  STD_LOGIC                     ;
      clkspi    : in  STD_LOGIC                     ;
      di        : in  STD_LOGIC                     ;

      enable    : in  STD_LOGIC                     ;

      StartComp : out STD_LOGIC                     ;
      r_dv_o    : out STD_LOGIC                     ;
      r_q       : out STD_LOGIC_VECTOR(15 downto 0)
      );
end a_DeSerialSpi;

architecture behavioral of a_DeSerialSpi is

-- Description des Signaux Internes

signal CptWd      : STD_LOGIC_VECTOR(4 downto 0)  ;
signal DataInt    : STD_LOGIC_VECTOR(15 downto 0) ;
signal DataCapt   : STD_LOGIC_VECTOR(15 downto 0) ;
signal DvCapt     : STD_LOGIC                     ;
signal FlagCapt   : STD_LOGIC                     ;
signal StopFlag   : STD_LOGIC                     ;
signal DetectMot  : STD_LOGIC                     ;
signal PremierMot : STD_LOGIC                     ;
signal DvOut      : STD_LOGIC                     ;
signal PipeDvCapt : STD_LOGIC_VECTOR(2 downto 0)  ;
signal CsInv      : STD_LOGIC                     ;
signal MiseZero   : STD_LOGIC                     ;

component a_compteur_param
  generic (
          SIZE_CPT: integer := 4);
  port(
          Clk       : in   STD_LOGIC;
          ClkEn     : in   STD_LOGIC;
          resetn    : in   STD_LOGIC;
          Enable    : in   STD_LOGIC;
          MiseZero  : in   STD_LOGIC;
          DataOut   : out  STD_LOGIC_VECTOR (SIZE_CPT-1  downto 0)
       );
end component;

  begin

-- Creation du Vector 16 bits

MiseZero <= '1' when (CptWd="10000") else '0';
CsInv <= not cs and not MiseZero;

CptWord : a_compteur_param
           generic map(SIZE_CPT => 5)
           port map(
                   Clk      => ClkRef     ,
                   ClkEn    => ClkEnCom   ,
                   resetn   => resetn     ,
                   Enable   => clkspi     ,
                   MiseZero => CsInv      ,
                   DataOut  => CptWd
                   );

DecalgeData : process (ClkRef, resetn)
  begin
      if resetn = '0' then
                   DataInt <= (others => '0')           ;

        elsif rising_edge (ClkRef) then
         if(ClkEnCom='1') then
          if(clkspi='1') then
--                   DataInt <= di & DataInt(15 downto 1) ;
                   DataInt <= di & DataInt(15 downto 1);

              else
                   DataInt <= DataInt                   ;

          end if;
         end if;
      end if;
end process DecalgeData;

StopFlag <= '0' when (CptWd="0000") else '1' ;

MemoDataCapt :  process (ClkRef, resetn)
  begin
      if resetn = '0' then
                   DataCapt   <= (others => '0')                            ;
                   DvCapt     <= '0'                                        ;
                   FlagCapt   <= '0'                                        ;

        elsif rising_edge (ClkRef) then
         if(ClkEnCom='1') then
          if(MiseZero='1' and FlagCapt='0') then
--                   DataCapt   <= DataInt(7 downto 0) & DataInt(15 downto 8) ;
                   DataCapt   <= DataInt                                    ;
                   DvCapt     <= '1'                                        ;
                   FlagCapt   <= '1'                                        ;

              elsif(FlagCapt='1') then
                   DataCapt   <= DataCapt                                   ;
                   DvCapt     <= '0'                                        ;
                   FlagCapt   <= StopFlag                                   ; 

                else
                   DataCapt   <= DataCapt                                   ;
                   DvCapt     <= '0'                                        ;
                   FlagCapt   <= '0'                                        ;

          end if;
         end if;
      end if;
end process MemoDataCapt;

-- Dectection du premier Mot de 16 bit 

DetectMot <= DvCapt and not cs and not PremierMot;

DectFirstMot : process (ClkRef, resetn)
  begin
      if resetn = '0' then
                  PremierMot <= '0'        ;
                  StartComp  <= '0'        ;

        elsif rising_edge (ClkRef) then
         if(ClkEnCom='1') then
          if(DetectMot='1') then
                  PremierMot <= '1'        ;
                  StartComp  <= '1'        ;

            elsif(cs='1') then
                  PremierMot <= '0'        ;
                  StartComp  <= '0'        ;

              else
                  PremierMot <= PremierMot ;
                  StartComp  <= '0'        ;

          end if;
         end if;
       end if;
end process DectFirstMot;

-- Ecriture ou Lecture FIFO

PipeDv : process (ClkRef, resetn, PipeDvCapt(2 downto 0))
  begin
      if resetn = '0' then
                  DvOut      <= '0'                             ;
                  PipeDvCapt <= (others => '0')                 ;

        elsif rising_edge (ClkRef) then
         if(ClkEnCom='1') then
          if(enable='1') then
                  DvOut      <= '0'                             ;
                  PipeDvCapt <= (others => '0')                 ;
            else
                  DvOut      <= PipeDvCapt(2)                   ;
                  PipeDvCapt <= PipeDvCapt(1 downto 0) & DvCapt ;

          end if;
         end if;
       end if;
end process PipeDv;


r_dv_o <= DvOut    ;
r_q    <= DataCapt ;

end behavioral;

