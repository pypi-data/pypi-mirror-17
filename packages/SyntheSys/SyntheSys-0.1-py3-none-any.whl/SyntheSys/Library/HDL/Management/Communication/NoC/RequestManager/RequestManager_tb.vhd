USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;


ENTITY RequestManager_tb IS
END RequestManager_tb;

ARCHITECTURE Behavioral OF RequestManager_tb IS 

  constant FlitWidth : natural := 16;
  constant NbInputs : natural := 5;
  -----------------------------------------------------------------------------
  component RequestManager
    generic (
      NbInputs : natural);
    port (
      FIFO_IsEmpty   : in  std_logic_vector(NbInputs-1 downto 0);
      RequestTable   : out std_logic_vector(NbInputs-1 downto 0);
      TransfertTable : in  std_logic_vector(NbInputs-1 downto 0));
  end component;
  
  -----------------------------------------------------------------------------
  signal RequestTable : std_logic_vector(NbInputs-1 downto 0);

  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := NbInputs+1;
  signal Stimuli : std_logic_vector(2*NbStimuli-1 downto 0) := (others=>'0');
  alias FIFO_IsEmpty is Stimuli(NbInputs-1 downto 0);
  alias TransfertTable is Stimuli(2*NbInputs-1 downto NbInputs);
  
  
  
BEGIN

  
  -----------------------------------------------------------------------------
  RequestManager_1: RequestManager
    generic map (
      NbInputs => NbInputs)
    port map (
      FIFO_IsEmpty   => FIFO_IsEmpty,
      RequestTable   => RequestTable,
      TransfertTable => TransfertTable);
  
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./RequestManager_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Start RequestManager test ***");
    write(output, "*** Start RequestManager test ***");

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
