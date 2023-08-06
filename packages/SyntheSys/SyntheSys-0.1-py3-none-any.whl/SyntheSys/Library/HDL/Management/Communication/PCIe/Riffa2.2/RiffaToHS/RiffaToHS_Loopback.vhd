
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
				
	signal Toggle_i        : std_logic := '0';

	signal Payload_i            : unsigned(FlitWidth-1 downto 0);
	signal Packet_Cnt_i         : unsigned(FlitWidth-1 downto 0);
	signal Header_i             : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	
begin  -- v0

	ConfigRegister <= ConfigRegister_i(ConfigRegisterIdx);
	--------------------------------------------------
--	LED(3 downto 0) <= STD_LOGIC_VECTOR(OutcommingData_i(3 downto 0)); 
--	LED(7 downto 4) <= STD_LOGIC_VECTOR(OutcommingData_i(3 downto 0));
	LED(0) <= Toggle_i;
	LED(2 downto 1) <= TX_FIFO_IsEmpty_i & RX_FIFO_IsEmpty_i;
--	LED(2) <= '1' when RX_State_i/=WAITREQ_STATE else '0';
	LED(3) <= '1' when TX_State_i=DATA_STATE else '0';
	LED(7 downto 4) <= STD_LOGIC_VECTOR(Rx_Len_i(3 downto 0));
	
--	--------------------------------------------------
--	LED_CntRx_Process : process(CLK)
--	begin
--		if rising_edge(CLK) then
--			if RST='1' then
----				IncomingData_i  <= (others=>'0');
--				LED(0)  <= '1';
--			else
--				LED(0)  <= '0';
----				if RX_FIFO_Write_i='1' then
----					IncomingData_i <= IncomingData_i+1;
----				end if;
--			end if;
--		end if;
--	end process;	
--	
	ConfigRegister_i(0) <= STD_LOGIC_VECTOR(Rx_Len_i(FlitWidth-1 downto 0));
	ConfigRegister_i(1) <= STD_LOGIC_VECTOR(Tx_Max_i(FlitWidth-1 downto 0));
	ConfigRegister_i(2) <= STD_LOGIC_VECTOR(Tx_Count_i(FlitWidth-1 downto 0));
	ConfigRegister_i(3) <= STD_LOGIC_VECTOR(Payload_i);
--	ConfigRegister_i(4) <= (others=>'0');
--	ConfigRegister_i(5) <= (others=>'0');
--	ConfigRegister_i(6) <= (others=>'0');
--	ConfigRegister_i(7) <= (others=>'0');
--	ConfigRegister_i(8) <= (others=>'0');
--	ConfigRegister_i(9) <= (others=>'0');
--	ConfigRegister_i(10) <= (others=>'0');
	ConfigRegister_i(11) <= (others=>'0');
	ConfigRegister_i(12) <= (others=>'0');
	ConfigRegister_i(13) <= (others=>'0');
	ConfigRegister_i(14) <= (others=>'0');
	ConfigRegister_i(15) <= (others=>'0');


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
--			ConfigRegister_i <= (others=>(others=>'0'));
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
--						ConfigRegister_i(TO_INTEGER(Rx_Count_i)) <= CHNL_RX_DATA(FlitWidth-1 downto 0);
						Rx_Count_i <= Rx_Count_i + 1;
					end if;
					if Rx_Count_i >= Rx_Len_i then
						Rx_State_i <= WAITREQ_STATE;
					end if;
					
--				when SEND_BACK_STATE => 
--					Rx_State_i <= WAITREQ_STATE;
--					Toggle_i <= not Toggle_i;
					
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

	------------------------------------------------
	FifoToHandShake : entity work.FifoToHandShake
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

			HS_Tx        => HS_Tx_i,
			HS_AckTx     => HS_AckTx_i,
			HS_DataOut   => HS_DataOut_i,

			FIFO_DataOut => RX_FIFO_DataOut_i,
			FIFO_Read    => RX_FIFO_Read_i,
			FIFO_IsEmpty => RX_FIFO_IsEmpty_i);
	

--###################################################################
-- INTERNAL
--###################################################################
	LOOPBACK_Mode : if Loopback=True generate
		--------------------------------------------------
		-- LOOPBACK CONNECTIONS
		HS_Rx_i      <= HS_Tx_i;
		HS_AckTx_i   <= HS_AckRx_i;
		HS_DataIn_i  <= HS_DataOut_i;
		
