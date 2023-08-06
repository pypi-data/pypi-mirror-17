//Description : Le module "gen_clk_user" a pour fonction de stocker la valeur de l'horloge utilisateur ou plus exactement le taux de division de 
//				l'horloge de r�ference et de g�n�rer ainsi l'horloge ad�quat � ce taux qui sera par la suite connect� au DUT mais aussi � d'autres
//				modules (cf. code source des modules "gen_sti_opt_64vN" et "opti_trace_Nv64"). 



module a_gen_clk_user(
                    clk_ref,
                    rst_n,
                    r_clk_prog_i,
                    r_w_i,
                    r_q_16data_i,
                    r_dv_i,
                    r_mode_pas_a_pas_i,
                    r_start_run_verif_i,
                    run_verif_i,
                    
                    egal_clk_ref,
                    deux_clk_ref_o,
                    r_dv_clk_u_o,
                    r_variable_prog,
                    send_stim_o,
                    capt_trce_o,
                    doublefront_o,
                    cycle_run_verif_o,
                    clk_user_o
                   );

input clk_ref, rst_n;
input r_clk_prog_i;
input r_w_i;
input[15:0] r_q_16data_i;
input r_dv_i;
input r_mode_pas_a_pas_i;
input r_start_run_verif_i;
input run_verif_i;
output[15:0] r_variable_prog;
output r_dv_clk_u_o;
output capt_trce_o;
output cycle_run_verif_o;
output clk_user_o;
output egal_clk_ref;
output deux_clk_ref_o;
output send_stim_o;
output doublefront_o;

wire clk_user_o;
reg cycle_run_verif_int, capt_trce_int;
wire capt_trce_o;
wire cycle_run_verif_o;

reg[15:0] r_variable_prog;
reg       r_dv_clk_u_o;
reg       nw_demarer_clk;
reg[1:0]  nw_cptdecalage;
reg[11:0] nw_cpt_cycle;
reg       clk_user_int;
wire      cmd_depart;
wire      cmd_stop_clk_u;
wire      standby;
wire      egal_clk_ref;
wire      sup_prog_val_trois;
wire      analyse_inf_trois, analyse_sup_trois;
wire      detect_pair_impaire;
wire      send_stim_o;
wire 			cmd_gen_clk_u;
wire 			traitement_inf_trois;
wire 			chgmnt_front;


wire[11:0] debug_inf_trois, debug_sup_trois;
reg        r_pas_a_pas;

reg fall_edge_clk_u;
wire xor_both, and_rise, and_fall;
reg and_start_run_verif;
wire doublefront_o;

always @(posedge clk_ref or negedge rst_n)
    if(!rst_n)
          begin
             r_variable_prog <= 16'd0;
             r_dv_clk_u_o <= 1'b0;
          end
    else if(r_clk_prog_i && r_dv_i && r_w_i)
          begin
             r_variable_prog <= r_q_16data_i;
             r_dv_clk_u_o <= 1'b0;
          end
    else if(r_clk_prog_i && !r_w_i)
          begin
             r_variable_prog <= r_variable_prog;
             r_dv_clk_u_o <= 1'b1;
          end
    else
          begin
             r_variable_prog <= r_variable_prog;
             r_dv_clk_u_o <= 1'b0;
          end

// Generation Clk_user
//

