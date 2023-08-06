
library IEEE;
use IEEE.std_logic_1164.all;

use work.RoutePack.all;

-------------------------------------------------------------------------------
-- ENTITY: RoutingTable that 
-------------------------------------------------------------------------------
entity RoutingTable is

	generic (
		NbOutputs : natural := 5;
		NbInputs  : natural := 5); -- North, South, East, West, Local

	port (    
		Clk               : in  std_logic;
		RoutingReady      : in  std_logic;
		Requests          : in  std_logic_vector(NbInputs-1 downto 0);
		Connected         : in  std_logic_vector(NbInputs-1 downto 0);
		OutputPort        : in  natural;
		SelectedInput     : in  natural;
		InputConnections  : out NATURALS(NbInputs-1 downto 0);
		OutputConnections : out NATURALS(NbOutputs-1 downto 0));

end RoutingTable;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of RoutingTable is

	constant AllOnes_In  : natural range 0 to 7 :=2**(NbInputs-2)-1;
	constant AllOnes_Out : natural range 0 to 7 :=2**(NbOutputs-2)-1;

	signal OutputConnections_table  : NATURALS(NbOutputs-1 downto 0) := (others=>AllOnes_Out);
	signal InputConnections_table   : NATURALS(NbOutputs-1 downto 0) := (others=>AllOnes_In);

	signal SelectedIn, SelectedOut : natural := 0;
--	signal FreeInport : std_logic_vector(NbInputs-1 downto 0) := (others=>'0');
--	signal OutConnection        : natural;

begin  -- RTL

	InputConnections  <= InputConnections_table; 
	OutputConnections <= OutputConnections_table;

--	OutConnection <= OutputConnections_table(SelectedOut);

	SelectedIn <= SelectedInput when SelectedInput<NbInputs else AllOnes_In;
	SelectedOut <= OutputPort   when OutputPort<NbOutputs   else AllOnes_Out;

--  -----------------------------------------------------------------------------
--  -- 0:NORTH, 1:SOUTH, 2:EAST, 3:WEST, 4:LOCAL   
--  RoutingTableIn: for i in 0 to NbInputs-1 generate            
--    TableInput(i) <= SelectedOut when SelectedInput=i and RoutingReady='1'and Requests(i)='1' else   
--                     AllOnes_Out;  
--                            
--    InputConnections_table(i) <= TableInput(i) when Connected(i)='0' else 
--                                 InputConnections_table(i);
--                                 
--  
--  end generate RoutingTableIn;
--  
--  -----------------------------------------------------------------------------
--  -- 0:NORTH, 1:SOUTH, 2:EAST, 3:WEST, 4:LOCAL     
--  RoutingTableOut: for j in 0 to NbOutputs-1 generate   
--    TableOutput(j) <= SelectedIn when InputConnections_table(SelectedIn)=j else
--                       AllOnes_In;                         
--                            
--    OutputConnections_table(j) <= TableOutput(j) when RoutingReady='1' and SelectedOut=j and Connected(SelectedIn)='0' else OutputConnections_table(j);
----    OutputConnections_table(j) <= TableOutput(j) when OutputPort=j else 
----                                  OutputConnections_table(j);
--  end generate RoutingTableOut;

  -----------------------------------------------------------------------------
--	SetTable: process (Clk)
--		variable InputTable  : NATURALS(NbInputs-1  downto 0) := (others=>AllOnes_In);
--		variable OutputTable : NATURALS(NbOutputs-1 downto 0) := (others=>AllOnes_Out);
--	begin  -- process SetTable
--		if rising_edge(Clk) then  -- rising clock edge
--			if RoutingReady='1' then
--			
--				for i in 0 to NbInputs-1 loop
--					if Requests(i)='0' and Connected(i)='0' then
--						-- RESET
--						if InputTable(i) /= AllOnes_In then
--							OutputTable(InputTable(i)) := AllOnes_In; 
--							InputTable(i)              := AllOnes_Out; 
--						end if;
--					elsif Requests(i)='1' and Connected(i)='0' and SelectedIn=i  then
--						-- CONNECTION
--						if OutConnection=AllOnes_In then
--							-- RESET FIRST IF NOT
--							if InputTable(i) /= AllOnes_In then
--								OutputTable(InputTable(i)) := AllOnes_In; 
--								InputTable(i)              := AllOnes_Out; 
--							else 
--								InputTable(SelectedIn)   := SelectedOut;
--								OutputTable(SelectedOut) := SelectedIn;   
--							end if;
--						end if;
--					end if; --Output connection test
--				end loop; -- i
--				
--			end if;
--		end if;
--	OutputConnections_table <= OutputTable;
--	InputConnections_table <= InputTable;

--	end process SetTable;



  -----------------------------------------------------------------------------
	InputForLoop : for i in 0 to NbInputs-1 generate
		InputTableAssignment: process(Clk)
	
		begin
			if rising_edge(Clk) then 
				if Requests(i)='1' then 
					if SelectedIn=i then 
						if Connected(i)='0' and OutputConnections_table(SelectedOut)=AllOnes_In then
							if RoutingReady='1' then
								InputConnections_table(i) <= SelectedOut;
							end if;
						end if;
					end if;
				else
					InputConnections_table(i) <= AllOnes_Out;
				end if;
			end if;
		end process InputTableAssignment;
	end generate; -- i

  -----------------------------------------------------------------------------
	OutputForLoop : for i in 0 to NbOutputs-1 generate
		OutputTableAssignment: process(Clk)
	
		begin
			if rising_edge(Clk) then 
				if OutputConnections_table(i)=AllOnes_In then
					if SelectedOut=i then  
						if RoutingReady='1' then
							OutputConnections_table(i) <= SelectedIn;
						end if;
					end if;
				else
					if Requests(OutputConnections_table(i))='0' then
						OutputConnections_table(i) <= AllOnes_Out;
					end if;
				end if;
			end if;
		end process OutputTableAssignment;
	end generate; -- i
	
  -----------------------------------------------------------------------------

end RTL;


