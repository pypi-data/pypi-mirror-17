
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;

use work.CrossPack.all;

-------------------------------------------------------------------------------
-- ENTITY: Asynchronous request manager for Message routing request
-------------------------------------------------------------------------------
entity CrossBar is
  
  generic (
    FlitWidth : natural := 64;
    NbOutputs : natural := 5;
    NbInputs  : natural := 5); -- North, South, East, West, Local

  port (    
    OutputConnections : in  NATURALS(NbOutputs-1 downto 0);
    InputConnections  : in  NATURALS(NbInputs-1 downto 0);
    Input_AckTx       : out std_logic_vector(NbInputs-1 downto 0);
    Output_AckTx      : in  std_logic_vector(NbOutputs-1 downto 0);
    Input_Tx          : in  std_logic_vector(NbInputs-1 downto 0);
    Output_Tx         : out std_logic_vector(NbOutputs-1 downto 0);
    Input_DataOut     : in  FLITS(NbInputs-1 downto 0);
    Output_DataOut    : out FLITS(NbOutputs-1 downto 0)
    );

end CrossBar;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of CrossBar is
  
begin  -- RTL

	-----------------------------------------------------------------------------
	OutputIteration: for N in 0 to NbOutputs-1 generate

		Output_DataOut(N) <= Input_DataOut(OutputConnections(N)) when OutputConnections(N)<NbInputs else (others=>'0'); 
		Output_Tx(N) <= Input_Tx(OutputConnections(N)) when OutputConnections(N)<NbInputs else '0';

	end generate OutputIteration;

	-----------------------------------------------------------------------------
	InputIteration: for M in 0 to NbOutputs-1 generate

		Input_AckTx(M) <= Output_AckTx(InputConnections(M)) when InputConnections(M)<NbOutputs else '0';

	end generate InputIteration;

end RTL;


