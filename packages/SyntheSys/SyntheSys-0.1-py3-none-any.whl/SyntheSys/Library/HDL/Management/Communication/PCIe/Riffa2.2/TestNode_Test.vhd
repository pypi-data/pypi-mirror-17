
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: TestNode
-------------------------------------------------------------------------------
entity TestNode_Test is
	GENERIC (
		FlitWidth          : natural := 16;
		ComHeader          : std_logic_vector(15 downto 0) := "0000000000000000"
	);
	PORT (
		Clock              : IN std_logic;
		Reset              : IN std_logic;
		
		-- PCIe FPGA pads
		LED                : OUT std_logic_vector(7 downto 0);
		
		-- Network interface
		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0); -- Connected to NoC local DataOutLocal
		Rx                 : IN  std_logic;    -- Connected to NoC local TX
		AckRx              : OUT std_logic;    -- Connected to NoC local AckTX

		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0); -- Connected to NoC local DataInLocal 
		Tx                 : OUT std_logic;    -- Connected to NoC local RX
		AckTx              : IN  std_logic--;     -- Connected to NoC local AckRX
		
--		Debug0_En          : OUT std_logic;
--		Debug0             : OUT std_logic_vector(FlitWidth-1 downto 0)
	);

end TestNode_Test;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture RTL of TestNode_Test is

	constant ZEROS  : UNSIGNED(FlitWidth-1 downto 0) := (others=>'0');

	signal HeaderTransmitted_i : std_logic_vector(FlitWidth-1 downto 0);
	signal HeaderValid_i       : std_logic;
	signal InputData_i         : std_logic_vector(FlitWidth-1 downto 0);
	signal InputDataValid_i    : std_logic;
	signal FIFO_DataIn_i       : std_logic_vector(FlitWidth-1 downto 0);
	signal FIFO_DataOut_i      : std_logic_vector(FlitWidth-1 downto 0);
	signal FIFO_Empty_i, CtrlFifoEmpty_i        : std_logic;
	signal FIFO_Read_i         : std_logic;
	signal FIFO_Write_i        : std_logic;
	signal PayloadTransmitted_i : std_logic_vector(FlitWidth-1 downto 0);
	signal PayloadValid_i      : std_logic;
	signal ReadHeaderFifo_i    : std_logic;
	signal SendBack_i          : std_logic;
	signal TerminalBusy_i      : std_logic;
	signal Transmitted_i       : std_logic;
	
	signal PayloadReceived_i   : UNSIGNED(FlitWidth-1 downto 0);

	signal Cnt_i               : unsigned(3 downto 0) := (others=>'0');
	signal Buffer_i            : std_logic_vector(FlitWidth-1 downto 0);
	
	type State_type is (INIT_STATE, FILL_STATE);
	signal State_i : State_type := INIT_STATE;

begin  -- v0

	--------------------------------------------------
	NetworkAdapter: entity work.NetworkAdapter(RTL)
		generic map(
			FlitWidth => FlitWidth
			)
		port map(
			Clk                => clock,
			Rst                => reset,
			
			DataIn             => DataIn,
			Tx                 => Tx,
			AckTx              => AckTx,
			
			DataOut            => DataOut,
			Rx                 => Rx,
			AckRx              => AckRx,
			
			SendBack           => '0',
			TerminalBusy       => '0',
			
			OutputData         => FIFO_DataOut_i,
			OutputRead         => FIFO_Read_i,
			OutputFifoEmpty    => CtrlFifoEmpty_i,
			
			ReadHeaderFifo     => open,
			
			HeaderValid        => HeaderValid_i,
			HeaderTransmitted  => HeaderTransmitted_i,
			PayloadValid       => PayloadValid_i,
			InputData          => InputData_i,
			InputDataValid     => InputDataValid_i,
			
			PayloadTransmitted => PayloadTransmitted_i,
			Transmitted        => Transmitted_i
			);
			
--	Debug0_En  <= InputDataValid_i;
--	Debug0     <= InputData_i;
	
	HeaderTransmitted_i  <= ComHeader;
	PayloadTransmitted_i <= "000000000000" & STD_LOGIC_VECTOR(Cnt_i-2);
	-----------------------------------------------------------------
	FIFO: entity work.fifo(RTL)
		generic map(
			largeur => FlitWidth,
			profondeur => 16
			)
		port map(
			clock_in  => clock,
			clock_out => clock,
			reset     => reset,
			
			data_out  => FIFO_DataOut_i,
			rd        => FIFO_Read_i,
			IsEmpty   => FIFO_Empty_i,
			
			data_in   => FIFO_DataIn_i,
			wr        => FIFO_Write_i,
			IsFull    => open,
			ack_rd    => open,
			ack_wr    => open
			);
	FIFO_DataIn_i <=  InputData_i;
	
	
	CtrlFifoEmpty_i <= '0' when InputDataValid_i='1' else FIFO_Empty_i;
	--------------------------------------------------
	LED <= STD_LOGIC_VECTOR(Cnt_i) & Buffer_i(3 downto 0);
	
	--------------------------------------------------
	Counters_Process : process(Clock)
	begin
		if rising_edge(Clock) then
			if HeaderValid_i='1' then
				Cnt_i    <= (others=>'0');
				Buffer_i <= (others=>'0');
			else
				if InputDataValid_i='1' then
					Cnt_i <= Cnt_i+1;
					Buffer_i <= InputData_i;
				end if;
			end if;
		end if;
	end process;


	--------------------------------------------------
--	FSM_SEQ_Process : process(Reset, Clock)
--	begin
--		if rising_edge(Clock) then
--			if Reset='1' then
--				State_i           <= INIT_STATE;
--				PayloadReceived_i <= ZEROS;
--				FIFO_DataIn_i     <= ComHeader;
--			else
--				case State_i is 
--					when INIT_STATE =>
--						FIFO_DataIn_i <= ComHeader;
--						if HeaderValid_i='1' then -- reception d'un packet
--							State_i       <= FILL_STATE;
--						else
--							State_i       <= INIT_STATE;
--						end if;
--						
--					when FILL_STATE => --envoie d'un packet
--						if PayloadReceived_i=ZEROS then
--							PayloadReceived_i <= UNSIGNED(InputData_i)-1;
--							FIFO_DataIn_i     <= InputData_i;
--							State_i           <= FILL_STATE;
--							
--						elsif InputDataValid_i='1' then -- au payload
--							FIFO_DataIn_i     <= STD_LOGIC_VECTOR(PayloadReceived_i);
--							if PayloadReceived_i=ZEROS then
--								State_i           <= INIT_STATE;
--							else
--								PayloadReceived_i <= PayloadReceived_i-1;
--								State_i           <= FILL_STATE;
--							end if;
--							
--						else
--							State_i           <= FILL_STATE;
--						end if;
--						
--					when others => NULL;
--				end case;
--			end if;
--		end if;
--	end process;

	FIFO_Write_i <= InputDataValid_i; --HeaderValid_i or PayloadValid_i or InputDataValid_i;

end RTL;




