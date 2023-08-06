--------------------------------------------------------------------------------
-- Company:       ADACSYS
-- Engineer: 
--
-- Create Date:    20/04/2013
-- Design Name:
-- Module Name:    a_Spi.vhd
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

entity a_Spi_Oli is
  Port(
--- Control Signals
      resetn   : in  STD_LOGIC                     ; -- Actif niveau Bas
      resetmem : in  STD_LOGIC                     ;
      ClkRef   : in  STD_LOGIC                     ; -- Clock Reference
      ClkEnCom : in  STD_LOGIC                     ;

      cs_spi   : in  STD_LOGIC                     ;
      clk_spi  : in  STD_LOGIC                     ;
      di_spi   : in  STD_LOGIC                     ;
      do_spi   : out STD_LOGIC                     ;

      r_dv_o   : out STD_LOGIC                     ;
      r_q      : out STD_LOGIC_VECTOR(15 downto 0) ;

      Data_i   : in  STD_LOGIC_VECTOR(15 downto 0) ;
      Dv_i     : in  STD_LOGIC                     ;
      r_busy_o : out STD_LOGIC                     ;

      LedRead  : out STD_LOGIC                     ;

      NcWire   : out STD_LOGIC
      );
end a_Spi_Oli;

architecture behavioral of a_Spi_Oli is

-- Description des Signaux Internes

signal DataInt     : STD_LOGIC_VECTOR(15 downto 0) ;
signal CptWd       : STD_LOGIC_VECTOR( 3 downto 0) ;

signal StartComp   : STD_LOGIC ;
signal StopComp    : STD_LOGIC ;
signal DataEgal    : STD_LOGIC ;

signal cs_rf       : STD_LOGIC ;
signal clkspi_ff   : STD_LOGIC ;
signal di_rf       : STD_LOGIC ;
signal clkspi_rf   : STD_LOGIC ;

signal DataCapt    : STD_LOGIC_VECTOR(15 downto 0) ;
signal DvCapt      : STD_LOGIC                     ;
signal DvCaptPipe  : STD_LOGIC                     ;
signal CompResult  : STD_LOGIC                     ;
signal CompCal     : STD_LOGIC                     ;

signal DataOut     : STD_LOGIC_VECTOR(15 downto 0) ;
signal DvOut       : STD_LOGIC                     ;
signal FlagComp    : STD_LOGIC                     ;
signal SendData    : STD_LOGIC                     ;
signal DoInt       : STD_LOGIC                     ;
signal DoIntNw     : STD_LOGIC                     ;
signal DataDoPipe  : STD_LOGIC_VECTOR(19 downto 0) ;
signal PipeDo      : STD_LOGIC_VECTOR(19 downto 0) ;
signal Nc          : STD_LOGIC                     ;
signal NcNw        : STD_LOGIC                     ;
signal MiseAZero   : STD_LOGIC                     ;
--signal DoFinal     : STD_LOGIC                     ;
--signal DoFinal2     : STD_LOGIC                     ;
--signal DoFinal3     : STD_LOGIC                     ;
--signal DoFinal4     : STD_LOGIC                     ;


constant VarComp  : STD_LOGIC_VECTOR(15 downto 0) := X"ffff" ;
constant ProgReg  : STD_LOGIC                     := '0'     ;

signal VerifNw    : STD_LOGIC_VECTOR(13 downto 0) ;
--signal Verifw     : STD_LOGIC_VECTOR(13 downto 0) ;

component a_GenClkSpi
  Port(
--- Control Signals
      resetn    : in  STD_LOGIC                     ; -- Actif niveau Bas
      ClkRef    : in  STD_LOGIC                     ; -- Clock Reference
      ClkEnCom  : in  STD_LOGIC                     ;

      cs        : in  STD_LOGIC                     ;
      clkspi    : in  STD_LOGIC                     ;
      di        : in  STD_LOGIC                     ;

      cs_rf     : out STD_LOGIC                     ;-- \
      clkspi_ff : out STD_LOGIC                     ;--  > Synchronisation sur ClkRef
      di_rf     : out STD_LOGIC                     ;-- /

      clkspi_rf : out STD_LOGIC                     
      );
end component;

component a_CompSpi
  generic(DataComp : STD_LOGIC_VECTOR(15 downto 0) := X"ffff");
  Port(
      resetn    : in   STD_LOGIC                     ;
      ClkRef    : in   STD_LOGIC                     ;
      ClkEnCom  : in   STD_LOGIC                     ;

      StartComp : in  STD_LOGIC                      ;
      StopComp  : in  STD_LOGIC                      ;
      dataIn    : in  STD_LOGIC_VECTOR (15 downto 0) ;

      DataEgal  : out STD_LOGIC
      );
end component;

