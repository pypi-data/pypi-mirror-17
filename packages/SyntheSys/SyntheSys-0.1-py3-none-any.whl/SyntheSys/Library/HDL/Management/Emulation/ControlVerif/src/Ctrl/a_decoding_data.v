//Description : Le module "decoding_data" a pour fonction de décoder toutes les instructions recues sur 16 bits et d'ainsi contrôler l'état des
//				signaux de contrôle associés à l'instruction et connectés au divers modules constituant le système d'accélération de verification. 




module a_decoding_data(
                    rst_n, 
//                    reset_soft_o,
                    clk_ref,
                    dv_i,
                    data_i,
                    
                    carte_o,
                    r_fpga_o,
                    r_w_o,
                    r_memoire_stimuli_o,
                    r_ctrl_trace_o,
                    r_run_verif_o,
                    r_start_run_verif_o,
                    r_clk_prog_o,
                    r_mode_pas_a_pas_o,
                    data_send_i,
                    r_stop,
                    r_attente_data_o
                    );

input rst_n, clk_ref;
input dv_i;
input[15:0] data_i;
input data_send_i;

output[13:0] carte_o;
output[3:0] r_fpga_o;
output r_w_o;
output r_memoire_stimuli_o;
output r_ctrl_trace_o;
output r_run_verif_o;
output r_start_run_verif_o;
output r_clk_prog_o;
output r_mode_pas_a_pas_o;
output r_attente_data_o;                    
output r_stop;
//output reset_soft_o;
// ###### DECLARATION DES SIGNAUX ENTREES ##############
//wire reset_soft_o;
wire rst_n, clk_ref;
wire dv_i;
wire[15:0] data_i;
wire data_send_i;
//wire reset_soft_int;
reg [13:0] carte_o;
wire[3:0] r_fpga_o;
reg r_w_o;
reg r_memoire_stimuli_o;
reg r_ctrl_trace_o;
reg r_run_verif_o;
reg r_start_run_verif_o;
reg r_clk_prog_o;
reg r_mode_pas_a_pas_o;
reg r_attente_data_o;
// ###### DECLARATION DES SIGNAUX INTERNEs ###############
reg[15:0] r_memo_first_word, r_memo_nbr_data, r_compteur_data;
reg r_cmd_memo;
reg r_stop;
reg r_start_cpt;

//wire[15:0] Test ;

// #######################################
// ##      DECODAGE DE LA COMMANDE      ##
// #######################################
// ##  data_i[3:0] = Selection Module   ##
// ##  data_i[4] = r_w                  ##
// ##  data_i[5] = Pathern Test         ##
// ##  data_i[6] = Clock_user           ##
// ##  data_i[7] = Run_proto            ##
// ##  data_i[8] = Start_verif          ##
// ##  data_i[9] = trace_o              ##
// ##  data_i[10] = trace_o             ##
// ##  data_i[14:11] = fpga_o           ##
// ##  data_i[15] = Stop_verif          ##
// ##                                   ##
// #######################################
// ##    DECODAGE DU MODULE CONCERNE    ##
// ##         6 pour le moment          ##
// ##               ET                  ##
// ##      GESTION DU Nbre de DATAs     ##
// #######################################

//assign Test = r_w_o || r_memo_first_word[4] ? 16'h0000 : 16'h0004;

// #### CAPTURE DU PREMIER MOT et CALCUL DU NBR DATAs PASSE #######
always @(posedge clk_ref or negedge rst_n)
  if(!rst_n)
       begin 
             r_compteur_data <= 16'b1;
             r_stop <= 1'b0;
             r_start_cpt <= 1'b0;
             r_memo_first_word <= 16'b0;
             r_memo_nbr_data <= 16'hffff;
             r_cmd_memo <= 1'b0;
             r_w_o <= 1'b0;
             r_memoire_stimuli_o <= 1'b0;
             r_run_verif_o <= 1'b0;
             r_start_run_verif_o <= 1'b0;
             r_ctrl_trace_o <= 1'b0;
             r_clk_prog_o <= 1'b0;
             r_mode_pas_a_pas_o <= 1'b0;
             r_attente_data_o <= 1'b0;
