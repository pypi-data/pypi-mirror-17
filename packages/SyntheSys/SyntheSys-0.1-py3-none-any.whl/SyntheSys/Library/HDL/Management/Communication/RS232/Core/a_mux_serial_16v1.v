module a_mux_serial_16v1(
                      rst_n, 
                      clk_ref, 
                      clk_send, 
                      data_i, 
                      dv_i,
                        
                      r_do_o, 
                      r_busy_o
                      );
                                                                                            
  input rst_n, clk_ref, clk_send;
  input[15:0] data_i;
  input dv_i;
  output r_do_o;
  output r_busy_o;

  wire rst_n, clk_ref, clk_send;
  wire[15:0] data_i;
  wire dv_i;

  reg r_do_o;
  reg r_busy_o;

// -------- SIGNAUX INTERNE -------------------
           
reg[19:0] r_tmp_data;
reg[4:0] r_cpt_send;

always @(posedge clk_ref or negedge rst_n)
  if(!rst_n)
     begin
           r_do_o <= 1'b1;
           r_busy_o <= 1'b0;
           r_tmp_data <= 20'b0;
           r_cpt_send <= 5'b0;
     end
  else if(dv_i)
     begin
           r_do_o <= 1'b1;
           r_busy_o <= 1'b1;
           r_tmp_data <= {1'b1,data_i[15:8],1'b0,1'b1,data_i[7:0],1'b0};
           r_cpt_send <= 5'b0;
     end
  else if(r_cpt_send == 5'd19 && clk_send)
     begin
           r_do_o <= 1'b1;
           r_busy_o <= 1'b0;
           r_tmp_data <= 20'b0;
           r_cpt_send <= 5'b0;
     end
  else if(r_busy_o && clk_send)
     begin
           r_do_o <= r_tmp_data[r_cpt_send];
           r_busy_o <= (r_cpt_send == 5'd19) ? 1'b0 : 1'b1;
           r_tmp_data <= r_tmp_data;
           r_cpt_send <= r_cpt_send + 1'b1;
     end
  else
     begin
           r_do_o <= r_do_o;
           r_busy_o <= r_busy_o;
           r_tmp_data <= r_tmp_data;
           r_cpt_send <= r_cpt_send;
     end


endmodule
