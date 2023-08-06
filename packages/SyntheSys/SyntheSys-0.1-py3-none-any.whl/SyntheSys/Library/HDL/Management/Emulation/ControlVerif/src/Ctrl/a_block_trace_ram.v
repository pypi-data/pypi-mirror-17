`define LENGTH_RAM_TRACE 13                 
`define PROF_RAM_TRACE 8192
`define FULL_RAM_TRACE 13'b1_1111_1111_0111  // Max -10

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
//            |a_trace_ram  |===64=========>|                      |                 |                   |
//            |             |din            |                      |                 |                   |
//            |             |<==64==========|                      |                 |a_opti_trace_48v64 | 
//            |  PARAM2     |wen            |a_trace_ram_ctrl      |r_stimuli_verif_o|                   |
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

module a_block_trace_ram(
                        carte_i,
                        fpga_i,
                        id_i,
                        clk_ref,
                        rst_n,
                        fp1_data_i,
                        fp1_dv_i,
                        run_verif_i,
                        capt_i,
                        read_enable_i,
                        stop_verification_trce_o,
                        busi_i,
                        data_rd_o,
                        r_dv_trce_o,
                        clk_user_i,
                        r_enable_trace_i,
                        egal_un_i,
                        deux_clk_ref_i,

                        r_q_dut_i
                        );

input carte_i;
input[3:0] fpga_i, id_i;
input[15:0] fp1_data_i;
input fp1_dv_i;
input run_verif_i;
input clk_ref, rst_n, capt_i, read_enable_i, busi_i;
input clk_user_i;
input r_enable_trace_i;
output[15:0] data_rd_o;
output r_dv_trce_o;
output stop_verification_trce_o;
input[47:0] r_q_dut_i;
input egal_un_i, deux_clk_ref_i;

wire carte_i;
wire[3:0] fpga_i;
wire[15:0] fp1_data_i;
wire fp1_dv_i;
wire run_verif_i;
wire clk_ref, rst_n, capt_i, read_enable_i, busi_i;
wire clk_user_i;
wire r_enable_trace_i;
wire[15:0] data_rd_o;
wire r_dv_trce_o;
wire stop_verification_trce_o;
//#----- DECLARATION SIGNAUX INTERNES ----
//#- Signaux memoire <--> ctrl -
wire[63:0] data_o;
wire wen_o;
wire[`LENGTH_RAM_TRACE-1:0] rdaddr_o, wraddr_o;
wire[63:0] data_read_i;
//#- Signaux Optimisation <--> ctrl -
wire r_comp_capt_o;
wire[63:0] r_data_o;
//#- Signaux de cmd pour stimu -
//#- Signaux entree du mux -
wire[239:0] r_o;
wire[47:0] r_q_dut_i;
wire[3:0] id_i;
wire soft_init;
wire egal_un_i;
reg[63:0] pipe_data_o;

a_trace_ctrl u_ctrl_trace(
                         .carte_i(carte_i),
                         .fpga_i(fpga_i),
                         .id_i(id_i),
                         .clk_ref(clk_ref),
                         .rst(rst_n),
                         .fp1_data_i(fp1_data_i),
                         .fp1_dv_i(fp1_dv_i),
                         .capt_i(r_comp_capt_o),
                         .ctrl_trce_i(read_enable_i),
                         .busi_i(busi_i),
                         .clk_user_i(clk_user_i),
                         .r_enable_trace_i(r_enable_trace_i),
                         .egal_un_i(egal_un_i),
                         .stop_verification_trce_o(stop_verification_trce_o),
                         .data_rd_o(data_rd_o),
                         .r_dv_trce_o(r_dv_trce_o),
                         .data_dut_i(r_data_o),
                         .soft_init(soft_init),
                         .data_o(data_o),
                         .wen_o(wen_o),
                         .rdaddr_o(rdaddr_o),
                         .wraddr_o(wraddr_o),
                         .data_read_i(data_read_i)
                         );

always @(posedge clk_ref)
  begin 
      pipe_data_o <= data_o;
  end

a_trace_ram u_trace_ram(
                       .din(data_o),
                       .wen(wen_o),
                       .rdaddr(rdaddr_o),
                       .wraddr(wraddr_o),
                       .clk(clk_ref),
                       .oclk(clk_ref),
                       .dout(data_read_i)
                       );

a_opti_trace_48v64 u_a_opti_trace_48v64(
                                   .rst_n(rst_n && !soft_init),
                                   .clk_ref(clk_ref),
                                   .run_verif_i(run_verif_i),
                                   .egal_un_i(egal_un_i),
                                   .deux_clk_ref_i(deux_clk_ref_i),
                                   .capt_i(capt_i),
                                   .data_user_i(r_q_dut_i),
                                   .r_comp_capt_o(r_comp_capt_o),
                                   .r_data_o(r_data_o)
                                   );
endmodule
