--	Package File Template
--
--	Purpose: This package defines supplemental types, subtypes, 
--	  constants, and functions 
--   Version 1 for multisources to one destination with data injection rate automatic
--   TAN Junyan, FRESSE Virginie, ROUSSEAU Frédéric.


library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.STD_LOGIC_unsigned.all;


-------------------------------------------------------------------------------
-- PACKAGE: Parameters for traffic emulation of HERMES NoC - ONE DESTINATION
-------------------------------------------------------------------------------
package EmulationPackage is
  
  type integNORT    is array (0 to (NROT-1)) of integer;
  type DESTs        is array (0 to (NROT-1)) of regmetadeflit;
  type Addrs        is array (0 to (NROT-1)) of integNORT;
  type TotalRegflit is array (0 to (NROT-1)) of regflit;
  
  constant Adrs : DESTs := ("00000000","00010000","00100000","00000001","00010001","00100001","00000010","00010010","00100010");

  constant taille_pk_int_generic : integNORT := (0,0,0,0,0,0,0,0,0);
  constant nbre_paket_generic	 : integNORT := (0,0,0,0,0,0,0,0,0);
  constant idle_paket_generic	 : integNORT := (0,0,0,0,0,0,0,0,0);  
  
  --destinations des paquets
  constant destinations		 : integNORT := (0,0,0,0,0,0,0,0,0);
  constant last_dest		 : integNORT := (0,0,0,0,0,0,0,0,3);
  constant total_paquets	 : integNORT := (10,10,0,0,10,0,0,0,0);
  
  constant destinos		 : Addrs     := ((0,0,0,0,0,0,0,0,0), --0
                                                 (0,0,0,0,0,0,0,0,0), --1
                                                 (0,0,0,0,0,0,0,0,0), --2
                                                 (0,0,0,0,0,0,0,0,0), --3
                                                 (0,0,0,0,0,0,0,0,0), --4
                                                 (0,0,0,0,0,0,0,0,0), --5 
                                                 (0,0,0,0,0,0,0,0,0), --6
                                                 (0,0,0,0,0,0,0,0,0), --7
                                                 (0,0,0,0,0,0,0,0,0) --8
                                                 );
end EmulationPackage;

