
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: Riffa Handshake adapter
-------------------------------------------------------------------------------
entity RiffaToHS is
	generic (
		Loopback           : boolean := True;
		C_PCI_DATA_WIDTH   : integer := 64;
		FlitWidth          : natural := 16;
		NBREG              : natural := 32);
	port (
		LED                : OUT std_logic_vector(7 downto 0);
		
		CLK                : in std_logic;
		RST                : in std_logic;
		
		-- RX Interface
		CHNL_RX_CLK        : out std_logic;
		CHNL_RX            : in  std_logic;
		CHNL_RX_ACK        : out std_logic;
		CHNL_RX_LAST       : in  std_logic;
		CHNL_RX_LEN        : in  std_logic_vector(31 downto 0);
		CHNL_RX_OFF        : in  std_logic_vector(30 downto 0);
		CHNL_RX_DATA       : in  std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
		CHNL_RX_DATA_VALID : in  std_logic;
		CHNL_RX_DATA_REN   : out std_logic;
		
		-- TX Interface
		CHNL_TX_CLK        : out std_logic;
		CHNL_TX            : out std_logic;
		CHNL_TX_ACK        : in  std_logic;
		CHNL_TX_LAST       : out std_logic;
		CHNL_TX_LEN        : out std_logic_vector(31 downto 0);
		CHNL_TX_OFF        : out std_logic_vector(30 downto 0);
		CHNL_TX_DATA       : out std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
		CHNL_TX_DATA_VALID : out std_logic;
		CHNL_TX_DATA_REN   : in  std_logic;
		
		ConfigRegister     : OUT std_logic_vector(FlitWidth-1 downto 0);
		ConfigRegisterIdx  : IN  natural;
		
		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0);
		Tx                 : OUT std_logic;
		AckTx              : IN  std_logic;
		
		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0);
		Rx                 : IN  std_logic;
		AckRx              : OUT std_logic);
end RiffaToHS;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Struct 
-------------------------------------------------------------------------------
architecture Struct of RiffaToHS is

	
	signal RX_FIFO_DataIn_i        : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal RX_FIFO_Write_i         : std_logic := '0';
	signal RX_FIFO_DataOut_i       : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal RX_FIFO_Read_i          : std_logic := '0';
	signal RX_FIFO_IsEmpty_i       : std_logic := '1';
	signal RX_FIFO_IsFull_i        : std_logic := '0';
	
	signal HS_DataIn_i             : std_logic_vector(FlitWidth-1 downto 0);
	signal HS_Rx_i                 : std_logic;
	signal HS_AckRx_i              : std_logic;

	signal HS_DataOut_i            : std_logic_vector(FlitWidth-1 downto 0);
	signal HS_Tx_i                 : std_logic;
	signal HS_AckTx_i              : std_logic;
	
	
	signal TX_FIFO_DataIn_i        : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal TX_FIFO_Write_i         : std_logic := '0';
	signal TX_FIFO_DataOut_i       : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal TX_FIFO_Read_i          : std_logic := '0';
	signal TX_FIFO_IsEmpty_i       : std_logic := '1';
	signal TX_FIFO_IsFull_i        : std_logic := '0';


	signal Tx_Data_i    : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal Tx_Len_i, Tx_Max_i     : unsigned(31 downto 0) := (others=>'0');
	signal Rx_Len_i     : unsigned(31 downto 0) := (others=>'0');
	signal Rx_Count_i, Tx_Count_i   : unsigned(31 downto 0) := (others=>'0');
--	signal rState : std_logic_vector(1 downto 0) := (others=>'0');
	signal CHNL_TX_DATA_VALID_i : std_logic;
	
	type Registers_Type is array (0 to NBREG-1) of std_logic_vector(FlitWidth-1 downto 0);
	signal ConfigRegister_i : Registers_Type;
	
	type Rx_State_type is (WAITREQ_STATE, DATA_STATE);
	signal Rx_State_i : Rx_State_type := WAITREQ_STATE;

	type Tx_State_type is (INIT_STATE, DATA_STATE);
	signal Tx_State_i : Tx_State_type := INIT_STATE;

	type Packet_State_type is (HEADER_STATE, PAYLOAD_STATE, DATA_STATE);
	signal Packet_State_i : Packet_State_type := HEADER_STATE;
	
	type LatencyCounter_State_type is (RESET_STATE, COUNT_STATE, STOP_STATE);
	signal LatencyCounter_State_i : LatencyCounter_State_type := STOP_STATE;
				
	signal Toggle_i        : std_logic := '0';

	signal Payload_i            : unsigned(FlitWidth-1 downto 0);
	signal Packet_Cnt_i         : unsigned(FlitWidth-1 downto 0);
	signal Header_i             : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	signal LatencyCounter_i     : unsigned(FlitWidth-1 downto 0);
	
	
	signal Router_Rx  : std_logic_vector(5-1 downto 0);
	signal Router_AckRx   : std_logic_vector(5-1 downto 0);
	signal Router_DataIn  : FLITS(5-1 downto 0);
	
	signal Router_Tx      : std_logic_vector(5-1 downto 0);
	signal Router_AckTx   : std_logic_vector(5-1 downto 0);
	signal Router_DataOut : FLITS(5-1 downto 0);
	
	signal Debug_Count_i   : unsigned(FlitWidth-1 downto 0);
	signal DebugReg1_i, DebugReg2_i, DebugReg3_i    : std_logic_vector(FlitWidth-1 downto 0);