//             reset_soft_int   <= 1'b0;
       end
// ############### MEMORISATION DE LA DESTINATION ################
  else if(dv_i && !r_cmd_memo)
       begin 
             r_compteur_data <= 16'b1;
             r_stop <= 1'b0;
             r_start_cpt <= 1'b0;
             r_memo_first_word <= data_i;
             r_memo_nbr_data <= 16'hffff;
             r_cmd_memo <= 1'b1;
             r_w_o <= r_memo_first_word[4];
             r_memoire_stimuli_o <= 1'b0;
             r_run_verif_o <= 1'b0;
             r_start_run_verif_o <= 1'b0;
             r_ctrl_trace_o <= 1'b0;
             r_clk_prog_o <= 1'b0;
             r_mode_pas_a_pas_o <= 1'b0;
             r_attente_data_o <= r_memo_first_word[4] ? 1'b1 : 1'b0;
//             reset_soft_int   <= r_memo_first_word[15];
       end
// ############### MEMORISATION DU NBR DE DATA A ENVOYER OU A RECEVOIR
  else if(dv_i && r_cmd_memo && !r_start_cpt && !r_stop)
       begin 
             r_compteur_data <= 16'b1;
             r_stop <= 1'b0;
             r_start_cpt <= 1'b1;
             r_memo_first_word <= r_memo_first_word;
             r_memo_nbr_data <= data_i; // + Test;
             r_cmd_memo <= 1'b1;
             r_w_o <= r_memo_first_word[4];
//             r_memoire_stimuli_o <= r_memo_first_word[5] && carte_o[0];
             r_memoire_stimuli_o <= r_memo_first_word[5];
             r_run_verif_o <= r_memo_first_word[7];
             r_start_run_verif_o <= r_memo_first_word[8];
             r_ctrl_trace_o <= r_memo_first_word[9];
             r_clk_prog_o <= r_memo_first_word[6];
             r_mode_pas_a_pas_o <= r_memo_first_word[10];
             r_attente_data_o <= r_memo_first_word[4] ? 1'b1 : 1'b0;
//             reset_soft_int   <= r_memo_first_word[15];
       end
// ################ COMPTE LE NBR DE DATAs en ECRITURE ########## 
  else if(r_memo_first_word[4] && dv_i && r_cmd_memo && r_start_cpt && !r_stop)
       begin 
             r_compteur_data <= r_compteur_data + 1'b1;
             r_stop <= (r_compteur_data == r_memo_nbr_data) ? 1'b1 : 1'b0;
             r_start_cpt <= 1'b1;
             r_memo_first_word <= r_memo_first_word;
             r_memo_nbr_data <= r_memo_nbr_data;
             r_cmd_memo <= 1'b1;
             r_w_o <= r_memo_first_word[4];
//             r_memoire_stimuli_o <= r_memo_first_word[5] && carte_o[0];
             r_memoire_stimuli_o <= r_memo_first_word[5];
             r_run_verif_o <= r_memo_first_word[7];
             r_start_run_verif_o <= r_memo_first_word[8];
//             r_ctrl_trace_o <= r_memo_first_word[9] && carte_o[0];
             r_ctrl_trace_o <= r_memo_first_word[9];
             r_clk_prog_o <= r_memo_first_word[6];
             r_mode_pas_a_pas_o <= r_memo_first_word[10];
             r_attente_data_o <= 1'b1;
//             reset_soft_int   <= r_memo_first_word[15];
       end
// ##### COMPTE LE NBR DE DATA EN RE-LECTURE #################
  else if(!r_memo_first_word[4] && r_start_cpt && !r_stop && data_send_i)
       begin 
             r_compteur_data <= r_compteur_data + 1'b1;
             r_stop <= (r_compteur_data == (r_memo_nbr_data)) ? 1'b1 : 1'b0;
             r_start_cpt <= 1'b1;
             r_memo_first_word <= r_memo_first_word;
             r_memo_nbr_data <= r_memo_nbr_data;
             r_cmd_memo <= 1'b1;
             r_w_o <= r_memo_first_word[4];
