`define LENGTH_RAM_STIMULI 13                 
`define PROF_RAM_STIMULI 8192
//capt_stimuli_i--------------------------------------------------------------------------
//                                                                                       |
//r_busy_i -------------------------------------------------------                       |
//                                                               |                       |
//data_16_o <==========16======================================  |                       |
//dv_o <----------------------------------------------------- "  |                       |
//                                                          | "  |                       |
//                                                          | "  |                       |
//r_w_i --------------------------------------------------  | "  |                       |
//memoire_stimuli_i------------------------------------  |  | "  |                       |
//r_q_16data_i======16==============================  |  |  | "  |                       |
//dv_i-------------------------------------------  "  |  |  | "  |                       |
//                                              |  "  |  |  | "  |                       |
//             _____________                 ___v__V__V__V__|_"__V_                   ___V_______________
//            |             |dout           | dv_i                 |                 |                   |
//            |a_stimuli_ram|===64=========>|                      |                 |                   |
//            |             |din            |                      |                 |a_gen_sti_opt_64v48|
//            |             |<==64==========|                      |                 |                   |
//            |  PARAM2     |wen            |a_stimuli_ram_ctrl    |r_stimuli_verif_o|                   |
//            |             |<--------------|                      |==64============>|                   |
//            |             |rdaddr         |                      |                 |                   |
//            |             |<==PARAM1======|                      |                 |                   |
//        --->|clk          |wraddr         |                      |                 |                   |
//        o-->|clk_o        |<==PARAM1======|                      |                 |                   |
//        |   |             |    ---------->|rst_n                 |                 |                   |
//        |   |_____________|    | -------->|clk_ref               |                 |                   |
//        |                      | |        |                      |                 |                   |
//        |                      | |        |            clk_user_i|<--dmx_sgnl_o----|r_incr_o           |
//        |                      | |        |______________________|                 |                   |
//        |                      | |           ^  ^                                  |                   |
//rst_n---|----------------------o-|-----------|--|--------------------------------->|                   |      
//        |                        |           |  |                                  |                   |
//clk_ref-o------------------------o-----------|--|--------------------------------->|                   | 
//                                             |  |                                  |                   |
//run_verif_i----------------------------------o--|--------------------------------->|                   |
//r_start_run_verif_i------------------------------                                  |___________________|
//
//
//PARAM1 = LENGTH_RAM_STIMULI                 
//PARAM2 = PROF_RAM_STIMULI

module a_block_stimuli_ram(
                          rst_n,
                          clk_ref,
             // From Decodeur
                          dv_i,
                          r_q_16data_i,
                          memoire_stimuli_i,
                          r_w_i,
                          run_verif_i,
                          r_start_run_verif_i,
             // From Controleur 
                          r_busy_i,
                          capt_stimuli_i,
                          egal_clk_ref_i,
              
             // To Decodeur
                          dv_o,
                          data_16_o,
             // To DUT in             
                          r_o
                          );

input rst_n, clk_ref, dv_i;
input[15:0] r_q_16data_i;
input memoire_stimuli_i;
input r_w_i;
input r_busy_i;
input run_verif_i;
input r_start_run_verif_i;
input capt_stimuli_i;
input egal_clk_ref_i;

output dv_o;
output[15:0] data_16_o;
output[47:0] r_o;


wire rst_n, clk_ref, dv_i;
wire[15:0] r_q_16data_i;
wire memoire_stimuli_i;
wire r_w_i;
wire r_busy_i;
wire run_verif_i;
wire r_start_run_verif_i;
wire egal_clk_ref_i;

wire dv_o;
wire[15:0] data_16_o;
wire [47:0] r_o;

// ##### Signaux Interne
wire dmx_sgnl_o;
wire[63:0] r_data_64_o, data_memo_stimuli_o;
wire r_write_mem_o;
wire[`LENGTH_RAM_STIMULI-1:0] r_rdaddr_o, r_wraddr_o;
wire[63:0] r_stimuli_verif_o;

a_stimuli_ram_ctrl u_Gestion_Pathern_Test_0(
                                           .rst_n(rst_n), 
                                           .clk_ref(clk_ref),
                                           .clk_user_i(dmx_sgnl_o),
                              // #### FROM DECODEUR
                                           .dv_i(dv_i),
                                           .r_q_16data_i(r_q_16data_i),
                                           .memoire_stimuli_i(memoire_stimuli_i),
                                           .r_w_i(r_w_i),
                              // #### TO DECODEUR
                                           .r_data_o(data_16_o),
                                           .r_dv_o(dv_o),

                                           .r_busy_i(r_busy_i),
                                           .run_verif_i(run_verif_i),
                                           .start_run_verif_i(r_start_run_verif_i),
                                           .r_stimuli_verif_o(r_stimuli_verif_o),
                           // ##### VERS LA MEMOIRE ###########
                                           .r_data_64_o(r_data_64_o),
                                           .r_write_mem_o(r_write_mem_o),
                                           .r_rdaddr_o(r_rdaddr_o),
                                           .r_wraddr_o(r_wraddr_o),
                                           .data_memo_stimuli_i(data_memo_stimuli_o)
                                           );

a_stimuli_ram u_stimuli_ram(
                           .din(r_data_64_o), 
                           .wen(r_write_mem_o), 
                           .rdaddr(r_rdaddr_o), 
                           .wraddr(r_wraddr_o), 
                           .clk(clk_ref), 
                           .oclk(clk_ref), 
                           .dout(data_memo_stimuli_o)
                           );

a_gen_sti_opt_64v48 u_a_gen_sti_opt_64v48(
                           .rst_n(rst_n),
                           .clk_ref(clk_ref),
                           .run_i(capt_stimuli_i),
                           .run_verif_i(run_verif_i),
                           .egal_clk_ref_i(egal_clk_ref_i),
                           .start_verif_i(r_start_run_verif_i),
                           .stimu_i(r_stimuli_verif_o),
                           .r_incr_o(dmx_sgnl_o),
                           .r_in_dut_o(r_o)
                           );

 
endmodule