--	signal Debug_Count_logic_i   : std_logic_vector(FlitWidth-1 downto 0);
	
begin  -- v0

	ConfigRegister <= ConfigRegister_i(ConfigRegisterIdx);
	--------------------------------------------------
	LED(0) <= Toggle_i;
	LED(2 downto 1) <= TX_FIFO_IsEmpty_i & RX_FIFO_IsEmpty_i;
	LED(3) <= '1' when TX_State_i=DATA_STATE else '0';
	LED(7 downto 4) <= STD_LOGIC_VECTOR(Rx_Len_i(3 downto 0));


--###################################################################
-- RX 
--###################################################################
	CHNL_RX_CLK <= CLK;
	CHNL_RX_ACK <= '1' when Rx_State_i = DATA_STATE else '0';
	CHNL_RX_DATA_REN <= '1' when Rx_State_i = DATA_STATE and RX_FIFO_IsFull_i='0' else '0';

	----------------------------------------------------
	FSM_RX : process(CLK, RST)
	begin
		if RST='1' then
			Rx_Len_i   <= (others=>'0');
			Rx_Count_i <= (others=>'0');
			Rx_State_i <= WAITREQ_STATE;
			Toggle_i <= '0';
			
		elsif rising_edge(CLK) then
			case Rx_State_i is 
				when WAITREQ_STATE => -- Wait for start of RX, save length
					if CHNL_RX='1' then
						Rx_Len_i   <= UNSIGNED(CHNL_RX_LEN) srl ((C_PCI_DATA_WIDTH/32)/2);
						Rx_Count_i <= (others=>'0');
						Rx_State_i <= DATA_STATE;
					end if;
					
				when DATA_STATE => -- Wait for last data in RX, save value
					if CHNL_RX_DATA_VALID='1'  then
						Rx_Count_i <= Rx_Count_i + 1;
					end if;
					if Rx_Count_i >= Rx_Len_i then
						Rx_State_i <= WAITREQ_STATE;
					end if;
					
				when others => null;
			end case;
		end if;
	end process;

	RX_FIFO_Write_i  <= '1' when CHNL_RX_DATA_VALID='1' and RX_FIFO_IsFull_i='0' else '0';
	RX_FIFO_DataIn_i <= CHNL_RX_DATA(FlitWidth-1 downto 0);
--	-----------------------------------------------------------------
	RXFIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 2048,
			largeur => FlitWidth
			)
		port map(
			reset     => RST,
			data_in   => RX_FIFO_DataIn_i, -- PCIe interface
			wr        => RX_FIFO_Write_i, -- PCIe interface
			IsFull    => RX_FIFO_IsFull_i,
			data_out  => RX_FIFO_DataOut_i,
			rd        => RX_FIFO_Read_i,
			IsEmpty   => RX_FIFO_IsEmpty_i,
			ack_wr    => open,
			ack_rd    => open,
			clock_out => CLK,
			clock_in  => CLK
			);

	----------------------------------------------
	FifoToHandShake : entity work.FifoToHandShake
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

			HS_Tx        => HS_Rx_i,
			HS_AckTx     => HS_AckRx_i,
			HS_DataOut   => HS_DataIn_i,

			FIFO_DataOut => RX_FIFO_DataOut_i,
			FIFO_Read    => RX_FIFO_Read_i,
			FIFO_IsEmpty => RX_FIFO_IsEmpty_i);
	

