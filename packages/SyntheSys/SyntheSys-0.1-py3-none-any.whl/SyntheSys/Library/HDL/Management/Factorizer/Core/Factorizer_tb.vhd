library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;
----------------------------------------------------------
ENTITY Factorizer_tb IS
END Factorizer_tb;

----------------------------------------------------------
ARCHITECTURE behavior OF Factorizer_tb IS 
 
   constant DATAWIDTH  : natural := 32;
   constant ADDRWIDTH  : natural := 10;
   constant NBDEP      : natural := 2;
   
   -- Clock period definitions
   constant clk_period : time := 10 ns;
   
   COMPONENT Factorizer 
    generic (
      DATAWIDTH : natural := 16;
      Payload   : natural := 3;
      Header    : std_logic_vector := (others=>'0');
      NBDEP     : natural := 2);
      
    port (
      Clk      : in std_logic;
      Rst      : in std_logic;
      
      -- External interface
      Debug_Idle  : out  std_logic;
      
      -- Network interface
      Rx       : in  std_logic;-- Connected to NoC local TX
      AckRx    : out std_logic;-- Connected to NoC local AckTX 
      DataIn   : in  std_logic_vector(DataWidth-1 downto 0);-- Connected to NoC local DataOutLocal
      
      Tx       : out std_logic;-- Connected to NoC local RX
      AckTx    : in  std_logic;-- Connected to NoC local AckRX
      DataOut  : out std_logic_vector(DataWidth-1 downto 0));-- Connected to NoC local DataInLocal
    END COMPONENT;
    
    -- Network interface
    signal Rx       : std_logic;-- Connected to NoC local TX
    signal AckRx    : std_logic;-- Connected to NoC local AckTX 
    signal DataIn   : std_logic_vector(DataWidth-1 downto 0);-- Connected to NoC local DataOutLocal
    
    signal Tx       : std_logic;-- Connected to NoC local RX
    signal AckTx    : std_logic;-- Connected to NoC local AckRX
    signal DataOut  : std_logic_vector(DataWidth-1 downto 0);-- Connected to NoC local DataInLocal
   
    signal Clk      : std_logic;
    signal Rst      : std_logic;
    signal Debug_Idle      : std_logic;
    
    
    signal INDEX : natural range 0 to 1024:= 0;
    type Tuple is array (natural range 0 to 1) of std_logic_vector(DataWidth-1 downto 0);
    type StimTable is array (natural range <>) of Tuple;
    signal Stimuli : StimTable(0 to 9) := ( -- ADDRESS, DATA
                                    (X"0000"&X"0000", X"FFFF"&X"FFF0"),
                                    (X"0000"&X"0004", X"FFFF"&X"FFF1"),
                                    (X"0000"&X"0008", X"1FFF"&X"0000"),
                                    (X"0000"&X"000C", X"1FFF"&X"FFF3"),
                                    (X"0000"&X"0010", X"1FFF"&X"0000"),
                                    (X"0000"&X"0014", X"1FFF"&X"FFF5"),
                                    (X"0000"&X"0018", X"1FFF"&X"FFF6"),
                                    (X"0000"&X"001C", X"1FFF"&X"FFF7"),
                                    (X"0000"&X"0020", X"1FFF"&X"FFF8"),
                                    (X"0000"&X"0024", X"1FFF"&X"FFF9")
                                   );
    signal DEP_ADDR : std_logic_vector(DataWidth-1 downto 0);
    signal DEP_DATA : std_logic_vector(DataWidth-1 downto 0);
    
    signal Results : StimTable(0 to 9) := ( -- ADDRESS, DATA
                                    (X"0000"&X"0000", X"ADAC"&X"6000"),
                                    (X"0000"&X"0004", X"ADAC"&X"6001"),
                                    (X"0000"&X"0008", X"ADAC"&X"6002"),
                                    (X"0000"&X"000C", X"ADAC"&X"6003"),
                                    (X"0000"&X"0010", X"ADAC"&X"6004"),
                                    (X"0000"&X"0014", X"ADAC"&X"6005"),
                                    (X"0000"&X"0018", X"ADAC"&X"6006"),
                                    (X"0000"&X"001C", X"ADAC"&X"6007"),
                                    (X"0000"&X"0020", X"ADAC"&X"6008"),
                                    (X"0000"&X"0024", X"ADAC"&X"6009")
                                   );
    signal RES_ADDR : std_logic_vector(DataWidth-1 downto 0);
    signal RES_DATA : std_logic_vector(DataWidth-1 downto 0);
	 
BEGIN

   DEP_ADDR <= Stimuli(INDEX)(0);
   DEP_DATA <= Stimuli(INDEX)(1);

   RES_ADDR <= Results(INDEX)(0);
   RES_DATA <= Results(INDEX)(1);

   -- Clock process definitions
   clk_process :process
   begin
    Clk <= '0';
    wait for clk_period/2;
    Clk <= '1';
    wait for clk_period/2;
   end process clk_process;

   ----------------------------------------------------------
   Factorizer_1: Factorizer 
   GENERIC MAP (
         DATAWIDTH => DATAWIDTH,
         Payload   => 3,
         Header    => X"00000001",
         NBDEP     => NBDEP
        )
   PORT MAP (
         Rst        => Rst,
         Clk        => Clk,
         Debug_Idle => Debug_Idle,
    
         Rx         => Rx,-- Connected to NoC local TX
         AckRx      => AckRx,-- Connected to NoC local AckTX 
         DataIn     => DataIn,-- Connected to NoC local DataOutLocal
          
         Tx         => Tx,-- Connected to NoC local RX
         AckTx      => AckTx,-- Connected to NoC local AckRX
         DataOut    => DataOut
        );
        
   ------------------------------------------------------
   -- Stimulus process
   stim_proc: process
   begin
     ----------------------------------
     Rst      <= '1';
     Rx       <= '0';
     AckTx    <= '0';
     DataIn   <= (others=>'0');
     
     ----------------------------------
     -- hold reset state for 200 ns.
     wait for clk_period*20;
     Rst      <= '0';
    
     -----------------------------------------------------------------------------
     -- RAM INIT PACKETS
     -----------------------------------------------------------------------------
     for i in 0 to Stimuli'length-1 loop
       INDEX <= i;
       wait for 30 ns;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0001"; -- Header
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0003"; -- Payload (3)
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0001"; -- Data = RAM INIT COMMAND
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= DEP_ADDR; -- Data = ADDRESS
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= DEP_DATA; -- Data = ADDRESS DEP 1 & 2
       wait for clk_period;
       
     end loop;
     
     INDEX <= 0;
     wait for 50 ns;
     -----------------------------------------------------------------------------
     -- RESULT PACKETS
     -----------------------------------------------------------------------------
     for i in 0 to Results'length-1 loop
       INDEX <= i;
       wait for 30 ns;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0001"; -- Header
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0003"; -- Payload (3)
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= X"0000"&X"0002"; -- Data = STORE RESULT COMMAND
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= RES_ADDR; -- Data = ADDRESS
       wait for clk_period;
       
       ----------------------------------
       wait for clk_period;
       Rx       <= '1', '0' after clk_period;
       DataIn   <= RES_DATA; -- Data = Result
       wait for clk_period;
       
     end loop;

    --get all results	
     wait for 10*clk_period;

     report "Test completed";		
     assert false report "NONE. End of simulation." severity failure;

   end process stim_proc;


END;


