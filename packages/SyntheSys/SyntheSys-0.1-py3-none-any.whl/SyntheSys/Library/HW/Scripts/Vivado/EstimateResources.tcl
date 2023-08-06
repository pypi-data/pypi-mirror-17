# Define the output directory area. Mostly for debug purposes.
set part $FPGA
set Top $TOPENTITY
#set ConstraintFile $CONSTRAINTS
set OutputDir $OUTPUTPATH
file mkdir $OutputDir

# Set target part to fake current project, to read IPs
# More details: http://www.xilinx.com/support/answers/54317.html
set_part $part
set_property part $part [current_project]

#read_xdc $ConstraintFile

# Run logic synthesis
#synth_design -top VC709Gen2x8If128 -keep_equivalent_registers -flatten_hierarchy full -resource_sharing on
synth_design -top $Top -keep_equivalent_registers -resource_sharing on

set_property DONT_TOUCH true [get_cells -hierarchical "InputTable"]

write_verilog "./InputTable.vhd" -include_unisim -include_xilinx_libs -cell [lindex [get_cells -hierarchical "InputTable"] 0]
exit 0
#report_utilization -file "$TOPENTITY_post_synth_util.rpt"

# Run logic optimization - no trimming !
opt_design -retarget -propconst -bram_power_opt

#place_design -quiet

# Report timing and utilization estimates
report_utilization -file "$TOPENTITY_post_place_util.rpt"

#route_design -quiet

# Report timing and utilization estimates
report_utilization -file "$TOPENTITY_post_route_util.rpt"
