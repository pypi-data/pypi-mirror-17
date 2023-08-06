----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    17:46:57 15/06/2011 
-- Design Name:  TAN Junyan, FRESSE Virginie, ROUSSEAU Frédéric, Matthieu PAYET.
-- Module Name:    traffic_generator - Behavioral 
-- Project Name:   HERMES NoC emulation Platform
-- Target Devices: Xilinx V5 ML506
-- Tool versions: Xilinx 10.1
-- Description:  This version provides the HERMES NoC emulation in the scenario of multi initiators to multi destinations-
-- Dependencies: 
--
-- Revision: Multi-sources,multi-destination  Version 2
-- Revision 0.01 - File Created
-- Additional Comments:
--
----------------------------------------------------------------------------------


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
Use IEEE.std_logic_arith.all;

use work.EmulationPackage.all;  

-------------------------------------------------------------------------------
-- ENTITY: Traffic generator for multi-destination emulation
-------------------------------------------------------------------------------
Entity TrafficGenerator IS
  generic ( 
    LocalAddr_x      : natural ;  -- Adresse 'X' de la Source
    LocalAddr_y      : natural ;  -- Adresse 'Y' de la Source
    FlitWidth        : natural :=16;
    NbRouters        : natural :=9
    );
  port ( 
    Clk, Rst         : IN  std_logic;
    DestNB	     : IN  integer;   -- Number of target nodes
    DestSelect       : IN  std_logic_vector(NbRouters-1 downto 0);   -- One bit per target node
    PackSize         : IN  integer;   -- Packet size
    PackNB	     : IN  integer;   -- number of packets to be send
    IdleTime	     : IN  integer;   -- number of Clk cycles to wait between two packet sends
    Tx   	     : OUT std_logic;
    AckTx            : IN  std_logic;
    DataOut          : OUT std_logic_vector(FlitWidth-1 downto 0)
    );
end TrafficGenerator;

-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
Architecture RTL of TrafficGenerator IS

  type FlitTable is array (0 to (NbRouters-1)) of std_logic_vector(FlitWidth-1 downto 0);

  signal data_entre : FlitTable; --Signal que le Router_Data_In va envoyer
  signal routerrx   : std_logic :='0';
  signal teste1sig,teste2sig :integer :=0;  --chaque flit envoyé est dans un etat; 
  signal LocalAddr : std_logic_vector(FlitWidth/2-1 downto 0); -- XY source address
  signal sig_adresses : std_logic_vector((NbRouters-1)downto 0);
  signal pack_size : std_logic_vector(FlitWidth-1 downto 0);
  type state is (S0,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,SACK);
  signal ES, PES, NES: state := S0;
  
  
Begin

  sig_adresses <= conv_std_logic_vector(DestSelect, NbRouters);
  LocalAddr   <= conv_std_logic_vector(LocalAddr_x,FlitWidth/4)&conv_std_logic_vector(LocalAddr_y,FlitWidth/4);
  pack_size    <= CONV_STD_LOGIC_VECTOR(PackSize-2, FlitWidth);
  
--------------------------------------------------------------------
-- Control FSM - SNMP BUS CONTROL
--------------------------------------------------------------------
  process (Clk,Rst)
  begin
    if Rst='1' then
      ES<=S0;
    elsif Clk'event and Clk='0' then
      ES<=PES;
    end if;
  end process;
  
--------------------------------------------------------------------
  P: process (Clk)
    variable nbre : integer := 0;     -- compte le nbre de paquets ("mesure" du nbre de paquets)
    VARIABLE state, dest2, dest :INTEGER := 0; -- permet de se delacer dans le tableau des donnes a envoyer -- segundo destino
    VARIABLE sum,teste1,teste2:INTEGER := 0; -- compte le nombre de cycles entre 2 paquets ("mesure" de idle)
    VARIABLE nbre_dest:integer := 0; -- nombre de destinations --numero de fontes
    variable compteur, mesure_initial: integer := 0;
    variable mesure_initial_logic: std_logic_vector( FlitWidth*2-1 downto 0);
    
  begin
    
    if Clk'event and Clk='1' then
      
      case ES is
        --Rst state
        when S0 =>
          routerrx <= '0';
          router_data_in <= (others => '0');
          state:=0;
          nbre := 0;
          dest2 := 0;
          dest := 0;
          sum := 0;
          teste1 := 0;
          teste2 := 0;
          nbre_dest := 0;
          compteur := 0;
          mesure_initial := 0;
          mesure_initial_logic := (OTHERS=>'0');	
          PES <= S1;
          
          --select the next destination
        when S1 =>
          for j in 0 to (NbRouters-1) loop
            if sig_adresses(j) = '1' then
              if ( j < dest2 ) then
                next;
              else  
                if ( j = dest2 ) and ( j /= 0 ) then next; end if;
                dest2 := j;
                PES <= S2;
                exit;
              end if;
            end if;
          end loop; 
          
          --start the transmition of the packet
        when S2 =>
          state:=0;
          mesure_initial := compteur;
          mesure_initial_logic:= conv_std_logic_vector (mesure_initial,FlitWidth*2);		
          router_data_in <= "00000000" & Adrs(dest2);
          routerrx <='1';
          PES <= SACK;
          NES <= S3;
          --send packet size 
        when S3 =>
          state:=1;
          router_data_in <= pack_size;	 
          routerrx <='1';
          PES <= SACK;
          NES <= S4;		
          --send local address 
        when S4 =>
          state:=2;	 
          router_data_in <= "00000000" & LocalAddr;
          routerrx <='1';
          PES <= SACK;
          NES <= S5;	  		   
          --send timestamp 00 
        when S5 =>
          state :=3;
          router_data_in <= mesure_initial_logic(FlitWidth-1 downto 0);
          routerrx <='1';
          PES <= SACK;
          NES <= S6;	  		   
          --send timestamp 01
        when S6 =>			 
          state := 4;
          router_data_in <= mesure_initial_logic(FlitWidth*2-1 downto FlitWidth);
          routerrx <='1';
          PES <= SACK;
          NES <= S7;	  		   
          --send the rest of the packet
        when S7 => 
          state := state + 1;
          if (state=1*PackSize) then -- fin du paquet
            state := 0 ; 
            nbre := nbre+1;
            sum :=1;
            PES <= S8;
          else
            router_data_in <= "1111111111100000";  
            routerrx <='1';
            PES <= SACK;
            NES <= S7;
          end if;		   
          
          --idle time counter
        when S8 =>
          sum:=sum+1;
          IF sum=idle_paket+2 THEN
            sum:=0;
            PES <= S9;
          END IF;	
          --check the number of sent packets	  
        when S9 =>
          if (nbre < nbre_paket) then
            PES <= S2;  -- same destination                                               -- Il a fini un paquet	
          elsif (nbre=nbre_paket) then              
            if (teste1=(DestNB-1)) then -- fin de données
              PES <= S10;                
            else
              routerrx<= '0';
              nbre:=0;
              state:=0;
              teste1:=teste1+1; 
              PES <= S1;  --look for another destination            
            end if;
          end if;        
          
          --end of transmition  	  
        when S10 =>
          PES <= S10;
          
          --wait ack from router	 
        when SACK =>
          if AckTx='1' then
            PES <= NES;
            routerrx<='0';
          end if;
          
      end case;
      
      compteur := compteur + 1;
    end if;
    
  end process P;
  -----------------------------------------------------------------------------
  
  Tx<=routerrx;
  
end RTL;


