<<<<<<< .mine
onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider {Control signals}
add wave -noupdate -format Literal -label outputport /routingtable_tb/routingtable_1/outputport
add wave -noupdate -format Literal -label selectedinput /routingtable_tb/routingtable_1/selectedinput
add wave -noupdate -format Literal -label connectionsresets /routingtable_tb/routingtable_1/connectionsresets
add wave -noupdate -divider {Output tables}
add wave -noupdate -format Literal -label inputconnections /routingtable_tb/routingtable_1/inputconnections
add wave -noupdate -format Literal -label outputconnections /routingtable_tb/routingtable_1/outputconnections
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {25000 ps} 0}
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {220500 ps}
=======
onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider {Control signals}
add wave -noupdate -format Literal -label selectedinput /routingcontrol_tb/routingcontrol_1/selectedinput
add wave -noupdate -divider Data
add wave -noupdate -format Literal -label fifo_dataout_list -radix hexadecimal -expand /routingcontrol_tb/routingcontrol_1/fifo_dataout_list
add wave -noupdate -divider Selected
add wave -noupdate -format Literal -label outputport /routingcontrol_tb/routingcontrol_1/outputport
add wave -noupdate -divider Addresses
add wave -noupdate -format Literal -label x_dest /routingcontrol_tb/routingcontrol_1/x_dest
add wave -noupdate -format Literal -label y_dest /routingcontrol_tb/routingcontrol_1/y_dest
add wave -noupdate -format Literal -label x_local /routingcontrol_tb/routingcontrol_1/x_local
add wave -noupdate -format Literal -label y_local /routingcontrol_tb/routingcontrol_1/y_local
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {92888 ps} 0}
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {220500 ps}
>>>>>>> .r2817
