// Copyright 1986-2015 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2015.2 (lin64) Build 1266856 Fri Jun 26 16:35:25 MDT 2015
// Date        : Tue Jan 12 10:25:52 2016
// Host        : cimepe30 running 64-bit Debian GNU/Linux 7.2 (wheezy)
// Command     : write_verilog -force -mode synth_stub /tima/payet/VIVADO_IP/clk_wiz_0/clk_wiz_0_stub.v
// Design      : clk_wiz_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7vx485tffg1761-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module clk_wiz_0(clk_in1_p, clk_in1_n, clk_out1)
/* synthesis syn_black_box black_box_pad_pin="clk_in1_p,clk_in1_n,clk_out1" */;
  input clk_in1_p;
  input clk_in1_n;
  output clk_out1;
endmodule