--###################################################################
-- INTERNAL
--###################################################################
--	LOOPBACK_Mode : if Loopback=True generate
--		--------------------------------------------------
--		-- LOOPBACK CONNECTIONS
--		HS_Rx_i      <= HS_Tx_i;-- when Loopback=True else HS_Rx;
--		HS_AckTx_i   <= HS_AckRx_i;--when Loopback=True else HS_AckTx;
--		HS_DataIn_i  <= HS_DataOut_i;--when Loopback=True else HS_DataIn;
--		
--	end generate LOOPBACK_Mode;
		
	NORMAL_Mode : if Loopback=False generate
		--------------------------------------------------
		-- LOOPBACK CONNECTIONS
--		HS_Rx_i      <= HS_Tx_i;
--		HS_AckTx_i   <= HS_AckRx_i;
--		HS_DataIn_i  <= HS_DataOut_i;
		------------
		RouterUnderTest : entity work.Router
			GENERIC MAP(
				FlitWidth      => FlitWidth,
				NbInputs       => 5,
				NbOutputs      => 5,
				X_Local        => 0,
				Y_Local        => 0,
				InputFifoDepth => 56)
			PORT MAP(
				HS_Rx      => Router_Rx, --: IN std_logic_vector(NbInputs-1 downto 0);
				HS_DataIn  => Router_DataIn, --: IN  FLITS(NbInputs-1 downto 0);
				HS_AckTx   => Router_AckTx, --: IN  std_logic_vector(NbOutputs-1 downto 0);
				HS_AckRx   => Router_AckRx, --: OUT std_logic_vector(NbInputs-1 downto 0);
				HS_Tx      => Router_Tx,      --: OUT std_logic_vector(NbOutputs-1 downto 0);
				HS_DataOut => Router_DataOut, --: OUT FLITS(NbOutputs-1 downto 0);
				clock      => CLK,-- : IN  std_logic;
				reset      => RST);-- : IN  std_logic);
----				
		Router_Rx(4)      <= HS_Rx_i;
		Router_DataIn(4)  <= HS_DataIn_i;
		Router_AckTx(4)   <= HS_AckTx_i;
		HS_AckRx_i        <= Router_AckRx(4);
		HS_Tx_i           <= Router_Tx(4);
		HS_DataOut_i      <= Router_DataOut(4);
		
--		--------------------------------------------------
--		TransfertController_i0: entity work.TransfertControl(RTL)
--			generic map(
--				FlitWidth => FlitWidth
--				)
--			port map(
--				clk => CLK,
--				rst => RST,
--				
--				FifoIn_DataOut => RX_FIFO_DataOut_i,
--				FifoIn_Read => RX_FIFO_Read_i,
--				FifoIn_IsEmpty => RX_FIFO_IsEmpty_i,
--				
--				InputRequests => ConfigRegister_i(12)(0),
--				InputConnected => ConfigRegister_i(12)(1),
--				
--				HS_Tx      => HS_Rx_i,
--				HS_AckTx   => HS_AckRx_i,
--				HS_DataOut => HS_DataIn_i
--				);
		
--		Debug_Count_i <= UNSIGNED(Debug_Count_logic_i);
		ConfigRegister_i(12)(0) <= '1' when Tx_State_i=INIT_STATE else '0';
		ConfigRegister_i(12)(FlitWidth-1 downto 1) <= (others=>'0');
	
		--------------------------------------------------
