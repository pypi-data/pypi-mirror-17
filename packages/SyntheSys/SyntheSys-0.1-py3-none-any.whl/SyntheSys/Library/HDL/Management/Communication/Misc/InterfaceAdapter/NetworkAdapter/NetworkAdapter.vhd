
library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_signed.all;
use IEEE.numeric_std.all;

 
--------------------------------------------------------------------------------
-- ENTITY: NetworkAdapter - Protocol conversion
--------------------------------------------------------------------------------
entity NetworkAdapter is 
	generic(
		FlitWidth : natural := 16);
	port(
		Rst                : IN  std_logic;
		Clk                : IN  std_logic;
		
		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0);
		Rx                 : IN  std_logic;
		AckRx              : OUT std_logic;
		
		InputData          : OUT std_logic_vector(FlitWidth-1 downto 0);
		HeaderValid        : OUT std_logic;
		PayloadValid       : OUT std_logic;
		InputDataValid     : OUT std_logic;
		
		SendBack           : IN std_logic; -- when '1', input packets are sent back to output port
		TerminalBusy       : IN std_logic; -- when '1', no input packets can be recieved
		
		OutputData         : IN  std_logic_vector(FlitWidth-1 downto 0);
		OutputFifoEmpty    : IN  std_logic;
		OutputRead         : OUT std_logic;
		Transmitted        : OUT std_logic;
		
		ReadHeaderFifo     : OUT std_logic;
		HeaderTransmitted  : IN  std_logic_vector(FlitWidth-1 downto 0);
		PayloadTransmitted : IN  std_logic_vector(FlitWidth-1 downto 0);
		
		Tx                 : OUT std_logic;
		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0);
		AckTx              : IN  std_logic
		
	);
end entity NetworkAdapter;

--------------------------------------------------------------------------------
-- ARCHITECTURE: RTL - Adapter that Convert HandShake_IN_HandShake_OUT protocol to SharedBOPM_Unit(simple)[v1.0].
--------------------------------------------------------------------------------
architecture RTL of NetworkAdapter is

	type STATE_INPUTADAPTER_FSM is (STATE_HEADER, STATE_PAYLOAD, STATE_DATA, STATE_SENDBACK, STATE_UNROLL);
	signal InputState_i : STATE_INPUTADAPTER_FSM := STATE_HEADER;

	type STATE_OUTPUTADAPTER_FSM is (SEND_HEADER, SEND_PAYLOAD, SEND_DATA, WAIT_ACK_HEADER);
	signal OutputState_i : STATE_OUTPUTADAPTER_FSM := SEND_HEADER;
--	signal SerializationCounter : natural := 0;
--	signal DataIn_TEMP : std_logic_vector(FlitWidth-1 downto 0);
	signal PayloadReceived_i    : UNSIGNED(FlitWidth-1 downto 0);
	signal HeaderReceived_i     : std_logic_vector(FlitWidth-1 downto 0);
--	signal HeaderFIFO_DataOut_i : std_logic_vector(FlitWidth-1 downto 0);
--	signal ReadHeaderFifo     : std_logic;
--	signal HeaderFIFO_Write_i   : std_logic;
--	signal ChangeState_i        : std_logic;
--	signal SendBackCtrl_i       : std_logic;
--	signal SyncSendBack_i       : std_logic;
--	signal SendBackMode_i       : std_logic := '1';
	constant ZEROS   : UNSIGNED(FlitWidth-1 downto 0) := TO_UNSIGNED(0, FlitWidth);
	constant ONE     : UNSIGNED(FlitWidth-1 downto 0) := TO_UNSIGNED(1, FlitWidth);
	signal DataCnt_i : UNSIGNED(FlitWidth-1 downto 0) := TO_UNSIGNED(0, FlitWidth);
	
--	signal OOO_FIFO_DataIn_i    : std_logic_vector(FlitWidth-1 downto 0);-- PCIe interface
--	signal OOO_FIFO_Write_i     : std_logic; -- PCIe interface
--	signal OOO_FIFO_IsFull_i    : std_logic;
--	signal OOO_FIFO_DataOut_i   : std_logic_vector(FlitWidth-1 downto 0);
--	signal OOO_FIFO_Read_i      : std_logic;
--	signal OOO_FIFO_IsEmpty_i   : std_logic;
	
	signal PayloadValid_i       : std_logic;
	signal OutputCnt_i          : unsigned(FlitWidth-1 downto 0) := (others=>'0');
	signal DataOut_i            : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal TX_FIFO_Read_i       : std_logic;
	signal TX_FIFO_IsEmpty_i    : std_logic;
	signal AckRx_i, Tx_i        : std_logic;
	
	signal FIFO_SB_DataOut_i    : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal FIFO_SB_Read_i       : std_logic;
	signal FIFO_SB_Empty_i      : std_logic;
			
	signal FIFO_SB_DataIn_i, DataIn2     : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal FIFO_SB_Write_i      : std_logic;
	
	signal InputData_i          : std_logic_vector(FlitWidth-1 downto 0);
	
	signal UnCounterReorderingFifo_i, NbReorderPacketCnt_i : unsigned(FlitWidth-1 downto 0) := (others=>'0');
	signal PacketSource_i : std_logic := '0';
	
