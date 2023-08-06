----------------------------------------------------------------------------------------------------
-- Actual File Name      = HSoutput.vhd
-- Title & purpose       = Output controler for handshake network interface
-- Author                = Matthieu PAYET (ADACSYS)
-- Creation Date         = 02/10/2012
-- Version               = 0.1
-- Simple Description    = Flux control adapter for generic IP to Handshake protocol.
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
-- ENTITY: NI Hanshake output flux control adapter
-------------------------------------------------------------------------------
entity HSoutput is
  
  generic (
    DataWidth : natural := 16);

  port (
    RST, CLK    : in  std_logic;
    
    -- Network interface
    TxLocal         : out std_logic;    -- Connected to NoC local RX
    AckTxLocal      : in  std_logic;    -- Connected to NoC local AckRX
    DataOutLocal    : out std_logic_vector(DataWidth-1 downto 0); -- Connected to NoC local DataInLocal 
    
    -- Message builder interface
    DataOutValid    : in std_logic;
    DataOut         : in std_logic_vector(DataWidth-1 downto 0));
  
end HSoutput;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture Behavioral_v0 of HSoutput is

  type HS_STATE_T is (STATE_IDLE, STATE_SEND);
  
  signal T_CurState_i, T_FutState_i : HS_STATE_T := STATE_IDLE;
  
  signal OutBuffer_i    : std_logic_vector(DataWidth-1 downto 0) := (others=>'0');
  
begin  -- v0

  -----------------------------------------------------------------------------
  -- State memorization
  StateMemory: process (CLK, RST)
  begin  -- process StateMemory
    if RST = '1' then                 -- asynchronous RST (active high)
      T_CurState_i <= STATE_IDLE;
    elsif rising_edge(CLK) then  -- rising CLK edge
      T_CurState_i <= T_FutState_i;
    end if;
  end process StateMemory;
    
  -----------------------------------------------------------------------------
  -- Transmission State allocation
  T_FutState_i <= STATE_SEND when T_CurState_i=STATE_IDLE and DataOutValid='1' else
                  STATE_IDLE when T_CurState_i=STATE_SEND and AckTxLocal='1';
  
  -----------------------------------------------------------------------------
  -- Transmission output allocation
  DataOutLocal <= OutBuffer_i;
  OutBuffer_i  <= DataOut when DataOutValid='1' else -- Get data before state STATE_SEND
                  OutBuffer_i;
  TxLocal      <= '1' when T_CurState_i=STATE_SEND else
                  '0';
  
  -----------------------------------------------------------------------------
  
  
end Behavioral_v0;


























