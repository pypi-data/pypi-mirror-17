
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

use work.RoutePack.all;

-------------------------------------------------------------------------------
-- ENTITY: RoutingControl that 
-------------------------------------------------------------------------------
entity RoutingControl is

	generic (
		FlitWidth : natural :=16;
		NbInputs  : natural :=5;
		NbOutputs : natural :=5;
		X_Local   : natural := 0;
		Y_Local   : natural := 0); -- North, South, East, West, Local

	port (    
		FIFO_DataOut_list : in  FLITS(NbInputs-1 downto 0);
		SelectedInput     : in  natural;
		OutputPort        : out natural;
		StartRouting      : in  std_logic_vector(NbInputs-1 downto 0);
		RoutingReady      : out std_logic);

end RoutingControl;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of RoutingControl is

	constant AddrWidth : natural :=FlitWidth/2;
	constant AllOnes_In  : natural range 0 to 7 :=2**(NbInputs-2)-1;
	constant AllOnes_Out : natural range 0 to 7 :=2**(NbOutputs-2)-1;
	signal X_Dest, Y_Dest : std_logic_vector((AddrWidth-1)/2 downto 0) := (others=>'0');
  
begin  -- RTL

	RoutingReady <= '1' when SelectedInput/=AllOnes_In and StartRouting(SelectedInput)='1' else '0'; -- Immediately ready !
	-----------------------------------------------------------------------------
	X_Dest <= FIFO_DataOut_list(SelectedInput)(AddrWidth-1 downto AddrWidth/2) when SelectedInput <= NbInputs-1 else (others=>'0');
	Y_Dest <= FIFO_DataOut_list(SelectedInput)(AddrWidth/2-1 downto 0) when SelectedInput <= NbInputs-1 else (others=>'0');

	-----------------------------------------------------------------------------
	-- 0:NORTH, 1:SOUTH, 2:EAST, 3:WEST 4:LOCAL
	OutputPort  <=  2 when TO_INTEGER(UNSIGNED(X_Dest)) > X_Local and SelectedInput/=AllOnes_In else -- To EAST
	                3 when TO_INTEGER(UNSIGNED(X_Dest)) < X_Local and SelectedInput/=AllOnes_In else -- To WEST
	                0 when TO_INTEGER(UNSIGNED(X_Dest)) = X_Local and TO_INTEGER(UNSIGNED(Y_Dest)) > Y_Local and SelectedInput/=AllOnes_In else -- To NORTH
	                1 when TO_INTEGER(UNSIGNED(X_Dest)) = X_Local and TO_INTEGER(UNSIGNED(Y_Dest)) < Y_Local and SelectedInput/=AllOnes_In else -- To SOUTH
	                4 when TO_INTEGER(UNSIGNED(X_Dest)) = X_Local and TO_INTEGER(UNSIGNED(Y_Dest)) = Y_Local and SelectedInput/=AllOnes_In else -- To LOCAL                                  
	                AllOnes_Out;
--	OutputPort  <=  4;
--	RoutProcess : process(X_Dest, Y_Dest, SelectedInput)
--	begin
--		if TO_INTEGER(UNSIGNED(X_Dest)) > X_Local and SelectedInput/=AllOnes_In then
--		else
--			if TO_INTEGER(UNSIGNED(X_Dest)) > X_Local and SelectedInput/=AllOnes_In then
--	end process;
  
end RTL;


