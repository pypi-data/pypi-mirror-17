//`include "DEFINE_fp0.v"
`define LENGTH_RAM_STIMULI 10                
`define PROF_RAM_STIMULI (1024)

module a_fp0(
	clk_ref,
	rst_ext_i,
	clk_spi,
	cs_spi,
	di_spi,
	do_spi,
	led_o,
	//######## SIGNAUX A CONNECTER SUR DUT
	clk_user_o,
	idut_o,    // 96 Bits sur entree DUT
	odut_i     // 96 Bits sur sortie DUT 
	);

input clk_ref, rst_ext_i;

input clk_spi;
input cs_spi;
input di_spi;
output do_spi;

output[95:0] idut_o;
output[10:0] led_o;

output clk_user_o;
input[95:0] odut_i;

wire[31:0] data_rd_o;
wire[1:0] r_dv_trce_o;

wire dmx_sgnl_i;
wire[1:0] stop_verification_trce_o;
wire clk_spi, cs_spi, di_spi, do_spi;
wire clk_ref, rst_ext_i;
wire[3:0] r_fpga_o;
wire r_do;
wire[13:0] carte_o;
wire r_w_o;
wire memoire_stimuli_o;
wire[63:0] r_stimuli_verif_o;
wire capt_trce_o;
wire clk_user_o;
wire r_ctrl_trace_o;

wire r_erreur_timeout_o;
wire[10:0] led_o;
wire rst_n_o;
wire[95:0] idut_o;
wire[95:0] odut_i;

//#### SIGNAUX INTERNEs ############

wire[63:0] r_data_64_o;
wire r_write_mem_o;
wire[`LENGTH_RAM_STIMULI-1:0] r_rdaddr_o;
wire[`LENGTH_RAM_STIMULI-1:0] r_wraddr_o;
wire[63:0] data_memo_stimuli_o;
wire run_verif_o;
wire egal_clk_ref_o;

wire r_dv_o;
wire[15:0] r_q_16data_o;
wire[31:0] data_i_16data_o;
wire r_start_run_verif_o;
wire[1:0] data_valid_o;

wire[15:0] data_rd_trce_o, data_i_16stim_o;
wire dv_stim_o, dv_trace_o;
wire capt_trce_pipe;
wire clk_user_pipe;
wire deux_clk_ref_o;
wire r_busy_o;

assign led_o[9] = rst_n_o;
assign led_o[10] = clk_ref;

a_fpga_ctrl u_fpga_ctrl_0(
	.rst_n_o(rst_n_o),
	.clk_ref(clk_ref),
	.switch_rst_i(rst_ext_i),

	 .cs_spi(cs_spi),
	 .clk_spi(clk_spi),
	 .di_spi(di_spi),
	 .do_spi(do_spi),

	.carte_o(carte_o),
	.r_fpga_o(r_fpga_o),
	.r_w_o(r_w_o),
	///#### POUR LE TEST 
	.memoire_stimuli_o(memoire_stimuli_o),
	// ########## SIGNAL DE START VERIFICATION ##########
	.egal_clk_ref_o(egal_clk_ref_o),
	.deux_clk_ref_o(deux_clk_ref_o),
	.run_verif_o(run_verif_o),
	// ######  VERS CTRL STIMULI
	.r_dv_o(r_dv_o),
	.r_q_16data_o(r_q_16data_o),
	.data_i_16data_i(data_i_16stim_o),
	.data_valid_i(dv_stim_o),
	.r_start_run_verif_o(r_start_run_verif_o),
	// ######  VERS MEMOIRE STIMULI ############
	.data_memo_stimuli_i(data_memo_stimuli_o),
	.data_trace_i(data_rd_trce_o),
	.dv_trace_i(dv_trace_o),
	// ######  PATHERNs de Sortie ############
	.capt_trce_o(capt_trce_o),
	.clk_user(clk_user_o),
	.ctrl_trace_o(r_ctrl_trace_o),

	.r_busy_o(r_busy_o),
	.r_erreur_timeout_o(r_erreur_timeout_o),
	.led_o(led_o[8:0])
	);

// #####  STIMULI

a_rd_cross_x2_ram a_rd_x2_cross_ram_0(
                               .ctrl_i(carte_o[1]),
                               .data_i_0(data_i_16data_o[15:0]),
                               .data_i_1(data_i_16data_o[31:16]),

                               .dv_i_0(data_valid_o[0]),
                               .dv_i_1(data_valid_o[1]),

                               .data_o(data_i_16stim_o),
                               .dv_o(dv_stim_o)
                               );
                     
