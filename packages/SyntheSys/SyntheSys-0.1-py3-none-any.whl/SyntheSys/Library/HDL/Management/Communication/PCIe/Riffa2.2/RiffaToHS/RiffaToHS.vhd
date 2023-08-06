
use work.Utilities.ALL;


library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: Riffa Handshake adapter
-------------------------------------------------------------------------------
entity RiffaToHS is
	generic (
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


	signal Tx_Data_i              : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal Tx_Len_i, Tx_Max_i     : unsigned(31 downto 0) := (others=>'0');
	signal Rx_Len_i               : unsigned(31 downto 0) := (others=>'0');
	signal Rx_Count_i, Tx_Count_i : unsigned(31 downto 0) := (others=>'0');
--	signal rState : std_logic_vector(1 downto 0) := (others=>'0');
	signal CHNL_TX_DATA_VALID_i : std_logic;
	
	type Registers_Type is array (0 to NBREG-1) of std_logic_vector(FlitWidth-1 downto 0);
	signal ConfigRegister_i : Registers_Type;
	
	type Rx_State_type is (WAITREQ_STATE, DATA_STATE, END_STATE);
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

	constant DimX                 : natural             := 2;
	constant DimY                 : natural             := 1;
	
--	signal NoC_0_AckRx : std_logic_vector(DimX*DimY-1 downto 0);
--	signal NoC_0_AckTx : std_logic_vector(DimX*DimY-1 downto 0);
--	signal NoC_0_DataIn : FLITS(DimX*DimY-1 downto 0);
--	signal NoC_0_DataOut : FLITS(DimX*DimY-1 downto 0);
--	signal NoC_0_Rx : std_logic_vector(DimX*DimY-1 downto 0);
--	signal NoC_0_Tx : std_logic_vector(DimX*DimY-1 downto 0);
	
	signal Debug_Count_Inputs_i, Debug_Count_Outputs_i   : unsigned(FlitWidth-1 downto 0);
--	signal DebugReg1_i, DebugReg2_i, DebugReg3_i    : std_logic_vector(FlitWidth-1 downto 0);
	signal Debug0_En_i   : std_logic;
	signal Debug0_i      : std_logic_vector(FlitWidth-1 downto 0);
	signal DebugVector_i : std_logic_vector(FlitWidth-1 downto 0);
--	signal Debug_Count_logic_i     : std_logic_vector(FlitWidth-1 downto 0);

	constant ZEROS                 : std_logic_vector(FlitWidth-1 downto 0) := (others=>'0');
	
	-------------------------------------------------
	-- WRAPPED_NODE
	signal FIFO_OutputFifoFull : std_logic;
	signal FIFO_Write : std_logic;
	signal FIFO_ack_rd : std_logic;
	signal FIFO_ack_wr : std_logic;
	signal HeaderFIFO_IsEmpty : std_logic;
	signal HeaderFIFO_IsFull : std_logic;
	signal HeaderFIFO_ack_rd : std_logic;
	signal HeaderFIFO_ack_wr : std_logic;
	signal PipelineManager_BBInputValid : std_logic;
	signal PipelineManager_InputHeader : std_logic_vector(FlitWidth-1 downto 0);
	signal PipelineManager_OutputHeader : std_logic_vector(FlitWidth-1 downto 0);
	signal TaskManager_BBInputs : std_logic_vector(16+16-1 downto 0);
	signal TaskManager_BBOutput : std_logic_vector(15 downto 0);
	signal TaskManager_OutputDataFlit : std_logic_vector(FlitWidth-1 downto 0);
	
	signal OutputData         : std_logic_vector(15 downto 0);
	signal OutputRead         : std_logic;
	signal OutputFifoEmpty    : std_logic;
	signal HeaderTransmitted  : std_logic_vector(FlitWidth-1 downto 0);
	signal PayloadTransmitted : std_logic_vector(FlitWidth-1 downto 0);
	signal Transmitted        : std_logic;
	signal PayloadValid       : std_logic;
	signal HeaderValid        : std_logic;
	signal InputData          : std_logic_vector(FlitWidth-1 downto 0);
	signal InputDataValid     : std_logic;
	signal ReadHeaderFifo     : std_logic;
	signal SendBack           : std_logic;
	signal TerminalBusy       : std_logic;
	-------------------------------------------------
	-- INPUT_TABLE
	signal PacketType_i      : std_logic_vector(2-1 downto 0); -- Encodes modes
	signal DataOutputValid_i : std_logic;
	signal BBInputs          : std_logic_vector(16+16-1 downto 0);
	signal DataIdx_i         : std_logic_vector(natural(ceil(log2(real(2))))-1 downto 0);
	signal TaskID_i          : std_logic_vector(natural(ceil(log2(real(5))))-1 downto 0);
	signal PayloadReceived_i : std_logic_vector(FlitWidth-1 downto 0);
--	constant ComHeader_i     : std_logic_vector(FlitWidth-1 downto 0):="0000000000010000";
	
	-------------------------------------------------
	signal NoC_0_AckRx : std_logic_vector(DimX*DimY-1 downto 0);
	signal NoC_0_AckTx : std_logic_vector(DimX*DimY-1 downto 0);
	signal NoC_0_DataIn : FLITS(DimX*DimY-1 downto 0);
	signal NoC_0_DataOut : FLITS(DimX*DimY-1 downto 0);
	signal NoC_0_Rx : std_logic_vector(DimX*DimY-1 downto 0);
	signal NoC_0_Tx : std_logic_vector(DimX*DimY-1 downto 0);
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_AckRx : std_logic;
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_AckTx : std_logic;
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_DataIn : std_logic_vector(FlitWidth-1 downto 0);
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_DataOut : std_logic_vector(FlitWidth-1 downto 0);
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_Rx : std_logic;
	signal Wrapped_BOPM_computation_unit_dummy_Service_0_Tx : std_logic;
	
	-------------------------------------------------
	type TEST_TYPE is (NORMAL, LOOPBACK, TRANSFERT_CTRL, ROUTER, NOC, TESTNODE, WRAPPED_NODE, SINGLE_NODE);
	constant TEST : TEST_TYPE := NORMAL;
	
begin  -- v0

	ConfigRegister <= ConfigRegister_i(ConfigRegisterIdx);
	--------------------------------------------------
	LED(0) <= Toggle_i;
--	LED(2 downto 1) <= TX_FIFO_IsEmpty_i & RX_FIFO_IsEmpty_i;
	LED(1) <= '1' when RX_State_i=DATA_STATE else '0';
	LED(2) <= '1' when TX_State_i=DATA_STATE else '0';
	LED(3) <= '0';
	LED(7 downto 4) <= STD_LOGIC_VECTOR(Rx_Len_i(3 downto 0));


--###################################################################
-- RX 
--###################################################################
	CHNL_RX_CLK      <= CLK;
	CHNL_RX_ACK      <= '1' when Rx_State_i = DATA_STATE else '0';
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
						Rx_State_i <= END_STATE;
					end if;
					
				when END_STATE => -- Wait for RX fall
					if CHNL_RX='0' then
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

--	REMOVABLE_CONVERTER : if TEST/=TRANSFERT_CTRL generate
		----------------------------------------------
		FifoToHandShake : entity work.FifoToHandShake
			GENERIC MAP(
				FlitWidth    => FlitWidth)
			PORT MAP(
				Clk          => CLK,
				Rst          => RST,

--				HS_Tx        => HS_Rx_i,
--				HS_AckTx     => HS_AckRx_i,
--				HS_DataOut   => HS_DataIn_i,
				HS_Tx        => Tx,
				HS_AckTx     => AckTx,
				HS_DataOut   => DataOut,

				FIFO_DataOut => RX_FIFO_DataOut_i,
				FIFO_Read    => RX_FIFO_Read_i,
				FIFO_IsEmpty => RX_FIFO_IsEmpty_i);
--	end generate;
	

--###################################################################
-- INTERNAL
--###################################################################
	
--	NORMAL_Mode : if TEST=NORMAL generate
--		--------------------------------------------------
--		-- LOOPBACK CONNECTIONS
--		--------------------------------------------------
--		DataOut      <= HS_DataOut_i;
--		Tx           <= HS_Tx_i;
--		HS_AckTx_i   <= AckTx;
--		
--		HS_DataIn_i  <= DataIn;
--		HS_Rx_i      <= Rx;
--		AckRx        <= HS_AckRx_i;
--		
--	end generate;
	
	LOOPBACK_Mode : if TEST=LOOPBACK generate
		--------------------------------------------------
		-- LOOPBACK CONNECTIONS
		--------------------------------------------------
		HS_Rx_i      <= HS_Tx_i;
		HS_AckTx_i   <= HS_AckRx_i;
		HS_DataIn_i  <= HS_DataOut_i;
	end generate;

--	ROUTER_Mode : if TEST=ROUTER generate
--		--------------------------------------------------
--		-- ROUTER CONNECTIONS
--		--------------------------------------------------
--		RouterUnderTest : entity work.Router
--			GENERIC MAP(
--				FlitWidth      => FlitWidth,
--				NbInputs       => 5,
--				NbOutputs      => 5,
--				X_Local        => 0,
--				Y_Local        => 0,
--				InputFifoDepth => 56)
--			PORT MAP(
--				HS_Rx      => Router_Rx, --: IN std_logic_vector(NbInputs-1 downto 0);
--				HS_DataIn  => Router_DataIn, --: IN  FLITS(NbInputs-1 downto 0);
--				HS_AckTx   => Router_AckTx, --: IN  std_logic_vector(NbOutputs-1 downto 0);
--				HS_AckRx   => Router_AckRx, --: OUT std_logic_vector(NbInputs-1 downto 0);
--				HS_Tx      => Router_Tx,      --: OUT std_logic_vector(NbOutputs-1 downto 0);
--				HS_DataOut => Router_DataOut, --: OUT FLITS(NbOutputs-1 downto 0);
--				clock      => CLK,-- : IN  std_logic;
--				reset      => RST);-- : IN  std_logic);
------				
--		Router_Rx(1)      <= HS_Rx_i;
--		HS_AckRx_i        <= Router_AckRx(1);
--		Router_DataIn(1)  <= HS_DataIn_i;
--		
--		HS_Tx_i           <= Router_Tx(4);
--		Router_AckTx(4)   <= HS_AckTx_i;
--		HS_DataOut_i      <= Router_DataOut(4);
--	end generate;
		
