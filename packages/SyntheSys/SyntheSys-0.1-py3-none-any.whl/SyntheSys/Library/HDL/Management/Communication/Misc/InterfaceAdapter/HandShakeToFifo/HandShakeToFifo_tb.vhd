

USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--USE ieee.numeric_std.ALL;

ENTITY HandShakeToFifo_tb IS
END HandShakeToFifo_tb;

ARCHITECTURE Behavioral OF HandShakeToFifo_tb IS 

  constant FlitWidth : natural := 16;
  -----------------------------------------------------------------------------
  component HandShakeToFifo
    generic (
      FlitWidth : natural);
    port (
      Clk         : in  std_logic;
      Rst         : in std_logic;
      HS_Rx       : in  std_logic;
      HS_AckRx    : out std_logic;
      HS_DataIn   : in  std_logic_vector(FlitWidth-1 downto 0);
      FIFO_DataIn : out std_logic_vector(FlitWidth-1 downto 0);
      FIFO_Write  : out std_logic;
      FIFO_IsFull : in  std_logic);
  end component;

  -----------------------------------------------------------------------------
  signal HS_AckRx    : std_logic;
  signal FIFO_DataIn : std_logic_vector(FlitWidth-1 downto 0);
  signal FIFO_Write  : std_logic;

  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := FlitWidth+4;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias Rst is Stimuli(0);
  alias Clk is Stimuli(1);
  alias HS_Rx is Stimuli(2);
  alias HS_DataIn is Stimuli(FlitWidth-1+3 downto 3);
  alias FIFO_IsFull is Stimuli(FlitWidth-1+4);
  
  
BEGIN

  -----------------------------------------------------------------------------
  HandShakeToFifo_1: HandShakeToFifo
    generic map (
      FlitWidth => FlitWidth)
    port map (
      Clk         => Clk,
      Rst         => Rst,
      HS_Rx       => HS_Rx,
      HS_AckRx    => HS_AckRx,
      HS_DataIn   => HS_DataIn,
      FIFO_DataIn => FIFO_DataIn,
      FIFO_Write  => FIFO_Write,
      FIFO_IsFull => FIFO_IsFull);

  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./HandShakeToFifo_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** StartHandshakeToFifo test ***");
    write(output, "*** Start StartHandshakeToFifo test ***");

    while not endfile(TestFile) loop
      readline(TestFile, L);
      --write(output, L);
      
      read(L, R, GOOD => good_number);-- read the time from the beginning of the line
      next when not good_number;-- skip the line if it doesn't start with a number
      
      TimeVector := real(R) * 1 ns; -- convert real number to time
      if (now < TimeVector) then -- wait until vector time
        wait for TimeVector - now;
      end if;
      index := 0;--NbStimuli-1;
      
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
        index := index +1;-- - 1;
      end loop;                         -- end of line
 
    end loop;                           -- end of file
    
    assert false report "*** Test complete ***";
    wait;
    
  end process TEST;-------------------------
  
  
  END;