a_block_stimuli_ram u_a_block_stimuli_ram_0(
                                           .rst_n(rst_n_o),
                                           .clk_ref(clk_ref),
             // From Decodeur
                                           .dv_i(r_dv_o & carte_o[0]),                // A modifier quand nbr change
                                           .r_q_16data_i(r_q_16data_o),              
                                           .memoire_stimuli_i(memoire_stimuli_o),
                                           .r_w_i(r_w_o),
                                           .run_verif_i(run_verif_o),
                                           .r_start_run_verif_i(r_start_run_verif_o),
             // From Controleur 
                                           .r_busy_i(r_busy_o),
                                           .capt_stimuli_i(capt_trce_o),
                                           .egal_clk_ref_i(egal_clk_ref_o),
              
             // To Decodeur
                                           .dv_o(data_valid_o[0]),                    // A modifier quand nbr change
                                           .data_16_o(data_i_16data_o[15:0]),         // A modifier quand nbr change
             // To DUT in             
                                           .r_o(idut_o[47:0])                         // A modifier quand nbr change
                                           );

a_block_stimuli_ram u_a_block_stimuli_ram_1(
                                           .rst_n(rst_n_o),
                                           .clk_ref(clk_ref),
             // From Decodeur
                                           .dv_i(r_dv_o & carte_o[1]),                 // A modifier quand nbr change  
                                           .r_q_16data_i(r_q_16data_o),               
                                           .memoire_stimuli_i(memoire_stimuli_o),
                                           .r_w_i(r_w_o),
                                           .run_verif_i(run_verif_o),
                                           .r_start_run_verif_i(r_start_run_verif_o),
             // From Controleur 
                                           .r_busy_i(r_busy_o),
                                           .capt_stimuli_i(capt_trce_o),
                                           .egal_clk_ref_i(egal_clk_ref_o),
              
             // To Decodeur
                                           .dv_o(data_valid_o[1]),                       // A modifier quand nbr change
                                           .data_16_o(data_i_16data_o[31:16]),           // A modifier quand nbr change
             // To DUT in             
                                           .r_o(idut_o[95:48])                           // A modifier quand nbr change
                                           );



// ##### TRACE

a_pipe_capt_trce a_pipe_capt_trce_0(
                                   .clk_ref(clk_ref),
                                   .rst_n(rst_n_o),
                                   .nbr_pipe(4'h4),
                                   .clk_user_i(clk_user_o),
                                   .signal_i(capt_trce_o), 
                 
                                   .clk_user_pipe(clk_user_pipe),
                                   .signal_o(capt_trce_pipe)
                                   );

a_rd_cross_x2_ram a_rd_cross_x2_ram_1(
                               .ctrl_i(carte_o[1]),
                               .data_i_0(data_rd_o[15:0]),
                               .data_i_1(data_rd_o[31:16]),

                               .dv_i_0(r_dv_trce_o[0]),
                               .dv_i_1(r_dv_trce_o[1]),

                               .data_o(data_rd_trce_o),
                               .dv_o(dv_trace_o)
                               );

a_block_trace_ram a_block_trace_ram_0(
                                     .carte_i(carte_o[0]),                                   // A modifier quand nbr change
                                     .fpga_i(r_fpga_o),
                                     .id_i(4'b0),
                                     .clk_ref(clk_ref),
                                     .rst_n(rst_n_o),

                                     .fp1_data_i(r_q_16data_o),
                                     .fp1_dv_i(r_dv_o),

                                     .run_verif_i(run_verif_o),
                                     .capt_i(capt_trce_pipe),
                                     .read_enable_i(r_ctrl_trace_o),
                                     .stop_verification_trce_o(stop_verification_trce_o[0]), // A modifier quand nbr change
                                     .busi_i(r_busy_o),
                                     .data_rd_o(data_rd_o[15:0]),                            // A modifier quand nbr change
                                     .r_dv_trce_o(r_dv_trce_o[0]),                           // A modifier quand nbr change

                                     .clk_user_i(clk_user_pipe),
                                     .r_enable_trace_i(1'b1),
                                     .egal_un_i(egal_clk_ref_o),
                                     .deux_clk_ref_i(deux_clk_ref_o),

                                     .r_q_dut_i(odut_i[47:0])
                                     );

a_block_trace_ram a_block_trace_ram_1(
                                     .carte_i(carte_o[1]),                                   // A modifier quand nbr change
                                     .fpga_i(r_fpga_o),
                                     .id_i(4'b0),
                                     .clk_ref(clk_ref),
                                     .rst_n(rst_n_o),

                                     .fp1_data_i(r_q_16data_o),
                                     .fp1_dv_i(r_dv_o),

                                     .run_verif_i(run_verif_o),
                                     .capt_i(capt_trce_pipe),
                                     .read_enable_i(r_ctrl_trace_o),
                                     .stop_verification_trce_o(stop_verification_trce_o[1]), // A modifier quand nbr change
                                     .busi_i(r_busy_o),
                                     .data_rd_o(data_rd_o[31:16]),                           // A modifier quand nbr change
                                     .r_dv_trce_o(r_dv_trce_o[1]),                           // A modifier quand nbr change

                                     .clk_user_i(clk_user_pipe),
                                     .r_enable_trace_i(1'b1),
                                     .egal_un_i(egal_clk_ref_o),
                                     .deux_clk_ref_i(deux_clk_ref_o),

                                     .r_q_dut_i(odut_i[95:48])
                                     );

 
endmodule
