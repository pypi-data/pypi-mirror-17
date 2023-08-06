library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a_compteur_param is
  generic (
         SIZE_CPT: integer := 4);
  Port (
        Clk       : in   STD_LOGIC                               ;
        ClkEn     : in   STD_LOGIC                               ;
        resetn    : in   STD_LOGIC                               ;
        Enable    : in   STD_LOGIC                               ;
        MiseZero  : in   STD_LOGIC                               ;
        DataOut   : out  STD_LOGIC_VECTOR (SIZE_CPT-1  downto 0)
  );
end a_compteur_param;

architecture behavioral of a_compteur_param is

   signal dataInt : STD_LOGIC_VECTOR (SIZE_CPT-1  downto 0);

  begin

-- synchronize inputs on fast sampling clk

  compteur : process (Clk, resetn)
    
  begin
      if resetn = '0' then
                dataInt <= (others => '0');
        elsif rising_edge (Clk) then
          if MiseZero = '0' then
                dataInt <= (others => '0');
            elsif Enable = '0' then
                dataInt <= dataInt;
              else
                dataInt <= dataInt + 1;
          end if;
      end if;
  end process compteur;

          DataOut <= dataInt;

end behavioral;
        

