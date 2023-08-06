
# Define the output directory area. Mostly for debug purposes.

# Run logic synthesis
#synth_design -top VC709Gen2x8If128 -keep_equivalent_registers -flatten_hierarchy full -resource_sharing on
synth_design -top $TOPENTITY -keep_equivalent_registers -resource_sharing on

# Run logic optimization
opt_design -verbose

# Run automated placement of the remaining of the design
place_design

# Physical logic optimization
phys_opt_design -directive AggressiveExplore


# Run first routing
route_design


set_property DONT_TOUCH true [get_cells -hierarchical "RiffaToHS"]
set_property DONT_TOUCH true [get_cells -hierarchical "InputTable"]
set_property DONT_TOUCH true [get_cells -hierarchical "HeaderTable"]

write_verilog "./InputTable.vhd" -include_unisim -include_xilinx_libs -cell [lindex [get_cells -hierarchical "InputTable"] 0]
write_verilog "./HeaderTable.vhd" -include_unisim -include_xilinx_libs -cell [lindex [get_cells -hierarchical "HeaderTable"] 0]
write_verilog "./TaskManager.vhd" -include_unisim -include_xilinx_libs -cell [lindex [get_cells -hierarchical "TaskManager"] 0]

exit 0










