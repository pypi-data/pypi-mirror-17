--------------------------------------------------------------------------------
-- Company:  ADACSYS
-- Engineer: OF
--
-- Create Date:    09/05/2013
-- Design Name:
-- Module Name:   a_SendDataSpi.vhd
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

entity a_SendDataSpi is
  Port(
      resetn    : in  STD_LOGIC                     ;
      resetmem  : in  STD_LOGIC                     ;
      ClkRef    : in  STD_LOGIC                     ;
      ClkEnCom  : in  STD_LOGIC                     ;
      EdgeSend  : in  STD_LOGIC                     ;

      DataNbrRd : in  STD_LOGIC_VECTOR(15 downto 0) ;

      Data_i    : in  STD_LOGIC_VECTOR(15 downto 0) ;
      Dv_i      : in  STD_LOGIC                     ;

      CmdRead   : in  STD_LOGIC                     ;

      Do        : out STD_LOGIC                     ;
      FifoFull  : out STD_LOGIC                     ;
      Nc        : out STD_LOGIC
      );
end a_SendDataSpi;

architecture behavioral of a_SendDataSpi is

-- signaux internes

signal ReadFifo    : STD_LOGIC                     ;
signal OrDecRdAddr : STD_LOGIC                     ;
signal DvOutInt    : STD_LOGIC                     ;
signal DataOutInt  : STD_LOGIC_VECTOR(15 downto 0) ;
--signal FifoFull    : STD_LOGIC                     ;
signal VideOut     : STD_LOGIC                     ;
signal NbrData     : STD_LOGIC_VECTOR(15 downto 0) ;

signal SendId      : STD_LOGIC                     ;
signal SendNbr     : STD_LOGIC                     ;
signal StepId      : STD_LOGIC                     ;
signal StepNbrData : STD_LOGIC                     ;
signal StepSdData  : STD_LOGIC                     ;
signal SendData    : STD_LOGIC                     ;
signal MxData      : STD_LOGIC_VECTOR(15 downto 0) ;
signal NbrDtMemo   : STD_LOGIC_VECTOR(15 downto 0) ;
signal DataTmp     : STD_LOGIC_VECTOR(15 downto 0) ;

signal NwData      : STD_LOGIC                     ;

signal ChgrData   : STD_LOGIC                     ;
signal FinSdData  : STD_LOGIC                     ;
signal PpId       : STD_LOGIC                     ;
--signal PpNbr      : STD_LOGIC                     ;
signal PpData     : STD_LOGIC                     ;
signal PlseId     : STD_LOGIC                     ;
--signal PlseNbrDt  : STD_LOGIC                     ;
--signal PlseData   : STD_LOGIC                     ;
signal CptSendBit : STD_LOGIC_VECTOR(4  downto 0) ;
signal RgDecal    : STD_LOGIC_VECTOR(15 downto 0) ;

-- OF signal PpCmdRead  : STD_LOGIC                     ;
signal EnCptSd    : STD_LOGIC                     ;
signal DoSpiNw    : STD_LOGIC                     ;

-- OF signal FinCmdRead    : STD_LOGIC                     ;
signal FinNbrDataDon : STD_LOGIC                     ;
signal ResultInt     : STD_LOGIC_VECTOR(3  downto 0) ;
signal CompData8b    : STD_LOGIC_VECTOR(15 downto 0) ;
signal ResultIntReg  : STD_LOGIC_VECTOR(3  downto 0) ;
signal StopSend      : STD_LOGIC                     ;
signal CompData      : STD_LOGIC_VECTOR(15 downto 0) ;

signal NbrDataCapt : STD_LOGIC_VECTOR(15 downto 0) ;
signal FlagCapt    : STD_LOGIC                     ;
signal StepCapt    : STD_LOGIC_VECTOR(1  downto 0) ;
signal NbrEgal     : STD_LOGIC                     ;
signal StopRd      : STD_LOGIC                     ;
signal CptCapt     : STD_LOGIC_VECTOR(4  downto 0) ;
signal CptRdFifo   : STD_LOGIC_VECTOR(15 downto 0) ;
signal PpNwData    : STD_LOGIC_VECTOR(3  downto 0) ;
-- OF signal Decr        : STD_LOGIC_VECTOR(1  downto 0) ;
signal StopCpt     : STD_LOGIC                     ;
signal DvEn        : STD_LOGIC                     ;
signal MxDataWd8 : STD_LOGIC_VECTOR(15 downto 0) ;
signal FlagSup   : STD_LOGIC                     ;
signal DetectSup : STD_LOGIC                     ;
signal DetectZer : STD_LOGIC                     ;
signal NbrDtMemoWd8 : STD_LOGIC_VECTOR(15 downto 0) ;
signal PpSendNbr : STD_LOGIC                     ;

