library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use work.HermesPackage.all;

entity Hermes_MUX is
port(
		data_out: out arrayNport_regflit;
		tx:       out regNport;
		data_ack: out regNport;
		
		data: in arrayNport_regflit;
		free    : in regNport;
		sender : in regNport;
		data_av : in regNport;
		ack_tx:   in  regNport
);
end entity;


architecture default of Hermes_MUX is
begin

	MUXS : for i in 0 to (NPORT-1) generate
		data_out(i) <= data(CONV_INTEGER(mux_out(i))) when free(i)='0' else (others=>'0');
		data_ack(i) <= ack_tx(CONV_INTEGER(mux_in(i))) when sender(i)='1' else '0';
		tx(i) <= data_av(CONV_INTEGER(mux_out(i))) when free(i)='0' else '0';
	end generate MUXS;
	
end architecture;