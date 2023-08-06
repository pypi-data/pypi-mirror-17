module a_demux_serial_1v8(
                        rst_n, 
                        clk_ref, 
                        clk_rcpt, 
                        r_di, 
                        
                        r_dv_o, 
                        r_q
                        );
                                                                                            
  input r_di, rst_n;
  input clk_ref, clk_rcpt;
  output[7:0] r_q; 
  output r_dv_o;

  wire r_di, rst_n;
  wire clk_ref, clk_rcpt;

  reg[7:0] r_q; 
  reg r_dv_o;

// -------- SIGNAUX INTERNE -------------------
  reg[2:0] r_cpt;
                                                                                            
always @(posedge clk_ref or negedge rst_n)
                                                                                            
if(!rst_n)
  begin
    r_q <= 'b0;
    r_dv_o <= 1'b0;
    r_cpt <= 'b0;
  end  
else if(clk_rcpt)
  begin
   case(r_cpt)
           3'b000 : begin r_q <= {r_q[7:1],r_di}; r_dv_o <= 1'b0; end
           3'b001 : begin r_q <= {r_q[7:2],r_di,r_q[0]}; r_dv_o <= 1'b0; end
           3'b010 : begin r_q <= {r_q[7:3],r_di,r_q[1:0]}; r_dv_o <= 1'b0; end
           3'b011 : begin r_q <= {r_q[7:4],r_di,r_q[2:0]}; r_dv_o <= 1'b0; end
           3'b100 : begin r_q <= {r_q[7:5],r_di,r_q[3:0]}; r_dv_o <= 1'b0; end
           3'b101 : begin r_q <= {r_q[7:6],r_di,r_q[4:0]}; r_dv_o <= 1'b0; end
           3'b110 : begin r_q <= {r_q[7],r_di,r_q[5:0]}; r_dv_o <= 1'b0; end
           3'b111 : begin r_q <= {r_di,r_q[6:0]}; r_dv_o <= 1'b1; end
			  
//           3'b000 : begin r_q <= {r_q[15:1],r_di}; r_dv_o <= 1'b0; end
//           3'b001 : begin r_q <= {r_q[15:2],r_di,r_q[0]}; r_dv_o <= 1'b0; end
//           3'b010 : begin r_q <= {r_q[15:3],r_di,r_q[1:0]}; r_dv_o <= 1'b0; end
//           3'b011 : begin r_q <= {r_q[15:4],r_di,r_q[2:0]}; r_dv_o <= 1'b0; end
//           3'b100 : begin r_q <= {r_q[15:5],r_di,r_q[3:0]}; r_dv_o <= 1'b0; end
//           3'b101 : begin r_q <= {r_q[15:6],r_di,r_q[4:0]}; r_dv_o <= 1'b0; end
//           3'b110 : begin r_q <= {r_q[15:7],r_di,r_q[5:0]}; r_dv_o <= 1'b0; end
//           3'b111 : begin r_q <= {r_q[15:8],r_di,r_q[6:0]}; r_dv_o <= 1'b1; end
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

