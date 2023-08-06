
setMode -bs
setCable -port auto
Identify -inferir
identifyMPM
assignFile -p $SCANCHAINPOS -file $BITSTREAM
program -p $SCANCHAINPOS
quit