--		DebugCount_Process : process(CLK)
--		begin
--			if rising_edge(CLK) then
--				if RST='1' then
--					Debug_Count_i <= (others=>'0');
--				else
--					if RX_FIFO_Read_i='1' then
--						Debug_Count_i <= Debug_Count_i + 1;
--					end if;
--				end if;
--			end if;
--		end process DebugCount_Process;
		--------------------------------------------------
		
		----------------------------------------------------
		FSM_TX : process(CLK, RST)
		begin
			if RST='1' then
				ConfigRegister_i(0)  <= (others=>'0');
				ConfigRegister_i(1)  <= (others=>'0');
				ConfigRegister_i(2)  <= (others=>'0');
				ConfigRegister_i(3)  <= (others=>'0');
				ConfigRegister_i(4)  <= (others=>'0');
				ConfigRegister_i(5)  <= (others=>'0');
				ConfigRegister_i(6)  <= (others=>'0');
				ConfigRegister_i(7)  <= (others=>'0');
				ConfigRegister_i(8)  <= (others=>'0');
				ConfigRegister_i(9)  <= (others=>'0');
				ConfigRegister_i(10) <= (others=>'0');
				ConfigRegister_i(11) <= (others=>'0');
				Debug_Count_i <= (others=>'0');
				
			elsif rising_edge(CLK) then
				if HS_AckRx_i='1' then
					Debug_Count_i <= Debug_Count_i + 1;
					if TO_INTEGER(Debug_Count_i)=0 then
						ConfigRegister_i(0) <= HS_DataIn_i;
						ConfigRegister_i(1) <= DebugReg3_i;
						ConfigRegister_i(2) <= DebugReg1_i;
					elsif TO_INTEGER(Debug_Count_i)=1 then
						ConfigRegister_i(3) <= HS_DataIn_i;
						ConfigRegister_i(4) <= DebugReg3_i;
						ConfigRegister_i(5) <= DebugReg1_i;
					elsif TO_INTEGER(Debug_Count_i)=2 then
						ConfigRegister_i(6) <= HS_DataIn_i;
						ConfigRegister_i(7) <= DebugReg3_i;
						ConfigRegister_i(8) <= DebugReg1_i;
					elsif TO_INTEGER(Debug_Count_i)=3 then
						ConfigRegister_i(9)  <= HS_DataIn_i;
						ConfigRegister_i(10) <= DebugReg3_i;
						ConfigRegister_i(11) <= DebugReg1_i;
					end if;
--					if TO_INTEGER(Debug_Count_i)=1 then
--						ConfigRegister_i(0) <= DebugReg1_i;
--						ConfigRegister_i(1) <= DebugReg2_i;
--						ConfigRegister_i(2) <= DebugReg3_i;
--					elsif TO_INTEGER(Debug_Count_i)=2 then
--						ConfigRegister_i(3) <= DebugReg1_i;
--						ConfigRegister_i(4) <= DebugReg2_i;
--						ConfigRegister_i(5) <= DebugReg3_i;
--					elsif TO_INTEGER(Debug_Count_i)=3 then
--						ConfigRegister_i(6) <= DebugReg1_i;
--						ConfigRegister_i(7) <= DebugReg2_i;
--						ConfigRegister_i(8) <= DebugReg3_i;
--					elsif TO_INTEGER(Debug_Count_i)=4 then
--						ConfigRegister_i(9)  <= DebugReg1_i;
--						ConfigRegister_i(10) <= DebugReg2_i;
--						ConfigRegister_i(11) <= DebugReg3_i;
--					end if;
				end if;
			end if;
		end process;
	--	ConfigRegister_i(0) <= STD_LOGIC_VECTOR(Rx_Len_i(FlitWidth-1 downto 0));
	--	ConfigRegister_i(1) <= STD_LOGIC_VECTOR(Payload_i);
	--	ConfigRegister_i(2) <= STD_LOGIC_VECTOR(Tx_Count_i(FlitWidth-1 downto 0));
	--	ConfigRegister_i(3) <= 
	--	ConfigRegister_i(4) <= (others=>'0');
	--	ConfigRegister_i(5) <= (others=>'0');
	--	ConfigRegister_i(6) <= (others=>'0');
	--	ConfigRegister_i(7) <= (others=>'0');
	--	ConfigRegister_i(8) <= (others=>'0');
	--	ConfigRegister_i(9) <= (others=>'0');
	--	ConfigRegister_i(10) <= (others=>'0');
	--	ConfigRegister_i(11) <= (others=>'0');
	--	ConfigRegister_i(12) <= (others=>'0');
		ConfigRegister_i(13)(FlitWidth-1 downto 0) <= STD_LOGIC_VECTOR(Rx_Len_i(FlitWidth-1 downto 0));
		ConfigRegister_i(14) <= STD_LOGIC_VECTOR(Payload_i);
		ConfigRegister_i(15)(FlitWidth-1 downto 0) <= STD_LOGIC_VECTOR(LatencyCounter_i);
--		BOPMTest_NoC : entity work.BOPMTest
--			GENERIC MAP(
--				FlitWidth      => FlitWidth)
--			PORT MAP(
--				clock          => CLK,
--				reset          => RST,

--				Rx             => HS_Tx_i,
--				AckRx          => HS_AckTx_i,
--				DataIn         => HS_DataOut_i,

--				Tx             => HS_Rx_i,
--				AckTx          => HS_AckRx_i,
--				DataOut        => HS_DataIn_i);
				
		----------------------------------------------------
