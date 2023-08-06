
# Define the output directory area. Mostly for debug purposes.
#set part $FPGA
#set OutputDir $OUTPUTPATH
#file mkdir $OutputDir

#set_msg_config -id {Vivado 12-1387} -new_severity {ERROR}

# Set target part to fake current project, to read IPs
# More details: http://www.xilinx.com/support/answers/54317.html
#set_part $part
#set_property part $FPGA [current_project]
#set log [list_targets [get_files src/PCIe_Riffa22_VC707/PCIeGen1x8If64.xci]]
#puts $log
#read_ip [get_files src/PCIe_Riffa22_VC707/PCIeGen1x8If64.xci]
#report_ip_status

#generate_target all [get_files src/PCIe_Riffa22_VC707/PCIeGen1x8If64.xci]
#synth_ip [get_ips PCIeGen1x8If64]
#report_ip_status

# Run logic synthesis
#synth_design -top VC709Gen2x8If128 -keep_equivalent_registers -flatten_hierarchy full -resource_sharing on
#set Top $TOPENTITY
synth_design -top $TOPENTITY -keep_equivalent_registers -resource_sharing on


#report_ip_status
# Run logic optimization
opt_design -verbose

# Report timing and utilization estimates
#report_timing_summary -file $OutputDir/[append "$TOPENTITY" "_post_synth_timing_summary.rpt"]
#report_utilization -file $OutputDir/[append "$TOPENTITY" "_post_synth_util.rpt"]
#report_utilization -file "$TOPENTITY_post_synth_util.rpt"
#report_clock_networks
# Write design checkpoint
#write_checkpoint -force $OutputDir/post_synth.dcp

# Note: For debug purposes, if you want to start from post- logic synthesis state,
# uncomment these lines and remove all above commands (except setting of parameters)
#read_checkpoint $OutputDir/post_synth.dcp
#link_design -top VC709Gen2x8If128 -part $part



# Early exit, for debug. The checkpoint can be opened with the Vivado GUI to test placement commands.
#exit

# Try using PBlocks to lock PCIe & Riffa in particular clock regions
#create_pblock pblock_pcieriffa
#add_cells_to_pblock pblock_pcieriffa [get_cells PCIeGen1x8If64]
#add_cells_to_pblock pblock_pcieriffa [get_cells riffa]
#resize_pblock pblock_pcieriffa -add CLOCKREGION_X1Y4:CLOCKREGION_X1Y5

# Set special placement constraints
#source place.tcl



# Run automated placement of the remaining of the design
place_design
#place_design -directive WLDrivenBlockPlacement
#place_design -directive ExtraNetDelay_high



# Physical logic optimization
phys_opt_design -directive AggressiveExplore

# write design checkpoint, report utilization and timing estimates
#report_clock_utilization -file $OutputDir/[append "$TOPENTITY" "_clock_util.rpt"]

# Report utilization and timing estimates
report_utilization -file "$TOPENTITY_post_place_util.rpt"
#report_timing_summary -file "$TOPENTITY_post_place_timing_summary.rpt"

# Write design checkpoint
#write_checkpoint -force $OutputDir/[append "$TOPENTITY" "_post_place.dcp"]



# Note: For debug purposes, if you want to start from post- placement state,
# uncomment these lines and remove all above commands (except setting of parameters)
#read_checkpoint $OutputDir/post_place.dcp
#link_design -top VC709Gen2x8If128 -part $part

# Run first routing
route_design

report_utilization -file "$TOPENTITY_post_route_util.rpt"
#route_design -tns_cleanup -directive Explore
#route_design -tns_cleanup -preserve

# Note: For more optimization, perform another placement optimization and re-route
#place_design -post_place_opt
#phys_opt_design -directive AggressiveExplore
#route_design

# Report the routing status, timing, power, design rule check
#set Top $TOPENTITY
#report_route_status -file $OutputDir/[append $Top "_post_route_status.rpt"]
#set Top $TOPENTITY
#report_timing_summary -file "$TOPENTITY_post_route_timing_summary.rpt"
#set Top $TOPENTITY
#report_power -file $OutputDir/[append $Top "_post_route_power.rpt"]
#set Top $TOPENTITY
#report_drc -file $OutputDir/[append $Top "_post_route_drc.rpt"]

# Write the post-route design checkpoint
#write_checkpoint -force $OutputDir/post_route.dcp



# Note: For debug purposes, if you want to start from post- routing state,
# uncomment these lines and remove all above commands (except setting of parameters)
#read_checkpoint $OutputDir/post_route.dcp
#link_design -top VC709Gen2x8If128 -part $part

# Optionally generate post- routing simulation model
#set postparDir $OutputDir/vhdl-postpar/
#file mkdir $postparDir
#write_vhdl -force $postparDir/top.vhd
#write_sdf -force $postparDir/top.sdf

# Generate the bitstream
write_bitstream -force $TOPENTITY.bit

