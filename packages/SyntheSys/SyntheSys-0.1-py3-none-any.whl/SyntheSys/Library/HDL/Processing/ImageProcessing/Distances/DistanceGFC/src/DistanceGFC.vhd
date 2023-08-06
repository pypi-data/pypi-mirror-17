
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity DistanceGFC is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		TabEs          : in  std_logic_vector(63 downto 0);
		TabMe          : in  std_logic_vector(63 downto 0);
		--outputs
		dis_gfc        : out std_logic_vector(63 downto 0)
		
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end DistanceGFC;



----------------------------------------------------------------------------
architecture RTL of DistanceGFC is

	signal Accu1   : std_logic_vector(65 downto 0) := (others=>'0');
	signal Accu2   : std_logic_vector(65 downto 0) := (others=>'0');
	signal Accu3   : std_logic_vector(65 downto 0) := (others=>'0');
	signal Cnt_i  : unsigned(15 downto 0) := (others=>'0');
	signal NbElement_i: unsigned(15 downto 0) := (others=>'0');
    signal I11 :std_logic_vector(65 downto 0):= (others=>'0');
    signal I22 :std_logic_vector(65 downto 0):= (others=>'0');
    signal I33 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s11 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s22 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s33 :std_logic_vector(65 downto 0):= (others=>'0');
	signal I3 :unsigned(15 downto 0):= (others=>'0');
    signal I1 :std_logic_vector(65 downto 0):= (others=>'0'); 
    signal SumEM :std_logic_vector(65 downto 0):= (others=>'0');
    signal SumEs :std_logic_vector(65 downto 0):= (others=>'0');
    signal SumMe :std_logic_vector(65 downto 0):= (others=>'0');
    signal ss1 :std_logic_vector(65 downto 0):= (others=>'0');
    signal ss2 :std_logic_vector(65 downto 0):= (others=>'0');
    signal ss3 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s :std_logic_vector(65 downto 0):= (others=>'0');
    signal t1 :std_logic_vector(65 downto 0):= (others=>'0');
    signal t2 :std_logic_vector(65 downto 0):= (others=>'0');
    signal t3 :std_logic_vector(65 downto 0):= (others=>'0');

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

	component FPDiv_11_52_F400 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
	end component;

	component FPSqrt_11_52 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
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
 



 
 
   type FSM_STATE is (INIT, READY, ATTAND,SEND);
	signal CurrentState_i : FSM_STATE := INIT;
begin
	NbElement_i <= x"0009";
	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;
			Accu1       <= (others=>'0');
			Accu2       <= (others=>'0');
			Accu3       <= (others=>'0');
				Cnt_i      <=(others=>'0');
				--Axis <= (others=>'0');
				I3 <= x"0000";
		else
		    if rising_edge(Clk) then  -- rising clock edge
		    case CurrentState_i is 
		      when INIT => 
				if Start = '1' then 
				    I3 <= I3+1;
					CurrentState_i     <= READY;
				end if;
				when READY => 
				    I3 <= I3+1;
				    if I3 > x"0007" then
					Accu1 <= s11;
					Accu2 <= s22;
					Accu3 <= s33;
					I3 <= (others=>'0');
					Cnt_i<=x"0001";
					CurrentState_i     <= ATTAND;
					end if;
				when ATTAND => 
					I3 <= I3+1;
					if I3 > x"000A" then
					Accu1 <= I11;
					Accu2 <= I22;
					Accu3 <= I33;
					I3 <= (others=>'0');
					Cnt_i<=Cnt_i+1;
					--CurrentState_i     <= ATTAND;
					end if;
				--when SEND =>
						--Accu <= I2;
						--Cnt_i<=Cnt_i+1;
					if Cnt_i=(NbElement_i) then
					  SumEs <=I11;
					  SumMe <=I22;
					  SumEM <=std_logic_vector(abs(signed(I33)));
					CurrentState_i     <= SEND;
					end if;
				when SEND =>
					Cnt_i<=Cnt_i+1;
				end case;
			end if;
		end if;
	end process Accumulator;
	
	DataRead <= '1' when Cnt_i<x"005E" else '0';


	Iput1:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => TabEs,
		r => t1);	
	
	Iput2:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => TabMe,
		r => t2);	
		
	Mul1:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t1,
		y => t1,
		r => s11);
		
	Mul2:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t2,
		y => t2,
		r => s22);
		
	Mul3:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t1,
		y => t2,
		r => s33);
	
	Add1:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s11,
		y => Accu1,
		Radd => I11);
		
	Add2:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s22,
		y => Accu2,
		Radd => I22);
		
	Add3:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s33,
		y => Accu3,
		Radd => I33);
	
	sqrt1:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => SumEs,
		r => ss1);
		
	sqrt2:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => SumMe,
		r => ss2);
		
	Mul:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ss1,
		y => ss2,
		r => ss3);
		
	
	Div:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => SumEM,
		y => ss3,
		r => s);
	
	Oput:OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s,
		r => dis_gfc);	

end RTL;


