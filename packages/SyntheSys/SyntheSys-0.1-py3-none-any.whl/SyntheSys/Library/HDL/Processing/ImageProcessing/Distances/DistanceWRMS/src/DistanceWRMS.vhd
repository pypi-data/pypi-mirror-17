
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity DistanceWRMS is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		Start             : in  std_logic;
		DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		Tab1          : in  std_logic_vector(63 downto 0);
		Tab2          : in  std_logic_vector(63 downto 0);
		--outputs
		dis_wrms        : out std_logic_vector(63 downto 0)
		
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end DistanceWRMS;



----------------------------------------------------------------------------
architecture RTL of DistanceWRMS is

	signal Accu  : std_logic_vector(65 downto 0) := (others=>'0');
	
	signal Cnt_i  : unsigned(15 downto 0) := (others=>'0');
	signal NbElement_i: unsigned(15 downto 0) := (others=>'0');
   signal I1 :std_logic_vector(65 downto 0):= (others=>'0');
   signal t1 :std_logic_vector(65 downto 0):= (others=>'0');
    signal t2 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s1 :std_logic_vector(65 downto 0):= (others=>'0');
    signal s2 :std_logic_vector(65 downto 0):= (others=>'0');
    signal st :std_logic_vector(65 downto 0):= (others=>'0');
    signal ss :std_logic_vector(65 downto 0):= (others=>'0');
    signal g :std_logic_vector(65 downto 0):= (others=>'0');
    signal tt :std_logic_vector(65 downto 0):= (others=>'0');
    signal sum :std_logic_vector(65 downto 0):= (others=>'0');
    signal ls :std_logic_vector(65 downto 0):= (others=>'0');
    signal dis :std_logic_vector(65 downto 0):= (others=>'0');
	 signal I3 :unsigned(15 downto 0):= (others=>'0');



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

component FPAddSub_11_52_uid2 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          Radd : out  std_logic_vector(11+52+2 downto 0);
          Rsub : out  std_logic_vector(11+52+2 downto 0)   );
end component; 



 
 


   type FSM_STATE is (INIT, READY, ATTAND,SEND);
	signal CurrentState_i : FSM_STATE := INIT;
begin
	NbElement_i <= x"0009";
	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;
			Accu       <= (others=>'0');
			
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
				    if I3 > x"0055" then
					Accu <= g;
					I3 <= (others=>'0');
					Cnt_i<=x"0001";
					CurrentState_i     <= ATTAND;
					end if;
				when ATTAND => 
					I3 <= I3+1;
					if I3 > x"0055" then
					Accu <= I1;
					I3 <= (others=>'0');
					Cnt_i<=Cnt_i+1;
					--CurrentState_i     <= ATTAND;
					end if;
				--when SEND =>
						--Accu <= I2;
						--Cnt_i<=Cnt_i+1;
					if Cnt_i=(NbElement_i) then
					  sum <=I1;
					CurrentState_i     <= SEND;
					end if;
				when SEND =>
					Cnt_i<=Cnt_i+1;
				end case;
			end if;
		end if;
	end process Accumulator;
	
	DataRead <= '1' when Cnt_i<x"0057" else '0';


	Iput1:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => Tab1,
		r => t1);	
	
	Iput2:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => Tab2,
		r => t2);
		
	Sub:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t1,
		y => t2,
		Rsub => st);	
		
	Mul1:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => st,
		y => st,
		r => ss);
		
	sqrt1:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t1,
		r => s1);
		
	sqrt2:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => t2,
		r => s2);
		
	Mul2:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s1,
		y => s2,
		r => tt);
		
	Div1:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ss,
		y => tt,
		r => g);
	
	Add:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => g,
		y => Accu,
		Radd => I1);
		
	Div2:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sum,
		y => "01" & x"4022000000000000",  --9.000
		r => ls);
		
	sqrt3:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ls,
		r => dis);
	
	Oput:OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => dis,
		r => dis_wrms);

end RTL;


