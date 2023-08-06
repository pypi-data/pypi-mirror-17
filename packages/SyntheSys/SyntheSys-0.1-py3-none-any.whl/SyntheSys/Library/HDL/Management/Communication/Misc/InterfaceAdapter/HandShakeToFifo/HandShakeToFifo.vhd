
----------------------------------------------------------------------------------------------------
-- Actual File Name      = HandshakeToFifo.vhd
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

-------------------------------------------------------------------------------
-- ENTITY: Handshake protocol to FIFO converter
-------------------------------------------------------------------------------
entity HandShakeToFifo is

	generic (
		GALS      : boolean :=True;
		FlitWidth : natural := 16);
	port (
		Clk         : in  std_logic;
		Rst         : in std_logic;

		HS_Rx       : in  std_logic;
		HS_AckRx    : out std_logic;
		HS_DataIn   : in  std_logic_vector(FlitWidth-1 downto 0);

		FIFO_DataIn : out std_logic_vector(FlitWidth-1 downto 0);
		FIFO_Write  : out std_logic;
		FIFO_IsFull : in  std_logic
--		DEBUG_VECTOR1     : OUT  std_logic_vector(FlitWidth-1 downto 0);
--		DEBUG_VECTOR2     : OUT  std_logic_vector(FlitWidth-1 downto 0);
--		DEBUG_VECTOR3     : OUT  std_logic_vector(FlitWidth-1 downto 0)--;
--		DEBUG_VECTOR4     : OUT  std_logic_vector(FlitWidth-1 downto 0)
	);

end HandShakeToFifo;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, manage Handshake protocol
-------------------------------------------------------------------------------
architecture RTL of HandShakeToFifo is

	type FSM_HS is (WAIT_REQUEST, ACKNOWLEDGE);
	signal CurrentState_i : FSM_HS := WAIT_REQUEST;
	signal DataToSend : std_logic_vector(FlitWidth-1 downto 0);
	
	signal HS_AckRx_i : std_logic;

begin  -- RTL

--	DEBUG_VECTOR1 <= HS_DataIn;
--	DEBUG_VECTOR2 <= DataToSend;
--	DEBUG_VECTOR3 <= DataToSend;
--	DEBUG_VECTOR4 <= x"000" & '0' & FIFO_IsFull & HS_Rx & '0';
--	MultiSyncMode : if GALS=True generate
--		-----------------------------------------------------------------------------
--		FIFO_DataIn <= DataToSend;
--		------------------------------------------------------------
--		-- Process FSMStateAssignment : FSM State assignments
--		FSMStateAssignment: process(Clk, Rst)
--		begin
--			if (Rst = '1') then 
--				CurrentState_i <= WAIT_REQUEST;
--				DataToSend     <= (others=>'0');
--			else 
--				if rising_edge(Clk) then 
--					case CurrentState_i is -- Assignments for FSM FuturState
--						when WAIT_REQUEST =>
--							if HS_Rx='1' and not FIFO_IsFull='1' then 
--								CurrentState_i <= ACKNOWLEDGE;
--								DataToSend  <= HS_DataIn; -- and HS_Rx='1' and not FIFO_IsFull='1'
--							else 
--								CurrentState_i <= WAIT_REQUEST;
--							end if;
--						when ACKNOWLEDGE =>
--							CurrentState_i <= WAIT_REQUEST;
--						when others => null;
--					end case;
--				
--				end if;
--			end if;
--	
--		end process;
--		------------------------------------------------------------
--	
--		------------------------------------------------------------
--		-- Process FSMSignalAssignments_InputAdapter_FSM : Signal assignments according to InputAdapter_FSM FSM state.
--		FSMSignalAssignments: process(CurrentState_i)
--	
--		begin
--	
--			case CurrentState_i is -- Assignments for FSM FuturState
--				when WAIT_REQUEST =>
--					HS_AckRx    <= '0'; -- and HS_Rx='1'
--					FIFO_Write  <= '0';
--				when ACKNOWLEDGE =>
--	--				DataToSend  <= DataToSend; -- and HS_Rx='1' and not FIFO_IsFull='1'
--					HS_AckRx    <= '1'; -- and HS_Rx='1'
--					FIFO_Write  <= '1';
--				when others =>
--	--				DataToSend  <= (others=>'0'); -- and HS_Rx='1' and not FIFO_IsFull='1'
--					HS_AckRx    <= '0'; -- and HS_Rx='1'
--					FIFO_Write  <= '0';
--			end case;
--		
--	
--		end process;
--		------------------------------------------------------------
--	end generate MultiSyncMode;
	
--	SyncMode : if GALS=False generate
	------------------------------------------------------------
--	HS_AckRx    <= '1' when FIFO_IsFull='0' else '0'; -- and HS_Rx='1'when (HS_Rx='1' and FIFO_IsFull='0') else '0';

	------------------------------------------------------------
	MainCtrl: process(Clk, Rst)
	begin
		if (Rst = '1') then
			HS_AckRx_i <= '0';
--			FIFO_Write  <= '0'; 
--			FIFO_DataIn <= x"DEAD";
		else 
			if rising_edge(Clk) then
				if HS_Rx='1' then
--					FIFO_Write  <= '1' ;
--					FIFO_DataIn <= HS_DataIn;
					HS_AckRx_i <= '1';
				else
--					FIFO_Write  <= '0'; 
					HS_AckRx_i <= '0';
				end if;
			end if;
		end if;
	end process;
	
	FIFO_DataIn <= HS_DataIn;
	FIFO_Write  <= HS_AckRx_i when FIFO_IsFull='0' else '0';
	HS_AckRx    <= HS_AckRx_i when FIFO_IsFull='0' else '0';
	------------------------------------------------------------

--	end generate SyncMode;

end RTL;




