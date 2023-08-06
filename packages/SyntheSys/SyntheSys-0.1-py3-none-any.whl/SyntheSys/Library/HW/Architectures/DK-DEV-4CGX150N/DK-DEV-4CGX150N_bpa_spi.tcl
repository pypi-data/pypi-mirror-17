#############################################################################
#
#							Global Pin Assignement :
#
#############################################################################


##** Assignement for the source clock **##

set_location_assignment PIN_AK16 -to sysclk
#set_instance_assignment -name IO_STANDARD "1.8 V" -to rst_ext_i
#set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to rst_ext_i
set_instance_assignment -name SLEW_RATE 2 -to sysclk

##*************************************************************************##
##** 			Assignement for the RESET connected to USER_DIPSW0				 **##
##*************************************************************************##

set_location_assignment PIN_A5 -to rst_ext_i
set_instance_assignment -name IO_STANDARD "2.5 V" -to rst_ext_i
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to rst_ext_i
set_instance_assignment -name SLEW_RATE 2 -to rst_ext_i

##*********************************************************##
##** Assignement for the LED connected to rst_ext_i port **##
##*********************************************************##

set_location_assignment PIN_E4 -to LedRstExt_o
set_instance_assignment -name IO_STANDARD "2.5 V" -to LedRstExt_o
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to LedRstExt_o
set_instance_assignment -name SLEW_RATE 2 -to LedRstExt_o

##***********************************************************##
##** Assignement for the LED connected to a_fp0 hdl module **##
##***********************************************************##

set_location_assignment PIN_C7 -to led_o[0]
set_location_assignment PIN_A4 -to led_o[1]
set_location_assignment PIN_F6 -to led_o[2]
set_instance_assignment -name IO_STANDARD "2.5 V" -to led_o[*]
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to led_o[*]
set_instance_assignment -name SLEW_RATE 2 -to led_o[*]

##******************************************##
##** Assignement for the SPI Module Ports **##
##******************************************##

# J13.6
set_location_assignment PIN_C3 -to cs_spi 										
set_instance_assignment -name IO_STANDARD "2.5 V" -to cs_spi
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to cs_spi
set_instance_assignment -name SLEW_RATE 2 -to cs_spi
set_instance_assignment -name FAST_INPUT_REGISTER ON -to cs_spi

# J13.5
set_location_assignment PIN_E6 -to clk_spi 										
set_instance_assignment -name IO_STANDARD "2.5 V" -to clk_spi
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to clk_spi
set_instance_assignment -name SLEW_RATE 2 -to clk_spi
set_instance_assignment -name FAST_INPUT_REGISTER ON -to clk_spi

#J13.8
set_location_assignment PIN_F9 -to di_spi 										
set_instance_assignment -name IO_STANDARD "2.5 V" -to di_spi
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to di_spi
set_instance_assignment -name SLEW_RATE 2 -to di_spi
set_instance_assignment -name FAST_INPUT_REGISTER ON -to di_spi

#J13.7
set_location_assignment PIN_C15 -to do_spi 										
set_instance_assignment -name IO_STANDARD "2.5 V" -to do_spi
set_instance_assignment -name CURRENT_STRENGTH_NEW "MAXIMUM CURRENT" -to do_spi
set_instance_assignment -name SLEW_RATE 2 -to do_spi
set_instance_assignment -name FAST_OUTPUT_REGISTER ON -to do_spi

