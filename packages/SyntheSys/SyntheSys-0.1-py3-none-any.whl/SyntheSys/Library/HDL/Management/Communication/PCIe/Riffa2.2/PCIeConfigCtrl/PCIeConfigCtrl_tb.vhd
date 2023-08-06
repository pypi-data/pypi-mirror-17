

USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;

ENTITY RiffaToHS_tb IS
END RiffaToHS_tb;

ARCHITECTURE Behavioral OF RiffaToHS_tb IS 
	
	constant C_PCI_DATA_WIDTH : natural := 64;
	constant FlitWidth : natural := 16;
	
	-----------------------------------------------------------------------------
	component RiffaToHS is
	generic (
		C_PCI_DATA_WIDTH   : integer := 64;
		FlitWidth          : natural := 16);
	port (
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
		
		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0);
		Tx                 : OUT std_logic;
		AckTx              : IN  std_logic;
		
		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0);
		Rx                 : IN  std_logic;
		AckRx              : OUT std_logic);
	end component RiffaToHS;
	
	-----------------
--	signal CLK                : std_logic; -- 0
--	signal RST                : std_logic; -- 1
--	
--	-- RX Interface
--	signal CHNL_RX            : std_logic; -- 2
--	signal CHNL_RX_LAST       : std_logic; -- 3
--	signal CHNL_RX_LEN        : std_logic_vector(31 downto 0); -- 4->35
--	signal CHNL_RX_OFF        : std_logic_vector(30 downto 0); -- 36->67
--	signal CHNL_RX_DATA       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0); -- 68->131
--	signal CHNL_RX_DATA_VALID : std_logic; -- 132
--	
--	-- TX Interface
--	signal CHNL_TX_ACK        : std_logic; -- 133
--	signal CHNL_TX_DATA_REN   : std_logic; -- 134
--	
--	signal AckTx              : std_logic; -- 135
--	
--	signal DataIn             : std_logic_vector(FlitWidth-1 downto 0); -- 136->152
--	signal Rx                 : std_logic; -- 153
		
	-- RX Interface
	signal CHNL_RX_CLK        : std_logic;
	signal CHNL_RX_ACK        : std_logic;
	signal CHNL_RX_DATA_REN   : std_logic;
	
	-- TX Interface
	signal CHNL_TX_CLK        : std_logic;
	signal CHNL_TX            : std_logic;
	signal CHNL_TX_LAST       : std_logic;
	signal CHNL_TX_LEN        : std_logic_vector(31 downto 0);
	signal CHNL_TX_OFF        : std_logic_vector(30 downto 0);
	signal CHNL_TX_DATA       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
	signal CHNL_TX_DATA_VALID : std_logic;
	
	signal DataOut            : std_logic_vector(FlitWidth-1 downto 0);
	signal Tx                 : std_logic;
	
	signal AckRx              : std_logic;

	-----------------------------------------------------------------------------
	-- TESTBENCH TEXTIO Stimuli
	
	constant NbStimuli : natural := 152;
	
	-- RX Interface
	signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
	alias CLK is Stimuli(0);
	alias RST is Stimuli(1);
	alias CHNL_RX is Stimuli(2);
	alias CHNL_RX_LAST is Stimuli(3);
	alias CHNL_RX_LEN is Stimuli(35 downto 4);
	alias CHNL_RX_OFF is Stimuli(66 downto 36);
	alias CHNL_RX_DATA is Stimuli(130 downto 67);
	alias CHNL_RX_DATA_VALID is Stimuli(131);
	
	-- TX Interface
	alias CHNL_TX_ACK is Stimuli(132);
	alias CHNL_TX_DATA_REN is Stimuli(133);
	
	alias AckTx is Stimuli(134);
	
	alias DataIn is Stimuli(150 downto 135);
	alias Rx is Stimuli(151);

BEGIN

	-----------------------------------------------------------------------------
	RiffaToHS_1: RiffaToHS
		generic map(
			C_PCI_DATA_WIDTH    => C_PCI_DATA_WIDTH,
			FlitWidth           => FlitWidth)
		port map(
			CLK                 => CLK,
			RST                 => RST,
	
			-- RX Interface
			CHNL_RX_CLK         => CHNL_RX_CLK,
			CHNL_RX             => CHNL_RX,
			CHNL_RX_ACK         => CHNL_RX_ACK,
			CHNL_RX_LAST        => CHNL_RX_LAST,
			CHNL_RX_LEN         => CHNL_RX_LEN,
			CHNL_RX_OFF         => CHNL_RX_OFF,
			CHNL_RX_DATA        => CHNL_RX_DATA,
			CHNL_RX_DATA_VALID  => CHNL_RX_DATA_VALID,
			CHNL_RX_DATA_REN    => CHNL_RX_DATA_REN,
	
			-- TX Interface
			CHNL_TX_CLK         => CHNL_TX_CLK,
			CHNL_TX             => CHNL_TX,
			CHNL_TX_ACK         => CHNL_TX_ACK,
			CHNL_TX_LAST        => CHNL_TX_LAST,
			CHNL_TX_LEN         => CHNL_TX_LEN,
			CHNL_TX_OFF         => CHNL_TX_OFF,
			CHNL_TX_DATA        => CHNL_TX_DATA,
			CHNL_TX_DATA_VALID  => CHNL_TX_DATA_VALID,
			CHNL_TX_DATA_REN    => CHNL_TX_DATA_REN,
	
			DataOut             => DataOut,
			Tx                  => Tx,
			AckTx               => AckTx,
	
			DataIn              => DataIn,
			Rx                  => Rx,
			AckRx               => AckRx);

  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./RiffaToHS_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** StartRiffaToHS test ***");
    write(output, "*** Start RiffaToHS test ***");

    while not endfile(TestFile) loop
      readline(TestFile, L);
      --write(output, L);
      
      read(L, R, GOOD => good_number);-- read the time from the beginning of the line
      next when not good_number;-- skip the line if it doesn't start with a number
      
      TimeVector := real(R) * 1 ns; -- convert real number to time
      if (now < TimeVector) then -- wait until vector time
        wait for TimeVector - now;
      end if;
      index := 0;
      
      --For each caracter in line:
      for i in L'range loop
        case L(i) is
          when '0' => -- Drive 0
            Stimuli(index) <= '0';
          when '1' => -- Drive 1
            Stimuli(index) <= '1';
          when 'H' => -- Test for 1
            assert Stimuli(index) = '1';
          when 'L' => -- Test for 0
            assert Stimuli(index) = '0';
          when 'X' => -- Don't care
            null;
          when ' '
            | HT => -- Skip white space
            next;
          when others =>
            -- Illegal character
            assert false report "Illegal char in vector file: " & L(i);
            exit;
        end case;
        index := index + 1;
      	if index=NbStimuli then
            exit;
      	end if;
      end loop;                         -- end of line
 
    end loop;                           -- end of file
    
    assert false report "*** Test complete ***";
    wait;
    
  end process TEST;-------------------------
  
  
  END;
