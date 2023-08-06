
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;

-------------------------------------------------------------------------------
-- ENTITY: TransfertControl that 
-------------------------------------------------------------------------------
entity TransfertControl is
	generic (
		FlitWidth  : natural := 16);
	port (
		Clk, Rst          : in  std_logic;

		FifoIn_IsEmpty    : in  std_logic;
		FifoIn_DataOut    : in  std_logic_vector(FlitWidth-1 downto 0);
		FifoIn_Read       : out std_logic;

		HS_AckTx          : in  std_logic;
		HS_Tx             : out std_logic;
		HS_DataOut        : out std_logic_vector(FlitWidth-1 downto 0);

		InputRequests     : out std_logic;
		InputConnected    : out std_logic
		);

end TransfertControl;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of TransfertControl is

--	type FSM_STATE is (IDLE, HEADER, PAYLOAD, CONNECTED, ENDCONNECTION);
--	signal CurrentState_i : FSM_STATE := IDLE;
--	signal Cnt : natural := 0;

--	signal FifoIn_Read_int  : std_logic :='0';
--	signal BothSideReady    : std_logic :='0';
	signal InputConnected_i : std_logic :='0';
	signal InputRequests_i  : std_logic :='0';
	signal FifoIn_Read_i    : std_logic :='0';

--	constant ZEROS : UNSIGNED(FlitWidth-1 downto 0) := TO_UNSIGNED(0, FlitWidth);
--	constant ONE   : UNSIGNED(FlitWidth-1 downto 0) := TO_UNSIGNED(1, FlitWidth);
	signal PayloadReceived_i   : UNSIGNED(FlitWidth-1 downto 0);
--	signal DataRead_i          : UNSIGNED(FlitWidth-1 downto 0);
	
	type MainCtrl_State_type is (DISCONNECTED_STATE, REQUEST_CONNECTION_STATE, PAYLOAD_STATE, DATA_STATE, WAIT_PAYLOAD_STATE, WAIT_DATA_STATE, STOP_CONNECTION_STATE);
	signal MainCtrl_State_i : MainCtrl_State_type := DISCONNECTED_STATE;
	
	signal FlitCounter_i : unsigned(FlitWidth-1 downto 0);
	
begin  -- RTL

	HS_DataOut     <= FifoIn_DataOut;
	
	InputConnected <= InputConnected_i;
	InputRequests  <= InputRequests_i;
	
	FifoIn_Read <= FifoIn_Read_i;
	
	--------------------------------------------------
	MainCtrl_Process : process(CLK)
	begin
		if rising_edge(CLK) then
			if RST='1' then
				PayloadReceived_i <= (others=>'0');
				FlitCounter_i     <= (others=>'0');
				MainCtrl_State_i <= DISCONNECTED_STATE;
			else
				case MainCtrl_State_i is 
					when DISCONNECTED_STATE => 
						PayloadReceived_i <= (others=>'0');
						FlitCounter_i     <= (others=>'0');
						if FifoIn_IsEmpty='0' then
							MainCtrl_State_i <= REQUEST_CONNECTION_STATE;
						end if;
					when REQUEST_CONNECTION_STATE => 
						if HS_AckTx='1' then
							if FifoIn_IsEmpty='0' then
								MainCtrl_State_i <= PAYLOAD_STATE;
							else
								MainCtrl_State_i <= WAIT_PAYLOAD_STATE;
							end if;
						end if;
					when PAYLOAD_STATE => 
						PayloadReceived_i <= UNSIGNED(FifoIn_DataOut);
						if HS_AckTx='1' then
							FlitCounter_i <= FlitCounter_i+1;
							if FifoIn_IsEmpty='0' then
								MainCtrl_State_i <= DATA_STATE;
							else
								MainCtrl_State_i <= WAIT_DATA_STATE;
							end if;
						end if;
					when DATA_STATE => 
						if HS_AckTx='1' then
							if PayloadReceived_i=FlitCounter_i then
								MainCtrl_State_i <= STOP_CONNECTION_STATE;
							else
								FlitCounter_i <= FlitCounter_i+1;
								if FifoIn_IsEmpty='1' then
									MainCtrl_State_i <= WAIT_DATA_STATE;
								end if;
							end if;
						end if;
					when WAIT_PAYLOAD_STATE => 
						if FifoIn_IsEmpty='0' then
							MainCtrl_State_i <= PAYLOAD_STATE;
						end if;
					when WAIT_DATA_STATE => 
						if FifoIn_IsEmpty='0' then
							MainCtrl_State_i <= DATA_STATE;
						end if;
					when STOP_CONNECTION_STATE => 
						MainCtrl_State_i <= DISCONNECTED_STATE;
					when others => null;
				end case;
			end if;
		end if;
	end process;	
	
	--------------------------------------------------
	MainCtrl_Process_Outputs : process(MainCtrl_State_i, FifoIn_IsEmpty, HS_AckTx, PayloadReceived_i, FlitCounter_i, FifoIn_DataOut)
	begin
		case MainCtrl_State_i is 
			when DISCONNECTED_STATE => 
				InputConnected_i  <= '0';
				HS_Tx             <= '0';
				InputRequests_i   <= '0';
				if FifoIn_IsEmpty='0' then
					FifoIn_Read_i     <= '1';
				else
					FifoIn_Read_i     <= '0';
				end if;
			when REQUEST_CONNECTION_STATE => 
				InputRequests_i  <= '1';
				if HS_AckTx='1' then
					InputConnected_i  <= '1';
					if FifoIn_IsEmpty='0' then
						HS_Tx            <= '1';
						FifoIn_Read_i    <= '1';
					else
						HS_Tx            <= '0';
						FifoIn_Read_i    <= '0';
					end if;
				else
					HS_Tx            <= '1';
					InputConnected_i <= '0';
					FifoIn_Read_i    <= '0';
				end if;
			when PAYLOAD_STATE => 
				InputConnected_i  <= '1';
				InputRequests_i   <= '1';
				if HS_AckTx='1' then
					if FifoIn_IsEmpty='0' then
						HS_Tx            <= '1';
						FifoIn_Read_i    <= '1';
					else
						HS_Tx            <= '0';
						FifoIn_Read_i    <= '0';
					end if;
				else
					HS_Tx            <= '1';
					FifoIn_Read_i    <= '0';
				end if;
			when DATA_STATE => 
				InputConnected_i  <= '1';
				InputRequests_i   <= '1';
				if HS_AckTx='1' then
					if PayloadReceived_i>=FlitCounter_i then
						FifoIn_Read_i     <= '0';
						HS_Tx             <= '0';
					else
						if FifoIn_IsEmpty='0' then
							FifoIn_Read_i    <= '1';
							HS_Tx            <= '1';
						else
							FifoIn_Read_i    <= '0';
							HS_Tx            <= '0';
						end if;
					end if;
				else
					HS_Tx            <= '1';
					FifoIn_Read_i    <= '0';
				end if;
			when WAIT_PAYLOAD_STATE => 
				InputRequests_i   <= '1';
				InputConnected_i  <= '1';
				HS_Tx             <= '0';
				if FifoIn_IsEmpty='0' then
					FifoIn_Read_i    <= '1';
				else
					FifoIn_Read_i    <= '0';
				end if;
			when WAIT_DATA_STATE => 
				InputRequests_i   <= '1';
				InputConnected_i  <= '1';
				HS_Tx             <= '0';
				if FifoIn_IsEmpty='0' then
					FifoIn_Read_i    <= '1';
				else
					FifoIn_Read_i    <= '0';
				end if;
			when STOP_CONNECTION_STATE => 
				InputRequests_i   <= '0';
				InputConnected_i  <= '0';
				HS_Tx             <= '0';
				FifoIn_Read_i     <= '0';
			when others => 
				InputRequests_i   <= '0';
				InputConnected_i  <= '0';
				HS_Tx             <= '0';
				FifoIn_Read_i     <= '0';
		end case;
	end process;	
	
	