-- Pour Verif

constant Id   : STD_LOGIC_VECTOR(15 downto 0) := "1111111111111111"; -- ffff Normalement sinon 11000011 195 10111101 189
constant Cnst : STD_LOGIC                     := '0'    ;

-- Definition du composant Compteur

component a_compteur_param
  generic (
         SIZE_CPT: integer := 4);
  Port (
        Clk       : in   STD_LOGIC                               ;
        ClkEn     : in   STD_LOGIC                               ;
        resetn    : in   STD_LOGIC                               ;
        Enable    : in   STD_LOGIC                               ;
        MiseZero  : in   STD_LOGIC                               ;
        DataOut   : out  STD_LOGIC_VECTOR (SIZE_CPT-1  downto 0)
  );
end component;

-- Definition du composant Fifo

component a_fifo_param 
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
end component;

component a_comp_param
  generic (
          SIZE_COMP: integer := 4);
  port(
          dataIn_a    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
          dataIn_b    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
          egalOut     : out STD_LOGIC
       );
end component;

component a_reg_memo_param
          generic (SIZE_IN: integer := 32);
          port(
              enable      : in   STD_LOGIC                     ;
              dataIn      : in  STD_LOGIC_VECTOR (SIZE_IN-1 downto 0);
              samplingClk : in  STD_LOGIC                            ;
              resetn      : in  STD_LOGIC                            ;
              syncDataOut : out STD_LOGIC_VECTOR (SIZE_IN-1 downto 0)
              );
end component;

  begin

DvEn <= Dv_i and ClkEnCom;

u_fifo_out : a_fifo_param
             generic map(
                        SIZE_ADDR_MEM => 16 , -- Augmentation Profondeur OF CHGMNT
                        SIZE_PORT_MEM => 16
                        )
             port map(
                     resetn    => resetn      ,
                     resetmem  => resetmem    ,
                     ClkWrite  => ClkRef      ,
                     ClkRead   => ClkRef      ,

                     Data_i    => Data_i      ,
                     Dv_i      => DvEn        ,

                     CmdRead   => ReadFifo    ,
                     DecRdAddr => Cnst        ,

                     DataOut   => DataOutInt  ,
                     DvOut     => DvOutInt    ,
                     NbrData   => NbrData     ,
                     FifoFull  => FifoFull    ,

                     VideOut   => VideOut 
                     );

-- Capture Du nombre de Data a Lire

StepCapt(0) <= CmdRead and EdgeSend and not FlagCapt ;                

StepCapt(1) <= '1' when CptCapt="10001" else '0' ;

CaptureNbr : process(ClkRef,resetn)
begin
  if(resetn='0') then
                 NbrDataCapt <= (others => '0') ;
                 FlagCapt    <= '0'             ;
                 CptCapt     <= (others => '0') ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(StepCapt(1)='1') then 
                 NbrDataCapt <= DataNbrRd       ;
                 FlagCapt    <= '1'             ;
                 CptCapt     <= (others => '0') ;
 
        elsif(StepCapt(0)='1') then
                 NbrDataCapt <= (others => '0') ;
                 FlagCapt    <= '0'             ;
                 CptCapt     <= CptCapt + 1     ;

          elsif(CmdRead='0') then 
                 NbrDataCapt <= (others => '0') ;
                 FlagCapt    <= '0'             ;
                 CptCapt     <= (others => '0') ;

      end if;
     end if;
   end if;
end process CaptureNbr;

-- Gestion de la partie lecture

SendId   <= CmdRead     and not StepId                 ; 
SendNbr  <= StepId      and not StepNbrData and NwData ;
SendData <= StepNbrData and not StepSdData  and NwData ;

