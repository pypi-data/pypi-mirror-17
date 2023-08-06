module a_demux_serial_1v16(
rst_n, 
                        clk_ref, 
                        clk_rcpt, 
                        r_di, 
                        
                        r_dv_o, 
                        r_q
                        );
                                                                                            
  input r_di, rst_n;
  input clk_ref, clk_rcpt;
  output[15:0] r_q;
  output r_dv_o;

  wire r_di, rst_n;
  wire clk_ref, clk_rcpt;

  reg[15:0] r_q;
  reg r_dv_o;

// -------- SIGNAUX INTERNE -------------------
  reg[3:0] r_cpt;
                                                                                            
always @(posedge clk_ref or negedge rst_n)
                                                                                            
if(!rst_n)
  begin
    r_q <= 16'b0;
    r_dv_o <= 1'b0;
    r_cpt <= 4'b0;
  end  
else if(clk_rcpt)
  begin
   case(r_cpt)
                                                                                            
           4'b0000 : begin r_q <= {r_q[15:1],r_di}; r_dv_o <= 1'b0; end
           4'b0001 : begin r_q <= {r_q[15:2],r_di,r_q[0]}; r_dv_o <= 1'b0; end
           4'b0010 : begin r_q <= {r_q[15:3],r_di,r_q[1:0]}; r_dv_o <= 1'b0; end
           4'b0011 : begin r_q <= {r_q[15:4],r_di,r_q[2:0]}; r_dv_o <= 1'b0; end
           4'b0100 : begin r_q <= {r_q[15:5],r_di,r_q[3:0]}; r_dv_o <= 1'b0; end
           4'b0101 : begin r_q <= {r_q[15:6],r_di,r_q[4:0]}; r_dv_o <= 1'b0; end
           4'b0110 : begin r_q <= {r_q[15:7],r_di,r_q[5:0]}; r_dv_o <= 1'b0; end
           4'b0111 : begin r_q <= {r_q[15:8],r_di,r_q[6:0]}; r_dv_o <= 1'b0; end
           4'b1000 : begin r_q <= {r_q[15:9],r_di,r_q[7:0]}; r_dv_o <= 1'b0; end
           4'b1001 : begin r_q <= {r_q[15:10],r_di,r_q[8:0]}; r_dv_o <= 1'b0; end
           4'b1010 : begin r_q <= {r_q[15:11],r_di,r_q[9:0]}; r_dv_o <= 1'b0; end
           4'b1011 : begin r_q <= {r_q[15:12],r_di,r_q[10:0]}; r_dv_o <= 1'b0; end
           4'b1100 : begin r_q <= {r_q[15:13],r_di,r_q[11:0]}; r_dv_o <= 1'b0; end
           4'b1101 : begin r_q <= {r_q[15:14],r_di,r_q[12:0]}; r_dv_o <= 1'b0; end
           4'b1110 : begin r_q <= {r_q[15],r_di,r_q[13:0]}; r_dv_o <= 1'b0; end
           4'b1111 : begin r_q <= {r_di,r_q[14:0]};  r_dv_o <= 1'b1; end

    default : r_q <= r_q;
   endcase
    r_cpt <= r_cpt + 1'b1;
  end
else
  begin 
    r_q <= r_q;
    r_dv_o <= 1'b0;
    r_cpt <= r_cpt;
  end
endmodule

