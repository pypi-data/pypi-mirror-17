<?xml version="1.0"?><!DOCTYPE service SYSTEM "serviceSimple.dtd">
<service name="FIFO" type="simple" version="1.0" category="application.service.noc">
	
	<parameter name="regNport" type="integer" default="5"/>
	<parameter name="arrayNport_regflit" type="integer" default="5x16"/>

	<input name="data" size="arrayNport_regflit" type="logic" default="0"/>
	<input name="free" size="regNport" type="logic" default="0"/>
	<input name="sender" size="regNport" type="logic" default="0"/>
	<input name="data_av" size="regNport" type="logic" default="0"/>
	<input name="ack_tx" size="regNport" type="logic" default="0"/>

	<output name="data_out" size="arrayNport_regflit" type="logic" default="open"/>
	<output name="tx" size="regNport" type="logic" default="open"/>
	<output name="data_ack" size="regNport" type="logic" default="open"/>

</service>