begin
	
	PayloadValid <= PayloadValid_i;

	------------------------------------------------------------
	-- Process FSMStateAssignment_InputAdapter_FSM : FSM State assignments
	FSMStateAssignment_InputAdapter_FSM: process(Rst, Clk)
	begin
	
		if (Rst = '1') then 
			InputState_i <= STATE_HEADER;
			PayloadReceived_i <= (others=>'0');
			HeaderReceived_i  <= (others=>'0');
			FIFO_SB_Write_i <= '0';
			NbReorderPacketCnt_i      <= (others=>'0');
			UnCounterReorderingFifo_i <=  (others=>'0');
			PacketSource_i <= '0';
		else 
			if rising_edge(Clk) then 
				case InputState_i is -- Assignments for FSM FuturState
					when STATE_HEADER =>
						PayloadReceived_i <= ZEROS;
						if AckRx_i='1' or FIFO_SB_Read_i = '1' then
							HeaderReceived_i <= DataIn;
							InputState_i <= STATE_PAYLOAD;
						end if;
					when STATE_PAYLOAD =>
						if SendBack='1' then
							FIFO_SB_Write_i <= '1';
							if FIFO_SB_Read_i = '0' then
								NbReorderPacketCnt_i <= NbReorderPacketCnt_i+1;
							end if;
							PayloadReceived_i <= UNSIGNED(InputData_i)+2;
							if AckRx_i='1' or FIFO_SB_Read_i = '1' then
								InputState_i <= STATE_SENDBACK;
							end if;
						else
							if FIFO_SB_Read_i = '1' then
								NbReorderPacketCnt_i <= NbReorderPacketCnt_i-1;
							end if;
							PayloadReceived_i <= UNSIGNED(InputData_i);
							if AckRx_i='1' or FIFO_SB_Read_i = '1' then
								InputState_i <= STATE_DATA;
							end if;
						end if;
						