--		Payload_i <= UNSIGNED(Rx_Len_i)-2;
		
	end generate LOOPBACK_Mode;
		
	NORMAL_Mode : if Loopback=False generate
		--------------------------------------------------
		-- LOOPBACK CONNECTIONS
		HS_Rx_i      <= HS_Tx_i;
		HS_AckTx_i   <= HS_AckRx_i;
		HS_DataIn_i  <= HS_DataOut_i;
		------------
--		BOPM_Unit : entity work.Wrapped_BOPM_computation_unit
--			GENERIC MAP(
--				PipelineLength => 8,
--				NBTask         => 16,
--				ComHeader      => (others=>'0'),
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
--		PACKET_DETECTION : process(CLK, RST)
--		begin
--			if RST='1' then
--				Packet_State_i <= HEADER_STATE;
--				Packet_Cnt_i   <= (others=>'0');
--			
--			elsif rising_edge(CLK) then
--				case Packet_State_i is 
--					--------
--					when HEADER_STATE => 
--						if HS_AckRx_i='1' then
--							Packet_State_i <= PAYLOAD_STATE;
--						end if;
--					--------
--					when PAYLOAD_STATE =>
--						Payload_i    <= UNSIGNED(HS_DataIn_i);
--						Packet_Cnt_i <= (others=>'0');
--						if HS_AckRx_i='1' then
--							Packet_State_i <= DATA_STATE;
--						end if;
--					--------
--					when DATA_STATE =>
--						if HS_AckRx_i='1' then
--							Packet_Cnt_i <= Packet_Cnt_i + 1;
--							if (Packet_Cnt_i >= (Payload_i-1)) then 
--								Packet_State_i <= HEADER_STATE;
--							end if;
--						end if;
--					--------
--					when others => null;
--				end case;
--			end if;
--		end process;
		----------------------------------------------------
	end generate NORMAL_Mode;
			
	------------------------------------------------
	HandShakeToFifo : entity work.HandShakeToFifo
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

			HS_Rx        => HS_Rx_i,
			HS_AckRx     => HS_AckRx_i,
			HS_DataIn    => HS_DataIn_i,

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
--	Tx_Max_i(Tx_Len_i'length-1 downto FlitWidth) <= (others=>'0');
--	Tx_Len_i <= Rx_Len_i;
	Tx_Max_i <= Payload_i+1;
	----------------------------------------------------
	FSM_TX : process(CLK, RST)
	begin
		if RST='1' then
			Tx_Count_i <= (others=>'0');
			Tx_State_i <= INIT_STATE;
--			Tx_Data_i  <= (others=>'0');
--			ConfigRegister_i(3) <= (others=>'0');
			ConfigRegister_i(4) <= (others=>'0');
			ConfigRegister_i(5) <= (others=>'0');
			ConfigRegister_i(6) <= (others=>'0');
			ConfigRegister_i(7) <= (others=>'0');
			ConfigRegister_i(8) <= (others=>'0');
			ConfigRegister_i(9) <= (others=>'0');
			ConfigRegister_i(10) <= (others=>'0');
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
					ConfigRegister_i(4) <= TX_FIFO_DataOut_i;
--				
				when DATA_STATE => -- Start TX with save length and data value
					if CHNL_TX_DATA_REN='1' and CHNL_TX_DATA_VALID_i='1' then
--						Tx_Data_i(FlitWidth-1 downto 0)  <= ConfigRegister_i(TO_INTEGER(Tx_Count_i));
						Tx_Count_i <= Tx_Count_i + 1;
						if (Tx_Count_i > Tx_Max_i) then --TO_UNSIGNED(15, Tx_Count_i'length)
							Tx_State_i <= INIT_STATE;
						end if;
					end if;
					if TO_INTEGER(Tx_Count_i)=1 then
						ConfigRegister_i(5) <= TX_FIFO_DataOut_i;
					elsif TO_INTEGER(Tx_Count_i)=2 then
						ConfigRegister_i(6) <= TX_FIFO_DataOut_i;
						Payload_i <= UNSIGNED(TX_FIFO_DataOut_i); -- Here we finally know the packet length
					elsif TO_INTEGER(Tx_Count_i)=3 then
						ConfigRegister_i(7) <= TX_FIFO_DataOut_i;
					elsif TO_INTEGER(Tx_Count_i)=4 then
						ConfigRegister_i(8) <= TX_FIFO_DataOut_i;
					elsif TO_INTEGER(Tx_Count_i)=5 then
						ConfigRegister_i(9) <= TX_FIFO_DataOut_i;
					elsif TO_INTEGER(Tx_Count_i)=6 then
						ConfigRegister_i(10) <= TX_FIFO_DataOut_i;
					end if;
					
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
	
end Struct;

























