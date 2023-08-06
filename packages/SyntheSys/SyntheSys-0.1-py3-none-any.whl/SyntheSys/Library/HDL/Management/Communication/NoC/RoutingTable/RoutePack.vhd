
library IEEE;
use IEEE.std_logic_1164.all;

package RoutePack is

  constant FlitWidth : natural :=16;
  constant NbInputs  : natural :=5;
  constant NbOutputs  : natural :=5;
  type NATURALS is array(natural range <>) of natural range 0 to 7;  -- Table of natural values
  type FLITS is array(natural range <>) of std_logic_vector(FlitWidth-1 downto 0);  -- Table of natural values

end RoutePack;
