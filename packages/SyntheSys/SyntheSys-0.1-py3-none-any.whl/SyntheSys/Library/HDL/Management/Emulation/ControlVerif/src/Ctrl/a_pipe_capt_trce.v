module a_pipe_capt_trce(
                       clk_ref,
                       rst_n,
                       nbr_pipe,
                       clk_user_i,
                       signal_i,
                       runverif_i,
                   
                       clk_user_pipe,
                       signal_o,
                       runpipe_o
                       );
                 
input clk_ref, rst_n, signal_i, clk_user_i;
input[3:0] nbr_pipe;
input runverif_i;

output clk_user_pipe, signal_o;
output runpipe_o;

wire clk_ref, rst_n, signal_i, clk_user_i;
wire[3:0] nbr_pipe;
wire runverif_i;
wire runpipe_o;

wire  clk_user_pipe, signal_o;
reg[14:0] decode_nbr;
reg[14:0] sig_pre_r;
reg[14:0] sig_clk_u;
reg[14:0] sig_runverif;

always @(nbr_pipe)
  case(nbr_pipe)
     4'h0 :  decode_nbr <= 15'b000_0000_0000_0001;
     4'h1 :  decode_nbr <= 15'b000_0000_0000_0010;
     4'h2 :  decode_nbr <= 15'b000_0000_0000_0100;
     4'h3 :  decode_nbr <= 15'b000_0000_0000_1000;
     4'h4 :  decode_nbr <= 15'b000_0000_0001_0000;
     4'h5 :  decode_nbr <= 15'b000_0000_0010_0000;
     4'h6 :  decode_nbr <= 15'b000_0000_0100_0000;
     4'h7 :  decode_nbr <= 15'b000_0000_1000_0000;
     4'h8 :  decode_nbr <= 15'b000_0001_0000_0000;
     4'h9 :  decode_nbr <= 15'b000_0010_0000_0000;
     4'ha :  decode_nbr <= 15'b000_0100_0000_0000;
     4'hb :  decode_nbr <= 15'b000_1000_0000_0000;
     4'hc :  decode_nbr <= 15'b001_0000_0000_0000;
     4'hd :  decode_nbr <= 15'b010_0000_0000_0000;
     4'he :  decode_nbr <= 15'b100_0000_0000_0000;
     4'hf :  decode_nbr <= 15'b000_0000_0000_0000;
  endcase

assign clk_user_pipe = decode_nbr[0] ? clk_user_i : sig_clk_u[0];
assign signal_o      = decode_nbr[0] ? signal_i   : sig_pre_r[0];
assign runpipe_o     = (decode_nbr[0] || decode_nbr[1]) ? runverif_i : sig_runverif[0];

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
     begin 
           sig_pre_r <= 'b0; 
     end
   else 
     begin 
           sig_pre_r[14] <= signal_i;
           sig_pre_r[13] <= decode_nbr[14] ? signal_i : sig_pre_r[14];
           sig_pre_r[12] <= decode_nbr[13] ? signal_i : sig_pre_r[13];
           sig_pre_r[11] <= decode_nbr[12] ? signal_i : sig_pre_r[12];
           sig_pre_r[10] <= decode_nbr[11] ? signal_i : sig_pre_r[11];
           sig_pre_r[9] <= decode_nbr[10] ? signal_i : sig_pre_r[10];
           sig_pre_r[8] <= decode_nbr[9] ? signal_i : sig_pre_r[9];
           sig_pre_r[7] <= decode_nbr[8] ? signal_i : sig_pre_r[8];
           sig_pre_r[6] <= decode_nbr[7] ? signal_i : sig_pre_r[7];
           sig_pre_r[5] <= decode_nbr[6] ? signal_i : sig_pre_r[6];
           sig_pre_r[4] <= decode_nbr[5] ? signal_i : sig_pre_r[5];
           sig_pre_r[3] <= decode_nbr[4] ? signal_i : sig_pre_r[4];
           sig_pre_r[2] <= decode_nbr[3] ? signal_i : sig_pre_r[3];
           sig_pre_r[1] <= decode_nbr[2] ? signal_i : sig_pre_r[2];
           sig_pre_r[0] <= decode_nbr[1] ? signal_i : sig_pre_r[1];

           sig_clk_u[14] <= clk_user_i;
           sig_clk_u[13] <= decode_nbr[14] ? clk_user_i : sig_clk_u[14];
           sig_clk_u[12] <= decode_nbr[13] ? clk_user_i : sig_clk_u[13];
           sig_clk_u[11] <= decode_nbr[12] ? clk_user_i : sig_clk_u[12];
           sig_clk_u[10] <= decode_nbr[11] ? clk_user_i : sig_clk_u[11];
           sig_clk_u[9]  <= decode_nbr[10] ? clk_user_i : sig_clk_u[10];
           sig_clk_u[8]  <= decode_nbr[9]  ? clk_user_i : sig_clk_u[9];
           sig_clk_u[7]  <= decode_nbr[8]  ? clk_user_i : sig_clk_u[8];
           sig_clk_u[6]  <= decode_nbr[7]  ? clk_user_i : sig_clk_u[7];
           sig_clk_u[5]  <= decode_nbr[6]  ? clk_user_i : sig_clk_u[6];
           sig_clk_u[4]  <= decode_nbr[5]  ? clk_user_i : sig_clk_u[5];
           sig_clk_u[3]  <= decode_nbr[4]  ? clk_user_i : sig_clk_u[4];
           sig_clk_u[2]  <= decode_nbr[3]  ? clk_user_i : sig_clk_u[3];
           sig_clk_u[1]  <= decode_nbr[2]  ? clk_user_i : sig_clk_u[2];
           sig_clk_u[0]  <= decode_nbr[1]  ? clk_user_i : sig_clk_u[1];

           sig_runverif[14] <= runverif_i;
           sig_runverif[13] <= runverif_i;
           sig_runverif[12] <= decode_nbr[14] ? runverif_i : sig_runverif[13];
           sig_runverif[11] <= decode_nbr[13] ? runverif_i : sig_runverif[12];
           sig_runverif[10] <= decode_nbr[12] ? runverif_i : sig_runverif[11];
           sig_runverif[9]  <= decode_nbr[11] ? runverif_i : sig_runverif[10];
           sig_runverif[8]  <= decode_nbr[10]  ? runverif_i : sig_runverif[9];
           sig_runverif[7]  <= decode_nbr[9]  ? runverif_i : sig_runverif[8];
           sig_runverif[6]  <= decode_nbr[8]  ? runverif_i : sig_runverif[7];
           sig_runverif[5]  <= decode_nbr[7]  ? runverif_i : sig_runverif[6];
           sig_runverif[4]  <= decode_nbr[6]  ? runverif_i : sig_runverif[5];
           sig_runverif[3]  <= decode_nbr[5]  ? runverif_i : sig_runverif[4];
           sig_runverif[2]  <= decode_nbr[4]  ? runverif_i : sig_runverif[3];
           sig_runverif[1]  <= decode_nbr[3]  ? runverif_i : sig_runverif[2];
           sig_runverif[0]  <= decode_nbr[2]  ? runverif_i : sig_runverif[1];

      end
endmodule

