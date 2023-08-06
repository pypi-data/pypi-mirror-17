onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider {Crossbar Control}
add wave -noupdate -format Literal -label outputconnections /crossbar_tb/outputconnections
add wave -noupdate -format Literal -label inputconnections /crossbar_tb/crossbar_1/inputconnections
add wave -noupdate -divider {Input FIFO interface}
add wave -noupdate -format Literal -label inputfifo_isempty -expand /crossbar_tb/crossbar_1/inputfifo_isempty
add wave -noupdate -format Literal -label inputfifo_read -expand /crossbar_tb/crossbar_1/inputfifo_read
add wave -noupdate -format Literal -label inputfifo_dataout -radix hexadecimal -expand /crossbar_tb/inputfifo_dataout
add wave -noupdate -divider {Output FIFO interface}
add wave -noupdate -format Literal -label outputfifo_isempty -expand /crossbar_tb/crossbar_1/outputfifo_isempty
add wave -noupdate -format Literal -label outputfifo_read -expand /crossbar_tb/crossbar_1/outputfifo_read
add wave -noupdate -format Literal -label outputfifo_dataout -radix hexadecimal -expand /crossbar_tb/outputfifo_dataout
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {25000 ps} 0}
configure wave -namecolwidth 253
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
WaveRestoreZoom {0 ps} {189288 ps}
