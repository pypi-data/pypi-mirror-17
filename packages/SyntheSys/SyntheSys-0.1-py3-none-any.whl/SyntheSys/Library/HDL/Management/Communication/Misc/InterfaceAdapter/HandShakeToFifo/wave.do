onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic -label clk /handshaketofifo_tb/handshaketofifo_1/clk
add wave -noupdate -format Logic -label rst /handshaketofifo_tb/handshaketofifo_1/rst
add wave -noupdate -format Logic -label hs_rx /handshaketofifo_tb/handshaketofifo_1/hs_rx
add wave -noupdate -format Logic -label hs_ackrx /handshaketofifo_tb/handshaketofifo_1/hs_ackrx
add wave -noupdate -format Literal -height 16 -label currentstate /handshaketofifo_tb/handshaketofifo_1/currentstate
add wave -noupdate -format Literal -label hs_datain /handshaketofifo_tb/handshaketofifo_1/hs_datain
add wave -noupdate -format Literal -label fifo_datain /handshaketofifo_tb/handshaketofifo_1/fifo_datain
add wave -noupdate -format Logic -label fifo_write /handshaketofifo_tb/handshaketofifo_1/fifo_write
add wave -noupdate -format Logic -label fifo_isfull /handshaketofifo_tb/handshaketofifo_1/fifo_isfull
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {40857 ps} 0}
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
WaveRestoreZoom {0 ps} {145919 ps}