--						if UNSIGNED(DataIn)<=ONE and UnCounterReorderingFifo_i=ONE then
--							UnCounterReorderingFifo_i <= (others=>'0');
--						end if;
					when STATE_DATA =>
						if AckRx_i='1' or UnCounterReorderingFifo_i>ZEROS then
							PayloadReceived_i <= PayloadReceived_i-1;
							if PayloadReceived_i<=ONE then 
								PacketSource_i <= '0';
								if UnCounterReorderingFifo_i>ZEROS then
								-- Uncount each time a packet has been transmitted from the reordering fifo
									UnCounterReorderingFifo_i <= UnCounterReorderingFifo_i-1;
									if UnCounterReorderingFifo_i>1 then
										InputState_i <= STATE_UNROLL;
									else
										InputState_i <= STATE_HEADER;
									end if;
								else
									if FIFO_SB_Empty_i='0' then
									-- Try the saved packets at each new accepted packet
										InputState_i <= STATE_UNROLL;
									else
										InputState_i <= STATE_HEADER;
									end if;
								end if;
							end if;
						end if;
					when STATE_SENDBACK => 
						PayloadReceived_i <= PayloadReceived_i-1;
						if PayloadReceived_i<=ONE then
							PacketSource_i <= '0';
							if UnCounterReorderingFifo_i>0 then
							-- Uncount each time a packet has been transmitted from the reordering fifo
								UnCounterReorderingFifo_i <= UnCounterReorderingFifo_i-1;
								if UnCounterReorderingFifo_i>1 then
									InputState_i <= STATE_UNROLL;
								else
									InputState_i <= STATE_HEADER;
								end if;
							else
								InputState_i <= STATE_HEADER;
							end if;
							FIFO_SB_Write_i <= '0';
						end if;
					when STATE_UNROLL => 
						if TerminalBusy='0' then
							PacketSource_i <= '1';
							if UnCounterReorderingFifo_i=0 then
								UnCounterReorderingFifo_i <= NbReorderPacketCnt_i; 
							end if;
							if FIFO_SB_Read_i='1' then
								InputState_i <= STATE_HEADER;
							end if;
						end if;
						
					when others => null;
				end case;
				
			end if;
		end if;
	
	end process;
	------------------------------------------------------------
	-- Process OutputAssignment_InputAdapter_FSM : output State assignments
	OutputAssignment_InputAdapter_FSM: process(InputState_i, AckRx_i, FIFO_SB_Read_i) --TerminalBusy, SendBack
	begin
		case InputState_i is -- Assignments for FSM FuturState
			when STATE_HEADER =>
				if AckRx_i='1' or FIFO_SB_Read_i='1' then
					HeaderValid  <= '1';
				else 
					HeaderValid  <= '0';
				end if;
				PayloadValid_i    <= '0';
				InputDataValid    <= '0';
				
			when STATE_PAYLOAD =>
				HeaderValid <= '0';
				if AckRx_i='1' or FIFO_SB_Read_i='1' then
					PayloadValid_i <= '1';
				else 
					PayloadValid_i <= '0';
				end if;
				InputDataValid <= '0';
			
			when STATE_DATA => 
				HeaderValid    <= '0';
				PayloadValid_i <= '0';
				if AckRx_i='1' or UnCounterReorderingFifo_i>0 then
					InputDataValid <= '1';
				else
					InputDataValid <= '0';
				end if;
				
			when others => 
				HeaderValid    <= '0';
				PayloadValid_i <= '0';
				InputDataValid <= '0';
		end case;
	
	end process;
	
	------------------------------------------------------------
	InputData_i  <= FIFO_SB_DataOut_i when PacketSource_i='1' else DataIn;
	InputData    <= InputData_i;
	
	------------------------------------------------------------
	AckRxCtrl: process(Clk, Rst)
	begin
		if (Rst = '1') then
			AckRx_i <= '0';
		else 
			if rising_edge(Clk) then
				if Rx='1' and TerminalBusy='0' and UnCounterReorderingFifo_i=0 and InputState_i/=STATE_SENDBACK and InputState_i/=STATE_UNROLL then
					AckRx_i <= '1';
				else
					AckRx_i <= '0';
				end if;
			end if;
		end if;
	end process;
	
	AckRx <= AckRx_i;
	
	------------------------------------------------------------
	ReadReorderingFifo: process(InputState_i, UnCounterReorderingFifo_i, PayloadReceived_i, TerminalBusy)
	begin
		if TerminalBusy='0' then
			if (UnCounterReorderingFifo_i>0) then
				if (InputState_i=STATE_DATA and PayloadReceived_i>ONE) or (InputState_i=STATE_PAYLOAD) or (InputState_i=STATE_HEADER) or (InputState_i=STATE_UNROLL) then
					FIFO_SB_Read_i <= '1';
				else
					FIFO_SB_Read_i <= '0';
				end if;
			else
				if InputState_i=STATE_UNROLL then
					FIFO_SB_Read_i <= '1';
				else
					FIFO_SB_Read_i <= '0';
				end if;
			end if;
		else
			FIFO_SB_Read_i <= '0';
		end if;
	end process;
