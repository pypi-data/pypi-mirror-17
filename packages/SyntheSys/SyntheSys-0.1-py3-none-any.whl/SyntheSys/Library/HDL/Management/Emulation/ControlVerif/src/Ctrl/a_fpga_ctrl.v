//Description : Le module "fpga_ctrl" instancie divers modules dont : le module "RS232" correspondant à l'interface avec la liason série, le module 
//				"cross_read" qui se charge de piloter le module "RS232" pour l'envoie de données via ce dernier, le module "rst_block" qui se charge
//				d'effectuer une remise à zéro de tous les modules incluant ceux externes à "fpga_ctrl", le module "gen_clk_user" se charge de générer
//				une horloge "utilisateur" qui sera connectée au DUT dont nous cherchons à effectuer la verification, le module "set_verification" a pour 
//				fonction de configurer le système en mode verification via un ensemble de signaux de contrôle, le module "decoding_data" a pour rôle 
//				de décoder toutes les instructions du système, enfin le module "timeout" a pour fonction d'alerter l'utilisateur que l'instruction spécifique
//				à l'écriture du nombre de données n'a pas été respectée. Pour plus d'information sur ces modules se référer à leur description.


//################### FPGA DE CONTROLE ############

module a_fpga_ctrl(
                rst_n_o,
                clk_ref,
                switch_rst_i,
					 
					 clk_spi,
					 cs_spi,
					 di_spi,
					 do_spi,
                 
                carte_o,
                r_fpga_o,
                r_w_o,
///#### POUR LE TEST 
                memoire_stimuli_o,
// ########## SIGNAL DE START VERIFICATION ##########
                egal_clk_ref_o,
                deux_clk_ref_o,
                run_verif_o,
// ######  VERS CTRL STIMULI
                r_dv_o,
                r_q_16data_o,
                data_i_16data_i,
                data_valid_i,
                r_start_run_verif_o,
// ######  VERS MEMOIRE STIMULI ############
                data_memo_stimuli_i,
                data_trace_i,
                dv_trace_i,
// ######  PATHERNs de Sortie ############
                send_stim_o,
                capt_trce_o,
                doublefront_o,
                clk_user,
// ####### CTRL DE TRACE #################      
       
                ctrl_trace_o,
                r_busy_o,
                
                r_erreur_timeout_o,
                led_o
               
                );

output r_dv_o;
output[15:0] r_q_16data_o;
input[15:0] data_i_16data_i;
input data_valid_i;
input switch_rst_i;
output r_start_run_verif_o;
//input rst_n;
input clk_ref;
output rst_n_o;
input clk_spi;
input cs_spi;
input di_spi;
output do_spi;
output[13:0] carte_o;
output[3:0] r_fpga_o;
output r_w_o;
output memoire_stimuli_o;
output egal_clk_ref_o;
output deux_clk_ref_o;
output doublefront_o;

input[63:0] data_memo_stimuli_i;
input[15:0] data_trace_i;
input dv_trace_i;
//output[63:0] r_data_64_o;
//output r_write_mem_o;
//output[9:0] r_rdaddr_o;
//output[9:0] r_wraddr_o;
output run_verif_o;
//output[63:0] r_stimuli_verif_o;
output capt_trce_o;
output clk_user;
output ctrl_trace_o;
output r_busy_o;
output r_erreur_timeout_o;
output[8:0] led_o;
output send_stim_o;
// #### DECLARATION SIGNAUX #####

//wire rst_n;
wire clk_ref;
wire clk_spi, cs_spi, di_spi, do_spi;
wire rst_n_o;
wire[13:0] carte_o;
wire[3:0] r_fpga_o;
wire r_w_o, memoire_stimuli_o;
wire egal_clk_ref_o, deux_clk_ref_o;

wire[63:0] data_memo_stimuli_i;
wire[15:0] data_trace_i;
wire dv_trace_i;
//wire[63:0] r_data_64_o;
//wire r_write_mem_o;
//wire[9:0] r_wraddr_o, r_rdaddr_o;
wire r_run_verif_o;
//wire[63:0] r_stimuli_verif_o;
wire r_mode_pas_a_pas_o;
wire clk_user;
wire capt_trce_o;
wire switch_rst_i;
//##### SIGNAUX INTERNE #######
wire r_dv_o;
wire[15:0] r_q_16data_o;
wire[15:0] data_i_16data_i;
wire data_valid_i;
wire r_busy_o;
wire r_start_run_verif_o;
wire run_verif_o;
wire[15:0] data_station_o;
wire data_v_station_o;
wire ctrl_trace_o;
reg cptdecalage;

wire[8:0] led_o;
wire r_erreur_timeout_o;
wire r_stop_o;
wire r_attente_data_o;
wire r_dv_clk_u_o;
wire r_clk_prog_o;
wire[15:0] r_data_nbr_cyc_o;
wire r_dv_nbr_cyc_o;
wire[15:0] r_variable_prog;
wire cycle_run_verif_o;

wire r_dv_clk_u_o_old,
     capt_trce_o_old,
     cycle_run_verif_o_old,
     clk_user_old;
wire[15:0] r_variable_prog_old;
wire LedRead;
wire send_stim_o;
wire doublefront_o;
reg[15:0] pipedata;
reg[3:0] pipedv;
wire nc;

