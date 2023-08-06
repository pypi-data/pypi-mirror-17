onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic -label clk /arbiter_tb/clk
add wave -noupdate -format Logic -label rst /arbiter_tb/rst
add wave -noupdate -format Literal -label requesttable /arbiter_tb/requesttable
add wave -noupdate -format Literal -label cnt /arbiter_tb/arbiter_1/cnt
add wave -noupdate -format Literal -label selectedport /arbiter_tb/selectedport
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {69990 ps} 0}
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