--	FIFO_SB_Read_i <= '1' when ((InputState_i=STATE_UNROLL and UnCounterReorderingFifo_i<ONE) or (UnCounterReorderingFifo_i>0) or (InputState_i=STATE_DATA and PayloadReceived_i>ONE and UnCounterReorderingFifo_i>0)) and TerminalBusy='0' else '0';
	
	
	------------------------------------------------------------
	ReorderingFifoInput: process(Clk, Rst)
	begin
		if (Rst = '1') then
			FIFO_SB_DataIn_i <= (others=>'0');
			DataIn2          <= (others=>'0');
		else 
			if rising_edge(Clk) then
				DataIn2          <= InputData_i;
				FIFO_SB_DataIn_i <= DataIn2;
			end if;
		end if;
	end process;
	
	--###########################################################################
	
	----------------------------------------------
	FifoToHandShake : entity work.FifoToHandShake
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

			HS_Tx        => Tx_i,
			HS_AckTx     => AckTx,
			HS_DataOut   => DataOut,

			FIFO_DataOut => DataOut_i,
			FIFO_Read    => TX_FIFO_Read_i,
			FIFO_IsEmpty => TX_FIFO_IsEmpty_i);


	-----------------------------------------------------------------
	FIFO_SendBack: entity work.fifo(RTL)
		generic map(
			largeur => FlitWidth,
			profondeur => 64
			)
		port map(
			clock_in  => Clk,
			clock_out => Clk,
			reset     => Rst,
			
			data_out  => FIFO_SB_DataOut_i,
			rd        => FIFO_SB_Read_i,
			IsEmpty   => FIFO_SB_Empty_i,
			
			data_in   => FIFO_SB_DataIn_i,
			wr        => FIFO_SB_Write_i,
			IsFull    => open,
			ack_rd    => open,
			ack_wr    => open
			);


	Tx <= Tx_i;

	------------------------------------------------------------
	-- Process FSMSignalAssignments_InputAdapter_FSM : Signal assignments according to InputAdapter_FSM FSM state.
	OutputFSMStateAssignments: process(Rst, Clk)
	begin
	
		if (Rst = '1') then
			OutputCnt_i <= (others=>'0');
			OutputState_i <= SEND_HEADER;
		else 
			if rising_edge(Clk) then 
				case OutputState_i is -- Assignments for FSM FuturState
					when SEND_HEADER =>
						OutputCnt_i <= (others=>'0');
						if AckTx='1' then
							OutputState_i <= SEND_PAYLOAD;
						elsif OutputFifoEmpty='0' and TX_FIFO_Read_i='0' then
							OutputState_i <= WAIT_ACK_HEADER;
						end if;
					when SEND_PAYLOAD =>
						if AckTx='1' then
							OutputState_i <= SEND_DATA;
							OutputCnt_i   <= UNSIGNED(PayloadTransmitted);
--							assert UNSIGNED(PayloadTransmitted)<3 report "INVALID PAYLOAD" severity failure;
						end if;
					when SEND_DATA =>
						if AckTx='1' then
							OutputCnt_i <= OutputCnt_i-1;
							if OutputCnt_i=TO_UNSIGNED(1, FlitWidth) then
								OutputState_i <= SEND_HEADER;
							end if;
						end if;
					when WAIT_ACK_HEADER =>
						if AckTx='1' then
							OutputState_i <= SEND_PAYLOAD;
						end if;
				
					when others =>null;
				end case;
			end if;
		end if;
	end process;
				
	OutputFSMSignalAssignments: process(OutputState_i, OutputFifoEmpty, TX_FIFO_Read_i, AckTx, HeaderTransmitted, PayloadTransmitted, OutputData, OutputCnt_i)
	begin
		case OutputState_i is -- Assignments for FSM FuturState
			when SEND_HEADER =>
				OutputRead     <= '0';
				if OutputFifoEmpty='0' then
					ReadHeaderFifo <= TX_FIFO_Read_i;
				else
					ReadHeaderFifo <= '0';
				end if;
				DataOut_i       <= HeaderTransmitted;
				Transmitted    <= '0';
				
			when SEND_PAYLOAD =>
				if AckTx='1' then
					OutputRead <= '1';
				else
					OutputRead <= '0';
				end if;
				ReadHeaderFifo <= '0';
				DataOut_i       <= PayloadTransmitted;
				Transmitted    <= '0';
				
			when SEND_DATA =>
				OutputRead     <= TX_FIFO_Read_i;
				ReadHeaderFifo <= '0';
				DataOut_i       <= OutputData;
				if AckTx='1' then
					if OutputCnt_i=TO_UNSIGNED(1, FlitWidth) then
						Transmitted    <= '1';
					else
						Transmitted    <= '0';
					end if;
				else
					Transmitted    <= '0';
				end if;
				
			when WAIT_ACK_HEADER =>
				OutputRead     <= '0';
				ReadHeaderFifo <= '0';
				DataOut_i         <= HeaderTransmitted;
				Transmitted    <= '0';
			
			when others =>
				OutputRead     <= '0';
				ReadHeaderFifo <= '0';
				DataOut_i         <= HeaderTransmitted;
				Transmitted    <= '0';
		end case;
	
	end process;
	
	TX_FIFO_IsEmpty_i <= '1' when OutputState_i=SEND_DATA and OutputCnt_i<=TO_UNSIGNED(1, FlitWidth) else OutputFifoEmpty;
