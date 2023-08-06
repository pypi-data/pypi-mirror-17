
# TCL Script for TB 'BOPM_tb'
# Shows current scope in design hierarchy.
scope
divider add "LOOPBACK"
wave add ControlVerif_Loopback_96_96_0_TB/ControlVerif_Loopback_96_96_0_DUT/

vcd dumpfile LOOPBACK.vcd
vcd dumpvars -m ControlVerif_Loopback_96_96_0_DUT -l 2
# Runs simulation for an additional 8000 ns.
run 8000 ns
vcd dumpflush
# Quits simulation.
exit 0