--	TRANSFERT_CTRL_Mode : if TEST=TRANSFERT_CTRL generate
--		--------------------------------------------------
--		-- TRANSFERT CONTROLLER CONNECTIONS
----		--------------------------------------------------
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
--				HS_Tx      => HS_Tx_i,
--				HS_AckTx   => HS_AckTx_i,
--				HS_DataOut => HS_DataOut_i--,
--				
----				STATE       => DebugReg1_i,
----				FlitCounter => DebugReg2_i,
----				DataOut     => DebugReg3_i
--				);
--	end generate;
	
--	NOC_Mode : if TEST=NOC generate
--		--------------------------------------------------
--		-- NOC CONNECTIONS
--		--------------------------------------------------
--		-- AdOCNet On-Chip-Network
--		NoC_0: entity work.AdOCNet(RTL)
--			generic map(
--				InputFifoDepth_Table => (32,32),
--				NbOutputs_Table      => (5,5),
--				NbInputs_Table       => (5,5),
--				FlitWidth            => FlitWidth,
--				DimY                 => DimY,
--				DimX                 => DimX
--				)
--			port map(
--				clock   => CLK,
--				reset   => RST,
--				Rx      => NoC_0_Rx,
--				DataIn  => NoC_0_DataIn,
--				AckRx   => NoC_0_AckRx,
--				DataOut => NoC_0_DataOut,
--				AckTx   => NoC_0_AckTx,
--				Tx      => NoC_0_Tx
--				);
--				
--		HS_Tx_i <= NoC_0_Tx(0);
--		NoC_0_AckTx(0) <= HS_AckTx_i;
--		HS_DataOut_i <= NoC_0_DataOut(0);
--		
----		PCIe_0_AckTx <= NoC_0_AckRx(0);
----		NoC_0_DataIn(0) <= PCIe_0_DataOut;
----		NoC_0_Rx(0) <= PCIe_0_Tx;
--		
----		Wrapped_BOPM_computation_unit_dummy_Service_1_Rx <= NoC_0_Tx(1);
----		NoC_0_AckTx(1) <= Wrapped_BOPM_computation_unit_dummy_Service_1_AckRx;
----		Wrapped_BOPM_computation_unit_dummy_Service_1_DataIn <= NoC_0_DataOut(1);
--		
--		HS_AckRx_i <= NoC_0_AckRx(1);
--		NoC_0_DataIn(1) <= HS_DataIn_i;
--		NoC_0_Rx(1) <= HS_Rx_i;
--	end generate;
	
	
--	TESTNODE_Mode : if TEST=TESTNODE generate
--		
--		-----------------------------------------------------------------
--		-- TestNode controller
--		TestNode_0: entity work.TestNode_Test(RTL)
--			generic map(
--				ComHeader => ComHeader_i,
--				FlitWidth => FlitWidth
--				)
--			port map(
--				Clock   => CLK,
--				Reset   => RST,
--			
--				AckTx   => HS_AckTx_i,
--				Rx      => HS_Rx_i,
--				DataIn  => HS_DataIn_i,
--				Tx      => HS_Tx_i,
--				DataOut => HS_DataOut_i,
--				AckRx   => HS_AckRx_i--,
--				
----				Debug0_En => Debug0_En_i,
----				Debug0    => Debug0_i
--				);
--	end generate;
	
