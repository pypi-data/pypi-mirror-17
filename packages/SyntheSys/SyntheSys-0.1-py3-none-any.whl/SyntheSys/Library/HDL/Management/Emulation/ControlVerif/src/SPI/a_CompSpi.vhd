--------------------------------------------------------------------------------
-- Company:  ADACSYS
-- Engineer: OF
--
-- Create Date:    08/05/2013
-- Design Name:
-- Module Name:   a_CompSpi.vhd
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity a_CompSpi is
  generic(DataComp : STD_LOGIC_VECTOR(15 downto 0) := X"ffff");
  Port(
      resetn    : in   STD_LOGIC                     ;
      ClkRef    : in   STD_LOGIC                     ;
      ClkEnCom  : in   STD_LOGIC                     ;

      StartComp : in  STD_LOGIC                      ;
      StopComp  : in  STD_LOGIC                      ;
      dataIn    : in  STD_LOGIC_VECTOR (15 downto 0) ;

      DataEgal  : out STD_LOGIC
      );
end a_CompSpi;

architecture behavioral of a_CompSpi is
-- Definition du composant Synchronisation

    signal   CompOutInt     : STD_LOGIC_VECTOR(3 downto 0) ;
    signal   CompOutIntReg  : STD_LOGIC_VECTOR(3 downto 0) ;
    signal   egalOutputInt  : STD_LOGIC_VECTOR(3 downto 0) ;
    signal   egalOutput     : STD_LOGIC                    ;
    signal   DataEgalInt    : STD_LOGIC                    ;

--    constant DataComp : STD_LOGIC_VECTOR(15 downto 0) := X"ffff" ;

-- Definition du composant de Pipe

  component a_reg_memo_param
  generic (
         SIZE_IN: integer := 32);
  port(
       enable      : in  STD_LOGIC                            ;
       dataIn      : in  STD_LOGIC_VECTOR (SIZE_IN-1 downto 0);
       samplingClk : in  STD_LOGIC                            ;
       resetn      : in  STD_LOGIC                            ;
       syncDataOut : out STD_LOGIC_VECTOR (SIZE_IN-1 downto 0)
      );
  end component;


-- Definition du composant Comparateur Parametrable

 component a_comp_param
  generic (
          SIZE_COMP: integer := 4);
  port(
          dataIn_a    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
          dataIn_b    : in  STD_LOGIC_VECTOR (SIZE_COMP-1 downto 0);
          egalOut     : out STD_LOGIC
       );
  end component;

  begin
-- Instantiation du Comparateur de signaux

Ginst_Comp : for i in 0 to 3 generate
   comp : a_comp_param generic map (SIZE_COMP => 4)
                       port map    (
                                   dataIn_a   => DataComp(((i*4)+3) downto i*4),
                                   dataIn_b   => dataIn  (((i*4)+3) downto i*4),
                                   egalOut    => CompOutInt(i)
                                   );
end generate Ginst_Comp;

-- Cellule de Pipe 

   ffSpeed : a_reg_memo_param generic map (SIZE_IN => 4)
                              port map    (
                                          enable       => ClkEnCom      ,
                                          dataIn       => CompOutInt    ,
                                          samplingClk  => ClkRef        ,
                                          resetn       => resetn        ,
                                          syncDataOut  => CompOutIntReg
                                          );

egalOutputInt <= CompOutIntReg;

-- Gestion du AND de tous les Bits du Vecteur egalOutputInt

ProcAnd : process(egalOutputInt)
          variable V : STD_LOGIC;
  begin
           V:= egalOutputInt(0);
    for j in 1 to 3 loop
           V:= V AND egalOutputInt(j);
    end loop;

           egalOutput <= V;
  end process ProcAnd;

-- Gestion de la prise en compte de la data

CtrlComp : process (ClkRef, resetn)
  begin
      if resetn = '0' then
                   DataEgalInt <= '0'        ;

        elsif rising_edge (ClkRef) then
         if(ClkEnCom='1') then
          if(StartComp='1') then
                   DataEgalInt <= egalOutput ;

            elsif(StopComp='1' and DataEgalInt='1') then
                   DataEgalInt <= '0'        ;

          end if;
         end if;
      end if;
end process CtrlComp;

DataEgal <= DataEgalInt;

end behavioral;

