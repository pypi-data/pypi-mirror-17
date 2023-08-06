library IEEE;
use IEEE.std_logic_1164.all;
--use work.ReqPack.all;

-------------------------------------------------------------------------------
-- ENTITY: Asynchronous request manager for Message routing request
-------------------------------------------------------------------------------
entity RequestManager is
  
  generic (
    NbInputs : natural := 5); -- North, South, East, West, Local

  port (    
    Clk, Rst            : in  std_logic;
    FifosAreEmpty       : in  std_logic_vector(NbInputs-1 downto 0);
    FifosAreEmpty_clean : out std_logic_vector(NbInputs-1 downto 0);
    RequestTable        : out std_logic_vector(NbInputs-1 downto 0);
    FifosRead           : in  std_logic_vector(NbInputs-1 downto 0);
    FifosRead_clean     : out std_logic_vector(NbInputs-1 downto 0)
    );

end RequestManager;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of RequestManager is

  signal ReqTab : std_logic_vector(NbInputs-1 downto 0) := (others=>'0');
  
begin  -- RTL

  -----------------------------------------------------------------------------
  RequestStates: for n in 0 to NbInputs-1 generate
  
    RequestState: process(Clk, Rst)
      variable Header : boolean := True;
    begin
      if rising_edge(Clk) then
        if FifosAreEmpty(n)='0' then
          if Header=True then -- First: read the header
            FifosRead_clean(n) <= '1';
            ReqTab(n)  <= '0';
            Header:=False;
          else
            FifosRead_clean(n) <= FifosRead(n);
            ReqTab(n)  <= '1';
            Header:=False;
          end if;
            
        else                                           -- Then: drive with connected signals
          FifosRead_clean(n) <= FifosRead(n);
          ReqTab(n)  <= '1';
          Header:=False;
        end if;
      end if;
    end process RequestState;
                         
    FifosAreEmpty_clean(n) <= FifosAreEmpty(n) or not (ReqTab(n) or FifosAreEmpty(n));
    
  end generate RequestStates;
  
  -----------------------------------------------------------------------------
  RequestTable <= ReqTab;


end RTL;


