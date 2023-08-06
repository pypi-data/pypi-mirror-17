
# Define the output directory area. Mostly for debug purposes.
set part $FPGA
set Top $TOPENTITY
set OutputDir $OUTPUTPATH
file mkdir $OutputDir

# Set target part to fake current project, to read IPs
# More details: http://www.xilinx.com/support/answers/54317.html

#foreach item [get_parts] {
#	puts $item
#}
set_part $part
set_property part $part [current_project]
#set_property GENERATE_SYNTH_CHECKPOINT FALSE [get_files src/PCIe_Riffa22_VC707/PCIeGen1x8If64.xci]


