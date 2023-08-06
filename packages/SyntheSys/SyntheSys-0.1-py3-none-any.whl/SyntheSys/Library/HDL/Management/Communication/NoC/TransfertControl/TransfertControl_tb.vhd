USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;

--use work.TransCtrlPack.all;

ENTITY TransfertControl_tb IS
END TransfertControl_tb;

ARCHITECTURE Behavioral OF TransfertControl_tb IS 

  constant AddrWidth : natural := 8;
  constant NbInputs  : natural := 5;
  constant FlitWidth : natural := 16;
  -----------------------------------------------------------------------------
  component TransfertControl
	generic (
		FlitWidth  : natural := 16);
	port (
		Clk, Rst          : in  std_logic;

		FifoIn_IsEmpty    : in  std_logic;
		FifoIn_DataOut    : in  std_logic_vector(FlitWidth-1 downto 0);
		FifoIn_Read       : out std_logic;

		HS_Tx             : out std_logic;
		HS_AckTx          : in  std_logic;
		HS_DataOut        : out std_logic_vector(FlitWidth-1 downto 0);

		InputRequests     : out std_logic;
		InputConnected    : out std_logic
		);
  end component;
  
  -----------------------------------------------------------------------------
  signal FifoIn_Read     : std_logic;
  signal HS_Tx           : std_logic;
  signal HS_DataOut      : std_logic_vector(FlitWidth-1 downto 0);
  signal ConnectionReset : std_logic;
  
  signal InputRequests   : std_logic;
  signal InputConnected  : std_logic;
  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := FlitWidth+4;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias FifoIn_DataOut is Stimuli(FlitWidth-1 downto 0);
  alias HS_AckTx is Stimuli(FifoIn_DataOut'length);
  alias FifoIn_IsEmpty is Stimuli(FifoIn_DataOut'length+1);
  alias Clk is Stimuli(FifoIn_DataOut'length+2);
  alias Rst is Stimuli(FifoIn_DataOut'length+3);
  
BEGIN
    
  -----------------------------------------------------------------------------
  TransfertControl_1: TransfertControl
    port map (
      Clk             => Clk,
      Rst             => Rst,
      FifoIn_IsEmpty  => FifoIn_IsEmpty,
      FifoIn_DataOut  => FifoIn_DataOut,
      FifoIn_Read     => FifoIn_Read,
      
      HS_Tx           => HS_Tx,
      HS_AckTx        => HS_AckTx,
      HS_DataOut      => HS_DataOut,
      InputRequests   => InputRequests,
      InputConnected  => InputConnected);
  
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./TransfertControl_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Start TransfertControl test ***");
    write(output, "*** Start TransfertControl test ***");

    while not endfile(TestFile) loop
      readline(TestFile, L);
      --write(output, L);
      
      read(L, R, GOOD => good_number);-- read the time from the beginning of the line
      next when not good_number;-- skip the line if it doesn't start with a number
      
      TimeVector := real(R) * 1 ns; -- convert real number to time
      if (now < TimeVector) then -- wait until vector time
        wait for TimeVector - now;
      end if;
      index := NbStimuli-1;
      
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
        index := index-1;
      end loop;                         -- end of line
 
    end loop;                           -- end of file
    
    assert false report "*** Test complete ***";
    wait;
    
  end process TEST;-------------------------
  
  
  END;
