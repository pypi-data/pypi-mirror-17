`define LENGTH_RAM_TRACE 13                 
`define PROF_RAM_TRACE 8192
`define FULL_RAM_TRACE 13'b1_1111_1111_0111  // Max -10

module a_trace_ram(din, wen, rdaddr, wraddr, clk, oclk, dout);
// ##### MEMOIRE 64x1024                                                                                            
input[63:0] din;
input wen, clk, oclk;
input[`LENGTH_RAM_TRACE-1:0] rdaddr, wraddr;
output[63:0] dout;
                                                                                            
wire[`LENGTH_RAM_TRACE-1:0] rdaddr, wraddr;
wire wen, clk, oclk;
wire[63:0] din;
wire[63:0] int_dout;
                                                                                            
reg[63:0] dout;
reg[63:0] mem[`PROF_RAM_TRACE-1:0];
                                                                                            
// ################# ECRITURE ###############################
                                                                                            
always @(posedge clk)
                                                                                            
     if(wen)
           begin
               mem[wraddr] <= din;
           end
                                                                                            
// ################# LECTURE ###############################
                                                                                            
assign int_dout = mem[rdaddr];
                                                                                            
always @(posedge oclk)
                                                                                            
       dout <= int_dout;

endmodule