--	------------------------------------------------------------
--	-- Process FSMStateAssignment : FSM State assignments
--	FSM_Output_StateAssignment: process(Clk, Rst)
--	begin
--		if (Rst = '1') then 
--			OutputState_i <= WAIT_INCOMING_DATA;
--			DataCnt_i      <= (others=>'0');
--		else 
--			if rising_edge(Clk) then 
--				case OutputState_i is -- Assignments for FSM FuturState
--					when WAIT_INCOMING_DATA =>
--						DataCnt_i      <= (others=>'0');
--						if OutputFifoEmpty='0' then 
--							OutputState_i <= SEND_HEADER;
--						else
--							OutputState_i <= WAIT_INCOMING_DATA;
--						end if;
--					when SEND_HEADER =>
--						if AckTx='1' then
--							OutputState_i <= SEND_PAYLOAD;
--						else
--							OutputState_i <= SEND_HEADER;
--						end if;
--					when SEND_PAYLOAD =>
--						if AckTx='1' then
--							if OutputFifoEmpty='0' then 
--								OutputState_i <= SEND_DATA;
--							else
--								OutputState_i <= SEND_PAYLOAD;
--							end if;
--						else
--							OutputState_i <= SEND_PAYLOAD;
--						end if;
--						DataCnt_i      <= UNSIGNED(PayloadTransmitted);
--					when SEND_DATA =>
--						if DataCnt_i=ONE then
--							if AckTx='1' then
--								OutputState_i <= WAIT_INCOMING_DATA;
--							else
--								OutputState_i <= SEND_DATA;
--							end if;
--						else 
--							OutputState_i <= SEND_DATA;
--							if AckTx='1' then
--								if OutputFifoEmpty='0' then 
--									DataCnt_i      <= DataCnt_i-1;
--								else
--									OutputState_i <= WAIT_REMINDING_DATA;
--								end if;
--							end if;
--						end if;
--					when WAIT_REMINDING_DATA =>
--						if OutputFifoEmpty='0' then 
--							DataCnt_i      <= DataCnt_i-1;
--						end if;
----					when ACKNOWLEDGE =>
--					when others => null;
--				end case;
--				
--			end if;
--		end if;
--	
--	end process;
--	
--	------------------------------------------------------------
--	-- Process FSMStateAssignment : FSM State assignments
--	FSM_Output_OutputAssignment: process(Rst, OutputState_i, OutputFifoEmpty, AckTx, HeaderTransmitted, PayloadTransmitted, OutputData, DataCnt_i)
--	begin
--		if (Rst = '1') then 
--			Rx     <= '0';
--			DataOut <= HeaderTransmitted;
--			OutputRead     <= '0';
--			ReadHeaderFifo <= '0';
--		else 
--			case OutputState_i is -- Assignments for FSM FuturState
--				when WAIT_INCOMING_DATA =>
--					DataOut         <= HeaderTransmitted;
--					OutputRead     <= '0';
--					Rx             <= '0';
--					if OutputFifoEmpty='0' then 
--						ReadHeaderFifo <= '1';
--					else
--						ReadHeaderFifo <= '0';
--					end if;
--				when SEND_HEADER =>
--					DataOut         <= HeaderTransmitted;
--					Rx             <= '1';
--					OutputRead     <= '0';
--					ReadHeaderFifo <= '0';
--				when SEND_PAYLOAD =>
--					DataOut         <= PayloadTransmitted;
--					Rx             <= '1';
--					if AckTx='1' then
--						if OutputFifoEmpty='0' then 
--							OutputRead     <= '1';
--						else
--							OutputRead     <= '0';
--						end if;
--					else
--						OutputRead     <= '0';
--					end if;
--					ReadHeaderFifo <= '0';
--				when SEND_DATA =>
--					DataOut <= OutputData;
--					if DataCnt_i=ONE then
--						Rx     <= '0';
--						OutputRead     <= '0';
--					else
--						Rx     <= '1';
--						if AckTx='1' then
--							if OutputFifoEmpty='0' then 
--								OutputRead     <= '1';
--							else
--								OutputRead     <= '0';
--							end if;
--						else
--							OutputRead     <= '0';
--						end if;
--					end if;
--					ReadHeaderFifo <= '0';
--				when WAIT_REMINDING_DATA =>
--					DataOut <= OutputData;
--					Rx     <= '0';
--					if OutputFifoEmpty='0' then 
--						OutputRead     <= '1';
--					else
--						OutputRead     <= '0';
--					end if;
--					ReadHeaderFifo <= '0';
----					when ACKNOWLEDGE =>
--				when others => 
--					DataOut <= HeaderTransmitted;
--					Rx     <= '0';
--					OutputRead     <= '0';
--					ReadHeaderFifo <= '0';
--			end case;
--		end if;
--	end process;
	
end architecture RTL;

