library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package constant_definition is
--GLOBAL
  constant PIPELINE_LENGTH : integer := 14+5+2;  -- pipeline length of a
                                             -- computation unit
  constant STD_PIPELINE_LENGTH : std_logic_vector(4 downto 0) := "10101";

--LOCAL
  constant DELAY_S_K : integer := 8+2+2;  -- constant used for delaying S_k_trace in a computation unit
  --SYNTHESIS ONLY:
  --constant DELAY_K   : integer := 3+1;  -- constant used for delaying K_stim by the multiplier stage pipeline.
	--Behavioral only:
	constant DELAY_K   : integer := 3+5;

  type array_S_k is array (0 to DELAY_S_K -1) of std_logic_vector(55 downto 0);
  type array_K is array (0 to DELAY_K -1) of std_logic_vector(55 downto 0);
end constant_definition;


package body constant_definition is

end package body constant_definition;
