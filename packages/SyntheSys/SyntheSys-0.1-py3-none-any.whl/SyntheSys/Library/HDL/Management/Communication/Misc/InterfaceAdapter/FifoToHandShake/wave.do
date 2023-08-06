onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic -label clk /fifotohandshake_tb/fifotohandshake_1/clk
add wave -noupdate -format Logic -label rst /fifotohandshake_tb/fifotohandshake_1/rst
add wave -noupdate -divider {FIFO Interface}
add wave -noupdate -format Logic -label fifo_isempty /fifotohandshake_tb/fifo_isempty
add wave -noupdate -format Logic -label fifo_read /fifotohandshake_tb/fifo_read
add wave -noupdate -format Literal -label fifo_dataout -radix hexadecimal /fifotohandshake_tb/fifo_dataout
add wave -noupdate -divider {Internal State}
add wave -noupdate -format Literal -height 16 -label currentstate /fifotohandshake_tb/fifotohandshake_1/currentstate
add wave -noupdate -divider {HS interface}
add wave -noupdate -format Logic -label hs_tx /fifotohandshake_tb/hs_tx
add wave -noupdate -format Logic -label hs_acktx /fifotohandshake_tb/hs_acktx
add wave -noupdate -format Literal -label hs_datain -radix hexadecimal /fifotohandshake_tb/hs_datain
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {21882 ps} 0}
configure wave -namecolwidth 148
configure wave -valuecolwidth 122
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
