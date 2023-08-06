--------------------------------------------------------------------------------
-- Company:      ADACSYS
-- Engineer: 
--
-- Create Date:    06/28/2012
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_sram
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--        SRAM double port Parametrable (Altera)
--
-- Revision 0.01 - File Created
-- Additional Comments:
--
--
--
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity a_sram is
  generic (
          SIZE_ADDR_MEM  : integer := 10 ;
          SIZE_PORT_MEM  : integer := 16 
          );
  Port(data   : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0) ;
       we     : in  STD_LOGIC                                    ;  
       wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
       rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
       wclk   : in  STD_LOGIC                                    ;
       rclk   : in  STD_LOGIC                                    ;
       q      : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0)
  );
end a_sram;

architecture behavioral of a_sram is

-- Definition des signaux internes

    constant profondeur : integer := 2**SIZE_ADDR_MEM ;

type mem is array (0 to profondeur-1) of std_logic_vector (SIZE_PORT_MEM-1 downto 0);
    signal memoire       : mem;

    signal outint        : std_logic_vector(SIZE_PORT_MEM-1 downto 0);
    signal data_read_int : std_logic_vector(SIZE_PORT_MEM-1 downto 0);

  begin

  Ecriture : process (wclk)

  begin
      if rising_edge (wclk) then
        if (we = '1') then
              memoire(conv_integer(wraddr)) <= data;
        end if;
      end if;
  end process Ecriture;

-- Description Re-lecture de la memoire 

              data_read_int <=  memoire(conv_integer(rdaddr));

 reLecture : process (rclk)

  begin
      if rising_edge (rclk) then
              outint <= data_read_int;
      end if;
  end process reLecture;

              q      <= outint;

end behavioral;
        
--------------------------------------------------------------------------------
-- Company:      ADACSYS
-- Engineer: 
--
-- Create Date:    06/28/2012
-- Design Name:
-- Module Name:   /dev/src/HW-common/a_sram_param
-- Project Name:
-- Target Device: None
-- Tool versions:
-- Description:
--        SRAM double port Parametrable .Compatible Xilinx et Altera
--
-- Revision 0.01 - File Created
-- Additional Comments:
--------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.NUMERIC_STD.ALL;

entity a_sram_param is
  generic (
          SIZE_ADDR_MEM  : integer := 15 ;
          SIZE_PORT_MEM  : integer := 16 
          );
  Port(din    : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0) ;
       wen    : in  STD_LOGIC                                    ;  
       wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
       rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
       clk    : in  STD_LOGIC                                    ;
       oclk   : in  STD_LOGIC                                    ;
       dout   : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0)
  );
end a_sram_param;
 -----------------------------------------------------------------------------
architecture behavioral of a_sram_param is

component a_sram 
  generic (
          SIZE_ADDR_MEM  : integer := 15 ;
          SIZE_PORT_MEM  : integer := 16 
          );
  Port(
      data   : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0) ;
      we     : in  STD_LOGIC                                    ;  
      wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
      rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0)  ;
      wclk   : in  STD_LOGIC                                    ;
      rclk   : in  STD_LOGIC                                    ;
      q      : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1  downto 0)
  );
end component;

begin

sram_altera : a_sram generic map (
                                 SIZE_ADDR_MEM => SIZE_ADDR_MEM,
                                 SIZE_PORT_MEM => SIZE_PORT_MEM
                                 )
                     port map(
                             data   => din    ,
                             we     => wen    ,  
                             wraddr => wraddr ,
                             rdaddr => rdaddr ,
                             wclk   => clk    , 
                             rclk   => oclk   ,
                             q      => dout 
                     );

end behavioral;


