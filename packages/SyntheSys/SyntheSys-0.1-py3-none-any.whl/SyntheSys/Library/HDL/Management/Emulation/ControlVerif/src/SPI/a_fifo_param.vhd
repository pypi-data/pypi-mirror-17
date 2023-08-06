
--------------------------------------------------------------------------------
-- Company:       ADACSYS
-- Engineer: 
--
-- Create Date:    03/29/2013
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_fifo_param.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity a_fifo_param is
  generic (
          SIZE_ADDR_MEM  : integer := 10 ;
          SIZE_PORT_MEM  : integer := 16 
          );
  Port(
      resetn     : in  STD_LOGIC                                   ;
      resetmem   : in  STD_LOGIC                                   ;
      ClkWrite   : in  STD_LOGIC                                   ;
      ClkRead    : in  STD_LOGIC                                   ;

      Data_i     : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0) ;
      Dv_i       : in  STD_LOGIC                                   ;

      CmdRead    : in  STD_LOGIC                                   ;
      DecRdAddr  : in  STD_LOGIC                                   ;

      DataOut    : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0) ;
      DvOut      : out STD_LOGIC                                   ;
      NbrData    : out STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0) ;
      FifoFull   : out STD_LOGIC                                   ;
      VideOut    : out STD_LOGIC
      );
end a_fifo_param;

architecture behavioral of a_fifo_param is

-- Definition des signaux internes

signal DvInt        : STD_LOGIC                                    ;
signal WraddrInt    : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
signal DataMemFF    : STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0)  ;
signal RdaddrInt    : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
signal RdaddrIntCal : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
signal RdaddCal     : STD_LOGIC_VECTOR (SIZE_ADDR_MEM   downto 0)  ;
signal RdAdrrCir    : STD_LOGIC_VECTOR (SIZE_ADDR_MEM   downto 0)  ;
--signal CalSupProf   : STD_LOGIC_VECTOR (SIZE_ADDR_MEM   downto 0)  ; 
signal CalNormProf  : STD_LOGIC_VECTOR (SIZE_ADDR_MEM   downto 0)  ;
signal DataOutInt   : STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0)  ;
signal VideInt      : STD_LOGIC                                    ;
signal StartRead    : STD_LOGIC                                    ;
signal SendData     : STD_LOGIC                                    ;
signal TmpNbr       : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1   downto 0)  ;
--signal CalSupRd     : STD_LOGIC_VECTOR (SIZE_ADDR_MEM   downto 0)  ;
--signal SupRd        : STD_LOGIC                                    ;
signal FlagDebut    : STD_LOGIC                                    ;
signal CptCircul    : STD_LOGIC_VECTOR (1 downto 0)                ;
signal CptCirculCal : STD_LOGIC_VECTOR (1 downto 0)                ;
signal FlagCir      : STD_LOGIC                                    ;
signal FlagOK       : STD_LOGIC                                    ;
--signal SupRdAddr    : STD_LOGIC                                    ;
signal RdAddrMax    : STD_LOGIC                                    ;
signal WrAddrMax    : STD_LOGIC                                    ;
signal FifoFullInt  : STD_LOGIC                                    ;
--signal RmiseZero    : STD_LOGIC                                    ;
signal FlagWrMax    : STD_LOGIC                                    ;
signal RstAddr      : STD_LOGIC                                    ;

constant Cnts       : STD_LOGIC                  := '0'                               ;
constant MaxAddr    : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  := (others => '1') ;
constant AdZero     : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  := (others => '0') ;
constant CnstInt    : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-2 downto 0)  := (others => '0') ;
constant CnstUn     : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  := CnstInt   & '1' ;

--signal RdAddCal     : STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;

-- Definition du composant de Synchronisation

 component a_sync
  generic (
         SIZE_IN: integer := 32);
  port(
      dataIn      : in  STD_LOGIC_VECTOR (SIZE_IN-1 downto 0) ;
      samplingClk : in  STD_LOGIC                             ;
      resetn      : in  STD_LOGIC                             ;
      syncDataOut : out STD_LOGIC_VECTOR (SIZE_IN-1 downto 0)
      );
  end component;

-- Definition de la cellule Memoire

component a_sram_param 
  generic (
          SIZE_ADDR_MEM  : integer := 10 ;
          SIZE_PORT_MEM  : integer := 16 
          );
  Port(
      din    : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0) ;
      wen    : in  STD_LOGIC                                    ;
      wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
      rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
      clk    : in  STD_LOGIC                                    ;
      oclk   : in  STD_LOGIC                                    ;
      dout   : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0)
  );
end component;

begin

-- Detection FIFO vide

VideInt <= '1' when (WraddrInt=RdaddrInt) else '0' ;

-- Synchronisation des Datas a Memoriser

DffDv    : process (ClkWrite, resetn)
  begin
    if resetn = '0' then 
                              DvInt      <=  '0'         ;

       elsif rising_edge (ClkWrite) then
                              DvInt      <=  Dv_i        ;
    end if;
end process DffDv;

DffDataIn : a_sync generic map (SIZE_IN => SIZE_PORT_MEM) 
                   port map    (
                               dataIn       => Data_i    ,
                               samplingClk  => ClkWrite  ,
                               resetn       => resetn    ,
                               syncDataOut  => DataMemFF 
                               );

-- Gestion de l ecriture 

WrAddrMax <= '1' when WraddrInt=MaxAddr else '0' ;

RstAddr <= resetn and not FlagWrMax ;