NbrEgal  <= '0' when CptRdFifo=NbrDataCapt else '1' ;
StopRd   <= NbrEgal and not VideOut and not StopSend;

GstnCptFifo : process(ClkRef,resetn)
begin
  if(resetn='0') then
                   CptRdFifo <= (others => '0') ;


    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(DvOutInt='1') then
                   CptRdFifo <= CptRdFifo + 2 ;

        elsif(CmdRead='0') then
                   CptRdFifo <= (others => '0') ;

      end if;
     end if;
   end if;
end process GstnCptFifo;

GstnLecture : process(ClkRef,resetn)
begin
  if(resetn='0') then
                  ReadFifo    <= '0'             ;
                  StepId      <= '0'             ;
                  StepNbrData <= '0'             ;
                  StepSdData  <= '0'             ;
                  MxData      <= (others => '0') ;
                  NbrDtMemo   <= (others => '0') ;
                  DataTmp     <= (others => '0') ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(CmdRead='0') then 
                  ReadFifo    <= '0'             ;
                  StepId      <= '0'             ;
                  StepNbrData <= '0'             ;
                  StepSdData  <= '0'             ;
                  MxData      <= (others => '0') ;
                  NbrDtMemo   <= (others => '0') ;
                  DataTmp     <= (others => '0') ;

        elsif(SendId='1') then 
                  ReadFifo    <= '0'             ;
                  StepId      <= '1'             ;
                  StepNbrData <= '0'             ;
                  StepSdData  <= '0'             ;
                  MxData      <= Id              ;
                  NbrDtMemo   <= (others => '0') ;
                  DataTmp     <= (others => '0') ;

          elsif(SendNbr='1') then 
--                  ReadFifo    <= StopRd          ;
                  ReadFifo    <= '1'             ;
                  StepId      <= '1'             ;
                  StepNbrData <= '1'             ;
                  StepSdData  <= '0'             ;
--OF CHGMNT                  MxData      <= Cnst & NbrData  ;
--OF CHGMNT                  NbrDtMemo   <= Cnst & NbrData  ;
                  MxData      <= MxDataWd8        ;
                  NbrDtMemo   <= MxDataWd8        ;
                  DataTmp     <= (others => '0') ; 

            elsif(DvOutInt='1') then
                  ReadFifo    <= '0'             ;
                  StepId      <= '1'             ;
                  StepNbrData <= '1'             ;
                  StepSdData  <= '0'             ;
                  MxData      <= MxData          ;
                  NbrDtMemo   <= NbrDtMemo       ;
                  DataTmp     <= DataOutInt      ;

              elsif(SendData='1') then
                  ReadFifo    <= StopRd          ;
                  StepId      <= '1'             ;
                  StepNbrData <= '1'             ;
                  StepSdData  <= '1'             ;
                  MxData      <= DataTmp         ;
                  NbrDtMemo   <= NbrDtMemo       ;
                  DataTmp     <= (others => '0') ;

                else
                  ReadFifo    <= '0'             ;
                  StepId      <= StepId          ;
                  StepNbrData <= StepNbrData     ;
                  StepSdData  <= '0'             ;
                  MxData      <= MxData          ;
                  NbrDtMemo   <= NbrDtMemo       ;
                  DataTmp     <= DataTmp         ;

        end if;
      end if;
  end if;
end process GstnLecture;

-- Gestion de l'envois sur la sortie

PpStep : process(ClkRef)
begin
  if rising_edge (ClkRef) then
    if(ClkEnCom='1') then
-- OF                PpCmdRead <= CmdRead     ;
                 PpId      <= StepId      ;
 
    end if;
  end if;
end process PpStep;

PlseId    <= StepId      and not PpId   ;
 
FinSdData  <= '1' when (CptSendBit(4 downto 0)="10000") else '0' ;

ChgrData   <= FinSdData or PlseId ;--or PlseNbrDt or PlseData ;

EnCptSd    <= EdgeSend and CmdRead;

DetectSup <= '1' when NbrData=X"7fff" else '0'    ;
DetectZer <= '0' when NbrData=X"7ffe" else '1'    ;

