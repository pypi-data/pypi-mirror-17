
----------------------------------------------------------------------------------------------------
-- Actual File Name      = FifoToHandShake.vhd
-- Title & purpose       = NoC router input: Handshake protocol to FIFO converter
-- Author                = Matthieu PAYET (ADACSYS) - matthieu.payet@adacsys.com
-- Creation Date         = 2012-12-10 19:30
-- Version               = 0.1
-- Simple Description    = Convert asynchronous Handshake protocol to FIFO protocol
-- Specific issues       = 
-- Speed                 = 
-- Area estimates        = 
-- Tools (version)       = Xilinx ISE (13.1)
-- HDL standard followed = VHDL 2001 standard
-- Revisions & ECOs      = 1.0
----------------------------------------------------------------------------------------------------
	
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;

-------------------------------------------------------------------------------
-- ENTITY: Handshake protocol to FIFO converter
-------------------------------------------------------------------------------
entity FifoToHandShake is
  
  generic (
    FlitWidth : natural := 16);

  port (
    Clk          : in  std_logic;
    Rst          : in  std_logic;
    
    HS_Tx        : out std_logic;
    HS_AckTx     : in  std_logic;
    HS_DataOut   : out std_logic_vector(FlitWidth-1 downto 0);
    
    FIFO_DataOut : in  std_logic_vector(FlitWidth-1 downto 0);
    FIFO_Read    : out std_logic;
    FIFO_IsEmpty : in  std_logic
    );

end FifoToHandShake;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, manage Handshake protocol
-------------------------------------------------------------------------------
architecture RTL of FifoToHandShake is

  type FSM_HS is (WAIT_FIFO, REQUEST);--, ACKNOWLEDGE);
  signal CurrentState_i : FSM_HS := WAIT_FIFO;
--  signal DataToSend : std_logic_vector(FlitWidth-1 downto 0);
  
begin  -- RTL

-----------------------------------------------------------------------------
	HS_DataOut <= FIFO_DataOut;
	------------------------------------------------------------
	-- Process FSMStateAssignment : FSM State assignments
	FSMStateAssignment: process(Clk, Rst)
	begin
		if (Rst = '1') then 
			CurrentState_i <= WAIT_FIFO;
		else 
			if rising_edge(Clk) then 
				case CurrentState_i is -- Assignments for FSM FuturState
					when WAIT_FIFO =>
						if FIFO_IsEmpty='0' then 
							CurrentState_i <= REQUEST;
						end if;
					when REQUEST =>
						if HS_AckTx='1' then
							if FIFO_IsEmpty='1' then 
								CurrentState_i <= WAIT_FIFO;
							end if;
						end if;
--					when WAIT_LAST_ACK =>
--						if HS_AckTx='1' then
--							if FIFO_IsEmpty='1' then 
--								CurrentState_i <= WAIT_FIFO;
--							else
--								CurrentState_i <= REQUEST;
--							end if;
--						end if;
					when others => null;
				end case;
				
			end if;
		end if;
	
	end process;
	------------------------------------------------------------
	
	------------------------------------------------------------
	-- Process FSMSignalAssignments_InputAdapter_FSM : Signal assignments according to InputAdapter_FSM FSM state.
	FSMSignalAssignments: process(CurrentState_i, FIFO_IsEmpty, HS_AckTx)
	
	begin
	
		case CurrentState_i is -- Assignments for FSM FuturState
			when WAIT_FIFO =>
				if FIFO_IsEmpty='0' then 
					FIFO_Read <= '1';
				else 
					FIFO_Read <= '0';
				end if;
				HS_Tx     <= '0';
				
			when REQUEST =>
				if HS_AckTx='1' then
					if FIFO_IsEmpty='0' then 
						HS_Tx <= '1';
						FIFO_Read <= '1';
					else 
						--  WAIT_LAST_ACK
						HS_Tx <= '0';
						FIFO_Read <= '0';
					end if;
				else 
					HS_Tx <= '1';
					FIFO_Read <= '0';
				end if;
				
--			when WAIT_LAST_ACK =>
--				if HS_AckTx='1' then
--					HS_Tx     <= '0';
--					if FIFO_IsEmpty='1' then 
--						FIFO_Read <= '0';
--					else
--						FIFO_Read <= '1';
--					end if;
--				else
--					HS_Tx <= '1';
--					FIFO_Read <= '0';
--				end if;
				
			when others =>
				FIFO_Read <= '0';
				HS_Tx     <= '0';
		end case;
		
	
	end process;
	------------------------------------------------------------

end RTL;


