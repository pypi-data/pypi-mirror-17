USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
use work.CrossPack.all;


ENTITY CrossBar_tb IS
END CrossBar_tb;

ARCHITECTURE Behavioral OF CrossBar_tb IS 

  constant FlitWidth : natural := 16;
  constant NbInputs  : natural := 5;
  constant NbOutputs : natural := 5;
  -----------------------------------------------------------------------------
  component CrossBar
    generic (
      NbOutputs : natural;
      NbInputs : natural);
    port (
      OutputConnections  : in  NATURALS(NbOutputs-1 downto 0);
      InputConnections   : in  NATURALS(NbInputs-1 downto 0);
      InputFIFO_AckTx  : in  std_logic_vector(NbInputs-1 downto 0);
      OutputFIFO_AckTx : out std_logic_vector(NbOutputs-1 downto 0);
      InputFIFO_Tx     : out std_logic_vector(NbInputs-1 downto 0);
      OutputFIFO_Tx    : in  std_logic_vector(NbOutputs-1 downto 0);
      InputFIFO_DataOut  : in  FLITS(NbInputs-1 downto 0);
      OutputFIFO_DataOut : out FLITS(NbOutputs-1 downto 0));
  end component;
  
  -----------------------------------------------------------------------------
  signal OutputConnections  : NATURALS(NbOutputs-1 downto 0);
  signal InputFIFO_Tx     : std_logic_vector(NbInputs-1 downto 0);
  signal InputFIFO_DataOut  : FLITS(NbInputs-1 downto 0);
  signal OutputFIFO_DataOut : FLITS(NbOutputs-1 downto 0);
  signal DataOut_bits       : std_logic_vector(NbInputs*FlitWidth-1 downto 0);
  signal ConnectionsIN_bits  : std_logic_vector(NbInputs*3-1 downto 0);
  signal ConnectionsOUT_bits : std_logic_vector(NbInputs*3-1 downto 0);
  signal OutputFIFO_AckTx : std_logic_vector(NbOutputs-1 downto 0);
  
  signal InputConnections : NATURALS(NbInputs-1 downto 0);
  
  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := NbOutputs+NbInputs+NbInputs*FlitWidth + NbOutputs*3 + NbInputs*3;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias OutputFIFO_Tx is Stimuli(NbInputs-1 downto 0);
  alias InputFIFO_DataOut_bits is Stimuli(NbInputs*FlitWidth-1+NbInputs downto OutputFIFO_Tx'length);
  alias OutputConnections_bits is Stimuli(NbOutputs*3-1+InputFIFO_DataOut_bits'length + OutputFIFO_Tx'length downto InputFIFO_DataOut_bits'length + OutputFIFO_Tx'length);
  alias InputConnections_bits  is Stimuli(NbInputs*3-1 + InputFIFO_DataOut_bits'length + OutputFIFO_Tx'length + OutputConnections_bits'length downto InputFIFO_DataOut_bits'length + OutputFIFO_Tx'length + OutputConnections_bits'length);
  alias InputFIFO_AckTx is Stimuli(NbOutputs+NbInputs+NbInputs*FlitWidth + NbOutputs*3 + NbInputs*3-1 downto NbInputs+NbInputs*FlitWidth + NbOutputs*3 + NbInputs*3);
  
BEGIN

  DataOut_bits <= InputFIFO_DataOut_bits;
  ConnectionsOUT_bits <= OutputConnections_bits;
  ConnectionsIN_bits <= InputConnections_bits;

  InputIteration: for i in 0 to NbInputs-1 generate
    OutputConnections(i) <= CONV_INTEGER(ConnectionsOUT_bits((i+1)*3-1 downto i*3)); -- 5 bits to encode port number
  end generate InputIteration;
  
  OutputIteration: for j in 0 to NbOutputs-1 generate
    InputConnections(j)  <= CONV_INTEGER(ConnectionsIN_bits((j+1)*3-1 downto j*3)); -- 5 bits to encode port number
    InputFIFO_DataOut(j) <= DataOut_bits((j+1)*FlitWidth-1 downto j*FlitWidth);
  end generate OutputIteration;
  
  
  -----------------------------------------------------------------------------
  CrossBar_1: CrossBar
    generic map (
      NbOutputs => NbOutputs,
      NbInputs  => NbInputs)
    port map (
      OutputConnections  => OutputConnections,
      InputConnections   => InputConnections,
      InputFIFO_AckTx    => InputFIFO_AckTx,
      OutputFIFO_AckTx   => OutputFIFO_AckTx,
      InputFIFO_Tx       => InputFIFO_Tx,
      OutputFIFO_Tx      => OutputFIFO_Tx,
      InputFIFO_DataOut  => InputFIFO_DataOut,
      OutputFIFO_DataOut => OutputFIFO_DataOut);
  
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./CrossBar_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Start CrossBar test ***");
    write(output, "*** Start CrossBar test ***");

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
