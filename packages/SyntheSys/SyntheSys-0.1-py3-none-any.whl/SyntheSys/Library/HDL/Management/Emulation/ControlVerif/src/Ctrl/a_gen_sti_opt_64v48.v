`define LENGTH_RAM_STIMULI 13                 
`define PROF_RAM_STIMULI 8192
module a_gen_sti_opt_64v48(
                           rst_n, 
                           clk_ref, 
                           run_i,
                           run_verif_i,
                           stimu_i,
                           egal_clk_ref_i,
                           start_verif_i,
                           r_incr_o,
                           r_in_dut_o
                           );

input rst_n, clk_ref, run_i, run_verif_i;
input[63:0] stimu_i;
input egal_clk_ref_i;
input start_verif_i;
output r_incr_o;
output[47:0] r_in_dut_o;

wire rst_n, clk_ref, run_i, run_verif_i;
wire[63:0] stimu_i;
wire egal_clk_ref_i;
wire[47:0] r_in_dut_o;
wire start_verif_i;
wire  r_incr_o;

//########## Declaration signaux Interne ##############
wire r_en_stimuli_o;
wire r_dv_o;
wire[63:0]  r_o;

assign r_in_dut_o = r_o[63:16];

a_dmx_stim_64x64 u_dmx_64x64(
                            .rst_n(rst_n),
                            .clk_ref(clk_ref),
                            .run_i(run_i),
                            .stimu_i(stimu_i),
                            .start_verif_i(start_verif_i & run_verif_i),
                            .egal_clk_ref_i(egal_clk_ref_i),
//### Signaux Optimisation
                            .stop_i(r_en_stimuli_o),
                            .r_dv_o(r_dv_o),

//### Signaux Out vers DUT et Ctrl_Stimu
                            .r_incr_o(r_incr_o),
                            .r_o(r_o)
                            );

a_optimisation_stim u_opt_stim(
                              .rst_n(rst_n),
                              .clk_ref(clk_ref),
                              .clk_user_i(run_i),
                              .run_verif_i(run_verif_i),
                            
                              .data_valid_i(r_dv_o),
                              .val_cpt_i(r_o[15:0]),

                              .r_en_stimuli_o(r_en_stimuli_o)
                              );

endmodule
