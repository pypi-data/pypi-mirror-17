USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;

use work.RoutePack.all;

ENTITY RoutingControl_tb IS
END RoutingControl_tb;

ARCHITECTURE Behavioral OF RoutingControl_tb IS 

  constant AddrWidth : natural := 8;
  constant NbInputs  : natural := 5;
  constant FlitWidth : natural := 16;
  -----------------------------------------------------------------------------
  component RoutingControl
    generic (
      X_Local : natural;
      Y_Local : natural;
      NbInputs     : natural);
    port (
      FIFO_DataOut_list : in  FLITS(NbInputs-1 downto 0);
      SelectedInput     : in  natural;
      OutputPort        : out  natural);
  end component;
  
  -----------------------------------------------------------------------------
  signal OutputPort  : natural;
  signal FIFO_DataOut_list : FLITS(NbInputs-1 downto 0);
  signal SelectedInput      : natural range 0 to 7 := 0;
  signal FIFO_DataOuts_bits: std_logic_vector(NbInputs*FlitWidth-1 downto 0);
  
  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := NbInputs*FlitWidth+3;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias SelectedInput_bits is Stimuli(3-1 downto 0);
  alias FIFO_DataOuts is Stimuli(NbInputs*FlitWidth-1 + SelectedInput_bits'length downto SelectedInput_bits'length);

  
BEGIN
  
  FIFO_DataOuts_bits <= FIFO_DataOuts;
  SelectedInput <= CONV_INTEGER(SelectedInput_bits);
  -----------------------------------------------------------------------------
  FifoData: for i in 0 to NbInputs-1 generate
  	FIFO_DataOut_list(i) <= FIFO_DataOuts_bits((i+1)*FlitWidth-1 downto i*FlitWidth);
  end generate;
  
  -----------------------------------------------------------------------------
  RoutingControl_1: RoutingControl
    generic map (
      X_Local => 0,
      Y_Local => 0,
      NbInputs     => NbInputs)
    port map (
      FIFO_DataOut_list => FIFO_DataOut_list,
      SelectedInput     => SelectedInput,
      OutputPort        => OutputPort);
  
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./RoutingControl_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Start RoutingControl test ***");
    write(output, "*** Start RoutingControl test ***");

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
  
  
  
