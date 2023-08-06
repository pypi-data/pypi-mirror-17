onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider Inputs
add wave -noupdate -format Literal -label fifo_isempty /requestmanager_tb/fifo_isempty
add wave -noupdate -divider Tables
add wave -noupdate -format Literal -label requesttable /requestmanager_tb/requesttable
add wave -noupdate -format Literal -label transferttable /requestmanager_tb/transferttable
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {209357 ps} 0}
configure wave -namecolwidth 240
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
