USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

use work.RoutePack.all;

ENTITY RoutingTable_tb IS
END RoutingTable_tb;

ARCHITECTURE Behavioral OF RoutingTable_tb IS 

  constant AddrWidth : natural := 8;
  constant NbInputs  : natural := 5;
  constant FlitWidth : natural := 16;
  -----------------------------------------------------------------------------
  component RoutingTable
    generic (
      NbOutputs    : natural;
      NbInputs     : natural);
    port (
      OutputPort        : in  natural;
      SelectedInput     : in  natural;
      InputConnections  : out NATURALS(NbInputs-1 downto 0);
      OutputConnections : out NATURALS(NbOutputs-1 downto 0);
      ConnectionsResets : in  std_logic_vector(NbOutputs-1 downto 0));  -- end of connections resets
  end component;
  
  -----------------------------------------------------------------------------
  signal InputConnections  : NATURALS(NbInputs-1 downto 0); 
  signal OutputConnections : NATURALS(NbOutputs-1 downto 0);
  signal SelectedInput     : natural range 0 to 7 := 0;
  signal OutputPort        : natural;
  --signal ConnectionsResets : std_logic_vector(NbOutputs-1 downto 0);
  
  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := NbOutputs+3+3;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias ConnectionsResets is Stimuli(NbInputs-1 downto 0);
  alias SelectedInput_bits is Stimuli(3-1+ConnectionsResets'length downto ConnectionsResets'length);
  alias OutputPort_bits is Stimuli(3-1 + ConnectionsResets'length + SelectedInput_bits'length downto ConnectionsResets'length + SelectedInput_bits'length);

  
BEGIN
  
  SelectedInput <= CONV_INTEGER(SelectedInput_bits);
  OutputPort <= CONV_INTEGER(OutputPort_bits);
  
  -----------------------------------------------------------------------------
  RoutingTable_1: RoutingTable
    generic map (
      NbOutputs    => NbOutputs,
      NbInputs     => NbInputs)
    port map (
      OutputPort        => OutputPort,
      SelectedInput     => SelectedInput,
      InputConnections  => InputConnections,
      OutputConnections => OutputConnections,
      ConnectionsResets => ConnectionsResets);
  
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./RoutingTable_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Start RoutingTable test ***");
    write(output, "*** Start RoutingTable test ***");

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
