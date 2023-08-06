vlib work
vmap work
vcom -work work -f FileList.txt
vsim -novopt +notimingchecks -L work -t "1ps" work.TransfertControl_tb
do wave.do
#force -freeze sim:/board/RP/TX_APP/TESTS_INST/test_num 5
run -all