CtrlWrSram    : process (ClkWrite, RstAddr)
  begin
    if RstAddr = '0' then 
                              WraddrInt  <=  (others => '0') ; 

       elsif rising_edge (ClkWrite) then
          if(DvInt='1') then
                              WraddrInt  <=  WraddrInt + 1   ;

            elsif((WrAddrMax='1' and FifoFullInt='0') or resetmem='1') then 
                              WraddrInt  <=  (others => '0') ;

              else
                              WraddrInt  <=  WraddrInt       ;
          end if;
    end if;
end process CtrlWrSram;

-- Gestion de la lecture 

StartRead   <= CmdRead and not VideInt and not SendData;
--CalSupProf  <= (('1' &  RdaddrInt) -1) ;
CalNormProf <=   '0' & (RdaddrInt - 1) ;

FlagCir  <= '1' when CptCircul="10" else '0' ;
FlagOk   <= FlagCir and FlagDebut and DecRdAddr;

RdaddCal <= RdAdrrCir when FlagOK='1' else CalNormProf  ;

--SupRdAddr <= '1' when RdaddrInt >= CnstUn else '0' ;
--RmiseZero <= SupRdAddr and VideInt and not CmdRead ;
RdAddrMax <= '1' when RdaddrInt=MaxAddr else '0' ;

RdaddrIntCal <= RdaddrInt  + 1 when CmdRead='1' else RdaddrInt;

CtrlRdSram    : process (ClkRead, RstAddr)
  begin
    if RstAddr = '0' then 
                              RdaddrInt <=  (others => '0') ;
                              DataOut   <=  (others => '0') ;
                              DvOut     <=  '0'             ;
                              SendData  <=  '0'             ;

       elsif rising_edge (ClkRead) then
          if(StartRead='1') then
                              RdaddrInt <=  RdaddrInt  + 1  ;
                              DataOut   <=  DataOutInt      ;
                              DvOut     <=  '0'             ;
                              SendData  <=  '1'             ;

            elsif(SendData='1') then
                              RdaddrInt <=  RdaddrIntCal    ;
                              DataOut   <=  DataOutInt      ;
                              DvOut     <=  '1'             ;
                              SendData  <=  CmdRead         ;

              elsif(DecRdAddr='1') then
--                              RdaddrInt <=  RdaddrInt - 1   ;
                              RdaddrInt <= RdaddCal(SIZE_ADDR_MEM-1 downto 0) ; 
                              DataOut   <=  (others => '0') ;
                              DvOut     <=  '0'             ;
                              SendData  <=  '0'             ;
 
                elsif((RdAddrMax='1' and FifoFullInt='0') or resetmem='1') then
                              RdaddrInt <=  (others => '0') ;
                              DataOut   <=  (others => '0') ;
                              DvOut     <=  '0'             ;
                              SendData  <=  '0'             ;
   
                else
                              RdaddrInt <=  RdaddrInt       ;
                              DataOut   <=  (others => '0') ;
                              DvOut     <=  '0'             ;
                              SendData  <=  '0'             ;

          end if;
    end if;
end process CtrlRdSram;

-- Dectection d'un tour complet 

CptCirculCal <= CptCircul when VideInt='1' else CptCircul + 1;

DetectComplet : process (ClkRead, resetn)
  begin
    if resetn = '0' then
                              FlagDebut <= '0'             ;
                              CptCircul <= (others => '0') ;

      elsif rising_edge (ClkRead) then
          if((RdaddrInt=MaxAddr) and FlagDebut='0') then
                              FlagDebut <= '1' ;
                              CptCircul <= (others => '0') ;

            elsif(FlagDebut='1' and (RdaddrInt(1 downto 0)<="10") and StartRead='1') then 
                              FlagDebut <= '1' ;
                              CptCircul <= CptCirculCal;

             elsif((RdaddrInt=AdZero+3) and FlagDebut='1') then
                              FlagDebut <= '0' ;
                              CptCircul <= (others => '0') ;

          end if;
    end if;
end process DetectComplet;

RdAdrrCir <= '1' & AdZero ;

-- Detection Fifo Full

DetectFifoFull : process (ClkRead, resetn)
  begin
    if resetn = '0' then
                              FifoFullInt <= '0' ;
                              FlagWrMax   <= '0' ;

      elsif rising_edge (ClkRead) then
          if(WraddrInt=MaxAddr-3 and FlagWrMax='0') then
                              FifoFullInt <= '1'     ;
                              FlagWrMax   <= VideInt ;

            else 
                              FifoFullInt <= '0' ;
                              FlagWrMax   <= '0' ;

          end if;
    end if;
end process DetectFifoFull;

sram : a_sram_param generic map (
                                SIZE_ADDR_MEM => SIZE_ADDR_MEM,
                                SIZE_PORT_MEM => SIZE_PORT_MEM
                                )
                    port map(
                            din    => DataMemFF  ,
                            wen    => DvInt      ,
                            wraddr => WraddrInt  ,
                            rdaddr => RdaddrInt  ,
                            clk    => ClkWrite   ,
                            oclk   => ClkRead    ,
                            dout   => DataOutInt 
                    );

VideOut  <= VideInt                                    ;
-- OF CHGMNT TmpNbr   <= Cnts & (WraddrInt - RdaddrInt)             ;
TmpNbr   <= WraddrInt - RdaddrInt ;
--SupRd    <= '1' when (RdaddrInt>WraddrInt) else '0'    ;
--CalSupRd <= Cnts & ((MaxAddr - RdaddrInt) + WraddrInt) ;

-- OF CHGMNT NbrData <= CalSupRd + CalSupRd when(SupRd='1') else TmpNbr + TmpNbr ;
NbrData  <= TmpNbr      ; -- Sur 16bits
FifoFull <= FifoFullInt ;

end behavioral;
