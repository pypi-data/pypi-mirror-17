
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity DistanceRMS is
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
		dis_rms        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end DistanceRMS;



----------------------------------------------------------------------------
architecture RTL of DistanceRMS is

	signal Accu   : std_logic_vector(65 downto 0) := (others=>'0');
	signal Cnt_i  : unsigned(15 downto 0) := (others=>'0');
	signal NbElement_i: unsigned(15 downto 0) := (others=>'0');
	 signal I3 :unsigned(15 downto 0):= (others=>'0');

   component FPSqrt_11_52 is
		port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
   end component;



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

component FPDiv_11_52_F400 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end component;
 
signal t1 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal t2 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sr :std_logic_vector(65 downto 0):= (others=>'0'); 
signal srr :std_logic_vector(65 downto 0):= (others=>'0'); 

signal I1 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sum :std_logic_vector(65 downto 0):= (others=>'0'); 
signal ss :std_logic_vector(65 downto 0):= (others=>'0'); 
signal s :std_logic_vector(65 downto 0):= (others=>'0'); 


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
				    if I3 > x"0024" then
					Accu <= srr;
					I3 <= (others=>'0');
					Cnt_i<=x"0001";
					CurrentState_i     <= ATTAND;
					end if;
				when ATTAND => 
					I3 <= I3+1;
					if I3 > x"000B" then
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
		Rsub => sr);
		
	Mul:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sr,
		y => sr,
		r => srr);

	Add:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => srr,
		y => Accu,
		Radd => I1);
		
	
	Sqrt:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sum,
		r => ss);
	
	Div:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ss,
		y => "01" & x"4022000000000000",  --9.000
		R => s);
	
	Oput:OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s,
		r => dis_rms);	

end RTL;