--		Tx         <= HS_Tx_i;
--		HS_AckTx_i <= AckTx;
--		DataOut    <= HS_DataOut_i;
--		
--		HS_Rx_i     <= Rx;
--		AckRx       <= HS_AckRx_i;
--		HS_DataIn_i <= DataIn;


	end generate NORMAL_Mode;
			
	------------------------------------------------
	HandShakeToFifo : entity work.HandShakeToFifo
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

			HS_Rx        => HS_Tx_i,
			HS_AckRx     => HS_AckTx_i,
			HS_DataIn    => HS_DataOut_i,

			FIFO_DataIn  => TX_FIFO_DataIn_i,
			FIFO_Write   => TX_FIFO_Write_i,
			FIFO_IsFull  => TX_FIFO_IsFull_i);
			
--	-----------------------------------------------------------------
	TXFIFO: entity work.fifo(RTL)
		generic map(
			profondeur => 2048,
			largeur => FlitWidth
			)
		port map(
			reset     => RST,
			data_in   => TX_FIFO_DataIn_i, -- PCIe interface
			wr        => TX_FIFO_Write_i, -- PCIe interface
			IsFull    => TX_FIFO_IsFull_i,
			data_out  => TX_FIFO_DataOut_i,
			rd        => TX_FIFO_Read_i,
			IsEmpty   => TX_FIFO_IsEmpty_i,
			ack_wr    => open,
			ack_rd    => open,
			clock_out => CLK,
			clock_in  => CLK
			);
			
--	-----------------------------------------------------------------

