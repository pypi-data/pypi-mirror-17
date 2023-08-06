library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

entity RS232 is
  generic (
    DataWidth : natural := 16;
    Payload   : natural := 1;
    Header    : std_logic_vector);
    
  port (
    Rst      : in std_logic;
    Clk      : in std_logic;
    
    -- External interface
    SerialRx      : in  std_logic;
    SerialTx      : out std_logic;
    LED_DataIn    : out std_logic;
    LED_Sync      : out std_logic;
    
    -- Network interface
    Rx       : in std_logic;-- Connected to NoC local TX
    AckRx    : out std_logic;-- Connected to NoC local AckTX 
    DataIn   : in std_logic_vector(DataWidth-1 downto 0);-- Connected to NoC local DataOutLocal
    
    Tx       : out std_logic;-- Connected to NoC local RX
    AckTx    : in std_logic;-- Connected to NoC local AckRX
    DataOut  : out std_logic_vector(DataWidth-1 downto 0));-- Connected to NoC local DataInLocal
    
end RS232;

architecture RTL of RS232 is
  -----------------------------------------------------------------------------
  component a_RS232
    port (
        rst_n      : in  std_logic;
        clk_ref    : in  std_logic;
        r_di       : in  std_logic;
        r_do       : out std_logic;
        r_dv_o     : out std_logic;
        r_q        : out std_logic_vector(DataWidth-1 downto 0);
        data_i     : in  std_logic_vector(DataWidth-1 downto 0);
        dv_i       : in  std_logic;
        r_busy_o   : out std_logic;
        led_di_o   : out std_logic;
        led_sync_o : out std_logic);
  end component;
        
  -----------------------------------------------------------------------------
  component NetworkAdapter_HandShake_input
    generic (
      DataWidth : natural;
      Payload   : natural);
    port (
      Rst, Clk  : in  std_logic;
      Rx        : in  std_logic;
      AckRx     : out std_logic;
      DataIn    : in  std_logic_vector(DataWidth-1 downto 0);
      IP_Busy   : in  std_logic;
      IP_Req    : out std_logic;
      IP_DataIn : out std_logic_vector(Payload*DataWidth-1 downto 0));
  end component;
  signal IP_Busy   : std_logic;
  signal IP_Req    : std_logic;
  signal IP_DataIn : std_logic_vector(Payload*DataWidth-1 downto 0);
  signal IP_DataIn_i : std_logic_vector(Payload*DataWidth-1 downto 0);
  
  -----------------------------------------------------------------------------
  component NetworkAdapter_HandShake_output
    generic (
      DataWidth : natural;
      Payload   : natural;
      Header    : std_logic_vector);
    port (
      Rst, Clk     : in  std_logic;
      Tx           : out std_logic;
      AckTx        : in  std_logic;
      DataOut      : out std_logic_vector(DataWidth-1 downto 0);
      IP_DataValid : in  std_logic;
      IP_Wait      : out std_logic;
      IP_DataOut   : in  std_logic_vector(Payload*DataWidth-1 downto 0));
  end component;
  signal IP_DataValid : std_logic;
  signal IP_Wait      : std_logic;
  signal IP_DataOut   : std_logic_vector(Payload*DataWidth-1 downto 0);
  
  -----------------------------------------------------------------------------
begin


  IP_DataIn_i <= IP_DataIn when IP_Req='1' else IP_DataIn_i;
  --IP_Busy     <= '1' when IP_Wait='1' else '0';
  -----------------------------------------------------------------------------
  ValidateData: process (Clk, Rst)
  begin  -- process ValidateData
    if Rst = '0' then                   -- asynchronous reset (active low)
      IP_DataValid <= '0';
    elsif Clk'event and Clk = '1' then  -- rising clock edge
      if Rx = '1' and IP_Wait='0' then
        IP_DataValid <='1';
      else
        IP_DataValid <= '0';
      end if;
    end if;
  end process ValidateData;
  -----------------------------------------------------------------------------
  RS232_CORE: a_RS232
    port map (
        rst_n      => Rst,
        clk_ref    => Clk,
        r_di       => SerialRx,
        r_do       => SerialTx,
        r_dv_o     => IP_DataValid,
        r_q        => IP_DataOut,
        data_i     => IP_DataIn,
        dv_i       => IP_Req,
        r_busy_o   => IP_Busy,
        led_di_o   => LED_DataIn,
        led_sync_o => LED_Sync);
  -----------------------------------------------------------------------------
  NetworkAdapter_HandShake_input_1: NetworkAdapter_HandShake_input
    generic map (
      DataWidth => DataWidth,
      Payload   => Payload)
    port map (
      Rst       => Rst,
      Clk       => Clk,
      Rx        => Rx,
      AckRx     => AckRx,
      DataIn    => DataIn,
      IP_Busy   => IP_Busy,
      IP_Req    => IP_Req,
      IP_DataIn => IP_DataIn);
  -----------------------------------------------------------------------------

  -----------------------------------------------------------------------------
  
  
end RTL;

