module a_optimisation_stim (
                           rst_n,
                           clk_ref,
                           clk_user_i,
                           run_verif_i,
                           data_valid_i,
                           val_cpt_i,

                           r_en_stimuli_o
                           );

input rst_n, clk_ref, clk_user_i;
input data_valid_i;
input[15:0] val_cpt_i;
input run_verif_i;

output r_en_stimuli_o;

wire rst_n, clk_ref, clk_user_i;
wire data_valid_i;
wire[15:0] val_cpt_i;
wire run_verif_i;
reg r_en_stimuli_o;

//###################### DECLARATION SIGNAUX INTERNE ################
reg[14:0] r_memo_data;
reg[14:0] r_cpt_cycle;

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
            begin 
                r_en_stimuli_o <= 1'b0;
                r_memo_data <= 15'b0;
                r_cpt_cycle <= 15'b0;
            end
     else if((val_cpt_i[0] && data_valid_i) && !r_en_stimuli_o)
            begin 
                r_en_stimuli_o <= 1'b1;
                r_memo_data <= val_cpt_i[15:1];
                r_cpt_cycle <= r_cpt_cycle + 1'b1;
            end
       else if(r_en_stimuli_o && run_verif_i)
            begin 
                r_en_stimuli_o <= (r_memo_data == r_cpt_cycle)  ? 1'b0 : 1'b1;
                r_memo_data <= r_memo_data;
                r_cpt_cycle <= clk_user_i ? r_cpt_cycle + 1'b1 : r_cpt_cycle;
            end
         else
            begin 
                r_en_stimuli_o <= 1'b0;
                r_memo_data <= 15'b0;
                r_cpt_cycle <= 15'b0;
            end

endmodule
