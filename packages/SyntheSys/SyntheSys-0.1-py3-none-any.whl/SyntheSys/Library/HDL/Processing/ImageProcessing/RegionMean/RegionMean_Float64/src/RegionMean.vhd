
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity RegionMean is

	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		NbElement         : in  std_logic_vector(63 downto 0);
		DataList          : in  std_logic_vector(63 downto 0);
		--outputs
		RegionMean        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end RegionMean;


----------------------------------------------------------------------------
architecture RTL of RegionMean is

	signal Accu        : std_logic_vector(65 downto 0) := (others=>'0');
	signal NbElement_i : std_logic_vector(63 downto 0) := (others=>'0');
	signal Data        : std_logic_vector(65 downto 0) := (others=>'0');
	signal rm          : std_logic_vector(65 downto 0) := (others=>'0');
	signal I2          : std_logic_vector(65 downto 0) := (others=>'0');
	signal RegionM     : std_logic_vector(65 downto 0) := (others=>'0');
	
	signal DataCnt_i   : natural range 0 to 1024 := 0;
	signal StepCnt_i   : natural range 0 to 23   := 0;
	
	component FPAddSub_11_52_uid2 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          Radd : out  std_logic_vector(11+52+2 downto 0);
          Rsub : out  std_logic_vector(11+52+2 downto 0)   );
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
	
	component FPDiv_11_52_F400 is
		port (clk, rst : in std_logic;
		      X : in  std_logic_vector(11+52+2 downto 0);
		      Y : in  std_logic_vector(11+52+2 downto 0);
		      R : out  std_logic_vector(11+52+2 downto 0));
	end component;
	
	type FSM_STATE is (INIT, ADD, DIVIDE);
	signal CurrentState_i : FSM_STATE := INIT;

begin
	NbElement_i <= NbElement;
	
	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;
			Accu      <= (others=>'0');
			RegionM   <= (others=>'0');
			DataCnt_i <= 0;
			StepCnt_i <= 0;
		else
			if rising_edge(Clk) then  -- rising clock edge
				case CurrentState_i is 
					when INIT => 
						if Start = '1' then 
							--StepCnt_i <= StepCnt_i+1;
							StepCnt_i      <= 0;
							CurrentState_i <= ADD;
							Accu           <= (others=>'0');
							DataCnt_i      <= 1;
						else
							DataCnt_i      <= 0;
						end if;
					when ADD => 
						if StepCnt_i > 14 then
							StepCnt_i <= 0;
							if DataCnt_i = unsigned(NbElement_i) then
								RegionM        <= I2;
								CurrentState_i <= DIVIDE;
							else 
								-- New data
								DataCnt_i <= DataCnt_i+1;
								StepCnt_i <= 0;
							end if;
						else
							StepCnt_i      <= StepCnt_i+1;
						end if;
					when DIVIDE => 
						if StepCnt_i = 23-1 then
							CurrentState_i <= INIT;
						else
							StepCnt_i      <= StepCnt_i+1;
						end if;
					when others => null;
				end case;
			end if;
		end if;
	end process Accumulator;
	
	DataRead <= '1' when (CurrentState_i=INIT and Start = '1') or (CurrentState_i=ADD and StepCnt_i > 14 and DataCnt_i/=unsigned(NbElement_i)) else '0';
	
	Iput1: InputIEEE_11_52_to_11_52 --InputIEEE to FloPoCo conversion
	PORT MAP(
		clk  => clk, 
		rst  => rst,
		x    => DataList,
		r    => Data);

	Adder:FPAddSub_11_52_uid2 -- Latency = 15 cycles
	PORT MAP(
		clk  => clk, 
		rst  => rst,		
		x    => Accu,
		y    => Data,
		Radd => I2);

	Div:FPDiv_11_52_F400 -- Latency = 23 cycles
	PORT MAP(
		clk => clk, 
		rst => rst,		
		x   => RegionM,
		y   => "01" & x"4022000000000000",    --9.000
		r   => rm);

	Oput: OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk => clk, 
		rst => rst,
		x   => rm,
		r   => RegionMean);


end RTL;