PassNbrWd16onWd8 : process(ClkRef,resetn)
begin
  if(resetn='0') then
                 MxDataWd8 <= (others => '0') ;
                 FlagSup   <= '0'             ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(DetectSup='1') then
                 MxDataWd8 <= NbrData + NbrData ;
                 FlagSup   <= '1'             ;

        elsif(FlagSup='1') then
                 MxDataWd8 <= MxDataWd8       ;
                 FlagSup   <= DetectZer       ;

          else 
                 MxDataWd8 <= NbrData + NbrData ;
                 FlagSup   <= '0'             ;
         
      end if;
     end if;
  end if;
end process PassNbrWd16onWd8;

MemoWd8 : process(ClkRef,resetn)
begin
  if(resetn='0') then
                 NbrDtMemoWd8 <= (others => '0') ;
                 PpSendNbr    <= '0'             ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
       if(PpSendNbr='1') then
                 NbrDtMemoWd8 <= MxDataWd8       ;
                 PpSendNbr    <= SendNbr         ;

         else
                 NbrDtMemoWd8 <= NbrDtMemoWd8    ;
                 PpSendNbr    <= SendNbr         ;

       end if;
     end if;
   end if;
end process MemoWd8;


ChgrRg : process(ClkRef,resetn)
begin
  if(resetn='0') then
                 RgDecal    <= (others => '0')           ;
                 CptSendBit <= (others => '0')           ;
                 NwData     <= '0'                       ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(ChgrData='1') then
                 RgDecal    <= MxData                    ; -- OF CHGMNT
                 CptSendBit <= (others => '0')           ;
                 NwData     <= '1'                       ;

        elsif(EnCptSd='1') then
                 RgDecal    <= '0'& RgDecal(15 downto 1) ;
                 CptSendBit <= CptSendBit + 1            ;
                 NwData     <= '0'                       ;

          else
                 RgDecal   <= RgDecal                    ;
                 CptSendBit <= CptSendBit                ;
                 NwData     <= '0'                       ;

      end if;
     end if;
  end if;
end process ChgrRg;

PipValSend : process(ClkRef,resetn)
begin
  if(resetn='0') then
                 DoSpiNw    <= '0'             ;

    elsif rising_edge (ClkRef) then
     if(ClkEnCom='1') then
      if(CmdRead='0') then
                 DoSpiNw    <= '0'             ;

          elsif(EdgeSend='1'and CmdRead='1') then
                 DoSpiNw    <= RgDecal(0)      ;
            else
                 DoSpiNw    <= DoSpiNw         ;

      end if;
     end if;
   end if;
end process PipValSend;

StopCpt <= DvOutInt and not StopSend;

CptNbrDataSend : a_compteur_param
          generic map(SIZE_CPT => 16)
          port map(
                  Clk      => ClkRef   ,
                  ClkEn    => ClkEnCom ,
                  resetn   => resetn   ,
                  Enable   => StopCpt  ,
                  MiseZero => CmdRead  ,
                  DataOut  => CompData    
                  );

-- CompData8b <= (Cnst&CompData) + (Cnst&CompData) ; -- OF CHGN
CompData8b <= CompData + CompData ;

Ginst_Comp : for i in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4)
                       port map    (
                                   dataIn_a   => CompData8b(((i*4)+3) downto i*4),
                                   dataIn_b   => NbrDtMemo(((i*4)+3) downto i*4)  ,
                                   egalOut    => ResultInt(i)
                                   );
end generate Ginst_Comp;

-- Cellule de Pipe 

   ffSpeed : a_reg_memo_param generic map (SIZE_IN => 4)
                              port map  (
                                        enable       => ClkEnCom     ,
                                        dataIn       => ResultInt    ,
                                        samplingClk  => ClkRef       ,
                                        resetn       => resetn       ,
                                        syncDataOut  => ResultIntReg
                                        );

ProcAnd : process(ResultIntReg)
          variable V : STD_LOGIC;
  begin
           V:= ResultIntReg(0);
    for j in 1 to 3 loop
           V:= V AND ResultIntReg(j);
    end loop;

           StopSend <= V;
  end process ProcAnd;

Nc <= VideOut              ; 
Do <= DoSpiNw and CmdRead  ;

end behavioral;