--	HS_Tx          <= '1' when DataRead_i/=ZEROS and PayloadReceived_i/=ONE else '0';
--	------------------------------------------------------------
--	MainCtrl: process(Clk, Rst)
--	begin
--		if (Rst = '1') then
--			PayloadReceived_i <= (others=>'0');
--			InputRequests_i   <= '0';
--			InputConnected_i  <= '0';
--		else 
--			if rising_edge(Clk) then
--				-----------------------
--				if FifoIn_IsEmpty='0' then
--					------ step 1 -------------
--					if InputRequests_i='0' then
--						InputRequests_i <= '1';
--					else
--						------ step 2 -------------
--						if InputConnected_i='0' then
--							if HS_AckTx='1' then
--								InputConnected_i <= '1';
--							end if;
--						else
--							------ step 3+ -------------
--							if PayloadReceived_i=ZEROS then -- INIT PAYLOAD
--								if HS_AckTx='1' then
--									PayloadReceived_i <= UNSIGNED(FifoIn_DataOut);
--								end if;
--							else
--								if HS_AckTx='1' then
--									PayloadReceived_i <= PayloadReceived_i-1;
--								end if;
--								if PayloadReceived_i=ONE then -- DISCONNECT
--									if HS_AckTx='1' then
--										PayloadReceived_i <= PayloadReceived_i-1;
--										InputConnected_i <= '0';
--										InputRequests_i  <= '0';
--									end if;
--								end if;
--							end if;
--						end if;
--					end if;
--				else
--					if PayloadReceived_i=ONE then -- DISCONNECT
--						if HS_AckTx='1' then
--							PayloadReceived_i <= PayloadReceived_i-1;
--							InputConnected_i <= '0';
--							InputRequests_i  <= '0';
--						end if;
--					end if;
--				end if;
--			end if;
--		end if;
--	end process;
--	
--	FifoIn_Read_i <= '0' when (FifoIn_IsEmpty='1' or PayloadReceived_i=ONE) else '1' when InputRequests_i='0' else HS_AckTx;
--	FifoIn_Read <= FifoIn_Read_i;

--	------------------------------------------------------------
--	SentDataCnt: process(Clk, Rst)
--	begin
--		if (Rst = '1') then
--			DataRead_i        <= (others=>'0');
--		else 
--			if rising_edge(Clk) then
--				if InputRequests_i='0' and FifoIn_IsEmpty='0' then
--					DataRead_i <= DataRead_i+1;
--				else
--					if FifoIn_IsEmpty='0' and PayloadReceived_i=ONE then -- DISCONNECT
--						if HS_AckTx='1' then
--							DataRead_i <= (others=>'0');
--						end if;
--					else
--						if FifoIn_Read_i='1' and HS_AckTx='0' then
--							DataRead_i <= DataRead_i+1;
--						elsif FifoIn_Read_i='0' and HS_AckTx='1' then
--							DataRead_i <= DataRead_i-1;
--						end if;
--					end if;
--				end if;
--			end if;
--		end if;
--	end process;


end RTL;


