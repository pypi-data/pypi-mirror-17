library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.STD_LOGIC_arith.ALL;
use ieee.numeric_std.all;


-------------------------------------------------------------------------------
-- ENTITY: RX pulse generator
-------------------------------------------------------------------------------
entity UARTStation is
  generic (
    UART_Clk_Cycle : time:= 500 ns);
  port (
    Rst          : in  std_logic;
    
    DataIn       : in  std_logic_vector(15 downto 0);
    DataValidIn  : in  std_logic;
    
    DataOut      : out std_logic_vector(15 downto 0);
    DataValidOut : out std_logic;

    TX           : out std_logic;
    RX           : in std_logic);

end UARTStation;


-------------------------------------------------------------------------------
-- ARCHITECTURE : version 0
-------------------------------------------------------------------------------
architecture v0 of UARTStation is

  signal BitstreamIN, BitstreamOUT : std_logic_vector(19 downto 0) := X"00000";

  signal DataReceived : std_logic_vector(15 downto 0) := X"0000";
  signal DataValidR   : std_logic := '0';

  signal TX_s         : std_logic := '0';
  signal ClkUART_RX, ClkUART_TX  : std_logic := '0';

  signal i         : natural   :=  0;         -- Number of bit received through RX
  signal Receiving : std_logic := '0';

begin  -- v0
  
  ClkUART_TX <= not ClkUART_TX after UART_Clk_Cycle;
               
  TX <= TX_s;

  DataValidOut <= DataValidR;
  DataOut      <= DataReceived;

               -- LSb ---------->------------->------------->-----------> MSb 
  BitstreamOUT <= '1' & DataIn(7 downto 0) & "01" & DataIn(15 downto 8) & '0' when DataValidIn ='1'
                  else X"00000" when Rst='1'
                  else BitstreamOUT;
  
  DataReceived <= BitstreamIN(18 downto 11) & BitstreamIN(8 downto 1) when DataValidR='1'
                  else X"0000" when Rst='1'
                  else DataReceived;
  
-------------------------------------------------------------------------------
  SendData: process (ClkUART_TX, Rst)
    variable k : natural := 0;         -- Number of bit to send through TX
  begin  -- process SendData
    if Rst = '1' then                   -- asynchronous reset (active high)
      TX_s <= '1';
      k  := 0;
    elsif ClkUART_TX'event and ClkUART_TX = '1' then  -- rising clock edge
      if DataValidIn = '1' then         -- if new data to send
        if k = 20 then                   --   and all bit already sent
          TX_s <= TX_s;
          k  := k; -- keep value until DataValidIn = '0'
        else                            --   send remaining bits
          TX_s <= BitstreamOUT(k);
          k  := k + 1;
        end if;
      else                              -- If no data to send
        TX_s <= TX_s;
        k  := 0;                       -- Reset
      end if;
    else
        TX_s <= TX_s;
        k  := k;
    end if;
  end process SendData;
  
-------------------------------------------------------------------------------
  ReceiveData: process (ClkUART_RX, Receiving)
  begin  -- process SendData
    if Receiving = '0' then                   -- asynchronous reset (active high)
      i <= 0;
    elsif ClkUART_RX'event and ClkUART_RX = '1' then  -- rising clock edge
      if Receiving = '1' then
        i <= i + 1;
        BitstreamIN <= RX & BitstreamIN(19 downto 1);
      else
        i <= 0;
        BitstreamIN <= BitstreamIN;
      end if;
      
    end if;
  end process ReceiveData;

  Receiving  <= '1' when  (RX = '0' and i=0)
                else '0' when i=20
                else Receiving;
  
  DataValidR <= '1' when i=20 else '0';

  ClkUART_RX <= not ClkUART_RX after UART_Clk_Cycle when Receiving='1' else '0';
    
end v0;

