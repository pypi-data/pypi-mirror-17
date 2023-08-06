library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library std;
use std.textio.all;
library work;


entity Blue is

	port (
		
		X                 : in  std_logic_vector(63 downto 0);
		Y                 : in  std_logic_vector(63 downto 0);
		Z                 : in  std_logic_vector(63 downto 0);
		clk, rst          : in std_logic;
		BlueValue          	      : out std_logic_vector(63 downto 0));

end Blue;



architecture RTL of Blue is
	signal I1:std_logic_vector(65 downto 0);
	signal I2:std_logic_vector(65 downto 0);
	signal I3:std_logic_vector(65 downto 0);
	signal I4:std_logic_vector(65 downto 0);
	signal xf:std_logic_vector(65 downto 0);	
	signal yf:std_logic_vector(65 downto 0);
	signal zf:std_logic_vector(65 downto 0);
	signal b:std_logic_vector(65 downto 0);
   
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

begin
	-- b=0.088581*Y-0.470634*X+1.00940*Z

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
		
	Iput3: InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => z,
		r => zf);
	
	Mul1: FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => yf,
		y =>"01" & x"3FB6AD3E920C069E",   --0.088581
		r => I1);
	
	Mul2: FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => xf,
		y =>"01" & x"3FDE1EDE1198AEB8",   --0.470634
		r => I2);
	
	Mul3: FPMult_11_52_11_52_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => zf,
		y =>"01" & x"3FF026809D495183",   --1.00940
		r => I3);
		
		
    Sub: FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => I1,
		y => I2,		
		Rsub => I4);
		
				
	Add:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => I3,
		y => I4,
		Radd => b);
		
	Oput: OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,
		x => b,
		r => BlueValue);




end RTL;

