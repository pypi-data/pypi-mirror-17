vlib work
vmap work
vcom -work work -f FileList.txt
vsim -voptargs="+acc" +notimingchecks -L work -t "1ps" work.FifoToHandShake_tb
do wave.do
#force -freeze sim:/board/RP/TX_APP/TESTS_INST/test_num 5
run -all
