----------------------------------------------------------------------------------------------------
-- Actual File Name      = RS232_HandShake.vhd
-- Title & purpose       = RS232 HandShake wrapper for Network on chip connection
-- Author                = Matthieu PAYET (ADACSYS)
-- Creation Date         = 02/10/2012
-- Version               = 0.1
-- Simple Description    = Connect RS232 core to Handshake input/output controler and Message builder.
-- Specific issues       =
-- Speed                 =
-- Area estimates        =
-- Tools (version)       = Xilinx ISE (13.1)
-- HDL standard followed = VHDL 93 / 2001 standard
-- Revisions & ECOs      =
----------------------------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.STD_LOGIC_arith.ALL;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: RS232 Handshake adapter
-------------------------------------------------------------------------------
entity RS232_HandShake is
  
  generic (
    DataWidth : natural := 16);

  port (
    RST, CLK    : in  std_logic;
    
    -- External interface
    Rx              : in  std_logic;
    Tx              : out std_logic;
    LED_DataIn      : out std_logic;
    LED_Sync        : out std_logic;
    
    -- Network interface
    RxLocal         : in  std_logic;    -- Connected to NoC local TX
    AckRxLocal      : out std_logic;    -- Connected to NoC local AckTX
    DataInLocal     : in  std_logic_vector(DataWidth-1 downto 0); -- Connected to NoC local DataOutLocal
    
    TxLocal         : out std_logic;    -- Connected to NoC local RX
    AckTxLocal      : in  std_logic;    -- Connected to NoC local AckRX
    DataOutLocal    : out std_logic_vector(DataWidth-1 downto 0)); -- Connected to NoC local DataInLocal 
  
end RS232_HandShake;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture Behavioral_v0 of RS232_HandShake is

  signal IP_DataOutValid_i  : std_logic :='0';
  signal IP_DataOut_i       : std_logic_vector(DataWidth-1 downto 0);
  signal IP_DataIn_i        : std_logic_vector(DataWidth-1 downto 0);
  signal IP_DataInValid_i   : std_logic :='0';
  signal IP_Busy_i          : std_logic :='0';
  signal MSG_DataOutValid_i : std_logic :='0';
  signal MSG_DataOut_i      : std_logic_vector(DataWidth-1 downto 0);

begin  -- v0

  -----------------------------------------------------------------------------
  RS232_CORE: entity work.a_RS232
    port map (
        rst_n      => RST,
        clk_ref    => CLK,
        r_di       => Rx,
        r_do       => Tx,
        r_dv_o     => IP_DataOutValid_i,
        r_q        => IP_DataOut_i,
        data_i     => IP_DataIn_i,
        dv_i       => IP_DataInValid_i,
        r_busy_o   => IP_Busy_i,
        led_di_o   => LED_DataIn,
        led_sync_o => LED_Sync);
  
  -----------------------------------------------------------------------------
  MsgGen_1: entity work.MsgGen
    generic map (
      MsgSize    => 2,  -- 2 packets per message
      QueueDepth => 32, -- Fifo buffer depth = 32
      DataWidth  => DataWidth) -- x=2, y=2
    port map (
      RST              => RST,
      CLK              => CLK,
      Stretch_ON       => open,
      IP_DataOutValid  => IP_DataOutValid_i,
      IP_DataOut       => IP_DataOut_i,
      MSG_DataOutValid => MSG_DataOutValid_i,
      MSG_DataOut      => MSG_DataOut_i);

  -----------------------------------------------------------------------------
  HSinput_1: entity work.HSinput
    generic map (
      DataWidth => DataWidth)
    port map (
      RST         => RST,
      CLK         => CLK,
      RxLocal     => RxLocal,
      AckRxLocal  => AckRxLocal,
      DataInLocal => DataInLocal,
      IP_Busy        => IP_Busy_i,
      IP_DataInValid => IP_DataInValid_i,
      IP_DataIn      => IP_DataIn_i);

  -----------------------------------------------------------------------------
  HSoutput_1: entity work.HSoutput
    generic map (
      DataWidth => DataWidth)
    port map (
      RST          => RST,
      CLK          => CLK,
      TxLocal      => TxLocal,
      AckTxLocal   => AckTxLocal,
      DataOutLocal => DataOutLocal,
      DataOutValid => MSG_DataOutValid_i,
      DataOut      => MSG_DataOut_i);
 
end Behavioral_v0;


























