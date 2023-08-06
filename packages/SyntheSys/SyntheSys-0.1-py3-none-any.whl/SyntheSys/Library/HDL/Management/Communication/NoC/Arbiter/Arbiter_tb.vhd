

USE std.textio.all;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
--USE ieee.numeric_std.ALL;
USE ieee.std_logic_unsigned.ALL;

ENTITY Arbiter_tb IS
END Arbiter_tb;

ARCHITECTURE RTL OF Arbiter_tb IS 

  constant NbInputs : natural := 5;
  -----------------------------------------------------------------------------
  component Arbiter
    generic (
      NbInputs : natural);
    port (
      Clk          : in  std_logic;
      Rst          : in  std_logic;
      RequestTable : in  std_logic_vector(NbInputs-1 downto 0);
      SelectedPort : out natural);
  end component;

  -----------------------------------------------------------------------------
  signal SelectedPort : natural;

  -----------------------------------------------------------------------------
  -- TESTBENCH TEXTIO Stimuli
  constant NbStimuli : natural := NbInputs+2;
  signal Stimuli : std_logic_vector(NbStimuli-1 downto 0) := (others=>'0');
  alias RequestTable is Stimuli(NbInputs-1 downto 0);
  alias Rst is Stimuli(NbInputs+1);
  alias Clk is Stimuli(NbInputs+0);

  
BEGIN

  -----------------------------------------------------------------------------
  Arbiter_1: Arbiter
    generic map (
      NbInputs => NbInputs)
    port map (
      Clk          => Clk,
      Rst          => Rst,
      RequestTable => RequestTable,
      SelectedPort => SelectedPort);

  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  TEST: process
    file TestFile : text is in "./Arbiter_tb_io.txt";
    variable L           : line;
    variable TimeVector  : time;
    variable R           : real;
    variable good_number : boolean;
    variable index       : integer;

  begin  -- process Test
    
    --WRITE_STRING (OUTPUT, "*** Arbiter test ***");
    write(output, "*** Start Arbiter test ***");

    while not endfile(TestFile) loop
      readline(TestFile, L);
      --write(output, L);
      
      read(L, R, GOOD => good_number);-- read the time from the beginning of the line
      next when not good_number;-- skip the line if it doesn't start with a number
      
      TimeVector := natural(R) * 1 ns; -- convert real number to time
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
  
  
  
  