--	WRAPPED_NODE_Mode : if TEST=WRAPPED_NODE generate
--		Wrapped_BOPM_computation_unit_dummy_Service_0: entity work.Wrapped_BOPM_computation_unit_dummy(RTL)
--			generic map(
--				ComHeader => "0000000000010000",
--				NBTask    => 5,
--				FlitWidth => FlitWidth
--				)
--			port map(
--				clock   => Clk,
--				reset   => Rst,
--				DataIn  => HS_DataIn_i,
--				Rx      => HS_Rx_i,
--				AckTx   => HS_AckTx_i,
--				AckRx   => HS_AckRx_i,
--				DataOut => HS_DataOut_i,
--				Tx      => HS_Tx_i
--				);
--	end generate;
	
	
--	SINGLE_NODE_Mode : if TEST=SINGLE_NODE generate
--	
--		SingleNode : entity work.SingleNodeBopm(RTL)
--		generic map(
--			ComHeader            => "0000000000010000",
--			DimX                 => 2,
--			DimY                 => 1,
--			FlitWidth            => 16,
--			NbInputs_Table       => (5,5),
--			NbOutputs_Table      => (5,5),
--			InputFifoDepth_Table => (32,32))
--		port map(
--			clock          => Clk,
--			reset          => Rst,
--		
--			PCIe_0_DataIn  => HS_DataOut_i,
--			PCIe_0_Rx      => HS_Tx_i,
--			PCIe_0_AckRx   => HS_AckTx_i,
--		
--			PCIe_0_AckTx   => HS_AckRx_i,
--			PCIe_0_DataOut => HS_DataIn_i,
--			PCIe_0_Tx      => HS_Rx_i);