// #### BLOCK COMMUNICATION AVEC STATION ##############
a_cross_read u_cross_read(
                       .memoire_stimuli_i(memoire_stimuli_o),
                       .data_i_16data_i(data_i_16data_i),
                       .data_valid_i(data_valid_i),
                
                       .ctrl_trace_i(ctrl_trace_o),
                       .data_trace_i(data_trace_i),
                       .dv_trace_i(dv_trace_i),

                       .ctrl_clk_user_i(r_clk_prog_o),
                       .data_clk_user_i(r_variable_prog),
                       .dv_clk_user_i(r_dv_clk_u_o),
                 
                       .ctrl_nbr_cycle_i(r_run_verif_o),
                       .data_nbr_cycle_i(r_data_nbr_cyc_o),
                       .dv_nbr_cycle_i(r_dv_nbr_cyc_o),

                       .data_station_o(data_station_o),
                       .data_v_station_o(data_v_station_o)
                       );
                       
a_rst_block u_rst_block (
                      .clk_ref(clk_ref),
                      .rst_n_i(switch_rst_i),

                      .init_rst_n_o(rst_n_o)
                      );

always @(posedge clk_ref or negedge rst_n_o)
if(!rst_n_o)
begin 
        pipedata <= 'b0;
        pipedv   <= 'b0;
end
else if(r_dv_o)
begin 
        pipedata <= 16'h0002;
        pipedv   <= {pipedv[2:0],1'b1};
end
else if(pipedv[3])
begin 
        pipedata <= r_q_16data_o;
        pipedv   <= 'b0;
end
else if(pipedv[0])
begin 
        pipedata <= r_q_16data_o;
        pipedv   <= {pipedv[2:0],1'b1};
end

assign nc = r_dv_o & (&data_v_station_o);

a_Spi_Oli u_a_Spi (
							.resetn(rst_n_o),
                                                        .resetmem(memoire_stimuli_o),
							.ClkRef(clk_ref), 
							.ClkEnCom(1'b1), 
							
							.cs_spi(cs_spi),
							.clk_spi(clk_spi),
							.di_spi(di_spi),
							.do_spi(do_spi),
							
							.r_dv_o(r_dv_o),
							.r_q(r_q_16data_o),
							
							.Data_i(data_station_o),
							.Dv_i(data_v_station_o),
//	    						.Data_i(pipedata),
//							.Dv_i(pipedv[0]),
							.r_busy_o(r_busy_o),

                                                        .LedRead(LedRead),
							
							.NcWire(led_o[0])
							);

a_gen_clk_user u_gen_clk_user(
                            .clk_ref(clk_ref),
                            .rst_n(rst_n_o),
                            .r_clk_prog_i(r_clk_prog_o),
                            .r_w_i(r_w_o),
                            .r_q_16data_i(r_q_16data_o),
                            .r_dv_i(r_dv_o),
                            .r_mode_pas_a_pas_i(r_mode_pas_a_pas_o),
                            .r_start_run_verif_i(r_start_run_verif_o),
                            .run_verif_i(run_verif_o),
                           
                            .egal_clk_ref(egal_clk_ref_o),
                            .deux_clk_ref_o(deux_clk_ref_o),
                            .r_dv_clk_u_o(r_dv_clk_u_o),
                            .r_variable_prog(r_variable_prog),
                            .send_stim_o(send_stim_o),
                            .capt_trce_o(capt_trce_o),
                            .doublefront_o(doublefront_o),
                            .cycle_run_verif_o(cycle_run_verif_o),
                            .clk_user_o(clk_user)
                            );

// ###### DECODAGE DES DONNEES ###################

assign led_o[2] = memoire_stimuli_o;
assign led_o[3] = r_clk_prog_o;
assign led_o[4] = r_run_verif_o;
assign led_o[5] = run_verif_o;
assign led_o[6] = r_start_run_verif_o;
assign led_o[7] = ctrl_trace_o;
assign led_o[8] = r_mode_pas_a_pas_o & nc;


a_decoding_data u_decoding_data_0(
                               .rst_n(rst_n_o), 
                               .clk_ref(clk_ref),
                               .dv_i(r_dv_o),
                               .data_i(r_q_16data_o),
                    
                               .carte_o(carte_o),
                               .r_fpga_o(r_fpga_o),
                               .r_w_o(r_w_o),
                               .r_memoire_stimuli_o(memoire_stimuli_o),
                               .r_ctrl_trace_o(ctrl_trace_o),
                               .r_run_verif_o(r_run_verif_o),
                               .r_start_run_verif_o(r_start_run_verif_o),
                               .r_clk_prog_o(r_clk_prog_o),
                               .r_mode_pas_a_pas_o(r_mode_pas_a_pas_o),
                               .data_send_i(data_v_station_o),
                               .r_stop(r_stop_o),
                               .r_attente_data_o(r_attente_data_o)
                               );

// ########################### TIMEOUT #####################
// 
a_timeout u_timeout(
                 .clk_ref(clk_ref),
                 .rst_n(rst_n_o),
                 .start_i(r_attente_data_o),
                 .stop_i(r_stop_o),
                 .r_erreur_timeout_o(r_erreur_timeout_o)
                 );

// ########################### RUN_VERIFICATION #####################
a_set_verification u_set_verif_0(
                              .rst_n(rst_n_o),
                              .clk_ref(clk_ref),
                              .clk_user(cycle_run_verif_o),
                              .r_w_i(r_w_o),
                              .busy_i(r_busy_o),
                              .select_module_i(r_run_verif_o),
                              .dv_i(r_dv_o),
                              .data_i(r_q_16data_o),

                              .egal_clk_ref_i(egal_clk_ref_o),
                              .deux_clk_ref_i(deux_clk_ref_o),
                    
                              .r_data_nbr_cyc_o(r_data_nbr_cyc_o),
                              .r_dv_nbr_cyc_o(r_dv_nbr_cyc_o),
                              .run_verif_o(run_verif_o)
                              );


endmodule
