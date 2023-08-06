
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity AxisXYZ is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		TabSp          : in  std_logic_vector(63 downto 0);
		TabRef          : in  std_logic_vector(63 downto 0);
		--outputs
		AxisXYZ        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end AxisXYZ;


----------------------------------------------------------------------------
architecture RTL of AxisXYZ is

	signal Accu   : std_logic_vector(65 downto 0) := (others=>'0');
	signal NbElement_i: unsigned(15 downto 0) := (others=>'0');
	signal I1 :std_logic_vector(65 downto 0);
	signal I2 :std_logic_vector(65 downto 0):= (others=>'0');
	signal tsp :std_logic_vector(65 downto 0):= (others=>'0');
	signal tref :std_logic_vector(65 downto 0):= (others=>'0');
	signal Axis :std_logic_vector(65 downto 0):= (others=>'0');
	
	signal DataCnt_i   : natural range 0 to 1024 := 0;
	signal StepCnt_i   : natural range 0 to 23   := 0;	
	
	component FPAddSub_11_52_uid2 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          Radd : out  std_logic_vector(11+52+2 downto 0);
          Rsub : out  std_logic_vector(11+52+2 downto 0)   );
	end component;


	component FPMult_11_52_11_52_11_52_uid2 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
	end component;
	
	component InputIEEE_11_52_to_11_52 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(63 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
	end component;

	component OutputIEEE_11_52_to_11_52 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(63 downto 0)   );
	end component;

    type FSM_STATE is (INIT, CALCUL,SEND);
	signal CurrentState_i : FSM_STATE := INIT;
begin
	NbElement_i <= x"0005";
	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;
			Accu       <= (others=>'0');
			Axis       <= (others=>'0');
			DataCnt_i <= 0;
			StepCnt_i <= 0;
		else
		    if rising_edge(Clk) then  -- rising clock edge
		    case CurrentState_i is 
		      when INIT => 
					if Start = '1' then 
						StepCnt_i      <= 0;
						CurrentState_i <= CALCUL;
						Accu           <= (others=>'0');
						DataCnt_i      <= 1;
				    else
						DataCnt_i      <= 0;
					end if;				    
			  when CALCUL => 
					if StepCnt_i > 14 then 
						StepCnt_i <=0;
						if DataCnt_i = 1 then
							Accu <= I1;
							DataCnt_i <= DataCnt_i+1;
						elsif DataCnt_i = unsigned(NbElement_i) then
							CurrentState_i     <= SEND;
							else
								--New data
								Accu <= I2;
								DataCnt_i <= DataCnt_i+1;
						end if;
					else 
						StepCnt_i      <= StepCnt_i+1;
					end if;
			  when SEND =>
					if StepCnt_i = 15-1 then
						Axis <= I2;
						CurrentState_i <= INIT;
					else
						StepCnt_i      <= StepCnt_i+1;
					end if;
			  when others => null;
			end case;
			end if;
		end if;
	end process Accumulator;
	
	--DataRead <= '1' when Cnt_i<x"000A" else '0';
	DataRead <= '1' when (CurrentState_i=INIT and Start = '1') or (CurrentState_i=CALCUL and StepCnt_i > 14 and DataCnt_i/=unsigned(NbElement_i)) else '0';
	
	Iput1: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => TabSp,
		r => tsp);
		
	Iput2: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => TabRef,
		r => tref);
	
	Mul: FPMult_11_52_11_52_11_52_uid2   -- Latency = 7 cycles
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => tsp,
		y => tref,
		r => I1);
		
	Add:FPAddSub_11_52_uid2          -- Latency = 15 cycles
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => Accu,
		y => I1,
		Radd => I2);

	Oput: OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => Axis,
		r => AxisXYZ);	

end RTL;