//             r_memoire_stimuli_o <= r_memo_first_word[5] && carte_o[0];
             r_memoire_stimuli_o <= r_memo_first_word[5];
             r_run_verif_o <= r_memo_first_word[7];
             r_start_run_verif_o <= 1'b0;
//             r_ctrl_trace_o <= r_memo_first_word[9] && carte_o[0];
             r_ctrl_trace_o <= r_memo_first_word[9];
             r_clk_prog_o <= r_memo_first_word[6];
             r_mode_pas_a_pas_o <= 1'b0;
             r_attente_data_o <= 1'b0;
//             reset_soft_int   <= r_memo_first_word[15];
       end
// ####### MODE STANDBY ##########################
  else if(r_stop)
       begin 
             r_compteur_data <= 16'b1;
             r_stop <= 1'b0;
             r_start_cpt <= 1'b0;
             r_memo_first_word <= 16'b0;
             r_memo_nbr_data <= 16'hffff;
             r_cmd_memo <= 1'b0;
             r_w_o <= 1'b0;
             r_memoire_stimuli_o <= 1'b0;
             r_run_verif_o <= 1'b0;
             r_start_run_verif_o <= 1'b0;
             r_ctrl_trace_o <= 1'b0;
             r_clk_prog_o <= 1'b0;
             r_mode_pas_a_pas_o <= 1'b0;
             r_attente_data_o <= 1'b0;
//             reset_soft_int   <= 1'b0;
       end  
// ####### MODE TIMEOUT ##########################
  else 
       begin 
             r_compteur_data <= r_compteur_data;
             r_stop <= r_stop;
             r_start_cpt <= r_start_cpt;
             r_memo_first_word <= r_memo_first_word;
             r_memo_nbr_data <= r_memo_nbr_data;
             r_cmd_memo <= r_cmd_memo;
             r_w_o <= r_w_o;
             r_memoire_stimuli_o <= r_memoire_stimuli_o;
             r_run_verif_o <= r_run_verif_o;
             r_start_run_verif_o <= r_start_run_verif_o;
             r_ctrl_trace_o <= r_ctrl_trace_o;
             r_clk_prog_o <= r_clk_prog_o;
             r_mode_pas_a_pas_o <= r_mode_pas_a_pas_o;
             r_attente_data_o <= 1'b0;
//             reset_soft_int   <= reset_soft_int        ;
       end  

  
// ##### PARTIE DECODAGE ######
// ##### POSSIBILITEE DE CONTROLER 14 Cartes #######
always @(r_memo_first_word[3:0])
    case(r_memo_first_word[3:0])
            4'h0  : begin carte_o <= 14'b00_0000_0000_0000; end
            4'h1  : begin carte_o <= 14'b00_0000_0000_0001; end
            4'h2  : begin carte_o <= 14'b00_0000_0000_0010; end
            4'h3  : begin carte_o <= 14'b00_0000_0000_0100; end
            4'h4  : begin carte_o <= 14'b00_0000_0000_1000; end
            4'h5  : begin carte_o <= 14'b00_0000_0001_0000; end
            4'h6  : begin carte_o <= 14'b00_0000_0010_0000; end
            4'h7  : begin carte_o <= 14'b00_0000_0100_0000; end
            4'h8  : begin carte_o <= 14'b00_0000_1000_0000; end
            4'h9  : begin carte_o <= 14'b00_0001_0000_0000; end
            4'ha  : begin carte_o <= 14'b00_0010_0000_0000; end
            4'hb  : begin carte_o <= 14'b00_0100_0000_0000; end
            4'hc  : begin carte_o <= 14'b00_1000_0000_0000; end
            4'hd  : begin carte_o <= 14'b01_0000_0000_0000; end
            4'he  : begin carte_o <= 14'b10_0000_0000_0000; end
            4'hf  : begin carte_o <= 14'b11_1111_1111_1111; end
    endcase

assign r_fpga_o = r_memo_first_word[14:11];

//assign r_w_o = r_memo_first_word[4];
//assign memoire_stimuli_o = r_memo_first_word[5] && carte_o[0];
//assign reset_soft_o = reset_soft_int ;
endmodule

