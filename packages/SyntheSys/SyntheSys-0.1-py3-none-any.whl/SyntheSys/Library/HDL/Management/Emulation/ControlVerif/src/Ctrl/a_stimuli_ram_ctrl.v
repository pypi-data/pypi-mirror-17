`define LENGTH_RAM_STIMULI 13                 
`define PROF_RAM_STIMULI 8192
module a_stimuli_ram_ctrl(
                         rst_n,
                         clk_ref,
                         clk_user_i,
                         dv_i,
                         r_q_16data_i,
                         memoire_stimuli_i,
                         r_w_i,

                         r_data_o,
                         r_dv_o,
                         r_busy_i,
                         run_verif_i,
                         start_run_verif_i,
                         r_stimuli_verif_o,
      // ##### VERS LA MEMOIRE ###########
                         r_data_64_o,
                         r_write_mem_o,
                         r_rdaddr_o,
                         r_wraddr_o,
                         data_memo_stimuli_i
                         );

                           
input rst_n, clk_ref, dv_i, clk_user_i;
input[15:0] r_q_16data_i;
input memoire_stimuli_i, r_w_i;
input r_busy_i;
input run_verif_i;
input start_run_verif_i;
output[15:0] r_data_o;
output[63:0] r_stimuli_verif_o;
output r_dv_o;

input[63:0] data_memo_stimuli_i;
output[63:0] r_data_64_o;
output r_write_mem_o;
output[`LENGTH_RAM_STIMULI-1:0] r_wraddr_o, r_rdaddr_o;

wire rst_n, clk_ref, clk_user_i;
wire memoire_stimuli_i, r_w_i;
wire r_busy_i;
wire run_verif_i;
wire start_run_verif_i;
reg[15:0] r_data_o;
reg r_dv_o;
reg[63:0] r_stimuli_verif_o;

wire[63:0] data_memo_stimuli_i;
reg[63:0] r_data_64_o;
reg r_write_mem_o;
reg[`LENGTH_RAM_STIMULI-1:0] r_wraddr_o, r_rdaddr_o;
// #### DECLARATION SIGNAUX INTERNE #######
reg[1:0] r_cpt_val;
reg r_start_stimuli;
reg r_send_data;
reg r_wait;

wire[3:0] ecriture_sti, lecture_sti;
wire[1:0] run_verif_lecture;
wire standby;

assign ecriture_sti[0] = r_w_i && dv_i && !r_start_stimuli && memoire_stimuli_i && !run_verif_i;
assign ecriture_sti[1] = r_w_i && dv_i && r_start_stimuli && memoire_stimuli_i && !run_verif_i;
assign ecriture_sti[2] = r_write_mem_o && !run_verif_i;
assign ecriture_sti[3] = r_start_stimuli && !memoire_stimuli_i && !run_verif_i;

assign lecture_sti[0] = !r_w_i && dv_i && !r_start_stimuli && memoire_stimuli_i && !r_busy_i && !run_verif_i;
assign lecture_sti[1] = r_wait && !run_verif_i;
assign lecture_sti[2] = !r_w_i && r_start_stimuli && memoire_stimuli_i && !r_busy_i && !r_send_data && !run_verif_i;
assign lecture_sti[3] = !r_w_i && r_start_stimuli && memoire_stimuli_i && r_send_data && !run_verif_i;

assign run_verif_lecture[0] = start_run_verif_i && dv_i  && run_verif_i;
assign run_verif_lecture[1] = run_verif_i;

assign standby = r_start_stimuli && !memoire_stimuli_i && !run_verif_i;

always @(posedge clk_ref or negedge rst_n)
  if(!rst_n)
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= 'h0;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b0;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
//###### MODE ECRITURE ####################
  else if(ecriture_sti[0])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= r_q_16data_i[9:0];
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
  else if(ecriture_sti[1])
         begin
            case(r_cpt_val)
              2'b00 :  r_data_64_o <= {r_data_64_o[63:16],r_q_16data_i};
              2'b01 :  r_data_64_o <= {r_data_64_o[63:32],r_q_16data_i,r_data_64_o[15:0]};
              2'b10 :  r_data_64_o <= {r_data_64_o[63:48],r_q_16data_i,r_data_64_o[31:0]};
              2'b11 :  r_data_64_o <= {r_q_16data_i,r_data_64_o[47:0]};
            endcase
              r_wraddr_o <= r_wraddr_o;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= r_cpt_val + 1'b1;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= (r_cpt_val == 2'b11) ? 1'b1 : 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
   else if(ecriture_sti[2])
         begin
              r_data_64_o <= r_data_64_o;
              r_wraddr_o <= r_wraddr_o + 1'b1;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= r_cpt_val;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
   else if(ecriture_sti[3])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b0;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
// ###### MODE LECTURE ##################

   else if(lecture_sti[0])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_q_16data_i[9:0];
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b1;
         end
   else if(lecture_sti[1])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= (r_cpt_val == 2'b11) ? 2'b0 : (r_cpt_val + 1'b1);
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= (r_cpt_val == 2'b11) ? 1'b0 : 1'b1;
         end
   else if(lecture_sti[2])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= (r_cpt_val == 2'b11) ? (r_rdaddr_o + 1'b1) : r_rdaddr_o;
            case(r_cpt_val)
              2'b00 : r_data_o <= data_memo_stimuli_i[15:0];
              2'b01 : r_data_o <= data_memo_stimuli_i[31:16];
              2'b10 : r_data_o <= data_memo_stimuli_i[47:32];
              2'b11 : r_data_o <= data_memo_stimuli_i[63:48];
            endcase
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b1;
              r_cpt_val <= r_cpt_val + 1'b1;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b1;
              r_wait <= 1'b0;
         end
   else if(lecture_sti[3])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= r_data_o;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= r_cpt_val;
              r_start_stimuli <= 1'b1;
              r_write_mem_o <= 1'b0;
              r_send_data <= (r_busy_i) ? 1'b1 : 1'b0;
              r_wait <= 1'b0;
         end

// ###### MODE LECTURE EN MODE RUN ##################

   else if(run_verif_lecture[0])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_q_16data_i[9:0];
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b0;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
   else if(run_verif_lecture[1])
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= clk_user_i ? (r_rdaddr_o + 1'b1) : r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= data_memo_stimuli_i;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b0;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end


// #### PASSAGE EN MODE STANDBY
   else if(standby)
         begin
              r_data_64_o <= 64'h0;
              r_wraddr_o <= 'h0;
              r_rdaddr_o <= r_rdaddr_o;
              r_data_o <= 16'h0;
              r_stimuli_verif_o <= 64'h0;
              r_dv_o <= 1'b0;
              r_cpt_val <= 2'b0;
              r_start_stimuli <= 1'b0;
              r_write_mem_o <= 1'b0;
              r_send_data <= 1'b0;
              r_wait <= 1'b0;
         end
endmodule
