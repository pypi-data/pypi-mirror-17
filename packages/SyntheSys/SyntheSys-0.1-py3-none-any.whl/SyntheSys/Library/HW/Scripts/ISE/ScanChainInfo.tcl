# TCL script for parsing Xilinx JTAG info file

set HOME [glob "~"]
#------------------------------------------------------------
# Write batch file for impact
#------------------------------------------------------------
set BatchContent \
"setMode -bs
setCable -port auto
Identify 
info
quit"
set BatchFilePath "$HOME/.adacsys/ImpactBatchCmd.txt" 
set BatchFile [open $BatchFilePath w]
	puts $BatchFile $BatchContent
close $BatchFile
#------------------------------------------------------------


#------------------------------------------------------------
# Execute Impact in batch mode
#------------------------------------------------------------

set XScanChainInfo [exec -keepnewline impact -batch $BatchFilePath 2>@1]
#if {[catch {set XScanChainInfo [exec impact -batch $BatchFilePath]} msg]}{
#   puts "Something seems to have gone wrong:"
#   puts "Information about it: $::errorInfo"
#}
#------------------------------------------------------------

#------------------------------------------------------------
# PARSE INFO FILE
#------------------------------------------------------------
set Mode "Ignore"
set ConfigFilePath "$HOME/.adacsys/XScanChain.ini"
set ConfigFile [open $ConfigFilePath w+]

#set InfoFile [open $XScanChainInfo r]
set Lines [split $XScanChainInfo "\n"]
foreach Line $Lines {
	if {[regexp {^\s*Connecting to cable (Usb Port - USB\d\d.*$} $Line]} {
		regexp {USB\d\d} $Line USB
	}
	if {$Mode=="Ignore"} {
		if {[regexp {^\s*Position\s+PartName\s+Version\s+FileName\s*$} $Line]} {
			set Mode "Parse"
		}
	} else {
		if {[regexp {^\s*-+\s*$} $Line]} {
			set Mode "Ignore"
		} else {
			set Words [regexp -all -inline {\S+} $Line]
			if [llength $Words]>3 {
				set Position [lindex $Words 0]
				set PartName [lindex $Words 1]
				puts $ConfigFile "\[$PartName\]" 
				puts $ConfigFile "ScanChainPos = $Position" 
				puts $ConfigFile "USBID        = $USB" 
			}
		}
	}
}
close $ConfigFile
#------------------------------------------------------------

