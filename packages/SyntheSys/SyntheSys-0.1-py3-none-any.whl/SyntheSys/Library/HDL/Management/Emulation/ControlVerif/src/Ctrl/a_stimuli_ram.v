`define LENGTH_RAM_STIMULI 13                 
`define PROF_RAM_STIMULI 8192
module a_stimuli_ram(din, wen, rdaddr, wraddr, clk, oclk, dout);
// ##### MEMOIRE 64x1024                                                                                            
input[63:0] din;
input wen, clk, oclk;
input[`LENGTH_RAM_STIMULI-1:0] rdaddr, wraddr;
output[63:0] dout;
                                                                                            
wire[`LENGTH_RAM_STIMULI-1:0] rdaddr, wraddr;
wire wen, clk, oclk;
wire[63:0] din;
wire[63:0] int_dout;
                                                                                            
reg[63:0] dout;
reg[63:0] mem[`PROF_RAM_STIMULI-1:0];
                                                                                            
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
