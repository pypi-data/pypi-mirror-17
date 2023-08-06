library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library std;
use std.textio.all;
library work;


entity CIE_b is
	port (
		
		X                 : in  std_logic_vector(63 downto 0);
		Y                 : in  std_logic_vector(63 downto 0);
		clk, rst          : in std_logic;
		--DataRead          : out std_logic;
		CIE_bValue          	      : out std_logic_vector(63 downto 0));
end CIE_b;



architecture RTL of CIE_b is
   

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

signal xf:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xd:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xs:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xp:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xm:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xe:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xmm:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xa:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xad:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xn:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xsa:std_logic_vector(11+52+2 downto 0):= (others=>'0');
signal xsb:std_logic_vector(11+52+2 downto 0):= (others=>'0');
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

type FSM_STATE is (INIT, START,FLOATA, FLOATB,FLOATC,FLOATD);
signal CurrentState_i : FSM_STATE := INIT;
begin

	Accumulator : process (Clk, Rst)
	begin  -- process Adder
		if (Rst = '1') then
			CurrentState_i <= INIT;
			--xs <= x;
		else
		    if rising_edge(Clk) then  -- rising clock edge
		    case CurrentState_i is 
		      when INIT => 
		        if  Cnt_i = x"0075" then
		              CurrentState_i <= START;		  
		        end if;
		        Cnt_i <= Cnt_i +1;
		      
			 when START => 
				if xs(63) = '1' then 
					if ys(63) = '1' then

						CurrentState_i     <= FLOATA;
					   else 
					     CurrentState_i     <= FLOATC;
					end if;
				else
					if xs(63) = '0' then 
				    if ys(63) = '0' then

						CurrentState_i     <= FLOATB;
					   else 
					     CurrentState_i     <= FLOATD;
					end if;
				    end if;
				end if;
				Cnt_i <= Cnt_i +1;
			when FLOATA => 
			Cnt_i <= Cnt_i +1;
			when FLOATB => 
			Cnt_i <= Cnt_i +1;
			when FLOATC => 
			Cnt_i <= Cnt_i +1;
			when FLOATD => 	
			Cnt_i <= Cnt_i +1;
			end case;
			end if;
		end if;
	end process Accumulator;

	xsa <= xd when CurrentState_i     = FLOATA else xd when CurrentState_i     = FLOATC else (others=>'0');
	xsb <= xd when CurrentState_i     = FLOATB else xd when CurrentState_i     = FLOATD else (others=>'0');
	xn <= xad when CurrentState_i  = FLOATA else xad when CurrentState_i     = FLOATC else xe;	
	ysa <= yd when CurrentState_i     = FLOATA else yd when CurrentState_i     = FLOATC else (others=>'0');
	ysb <= yd when CurrentState_i     = FLOATB else yd when CurrentState_i     = FLOATD else (others=>'0');
	yn <= yad when CurrentState_i  = FLOATA else yad when CurrentState_i     = FLOATC else ye;	

	--DataRead <= '1' when Cnt_i<x"00DB" else '0';
	Iput1: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => x,
		r => xf);
		
	Iput2: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => y,
		r => yf);
		
	Div11:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xf,
		y => "01" & x"4059000000000000",   --100.000
		r => xd);
		
	Div21:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => yf,
		y => "01" & x"405B3883126E978D",   --108.883
		r => yd);
	
	Sub11:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xd,
		y => "01" & x"3F82231832FCAC8E",   --0.008856
		Rsub => xs);
	
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
		x => xn,
		y => yn,
		Rsub => va);
	
	Mul:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => va,
		y => "01" & x"4069000000000000",   --200.000
		r => val_aa);
		
    Pow1:IterativeLog_11_52_10_400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xsb,
		r => xp);
		
		
	Mul11:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xp,
		y => "01" & x"3FD5555555555555",   --0.333333333333333333
		r => xm);

	Exp1:FPExp_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xm,
		r => xe);

	
	Mul12:FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xsa,
		y => "01" & x"408C3A6666666666",   --903.3
		r => xmm);
		
	Add11:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xmm,
		y => "01" & x"4030000000000000",   --16.000
		Radd => xa);
	
		
	Div12:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => xa,
		y => "01" & x"405D000000000000",   --116.000
		r => xad);
		
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
		y => "01" & x"408C3A6666666666",   --903.3
		r => ymm);
		
	Add21:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ymm,
		y => "01" & x"4030000000000000",   --16.000
		Radd => ya);
	
		
	Div22:FPDiv_11_52_F400
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ya,
		y => "01" & x"405D000000000000",   --116.000
		r => yad);
	
	Oput: OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => val_aa,
		r => CIE_bValue);
end RTL;


