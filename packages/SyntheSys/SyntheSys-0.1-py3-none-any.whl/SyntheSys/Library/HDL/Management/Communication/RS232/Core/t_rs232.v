`timescale 1 ns/10 ps

module t_rs232;

reg r_rst_n;
reg clk_ref;
reg r_di;
reg r_dv_i;

reg r_di_nw;

wire r_do, r_do_nw;
wire[15:0] r_q, r_q_nw;
wire r_dv_o, r_dv_o_nw;
wire r_busy_o, r_busy_o_nw;
wire r_led_o, led_sync, led_di;

reg r_clk_port_serie;

a_RS232 u_RS232(
                     .rst_n(r_rst_n),
                     .clk_ref(clk_ref), 
                     .r_di(r_di), 
                     .r_do(r_do_nw),
                   
                     .r_dv_o(r_dv_o_nw),
                     .r_q(r_q_nw),

                     .data_i(16'h5555),
                     .dv_i(r_dv_i),
                     .r_busy_o(r_busy_o_nw),
                     
                     .led_di_o(led_di),
                     .led_sync_o(led_sync)
                     );
 
initial
                                                                                                                
begin : stimuli
// ---- Signaux d'aide a la simu ----
          r_rst_n = 1'b0;
          clk_ref = 1'b0;
          r_di = 1'b1;
          r_dv_i = 1'b0;
          r_clk_port_serie = 1'b0;
 
        

#10000 r_rst_n = 1'b1;

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});
#2000000 Write({8'haa,8'haa});
#1000000 r_rst_n = 1'b0;
#10000 r_rst_n = 1'b1;

#5000 Write({8'd52,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd61});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd61,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd63});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd27,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd13});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd79,8'd83});
#5000 Write({8'd00,8'd83});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd63});

#5000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd10,8'd83});

//#10000 r_rst_n = 1'b1;

#500000 Write({8'd55,8'd00});
#5000 Write({8'd68,8'd65});
#5000 Write({8'd67,8'd65});
#5000 Write({8'd89,8'd83});
#5000 Write({8'd00,8'd83});
#20000 Write({8'haa,8'haa});
#10000000 r_rst_n = 1'b0;
//#5000 Write_Par(16'h0);
//#5000 Write_Par({1'b1,8'd68,1'b0,8'd65});

#10000

$stop;

end

always #10 clk_ref = ~clk_ref;
//always #4340 r_clk_port_serie = ~r_clk_port_serie;
always #1000 r_clk_port_serie = ~r_clk_port_serie;

// TASK
task Init_rs232;                                                                                  
                                                                                            
reg[19:0] r_final_data;
                                                                                            
integer k;
                                                                                            
begin
assign r_final_data = ({1'b1,8'b0,1'b0});
                                                                                            
                                                                                            
    for (k=0; k<10; k=k+1)
       begin
           @(posedge r_clk_port_serie)
                 r_di <= r_final_data[k];
       end
end
endtask

task Write;
input[15:0] data_i;
                                                                                            
                                                                                            
reg[15:0] data_i;
reg[19:0] r_final_data;
                                                                                            
                                                                                            
integer k;
                                                                                            
                                                                                            
begin
assign r_final_data = ({1'b1,data_i[15:8],1'b0,1'b1,data_i[7:0],1'b0});
                                                                                            
                                                                                            
    for (k=0; k<20; k=k+1)
       begin
           @(posedge r_clk_port_serie)
                 r_di <= r_final_data[k];
       end
end
endtask

task Write_Par;
input[17:0] data_i;                                                                      
                                                                                            
reg[17:0] data_i;
reg[19:0] r_final_data;
                                                                                            
                                                                                            
integer k;
                                                                                            
                                                                                            
begin
assign r_final_data = ({1'b1,data_i[17:9],1'b0,1'b1,data_i[8:0],1'b0});
                                                                                            
                                                                                            
    for (k=0; k<22; k=k+1)
       begin
           @(posedge r_clk_port_serie)
                 r_di <= r_final_data[k];
       end
end
endtask
endmodule

