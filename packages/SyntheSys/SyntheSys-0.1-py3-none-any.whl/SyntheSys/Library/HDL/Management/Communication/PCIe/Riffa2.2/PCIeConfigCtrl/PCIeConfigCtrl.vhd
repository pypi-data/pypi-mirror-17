
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: Riffa configuration controller
-------------------------------------------------------------------------------
entity PCIeConfigCtrl is
	GENERIC(
		C_PCI_DATA_WIDTH : natural := 32;
		FlitWidth        : natural := 16;
		NBREG            : natural := 16);
	PORT(
		LED          : OUT std_logic_vector(7 downto 0);
		CLK          : in  std_logic;
		RST          : in  std_logic;
		CHNL_RX_CLK  : out std_logic;
		CHNL_RX      : in  std_logic;
		CHNL_RX_ACK  : out std_logic;
		CHNL_RX_LAST : in  std_logic;
		CHNL_RX_LEN  : in  std_logic_vector(31 downto 0);
		CHNL_RX_OFF  : in  std_logic_vector(30 downto 0);
		CHNL_RX_DATA : in  std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
		CHNL_RX_DATA_VALID : in std_logic;
		CHNL_RX_DATA_REN   : out std_logic;
	
		CHNL_TX_CLK  : out std_logic;
		CHNL_TX      : out std_logic;
		CHNL_TX_ACK  : in  std_logic;
		CHNL_TX_LAST : out std_logic;
		CHNL_TX_LEN  : out std_logic_vector(31 downto 0);
		CHNL_TX_OFF  : out std_logic_vector(30 downto 0);
		CHNL_TX_DATA : out std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
		CHNL_TX_DATA_VALID : out std_logic;
		CHNL_TX_DATA_REN   : in  std_logic;
		
		ConfigRegister     : IN  std_logic_vector(FlitWidth-1 downto 0);
		ConfigRegisterIdx  : OUT natural);
end entity PCIeConfigCtrl;

------------------------------------------------------------------
architecture RTL of PCIeConfigCtrl is 

	signal Tx_Data_i    : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal Rx_Len_i     : unsigned(31 downto 0) := (others=>'0');
	signal Rx_Count_i, Tx_Count_i   : unsigned(31 downto 0) := (others=>'0');
--	signal rState : std_logic_vector(1 downto 0) := (others=>'0');
	signal CHNL_TX_DATA_VALID_i : std_logic;
	
	type Registers_Type is array (0 to NBREG-1) of std_logic_vector(FlitWidth-1 downto 0);
	signal ConfigRegister_i : Registers_Type;
	
	type Rx_State_type is (WAITREQ_STATE, DATA_STATE, SEND_BACK_STATE);
	signal Rx_State_i : Rx_State_type := WAITREQ_STATE;

	type Tx_State_type is (INIT_STATE, DATA_STATE);
	signal Tx_State_i : Tx_State_type := INIT_STATE;

begin 

--	LED(1) <= Toggle_i;
--	LED(2) <= '1' when Rx_State_i/=WAITREQ_STATE else '0';
--	LED(3) <= '1' when Tx_State_i=DATA_STATE else '0';
	LED(3 downto 0) <= STD_LOGIC_VECTOR(Rx_Count_i(3 downto 0));
	LED(7 downto 4) <= STD_LOGIC_VECTOR(Rx_Len_i(3 downto 0));
	
--	--------------------------------------------------
--	LED_CntRx_Process : process(CLK)
--	begin
--		if rising_edge(CLK) then
--			if RST='1' then
--				LED(0)  <= '1';
--			else
--				LED(0)  <= '0';
--			end if;
--		end if;
--	end process;	

	CHNL_RX_CLK <= CLK;
	CHNL_RX_ACK <= '1' when Rx_State_i = DATA_STATE else '0';
	CHNL_RX_DATA_REN <= '1' when Rx_State_i = DATA_STATE else '0';

	CHNL_TX_CLK <= CLK;
	CHNL_TX <= '1' when Tx_State_i = DATA_STATE else '0';
	CHNL_TX_LAST <= '1';-- when Rx_State_i = "01" else '0';
	CHNL_TX_LEN <= STD_LOGIC_VECTOR(TO_UNSIGNED(32, CHNL_TX_LEN'length)); -- in words
	CHNL_TX_OFF <= (others=>'0');
	CHNL_TX_DATA <= Tx_Data_i;
	CHNL_TX_DATA_VALID_i <= '1' when Tx_State_i = DATA_STATE else '0';
	CHNL_TX_DATA_VALID   <= CHNL_TX_DATA_VALID_i;


	----------------------------------------------------
	FSM_RX : process(CLK, RST)
	begin
		if RST='1' then
			Rx_Len_i   <= (others=>'0');
			Rx_Count_i <= (others=>'0');
			Rx_State_i <= WAITREQ_STATE;
			ConfigRegister_i <= (others=>(others=>'0'));
			
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
						ConfigRegister_i(TO_INTEGER(Rx_Count_i)) <= CHNL_RX_DATA(FlitWidth-1 downto 0);
						Rx_Count_i <= Rx_Count_i + 1;
					end if;
					if Rx_Count_i >= Rx_Len_i then
						Rx_State_i <= SEND_BACK_STATE;
					end if;
					
				when SEND_BACK_STATE => 
					Rx_State_i <= WAITREQ_STATE;
					
				when others => null;
			end case;
		end if;
	end process;
	
	ConfigRegisterIdx <= NATURAL(TO_INTEGER(Tx_Count_i));
	----------------------------------------------------
	FSM_TX : process(CLK, RST)
	begin
		if RST='1' then
			Tx_Count_i <= (others=>'0');
			Tx_State_i <= INIT_STATE;
			Tx_Data_i  <= (others=>'0');
			
		elsif rising_edge(CLK) then
			case Tx_State_i is 
				when INIT_STATE => -- Prepare for TX 
					Tx_Data_i(FlitWidth-1 downto 0)  <= ConfigRegister;
					if Rx_State_i=SEND_BACK_STATE then
						Tx_Count_i <= TO_UNSIGNED(1, Tx_Count_i'length);
						Tx_State_i <= DATA_STATE;
					else
						Tx_Count_i <= TO_UNSIGNED(0, Tx_Count_i'length);
					end if;
				
				when DATA_STATE => -- Start TX with save length and data value
					if CHNL_TX_DATA_REN='1' and CHNL_TX_DATA_VALID_i='1' then
						Tx_Data_i(FlitWidth-1 downto 0)  <= ConfigRegister;
						Tx_Count_i <= Tx_Count_i + 1;
						if (Tx_Count_i >= TO_UNSIGNED(16, Tx_Count_i'length)) then
							Tx_State_i <= INIT_STATE;
						end if;
					end if;
					
				when others => null;
			end case;
		end if;
	end process;


end architecture;














