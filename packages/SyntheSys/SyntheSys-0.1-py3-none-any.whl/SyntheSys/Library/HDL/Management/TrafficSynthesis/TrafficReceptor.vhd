----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    17:46:57 15/06/2011 
-- Design Name:  TAN Junyan, FRESSE Virginie, ROUSSEAU Frédéric.
-- Module Name:    TrafficReceptor- Behavioral 
-- Project Name:   HERMES NoC emulation Platform
-- Target Devices: Xilinx V5 ML506
-- Tool versions: Xilinx 10.1
-- Description:  This version provides the HERMES NoC emulation in the scenario of multi initiators to multi destinations-
-- Dependencies: 
--
-- Revision: Multi-sources,multi-destination  Version 1
-- Revision 0.01 - File Created
-- Additional Comments:
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
USE IEEE.std_logic_textio.all;
USE STD.TEXTIO.all;

-------------------------------------------------------------------------------
-- ENTITY: 
-------------------------------------------------------------------------------
Entity TrafficReceptor is
  generic ( 
    FlitWidth        : natural :=16
    );
  
  port (
    Clk  	  : IN  std_logic;
    Rst	          : IN  std_logic;
    
    DataIn        : IN  std_logic_vector(FlitWidth-1 downto 0);
    AckRx         : OUT std_logic;
    Rx            : IN  std_logic;
    
    ReceivedPackNB : in integer;
    TotalLatency  : out integer;
    EndCnt        : out integer
    );
END TrafficReceptor;

-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
Architecture RTL OF TrafficReceptor IS

  signal LastLatency : natural := 0;

BEGIN
  -----------------------------------------------------------------------------
  p1:process(Clk, Rst)
    variable mesure_EndCnt: integer:=0;
    variable latence_int: integer:=0;
    variable mesure_EndCnt_logic : std_logic_vector(FlitWidth*2-1  downto 0);
    variable count_flit : integer:=0;
    variable  nbre_flit : integer:=0;
    variable nbre_paquet : integer:=0;
    variable compteur: integer;

  begin 

    if Rst='1' then
      mesure_EndCnt := 0;
      latence_int :=0;
      compteur:=0; 
      TotalLatency<= 0;
      count_flit := 0;
      nbre_flit := 0;
      nbre_paquet := 0;
      mesure_EndCnt_logic := (OTHERS => '0');
      EndCnt<= 0 ; 
    else
      if Clk='1' and Clk'event  then 
        compteur:= compteur + 1;
        
        
        if rx ='1' then 
          
          if count_flit=1 then
            nbre_flit:= conv_integer(DataIn);
          end if;
          
          if count_flit=3 then
            mesure_EndCnt_logic(FlitWidth-1 downto 0) := DataIn;
          elsif count_flit=4 then
            mesure_EndCnt_logic(FlitWidth*2-1 downto FlitWidth) := DataIn;	
          end if;
          
          count_flit:= count_flit +1;
          
          if count_flit= nbre_flit+2 then
            mesure_EndCnt := conv_integer(mesure_EndCnt_logic);
            latence_int:=latence_int + (compteur- mesure_EndCnt); 
            LastLatency <= (compteur- mesure_EndCnt);
            count_flit:=0;
            nbre_paquet:=nbre_paquet+1;
            
            if nbre_paquet=ReceivedPackNB then
              EndCnt <= compteur;
              TotalLatency <= latence_int;
            end if;
            
          end if;
        end if;	

      end if;                    
    end if;     
  end process p1;
  -----------------------------------------------------------------------------
  
  AckRx <= rx;
  
  
end RTL;