component a_DeSerialSpi
  Port(
--- Control Signals
      resetn    : in  STD_LOGIC                     ; -- Actif niveau Bas
      clkRef    : in  STD_LOGIC                     ; -- Clock Reference
      ClkEnCom  : in   STD_LOGIC                     ;

      cs        : in  STD_LOGIC                     ;
      clkspi    : in  STD_LOGIC                     ;
      di        : in  STD_LOGIC                     ;

      enable    : in  STD_LOGIC                     ;

      StartComp : out STD_LOGIC                     ;
      r_dv_o    : out STD_LOGIC                     ;
      r_q       : out STD_LOGIC_VECTOR(15 downto 0)
      );
end component;

--component a_compteur_param
--  generic (
--          SIZE_CPT: integer := 4);
--  port(
--          Clk       : in   STD_LOGIC;
--          ClkEn     : in   STD_LOGIC;
--          resetn    : in   STD_LOGIC;
--          Enable    : in   STD_LOGIC;
--          MiseZero  : in   STD_LOGIC;
--          DataOut   : out  STD_LOGIC_VECTOR (SIZE_CPT-1  downto 0)
--       );
--end component;

component a_SendDataSpi
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
-- OF      Verif     : out STD_LOGIC_VECTOR(13 downto 0)        ;
-- OF      Verifw    : out STD_LOGIC_VECTOR(13 downto 0)        ;
      Nc        : out STD_LOGIC
      );
end component;

component a_reg_memo_param
  generic (
         SIZE_IN : integer := 32);
  Port (
        enable            : in   STD_LOGIC                              ;
        dataIn            : in   STD_LOGIC_VECTOR (SIZE_IN-1  downto 0) ;
        samplingClk       : in   STD_LOGIC                              ;
        resetn            : in   STD_LOGIC                              ;
        syncDataOut       : out  STD_LOGIC_VECTOR (SIZE_IN-1  downto 0)
       );
end component;

  begin

-- Synchronisation des entrees 

u_GenSync : a_GenClkSpi
            port map(
--- Control Signals
            resetn    => resetn    , -- Actif niveau Bas
            ClkRef    => ClkRef    , -- Clock Reference
            ClkEnCom  => ClkEnCom  ,

            cs        => cs_spi    ,
            clkspi    => clk_spi   ,
            di        => di_spi    ,

            cs_rf     => cs_rf     , -- \
            clkspi_ff => clkspi_ff , --  > Synchronisation sur ClkRef
            di_rf     => di_rf     , -- /

            clkspi_rf => clkspi_rf
            );

-- Creation du Vector 16 bits

u_DeSirial : a_DeSerialSpi
             port map(
--- Control Signals
                     resetn    => resetn    ,
                     clkRef    => ClkRef    ,
                     ClkEnCom  => ClkEnCom  ,

                     cs        => cs_rf     ,
                     clkspi    => clkspi_ff ,
                     di        => di_rf     ,

                     enable    => DataEgal  ,

                     StartComp => StartComp ,

                     r_dv_o    => r_dv_o    ,
                     r_q       => DataInt
                     );

-- Module de Detection de Read Fifo

u_comparateur : a_CompSpi
                generic map(DataComp => X"ffff")
                port map(
                        resetn    => resetn    ,
                        ClkRef    => ClkRef    ,
                        ClkEnCom  => ClkEnCom  ,

                        StartComp => StartComp ,
                        StopComp  => cs_rf     ,
                        dataIn    => DataInt   ,

                        DataEgal  => DataEgal
                        );

-- Module D'envois des Donnees

u_SendDataSpi : a_SendDataSpi
             port map(
                     resetn    => resetn    ,
                     resetmem  => resetmem  ,
                     ClkRef    => ClkRef    ,
                     ClkEnCom  => ClkEnCom  ,
                     EdgeSend  => clkspi_ff ,

                     DataNbrRd => DataInt   ,

                     Data_i    => Data_i    ,
                     Dv_i      => Dv_i      ,

                     CmdRead   => DataEgal  ,

                     Do        => DoInt     ,
                     FifoFull  => r_busy_o  ,
                     Nc        => Nc
                     );

-- A voir si necessaire avec Sylvain Pipe pour latence de Read

DataDoPipe <= PipeDo(18 downto 0) & DoInt;
MiseAZero  <= resetn and not cs_spi ;

PipeLatence : a_reg_memo_param 
              generic map(SIZE_IN => 20)
              port map(
                      enable      => clkspi_ff  , -- Version 10 Mhz
                      dataIn      => DataDoPipe ,
                      samplingClk => ClkRef     ,
                      resetn      => MiseAZero  ,
                      syncDataOut => PipeDo
                      );

do_spi <= PipeDo(14) ; -- pour 10 Mhz

NcWire   <= clkspi_rf and PipeDo(19) and PipeDo(18) and PipeDo(17) and PipeDo(16) and PipeDo(15) ;--and Nc ;
r_q      <= DataInt    ;
LedRead  <= DataEgal   ;
--r_busy_o <= DataEgal  ;

end behavioral;
