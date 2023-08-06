--------------------------------------------------------------------------------
-- Company:
-- Engineer: OF 
--
-- Create Date:    09/16/2031
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_FPCompare.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--
--------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY FPCompare_OL IS
	port (
	a: in std_logic_vector(31 downto 0);
	b: in std_logic_vector(31 downto 0);
	clk: in std_logic;
	ce: in std_logic;
	result: out std_logic);
END FPCompare_OL;

ARCHITECTURE FPCompare_OL OF FPCompare_OL IS

signal EgalEntier     : STD_LOGIC ;
signal EgalMantisse   : STD_LOGIC ;
signal SupBEntierA    : STD_LOGIC ;
signal SupBEntier     : STD_LOGIC ;
signal SupBMantisse   : STD_LOGIC ;
signal SupSigneB      : STD_LOGIC ;
--signal SupSigneA      : STD_LOGIC ;

signal PpEgalEntier   : STD_LOGIC ;
signal PpEgalMantisse : STD_LOGIC ;
signal PpSupBEntier   : STD_LOGIC ;
signal PpSupBMantisse : STD_LOGIC ;
signal PpSupSigneB    : STD_LOGIC ;
--signal PpSupSigneA    : STD_LOGIC ;
signal EgalData       : STD_LOGIC ;
signal resultInt      : STD_LOGIC ;

signal BEstSup        : STD_LOGIC ;

BEGIN

EgalEntier   <= '1' when (a(31 downto 23) = b(31 downto 23)) else '0';
EgalMantisse <= '1' when (a(23 downto  0) = b(23 downto  0)) else '0';
SupBEntier   <= '1' when (a(30 downto 23) < b(30 downto 23)) else '0';
SupBMantisse <= '1' when (a(23 downto  0) < b(23 downto  0)) else '0';

--SupBEntier <= SupBEntierA when (a(30) = '0' and b(30) = '0') else not SupBEntierA ;

SupSigneB  <= a(31) and not b(31); 
--SupSigneA  <= b(31) and not a(31);


BEstSup   <=     PpEgalEntier and PpSupBMantisse and not PpEgalMantisse                 ;
EgalData  <=     PpEgalEntier and PpEgalMantisse                                          ;
resultInt <= not (BEstSup     or  PpSupSigneB    or      PpSupBEntier) and not EgalData ;

AddReg : process (clk)
  begin
        if rising_edge (clk) then
          if(ce='1') then
                  PpEgalEntier   <= EgalEntier   ;
                  PpEgalMantisse <= EgalMantisse ;
                  PpSupBEntier   <= SupBEntier   ;
                  PpSupBMantisse <= SupBMantisse ;
--                  PpSupSigneA    <= SupSigneA    ;
                  PpSupSigneB    <= SupSigneB    ;
                  result         <= resultInt    ;

          end if;
        end if;
end process AddReg;
END FPCompare_OL;

