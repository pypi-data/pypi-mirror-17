----------------------------------------------------------------------------------------------------
-- Actual File Name      = HSinput.vhd
-- Title & purpose       = Intput controler for handshake network interface
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
-- ENTITY: Handshake input adapter
-------------------------------------------------------------------------------
entity HSinput is
  
  generic (
    DataWidth : natural := 16);

  port (
    RST, CLK  : in  std_logic;
       
    -- Network interface
    RxLocal       : in  std_logic;    -- Connected to NoC local TX
    AckRxLocal    : out std_logic;    -- Connected to NoC local AckTX
    DataInLocal   : in  std_logic_vector(DataWidth-1 downto 0); -- Connected to NoC local DataOutLocal
    
    -- IP interface
    IP_Busy        : in std_logic;    -- Connected to NoC local RX
    IP_DataInValid : out  std_logic;    -- Connected to NoC local AckRX
    IP_DataIn      : out std_logic_vector(DataWidth-1 downto 0)); -- Connected to NoC local DataInLocal 
  
end HSinput;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture Behavioral_v0 of HSinput is

  type HS_STATE_R is (STATE_IDLE, STATE_ACK);
  
  signal R_CurState_i, R_FutState_i: HS_STATE_R := STATE_IDLE;
  signal IP_DataIn_BUF_i : std_logic_vector(DataWidth-1 downto 0);
    
begin  -- v0
 
  -----------------------------------------------------------------------------
  -- State memorization
  StateMemory: process (CLK, RST)
  begin  -- process StateMemory
    if RST = '1' then                 -- asynchronous RST (active high)
      R_CurState_i<= STATE_IDLE;
    elsif rising_edge(CLK) then  -- rising CLK edge
      R_CurState_i<= R_FutState_i;
    end if;
  end process StateMemory;
  
  -----------------------------------------------------------------------------
  -- Reception State allocation
  R_FutState_i <= STATE_ACK  when R_CurState_i=STATE_IDLE and RxLocal='1' and IP_Busy='0' else
               STATE_IDLE when R_CurState_i=STATE_ACK  and RxLocal='0';
  
  -----------------------------------------------------------------------------
  -- Reception output allocation
  IP_DataIn_BUF_i <= DataInLocal when RxLocal='1' else
                     IP_DataIn_BUF_i;
                  
  IP_DataIn <= IP_DataIn_BUF_i;
  
  AckRxLocal <= '1' when R_CurState_i=STATE_ACK else
                '0';
  
  IP_DataInValid <= RxLocal;
  
end Behavioral_v0;


























