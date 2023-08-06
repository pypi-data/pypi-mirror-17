----------------------------------------------------------------------------------------------------
-- Actual File Name      = MsgGen.vhd
-- Title & purpose       = Message builder: 
-- Author                = Matthieu PAYET (ADACSYS)
-- Creation Date         = 02/10/2012
-- Version               = 0.1
-- Simple Description    = 
-- Specific issues       =
-- Speed                 =
-- Area estimates        =
-- Tools (version)       = Xilinx ISE (13.1)
-- HDL standard followed = VHDL 93 / 2001 standard
-- Revisions & ECOs      =
----------------------------------------------------------------------------------------------------


library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: Message builder
-------------------------------------------------------------------------------
entity MsgGen is
  
  generic (
    MsgSize    : natural := 1;
    QueueDepth : natural := 32;
    DataWidth  : natural := 16);

  port (
    RST, CLK         : in  std_logic;
    
    -- CLK Manager interface
    Stretch_ON       : out std_logic;
    
    -- IP interface
    IP_DataOutValid  : in std_logic;
    IP_DataOut       : in std_logic_vector(DataWidth-1 downto 0);
    
    -- Output flux control interface
    MSG_DataOutValid : out std_logic;
    MSG_DataOut      : out std_logic_vector(DataWidth-1 downto 0));
    
end MsgGen;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture Behavioral_v0 of MsgGen is

  type QueueState is (STATE_RST, STATE_HEADER, STATE_SENDING, STATE_NEXT);

  signal CurState_i, FutState_i : QueueState := STATE_RST;
  
  signal FIFO_DataIn_i        : std_logic_vector(DataWidth-1 downto 0);
  signal FIFO_DataOut_i       : std_logic_vector(DataWidth-1 downto 0);
  signal FIFO_DataIn_WR_i     : std_logic := '0';
  signal FIFO_DataOut_RD_i    : std_logic := '0';
  signal FIFO_DataOut_AckRD_i : std_logic := '0';
  signal FIFO_DataIn_AckWR_i  : std_logic := '0';
  signal FIFO_WR_i            : std_logic := '0';
  signal FIFO_RD_i            : std_logic := '0';
  signal FIFO_Empty_i         : std_logic := '0';
  signal FIFO_Full_i          : std_logic := '0';
  signal NbPackets_i          :natural := MsgSize;
  constant Address            : std_logic_vector(DataWidth-1 downto 0) := X"0022";
  
begin  -- v0
  -----------------------------------------------------------------------------
  fifo_out_diff_1: entity work.fifo_out_diff
    generic map (
      inbitt  => DataWidth,
      outbitt => DataWidth,
      mode    => 1,
      nb_mot  => QueueDepth)
    port map (
      rst       => RST,
      clk_in    => CLK,
      clk_out   => CLK,
      wr        => FIFO_WR_i,
      r         => FIFO_RD_i,
      empty     => FIFO_Empty_i,
      full      => FIFO_Full_i,
      data_en   => FIFO_DataIn_i,
      data_sort => FIFO_DataOut_i,
      led       => open);
  
  -----------------------------------------------------------------------------
  -- FIFO driver
  -----------------------------------------------------------------------------
  FIFO_WR_i <= '1' when IP_DataOutValid='1' and CLK='1' else
               '0';
  FIFO_RD_i <= '1' when CurState_i=STATE_NEXT else
               '0';
  FIFO_DataIn_i <= IP_DataOut when IP_DataOutValid='1' else
                   FIFO_DataIn_i;
  
  -----------------------------------------------------------------------------
  Stretch_ON <= '1' when FIFO_Full_i='1' else
                '0';
  -----------------------------------------------------------------------------  
  -- FSM Memory allocation
  -----------------------------------------------------------------------------
  FSM_Memory: process (CLK, RST)
  begin  -- process FSM_Memory
    if RST = '1' then                 -- asynchronous RST (active high)
      CurState_i <= STATE_RST;
      NbPackets_i<= 0;
    elsif rising_edge(CLK) then  -- rising CLK edge
      CurState_i <= FutState_i;
      if FutState_i=STATE_SENDING then
        NbPackets_i<=NbPackets_i-1;
      elsif FutState_i=STATE_RST then
        NbPackets_i<=MsgSize;
      else
        NbPackets_i<=NbPackets_i;
      end if;
    end if;
  end process FSM_Memory;
  
  -----------------------------------------------------------------------------
  FutState_i <= STATE_HEADER  when not FIFO_Empty_i='1' and NbPackets_i=MsgSize else
                STATE_SENDING when not FIFO_Empty_i='1' and (CurState_i=STATE_SENDING or CurState_i=STATE_NEXT) else
                STATE_NEXT    when CurState_i=STATE_SENDING and NbPackets_i<MsgSize and NbPackets_i/=0 else
                STATE_RST   when NbPackets_i=0;
  -----------------------------------------------------------------------------
  MSG_DataOutValid <= '1' when CurState_i=STATE_SENDING or CurState_i=STATE_HEADER else
                      '0';
  MSG_DataOut      <= Address when CurState_i=STATE_HEADER else 
                      FIFO_DataOut_i;
    
end Behavioral_v0;


























