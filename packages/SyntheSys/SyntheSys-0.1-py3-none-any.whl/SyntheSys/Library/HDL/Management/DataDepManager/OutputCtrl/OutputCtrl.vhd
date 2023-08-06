
use work.Utilities.ALL;
library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
-- ENTITY: OutputCtrl
-------------------------------------------------------------------------------
entity OutputCtrl is
	generic (
		FlitWidth          : natural := 16;
		NbInputFlit        : natural := 3;
		NbTask             : natural := 32;
		ResultSizes        : NaturalVector;
		ComHeader          : std_logic_vector); -- Number of task an operator can manage
	port (
		Rst, Clk           : IN  std_logic;
		
		HeaderReadMode     : IN  std_logic;
		MultiCastReadMode  : IN  std_logic;
		InputDataValid     : IN  std_logic;
		MemReadAddr        : OUT std_logic_vector(BitWidth(NbTask)-1 downto 0);

		Start              : IN  std_logic;
		SendResult         : IN  std_logic;
		MultiCast          : IN  std_logic_vector(FlitWidth/2-1 downto 0);

		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0);
		DataInRead         : IN  std_logic;
		DataInAddr         : OUT std_logic_vector(BitWidth(Maximum(ResultSizes))-1 downto 0);

		TaskID             : IN  std_logic_vector(BitWidth(NbTask)-1 downto 0);
		HeaderIn           : IN  std_logic_vector(FlitWidth-1 downto 0);
		HeaderAddr         : OUT std_logic_vector(BitWidth(NbTask)-1 downto 0);

		DataAvailable      : OUT std_logic;
		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0);
		HeaderOut          : OUT std_logic_vector(FlitWidth-1 downto 0);
		TerminalBusy       : OUT std_logic);
end OutputCtrl;

-------------------------------------------------------------------------------
-- ARCHITECTURE: RTL, update request table on inputs events
-------------------------------------------------------------------------------
architecture RTL of OutputCtrl is 

	constant MULTICAST_ONE     : unsigned(FlitWidth/2-1 downto 0) :=TO_UNSIGNED(1, FlitWidth/2);
	constant MULTICAST_ZERO    : unsigned(FlitWidth/2-1 downto 0) :=TO_UNSIGNED(0, FlitWidth/2);
	constant ZEROS_HALF_FLIT   : std_logic_vector(FlitWidth/2-1 downto 0) :=(others=>'0');

	signal MultiCastCounter_i  : unsigned(FlitWidth/2-1 downto 0) :=(others=>'0');
	signal OutputFlitCounter_i : unsigned(BitWidth(Maximum(ResultSizes))-1 downto 0) :=(others=>'0');

	signal BaseTaskID_i        : unsigned(BitWidth(NbTask)-1 downto 0) :=(others=>'0');
	signal HeaderOffset_i      : unsigned(BitWidth(NbTask)-1 downto 0) :=(others=>'0');

	signal MemReadCounter_i    : unsigned(BitWidth(NbTask)-1 downto 0);

	-------------------------------------------------------------------------------
	type FSM_STATE is (INIT, READY, SEND);
	signal CurrentState_i : FSM_STATE := INIT;
	
begin  -- RTL

	
	StateMachine : process(Clk, Rst)
	begin
		if (Rst = '1') then
			CurrentState_i <= INIT;
			OutputFlitCounter_i <= (others=>'0');
			MultiCastCounter_i  <= (others=>'0');
			BaseTaskID_i        <= (others=>'0');
			HeaderOffset_i      <= (others=>'0');
		else 
			if rising_edge(Clk) then
				case CurrentState_i is 
					when INIT => 
						OutputFlitCounter_i <= (others=>'0');
						HeaderOffset_i      <= (others=>'0');
						if Start='1' then
							BaseTaskID_i       <= UNSIGNED(TaskID);
							MultiCastCounter_i <= UNSIGNED(MultiCast);
							CurrentState_i     <= READY;
						end if;
					when READY => 
						if SendResult='1' then
							CurrentState_i     <= SEND;
						end if;
					when SEND => 
						if MultiCastCounter_i=MULTICAST_ZERO then
							CurrentState_i <= INIT;
						else
							if DataInRead='1' then
								if OutputFlitCounter_i=(TO_UNSIGNED(Maximum(ResultSizes), OutputFlitCounter_i'length)-1) then
									OutputFlitCounter_i <= (others=>'0');
									HeaderOffset_i     <= HeaderOffset_i+1;
									MultiCastCounter_i <= MultiCastCounter_i-1;
								else
									OutputFlitCounter_i <= OutputFlitCounter_i+1;
								end if;
--							else
--								if MultiCastCounter_i=MULTICAST_ZERO then
--									CurrentState_i <= INIT;
--								end if;
							end if; 
						end if;
				end case;
			end if;
		end if;
	end process StateMachine;
	
	HeaderAddr <= STD_LOGIC_VECTOR(BaseTaskID_i+HeaderOffset_i);
	
	TerminalBusy <= '1' when CurrentState_i/=INIT or Start='1' else '0';
	
	AddressReg : process(Clk)
	begin
		if rising_edge(Clk) then
			DataInAddr <= STD_LOGIC_VECTOR(OutputFlitCounter_i);
		end if;
	end process AddressReg;

	DataAvailable <= '1' when (MultiCastCounter_i/=MULTICAST_ZERO and CurrentState_i=SEND) or SendResult='1' else '0';
	DataOut       <= HeaderIn  when HeaderReadMode='1' else ZEROS_HALF_FLIT & MultiCast when MultiCastReadMode='1' else DataIn;
	HeaderOut     <= ComHeader when HeaderReadMode='1' or MultiCastReadMode='1' else HeaderIn;

	-----------------------------------------------------------------------------
	-- Select which header to read or write in running mode
	MEMORY_READ_COUNTER_PROC: process (Clk, Rst)
	begin 
		if (Rst = '1') then
			MemReadCounter_i <= TO_UNSIGNED(NbTask, MemReadCounter_i'length);
		else 
			if rising_edge(Clk) then 
				if MemReadCounter_i/=TO_UNSIGNED(NbTask, MemReadCounter_i'length) and DataInRead='1' then
					MemReadCounter_i <= MemReadCounter_i+1;
				else
					if InputDataValid='1' and (HeaderReadMode='1' or MultiCastReadMode='1') then
						MemReadCounter_i <= (others=>'0');--TO_UNSIGNED(NbTask, MemReadCounter_i'length);
					end if; 
				end if;
			end if;
		end if;
	end process MEMORY_READ_COUNTER_PROC;
	
	MemReadAddr <= STD_LOGIC_VECTOR(MemReadCounter_i);
	
end RTL;