--	end generate;
		
				
	--------------------------------------------------
	ConfigRegister_i(12)(0) <= '1' when Tx_State_i=INIT_STATE else '0';
	ConfigRegister_i(12)(FlitWidth-1 downto 1) <= (others=>'0');

	----------------------------------------------------
	CONFIG_REGISTERS: process(CLK, RST)
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
			Debug_Count_Inputs_i <= (others=>'0');
			Debug_Count_Outputs_i<= (others=>'0');
			
		elsif rising_edge(CLK) then
	
			if Rx_State_i=END_STATE and Rx_Count_i=TO_UNSIGNED(0, Rx_Count_i'length) then
				Debug_Count_Inputs_i  <= (others=>'0');
				Debug_Count_Outputs_i <= (others=>'0');
			else
				if HS_AckRx_i='1' then --
					Debug_Count_Inputs_i <= Debug_Count_Inputs_i + 1;
					if TO_INTEGER(Debug_Count_Inputs_i)=0 then
						ConfigRegister_i(0) <= HS_DataIn_i;--HS_DataIn_i
					elsif TO_INTEGER(Debug_Count_Inputs_i)=1 then
						ConfigRegister_i(1) <= HS_DataIn_i;
					elsif TO_INTEGER(Debug_Count_Inputs_i)=2 then
						ConfigRegister_i(2) <= HS_DataIn_i;
					elsif TO_INTEGER(Debug_Count_Inputs_i)=3 then
						ConfigRegister_i(3) <= HS_DataIn_i;
					elsif TO_INTEGER(Debug_Count_Inputs_i)=4 then
						ConfigRegister_i(4) <= HS_DataIn_i;
					elsif TO_INTEGER(Debug_Count_Inputs_i)=5 then
						ConfigRegister_i(5) <= HS_DataIn_i;
					end if;
				end if;
--			if HeaderValid='1' then
----				ConfigRegister_i(0)   <= InputData;--HS_DataIn_i
--				Debug_Count_Inputs_i  <= (others=>'0');
--				Debug_Count_Outputs_i <= (others=>'0');
--			else
--				if InputDataValid='1' then --HS_AckRx_i
----						Debug_Count_Inputs_i <= (others=>'0');
----					else
--					Debug_Count_Inputs_i <= Debug_Count_Inputs_i + 1;
----					end if;
--					if TO_INTEGER(Debug_Count_Inputs_i)=0 then
--						ConfigRegister_i(0) <= InputData;--HS_DataIn_i
--					elsif TO_INTEGER(Debug_Count_Inputs_i)=1 then
--						ConfigRegister_i(1) <= InputData;
--					elsif TO_INTEGER(Debug_Count_Inputs_i)=2 then
--						ConfigRegister_i(2) <= InputData;
--					elsif TO_INTEGER(Debug_Count_Inputs_i)=3 then
--						ConfigRegister_i(3) <= InputData;
--					elsif TO_INTEGER(Debug_Count_Inputs_i)=4 then
--						ConfigRegister_i(4) <= InputData;
--					elsif TO_INTEGER(Debug_Count_Inputs_i)=5 then
--						ConfigRegister_i(5) <= InputData;
--					end if;
--				end if;
--				if UNSIGNED(DebugVector_i)/=TO_UNSIGNED(5, DebugVector_i'length) then
----					if TO_INTEGER(Debug_Count_Outputs_i)=5 or HeaderValid='1' then
----						Debug_Count_Outputs_i <= (others=>'0');
----					else
--					Debug_Count_Outputs_i <= Debug_Count_Outputs_i + 1;
----					end if;
--					if TO_INTEGER(Debug_Count_Outputs_i)=0 then
--						ConfigRegister_i(6) <= DebugVector_i;
--					elsif TO_INTEGER(Debug_Count_Outputs_i)=1 then
--						ConfigRegister_i(7) <= DebugVector_i;
--					elsif TO_INTEGER(Debug_Count_Outputs_i)=2 then
--						ConfigRegister_i(8) <= DebugVector_i;
--					elsif TO_INTEGER(Debug_Count_Outputs_i)=3 then
--						ConfigRegister_i(9) <= DebugVector_i;
--					elsif TO_INTEGER(Debug_Count_Outputs_i)=4 then
--						ConfigRegister_i(10) <= DebugVector_i;
--					elsif TO_INTEGER(Debug_Count_Outputs_i)=5 then
--						ConfigRegister_i(11) <= DebugVector_i;
--	--						ConfigRegister_i(11) <= DebugReg2_i;
--					end if;
--				end if;
--			end if;
				if HS_AckTx_i='1' then
					Debug_Count_Outputs_i <= Debug_Count_Outputs_i + 1;
					if TO_INTEGER(Debug_Count_Outputs_i)=0 then
						ConfigRegister_i(6) <= HS_DataOut_i;
					elsif TO_INTEGER(Debug_Count_Outputs_i)=1 then
						ConfigRegister_i(7) <= HS_DataOut_i;
					elsif TO_INTEGER(Debug_Count_Outputs_i)=2 then
						ConfigRegister_i(8) <= HS_DataOut_i;
					elsif TO_INTEGER(Debug_Count_Outputs_i)=3 then
						ConfigRegister_i(9) <= HS_DataOut_i;
					elsif TO_INTEGER(Debug_Count_Outputs_i)=4 then
						ConfigRegister_i(10) <= HS_DataOut_i;
					elsif TO_INTEGER(Debug_Count_Outputs_i)=5 then
						ConfigRegister_i(11) <= HS_DataOut_i;
					end if;
				end if;
			end if;
		end if;
	end process;
	ConfigRegister_i(13)(Minimum(Rx_Len_i'length,FlitWidth)-1 downto 0) <= STD_LOGIC_VECTOR(Rx_Len_i(Minimum(Rx_Len_i'length,FlitWidth)-1 downto 0));
	ConfigRegister_i(14) <= STD_LOGIC_VECTOR(Payload_i);
	ConfigRegister_i(15)(FlitWidth-1 downto 0) <= STD_LOGIC_VECTOR(LatencyCounter_i);


--###################################################################
--           TX SIDE
--###################################################################
	
	------------------------------------------------
	HandShakeToFifo : entity work.HandShakeToFifo
		GENERIC MAP(
			FlitWidth    => FlitWidth)
		PORT MAP(
			Clk          => CLK,
			Rst          => RST,

--			HS_Rx        => HS_Tx_i,
--			HS_AckRx     => HS_AckTx_i,
--			HS_DataIn    => HS_DataOut_i,
			HS_Rx        => Rx,
			HS_AckRx     => AckRx,
			HS_DataIn    => DataIn,

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
	Tx_Max_i(Minimum(Tx_Max_i'length,FlitWidth)-1 downto 0) <= Payload_i(Minimum(Tx_Max_i'length,FlitWidth)-1 downto 0)+1;
	
	ZeroFill : if Tx_Max_i'length>FlitWidth generate
		Tx_Max_i(Tx_Max_i'length-1 downto FlitWidth) <= (others=>'0'); 
	end generate;
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
						if Rx_State_i=DATA_STATE and Rx_Count_i=TO_UNSIGNED(0, Rx_Count_i'length) then
							LatencyCounter_State_i <= RESET_STATE;
						elsif Tx_State_i=DATA_STATE and (Tx_Count_i > Tx_Max_i) then
							LatencyCounter_State_i <= STOP_STATE;
						end if;
					when others => null;
				end case;
			end if;
		end if;
	end process;	
	
end Struct;

























