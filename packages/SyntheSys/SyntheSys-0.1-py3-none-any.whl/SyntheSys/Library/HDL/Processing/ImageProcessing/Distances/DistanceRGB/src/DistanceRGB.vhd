
library IEEE;
use IEEE.std_logic_1164.all;
USE ieee.numeric_std.ALL;


----------------------------------------------------------------------------
entity DistanceRGB is
	port (
		--control signals    
		Clk               : in  std_logic;
		Rst               : in  std_logic;
		
		--Start             : in  std_logic;
		--DataRead          : out std_logic;
		--tree values (k and k-1 values from t+1)
		
		R1          : in  std_logic_vector(63 downto 0);
		G1          : in  std_logic_vector(63 downto 0);
		B1          : in  std_logic_vector(63 downto 0);
		R2          : in  std_logic_vector(63 downto 0);
		G2          : in  std_logic_vector(63 downto 0);
		B2          : in  std_logic_vector(63 downto 0);
		--outputs
		deta_E        : out std_logic_vector(63 downto 0)
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)
		);
		
end DistanceRGB;


----------------------------------------------------------------------------
architecture RTL of DistanceRGB is

	--signal Accu   : std_logic_vector(15 downto 0) := (others=>'0');
	--signal Cnt_i  : unsigned(15 downto 0) := (others=>'0');
	--signal NbElement_i: unsigned(15 downto 0) := (others=>'0');
	 --signal I1 :std_logic_vector(15 downto 0);
	 --signal I2 :std_logic_vector(15 downto 0):= (others=>'0');
	-- signal I3 :std_logic_vector(15 downto 0):= (others=>'0');

component FPSqrt_11_52 is
   port ( clk, rst : in std_logic;
          X : in  std_logic_vector(11+52+2 downto 0);
          R : out  std_logic_vector(11+52+2 downto 0)   );
end component;

component FPSquare_11_52_52_uid2 is
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
 
signal sr1 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sg1 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sb1 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sr2 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sg2 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sb2 :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sr :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sg :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sb :std_logic_vector(65 downto 0):= (others=>'0'); 
signal srr :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sgg :std_logic_vector(65 downto 0):= (others=>'0'); 
signal sbb :std_logic_vector(65 downto 0):= (others=>'0'); 
signal srg :std_logic_vector(65 downto 0):= (others=>'0'); 
signal s :std_logic_vector(65 downto 0):= (others=>'0'); 
signal ss :std_logic_vector(65 downto 0):= (others=>'0'); 

begin
			
	Iput1:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => R1,
		r => sr1);
		
	Iput2:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => G1,
		r => sg1);
		
	Iput3:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => B1,
		r => sb1);
		
	Iput4:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => R2,
		r => sr2);
		
	Iput5:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => G2,
		r => sg2);
		
	Iput6:InputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => B2,
		r => sb2);
		
	Sub1:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sr1,
		y => sr2,
		Rsub => sr);

	Sub2:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sg1,
		y => sg2,
		Rsub => sg);
		
	Sub3:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sb1,
		y => sb2,
		Rsub => sb);
	
	Square1:FPSquare_11_52_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sr,
		r => srr);

	Square2:FPSquare_11_52_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sg,
		r => sgg);
		
	Square3:FPSquare_11_52_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => sb,
		r => sbb);	
	
	Add1:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => srr,
		y => sgg,
		Radd => srg);
	
	Add2:FPAddSub_11_52_uid2
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => srg,
		y => sbb,
		Radd => s);
	
	Sqrt:FPSqrt_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => s,
		r => ss);
	
	Oput:OutputIEEE_11_52_to_11_52
	PORT MAP(
		clk=> clk, 
		rst=> rst,		
		x => ss,
		r => deta_E);	

end RTL;


