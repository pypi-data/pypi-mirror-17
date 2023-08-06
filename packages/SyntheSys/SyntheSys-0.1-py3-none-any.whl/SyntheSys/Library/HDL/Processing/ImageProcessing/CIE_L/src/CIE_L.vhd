library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library std;
use std.textio.all;
library work;


entity CIE_L is
	port (
		Y                 : in  std_logic_vector(63 downto 0);
		clk, rst          : in std_logic;
		--DataRead          : out std_logic;
		CIE_LValue          	      : out std_logic_vector(63 downto 0));
end CIE_L;



architecture RTL of CIE_L is
   

component FPAddSub_11_52_uid2 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          Radd : out  std_logic_vector(11+52+2 downto 0);
          Rsub : out  std_logic_vector(11+52+2 downto 0)   );
end component;

component FPDiv_11_52_F400 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          Y : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
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

component FPExp_11_52_F400 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end component;

component IterativeLog_11_52_10_400 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end component;

component OutputIEEE_11_52_to_11_52 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(63 downto 0)   );
end component;

signal yf:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal yd:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ys:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal yp:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ym:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ye:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ymm:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ya:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal yad:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal yn:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal va:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ysa:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal ysb:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal val_aa:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal Cnt_i  : unsigned(15 downto 0) := (others=>'0');

type FSM_STATE is (INIT, START,FLOATA, FLOATB);
signal CurrentState_i : FSM_STATE := INIT;
begin

	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;

		else
		    if rising_edge(Clk) then  -- rising clock edge
		    case CurrentState_i is 
		      when INIT => 
		        if  Cnt_i = x"0075" then
		              CurrentState_i <= START;		  
		        end if;
		        Cnt_i <= Cnt_i +1;
		      
			 when START => 
				
					if ys(63) = '1' then

						CurrentState_i     <= FLOATA;
					  
				else
					
				    if ys(63) = '0' then

						CurrentState_i     <= FLOATB;
					   
				    end if;
				end if;
				Cnt_i <= Cnt_i +1;
			when FLOATA => 
			Cnt_i <= Cnt_i +1;
			when FLOATB => 
			Cnt_i <= Cnt_i +1;
			end case;
			end if;
		end if;
	end process Accumulator;

	ysa <= yd when CurrentState_i     = FLOATA  else (others=>'0');
	ysb <= yd when CurrentState_i     = FLOATB  else (others=>'0');
	yn <= yad when CurrentState_i  = FLOATA  else ye;	

	--DataRead <= '1' when Cnt_i<x"00DB" else '0';

		
	Iput2: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => y,
		r => yf);
		

		
	Div21:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => yf,
		y => "01" & x"4059000000000000",   --100.000
		r => yd);
	

	
	Sub21:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => yd,
		y => "01" & x"3F82231832FCAC8E",   --0.008856
		Rsub => ys);
			
	Sub:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => va,
		y => "01" & x"4030000000000000",   --16.000
		Rsub => val_aa);
	
	Mul:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => yn,
		y => "01" & x"405D000000000000",   --116.000
		r => va);
			

    Pow2:IterativeLog_11_52_10_400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ysb,
		r => yp);
		
		
	Mul21:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => yp,
		y => "01" & x"3FD5555555555555",   --0.333333333333333333
		r => ym);

	Exp2:FPExp_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ym,
		r => ye);

	
	Mul22:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ysa,
		y => "01" & x"401F25E353F7CED9",   --7.787
		r => ymm);
		
	Add21:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ymm,
		y => "01" & x"3FC1A7B9170D62BF",   --0.137931   ---->  16/116
		Radd => yad);
	
		
	
	Oput: OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => val_aa,
		r => CIE_LValue);
end RTL;


