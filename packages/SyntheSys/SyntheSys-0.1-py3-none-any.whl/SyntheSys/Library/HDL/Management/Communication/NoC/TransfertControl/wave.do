onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic -label rst /transfertcontrol_tb/rst
add wave -noupdate -format Logic -label clk /transfertcontrol_tb/clk
add wave -noupdate -divider FifoIn
add wave -noupdate -format Logic -label fifoin_isempty /transfertcontrol_tb/transfertcontrol_1/fifoin_isempty
add wave -noupdate -format Literal -label fifoin_dataout -radix hexadecimal /transfertcontrol_tb/transfertcontrol_1/fifoin_dataout
add wave -noupdate -format Logic -label fifoin_read /transfertcontrol_tb/transfertcontrol_1/fifoin_read
add wave -noupdate -divider FifoOut
add wave -noupdate -format Logic -label fifoout_isfull /transfertcontrol_tb/transfertcontrol_1/fifoout_isfull
add wave -noupdate -format Logic -label fifoout_write /transfertcontrol_tb/transfertcontrol_1/fifoout_write
add wave -noupdate -format Literal -label fifoout_datain -radix hexadecimal /transfertcontrol_tb/transfertcontrol_1/fifoout_datain
add wave -noupdate -divider {Output Control}
add wave -noupdate -format Logic -label connectionreset /transfertcontrol_tb/transfertcontrol_1/connectionreset
add wave -noupdate -divider {Internal State}
add wave -noupdate -format Literal -label currentstate /transfertcontrol_tb/transfertcontrol_1/currentstate
add wave -noupdate -format Literal -label cnt /transfertcontrol_tb/transfertcontrol_1/cnt
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {42737 ps} 0}
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
