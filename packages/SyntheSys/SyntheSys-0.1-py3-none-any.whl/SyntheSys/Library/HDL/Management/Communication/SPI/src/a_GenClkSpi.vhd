--------------------------------------------------------------------------------
-- Company:       ADACSYS
-- Engineer:      OF
--
-- Create Date:    08/05/2013
-- Design Name:
-- Module Name:    a_GenClkSpi.vhd
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

entity a_GenClkSpi is
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
      di_rf     : out STD_LOGIC                     ; -- /

      clkspi_rf : out STD_LOGIC                     
      );
end a_GenClkSpi;

architecture behavioral of a_GenClkSpi is

-- Description des Signaux Internes

signal DataIn      : STD_LOGIC_VECTOR(2 downto 0)  ;
signal DataSync    : STD_LOGIC_VECTOR(2 downto 0)  ;
signal PipeClkSpi  : STD_LOGIC_VECTOR(1 downto 0)  ;
signal DiCsPipe    : STD_LOGIC_VECTOR(1 downto 0)  ;
signal DiCsInt     : STD_LOGIC_VECTOR(1 downto 0)  ;

signal ClkSpiIn    : STD_LOGIC_VECTOR(1 downto 0)  ;
signal FrontUp     : STD_LOGIC                     ;
signal FrontDown   : STD_LOGIC                     ;

component a_reg_memo_param
         generic (SIZE_IN: integer := 32);
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

DataIn <= Di & ClkSpi & Cs ;

SyncIn : a_reg_memo_param
          generic map(SIZE_IN => 3)
          port map(
                  enable      => ClkEnCom ,
                  dataIn      => DataIn   ,
                  samplingClk => ClkRef   ,
                  resetn      => resetn   ,
                  syncDataOut => DataSync
                  );

-- Synchronisation Interne par rapport a ClkSpi

DiCsPipe <= DataSync(2) & DataSync(0) ;

PipeIn : a_reg_memo_param
          generic map(SIZE_IN => 2)
          port map(
                  enable      => ClkEnCom ,
                  dataIn      => DiCsPipe ,
                  samplingClk => ClkRef   ,
                  resetn      => resetn   ,
                  syncDataOut => DiCsInt
                  );


-- Generation Front montant et descendant ClkSpi
ClkSpiIn <= PipeClkSpi(0) & DataSync(1);

PipePourGenFrontClk : a_reg_memo_param
                      generic map(SIZE_IN => 2)
                      port map(
                              enable      => ClkEnCom   ,
                              dataIn      => ClkSpiIn   ,
                              samplingClk => ClkRef     ,
                              resetn      => resetn     ,
                              syncDataOut => PipeClkSpi
                              );

FrontUp   <=     PipeClkSpi(0) and not PipeClkSpi(1) ;
FrontDown <= not PipeClkSpi(0) and     PipeClkSpi(1) ;

cs_rf     <= DiCsInt(0)  ;
clkspi_ff <= FrontDown   ;
di_rf     <= DiCsInt(1)  ;
clkspi_rf <= FrontUp     ;

end behavioral;