assign debug_inf_trois = (r_variable_prog[13:2] + detect_pair_impaire);
assign debug_sup_trois = ((r_variable_prog[13:1] - 1'b1) + detect_pair_impaire);
assign standby         = (nw_demarer_clk & !run_verif_i) & !r_pas_a_pas & !r_mode_pas_a_pas_i;
assign cmd_depart      = r_start_run_verif_i & run_verif_i & (r_dv_i || nw_cptdecalage[0]);
assign cmd_gen_clk_u   = (nw_cptdecalage[1] & run_verif_i) || r_pas_a_pas;

assign sup_prog_val_trois   = |r_variable_prog[13:2];
assign traitement_inf_trois = (r_variable_prog[13:2] == nw_cpt_cycle) & !egal_clk_ref;
assign egal_clk_ref         = !sup_prog_val_trois & !r_variable_prog[1] & r_variable_prog[0];
assign deux_clk_ref_o       = !sup_prog_val_trois &  r_variable_prog[1] & !r_variable_prog[0];
assign detect_pair_impaire  = (r_variable_prog[0] & clk_user_int);
assign analyse_inf_trois    = ((r_variable_prog[13:2] + detect_pair_impaire) == nw_cpt_cycle) & !egal_clk_ref;
assign analyse_sup_trois    = (((r_variable_prog[13:1] - 1'b1) + detect_pair_impaire) == nw_cpt_cycle);
assign chgmnt_front         = sup_prog_val_trois ? analyse_sup_trois : (analyse_inf_trois || egal_clk_ref);
assign cmd_stop_clk_u       = nw_demarer_clk & !run_verif_i;

assign clk_user_o = (egal_clk_ref & cmd_gen_clk_u & and_start_run_verif) ? clk_ref : clk_user_int;
assign cycle_run_verif_o = egal_clk_ref ? cmd_gen_clk_u : cycle_run_verif_int;

always @(negedge clk_ref)
    begin 
              and_start_run_verif <= r_start_run_verif_i & run_verif_i;
    end

always @(posedge clk_ref or negedge rst_n)
    if(!rst_n)
          begin 
              clk_user_int         <= 1'b0;
              cycle_run_verif_int  <= 1'b0;

              nw_cptdecalage       <= 'b0;
              nw_cpt_cycle         <= 'b0;
              nw_demarer_clk       <= 1'b0;
              r_pas_a_pas          <= 1'b0;
          end
    else if(r_mode_pas_a_pas_i) 
          begin 
              clk_user_int         <= chgmnt_front ? !clk_user_int : clk_user_int;
              cycle_run_verif_int    <= chgmnt_front && !clk_user_int;

              nw_cptdecalage       <= 2'b0;
              nw_cpt_cycle         <= chgmnt_front ? 'b0 : nw_cpt_cycle + 1'b1;
              nw_demarer_clk       <= 1'b1;
              r_pas_a_pas          <= 1'b1;
          end
    else if(cmd_depart) 
          begin 
              clk_user_int         <= 1'b0;
              cycle_run_verif_int    <= 1'b0;
              
              nw_cptdecalage       <= {nw_cptdecalage[0], 1'b1};
              nw_cpt_cycle         <= 'b0;
              nw_demarer_clk       <= 1'b1;
              r_pas_a_pas          <= 1'b0;
          end
      else if(cmd_gen_clk_u)
          begin 
              clk_user_int         <= chgmnt_front ? !clk_user_int : clk_user_int;
              cycle_run_verif_int    <= chgmnt_front && !clk_user_int;

              nw_cptdecalage       <= 2'b10;
              nw_cpt_cycle         <= chgmnt_front ? 'b0 : nw_cpt_cycle + 1'b1;
              nw_demarer_clk       <= nw_demarer_clk;
              r_pas_a_pas          <= chgmnt_front ? 1'b0 : r_pas_a_pas;
          end
        else if(standby)
          begin 
              clk_user_int         <= 1'b0;
              cycle_run_verif_int    <= 1'b0;

              nw_cptdecalage       <= 'b0;
              nw_cpt_cycle         <= 'b0;
              nw_demarer_clk       <= 1'b0;
              r_pas_a_pas          <= 1'b0;
          end 

// Generation Front Capture
//                             ___            ___
//             o------------->|   |          |   \
//             |              | & |---> rise |00  |
//             |       o---->o|___|          |11  |
//             |       |       ___           |    |
// clk_user_o--o-------|--o---|XOR|          |    |------> capt_trace_o
//             |       o--|-->|___|---> both |10  |
//             |   _   |  |    ___           |    |
//             -->| |--o  o->o| & |          |    |
//   !clk_ref---->|>|  |      |   |---> fall |01  |
//                     o----->|___|          |___/
//                                             /\
//                                             ||
//                                             ||
//r_variable_prog[15:14] ======================O
// 

always @(posedge clk_ref)
          begin
              fall_edge_clk_u <= clk_user_o & !egal_clk_ref;
          end

assign and_fall = !clk_user_o &  fall_edge_clk_u;
assign and_rise =  clk_user_o & !fall_edge_clk_u;
assign xor_both =  clk_user_o ^  fall_edge_clk_u;
               
always @(r_variable_prog[15:14],and_rise,and_fall,xor_both)
 case(r_variable_prog[15:14])
   2'b00 : capt_trce_int <= and_rise;
   2'b01 : capt_trce_int <= and_fall;
   2'b10 : capt_trce_int <= xor_both;
   2'b11 : capt_trce_int <= and_rise;
 endcase
   
assign capt_trce_o = capt_trce_int || (and_start_run_verif & egal_clk_ref);
assign send_stim_o = and_rise      || (and_start_run_verif & egal_clk_ref);
assign doublefront_o = r_variable_prog[15] & !r_variable_prog[14];

endmodule