--###################################################################
-- TX 
--###################################################################

	CHNL_TX_CLK <= CLK;
	CHNL_TX <= '1' when Tx_State_i = DATA_STATE else '0';
	CHNL_TX_LAST <= '1';-- when Rx_State_i = "01" else '0';
	CHNL_TX_LEN <= STD_LOGIC_VECTOR(TO_UNSIGNED(128, CHNL_TX_LEN'length)); -- in words
	CHNL_TX_OFF <= (others=>'0');
	CHNL_TX_DATA <= Tx_Data_i;
	CHNL_TX_DATA_VALID_i <= '1' when (Tx_State_i = DATA_STATE and TX_FIFO_IsEmpty_i='0') or (Tx_State_i = DATA_STATE and (Tx_Count_i > Tx_Max_i)) else '0';
	CHNL_TX_DATA_VALID   <= CHNL_TX_DATA_VALID_i;

	Tx_Data_i(FlitWidth-1 downto 0)      <= TX_FIFO_DataOut_i;
	Tx_Data_i(C_PCI_DATA_WIDTH-1 downto FlitWidth)      <= (others=>'0');
	
--	TX_FIFO_Read_i <= '1' when ((Tx_State_i=INIT_STATE and Rx_State_i=SEND_BACK_STATE) or (Tx_State_i=DATA_STATE and CHNL_TX_DATA_REN='1' and CHNL_TX_DATA_VALID_i='1' and (Tx_Count_i <= Tx_Len_i) )) and TX_FIFO_IsEmpty_i='0' else '0';
	
--	Tx_Len_i(FlitWidth-1 downto 0) <= UNSIGNED(Payload_i)+2; Tx_Len_i(Tx_Len_i'length-1 downto FlitWidth) <= (others=>'0');
--	Tx_Max_i(FlitWidth-1 downto 0) <= UNSIGNED(Payload_i)+1; 
	Tx_Max_i(Tx_Len_i'length-1 downto Tx_Max_i'length) <= (others=>'0');
--	Tx_Len_i <= Rx_Len_i;
	Tx_Max_i(FlitWidth-1 downto 0) <= Payload_i(FlitWidth-1 downto 0)+1;
	Tx_Max_i(Tx_Max_i'length-1 downto FlitWidth) <= (others=>'0'); 
	----------------------------------------------------
	FSM_TX : process(CLK, RST)
	begin
		if RST='1' then
			Tx_Count_i <= (others=>'0');
			Tx_State_i <= INIT_STATE;
--			Tx_Data_i  <= (others=>'0');
--			ConfigRegister_i(3) <= (others=>'0');
--			ConfigRegister_i(4) <= (others=>'0');
--			ConfigRegister_i(5) <= (others=>'0');
--			ConfigRegister_i(6) <= (others=>'0');
--			ConfigRegister_i(7) <= (others=>'0');
--			ConfigRegister_i(8) <= (others=>'0');
--			ConfigRegister_i(9) <= (others=>'0');
--			ConfigRegister_i(10) <= (others=>'0');
			Payload_i <= TO_UNSIGNED(3, Payload_i'length);
			
		elsif rising_edge(CLK) then
			case Tx_State_i is 
				when INIT_STATE => -- Prepare for TX
--					Tx_Data_i(FlitWidth-1 downto 0)  <= ConfigRegister_i(0);
					if TX_FIFO_IsEmpty_i='0' then
						Tx_State_i <= DATA_STATE;
						Tx_Count_i <= TO_UNSIGNED(1, Tx_Count_i'length);
						Payload_i  <= TO_UNSIGNED(3, Payload_i'length); -- Don't know the packet length yet
					else
						Tx_Count_i <= TO_UNSIGNED(0, Tx_Count_i'length);
					end if;
--				
				when DATA_STATE => -- Start TX with save length and data value
					if CHNL_TX_DATA_REN='1' and CHNL_TX_DATA_VALID_i='1' then
--						Tx_Data_i(FlitWidth-1 downto 0)  <= ConfigRegister_i(TO_INTEGER(Tx_Count_i));
						Tx_Count_i <= Tx_Count_i + 1;
						if (Tx_Count_i > Tx_Max_i) then --TO_UNSIGNED(15, Tx_Count_i'length)
							Tx_State_i <= INIT_STATE;
						end if;
					end if;
					if TO_INTEGER(Tx_Count_i)=2 then
						Payload_i <= UNSIGNED(TX_FIFO_DataOut_i); -- Here we finally know the packet length
					end if;
--					if TO_INTEGER(Tx_Count_i)=1 then
--						ConfigRegister_i(4) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=2 then
--						ConfigRegister_i(5) <= TX_FIFO_DataOut_i;
--						Payload_i <= UNSIGNED(TX_FIFO_DataOut_i); -- Here we finally know the packet length
--					elsif TO_INTEGER(Tx_Count_i)=3 then
--						ConfigRegister_i(6) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=4 then
--						ConfigRegister_i(7) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=5 then
--						ConfigRegister_i(8) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=6 then
--						ConfigRegister_i(9) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=7 then
--						ConfigRegister_i(10) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=8 then
--						ConfigRegister_i(11) <= TX_FIFO_DataOut_i;
--					elsif TO_INTEGER(Tx_Count_i)=9 then
--						ConfigRegister_i(12) <= TX_FIFO_DataOut_i;
--					end if;
					
				when others => null;
			end case;
		end if;
	end process;
	
	----------------------------------------------------
	TX_FIFO_READ_PROC : process(Tx_State_i, TX_FIFO_IsEmpty_i, CHNL_TX_DATA_REN, CHNL_TX_DATA_VALID_i, Tx_Count_i, Tx_Max_i)
	begin
		case Tx_State_i is 
			when INIT_STATE => -- Prepare for TX
				if TX_FIFO_IsEmpty_i='0' then
					TX_FIFO_Read_i <= '1';
				else
					TX_FIFO_Read_i <= '0';
				end if;
--				
			when DATA_STATE =>
					if CHNL_TX_DATA_REN='1' and CHNL_TX_DATA_VALID_i='1' then
						if (Tx_Count_i > Tx_Max_i) then 
							TX_FIFO_Read_i <= '0';
						else
							if TX_FIFO_IsEmpty_i='0' then
								TX_FIFO_Read_i <= '1';
							else
								TX_FIFO_Read_i <= '0';
							end if;
						end if;
					else
						TX_FIFO_Read_i <= '0';
					end if;
			when others => 
				TX_FIFO_Read_i <= '0';
		end case;
	end process;


--###################################################################
-- UTILITIES
--###################################################################
	--------------------------------------------------
	LatencyCounter_Process : process(CLK)
	begin
		if rising_edge(CLK) then
			if RST='1' then
				LatencyCounter_i <= (others=>'0');
				LatencyCounter_State_i <= STOP_STATE;
			else
				case LatencyCounter_State_i is 
					when STOP_STATE => 
						if Rx_State_i=DATA_STATE and Rx_Count_i=TO_UNSIGNED(0, Rx_Count_i'length) then
							LatencyCounter_State_i <= RESET_STATE;
						end if;
					when RESET_STATE => 
						LatencyCounter_i <= (others=>'0');
						LatencyCounter_State_i <= COUNT_STATE;
					when COUNT_STATE => 
						LatencyCounter_i <= LatencyCounter_i + 1;
						if Tx_State_i=DATA_STATE and (Tx_Count_i > Tx_Max_i) then
							LatencyCounter_State_i <= STOP_STATE;
						end if;
					when others => null;
				end case;
			end if;
		end if;
	end process;	
	
end Struct;

























