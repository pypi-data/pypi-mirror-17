
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;

-------------------------------------------------------------------------------
-- ENTITY: TransfertControl that controls the packet transfert
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

	signal InputConnected_i : std_logic :='0';
	signal InputRequests_i  : std_logic :='0';
	signal FifoIn_Read_i    : std_logic :='0';

	signal PayloadReceived_i   : UNSIGNED(FlitWidth-1 downto 0);
	
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
							FlitCounter_i <= FlitCounter_i+1;
							if FlitCounter_i>=PayloadReceived_i then
								MainCtrl_State_i <= STOP_CONNECTION_STATE;
							else
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
					if FifoIn_IsEmpty='0' then
						HS_Tx            <= '1';
						FifoIn_Read_i    <= '1';
					else
						HS_Tx            <= '0';
						FifoIn_Read_i    <= '0';
					end if;
					InputConnected_i  <= '1';
				else
					HS_Tx            <= '1';
					FifoIn_Read_i    <= '0';
					InputConnected_i <= '0';
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
					if FlitCounter_i>=PayloadReceived_i then
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
	

end RTL;


