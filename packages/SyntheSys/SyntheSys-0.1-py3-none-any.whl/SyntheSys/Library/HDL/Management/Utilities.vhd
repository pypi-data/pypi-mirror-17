
library IEEE;
use IEEE.std_logic_1164.all;
--use ieee.math_real.all;
USE ieee.numeric_std.ALL;
use IEEE.MATH_REAL.ALL;

-------------------------------------------------------------------------------
package Utilities is
	type NaturalVector is array(natural range <>) of natural;
	
	function BitWidth(N: natural) return natural;
	function Minimum(A, B : natural)  return natural;
	function Maximum(A, B : natural)  return natural;
	function Maximum(Vect : NaturalVector) return natural;
end package;

----------------
package body Utilities is

-------------
	function Maximum(Vect : NaturalVector) return natural is
		variable MaxValue : natural;
	begin
		MaxValue:=Vect(0);
		for i in 1 to Vect'length-1 loop
			if (Vect(i)>MaxValue) then
				MaxValue:=Vect(i);
			end if;
		end loop;
		return MaxValue;
	end function Maximum;
	
-------------
	function Minimum(A, B : natural) return natural is
	begin
		if (A<=B) then
			return(A);
		else
			return(B);
		end if;
	end function Minimum;

-------------
	function Maximum(A, B : natural) return natural is
	begin
		if (A>=B) then
			return(A);
		else
			return(B);
		end if;
	end function Maximum;
	
-------------
	function BitWidth(N: natural) return natural is
		variable BW : natural;
	begin
		BW:=natural(ceil(log2(real(N))));
		if BW<=1 then
			return 1;
		else
			return BW;
		end if;
	end function BitWidth; 

end package body;

