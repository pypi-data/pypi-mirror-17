`define LENGTH_RAM_TRACE 13                 
`define PROF_RAM_TRACE 8192
`define FULL_RAM_TRACE 13'b1_1111_1111_0111  // Max -10

module a_trace_ctrl(
//###### Identifiant #######
                   carte_i,
                   fpga_i,
                   id_i,
//### Signaux Commande
                   clk_ref,
                   rst,
                   fp1_data_i,
                   fp1_dv_i,
                   capt_i,
                   ctrl_trce_i,
                   busi_i,
                   clk_user_i,
                   r_enable_trace_i,
                   egal_un_i,

                   stop_verification_trce_o, // RAM FULL
//##### Re-Lecture #############
                   data_rd_o,
                   r_dv_trce_o,
//##### Signaux a tracer du DUT #################
                   data_dut_i,


//##### SIGNAUX RELIANT LA MEMOIRE #######
                   soft_init,
                   data_o,
                   wen_o,
                   rdaddr_o,
                   wraddr_o,
                   data_read_i
                   );
                 
input[3:0] id_i;
input carte_i;
input[3:0] fpga_i;
input[15:0] fp1_data_i;
input fp1_dv_i;
input clk_user_i;
input r_enable_trace_i;
input clk_ref, rst, capt_i, ctrl_trce_i, busi_i;                 
input[63:0] data_dut_i, data_read_i;
input egal_un_i;

output wen_o;
output[63:0] data_o;
output[`LENGTH_RAM_TRACE-1:0] rdaddr_o, wraddr_o;
output[15:0] data_rd_o;
output r_dv_trce_o;
output stop_verification_trce_o;
output soft_init;

wire[3:0] id_i;
wire carte_i;
wire[3:0] fpga_i;
wire[15:0] fp1_data_i;
wire fp1_dv_i;
wire clk_user_i;
wire egal_un_i;

wire clk_ref, rst, capt_i, busi_i;                 
wire[63:0] data_dut_i, data_read_i;
wire stop_verification_trce_o;

reg wen_o;
reg[63:0] data_o;
reg[`LENGTH_RAM_TRACE-1:0] rdaddr_o, wraddr_o;
reg[15:0] data_rd_o;
reg r_dv_trce_o;

//##### DECLARATION DES SIGNAUX INTERNE #########
reg[2:0] r_step_wv;
reg[2:0] r_step_rd;
reg r_standby;
wire enable;

wire detect_data;

wire w_addr, r_addr;
wire write_test_data;
wire read_enable;
wire init;

wire soft_init, charge_adr_w, charge_adr_r;
wire[2:0] charge_test_data;
wire[1:0] ecriture;
wire[6:0] relecture;
reg[1:0] r_capt;
wire egaladdr;

assign stop_verification_trce_o = (wraddr_o >= `FULL_RAM_TRACE) ? 1'b1 : 1'b0;
assign egaladdr = (wraddr_o == rdaddr_o) ? 1'b1 : 1'b0;

always @(posedge clk_ref)
  begin 
      r_capt[0] <= capt_i;
      r_capt[1] <= r_capt[0];
  end
      
a_logic_trace_ctrl u_logic_trace_ctrl(
                                     .carte_i(carte_i),
                                     .fpga_i(fpga_i),
                                     .id_i(id_i),
                                     .clk_ref(clk_ref),
                                     .rst(rst),
                                     .fp1_data_i(fp1_data_i),
                                     .fp1_dv_i(fp1_dv_i),
                                     .ctrl_trce_i(ctrl_trce_i),
                                     .clk_user_i(clk_user_i),
                                     .enable_o(enable),
                                     .detect_data_o(detect_data),
                                     .w_addr_o(w_addr),
                                     .r_addr_o(r_addr),
                                     .write_test_data_o(write_test_data),
                                     .read_enable_o(read_enable),
                                     .init_o(init)
                                     );


assign soft_init = init && enable;
assign charge_adr_w  = enable && w_addr;
assign charge_adr_r  = enable && r_addr;
assign charge_test_data[0] = enable && write_test_data && !r_step_wv[2] && detect_data;
assign charge_test_data[1] = enable && write_test_data && r_step_wv[2] && detect_data;
assign charge_test_data[2] = enable && write_test_data && r_step_wv[2] && !detect_data;
assign ecriture[0] = capt_i && r_enable_trace_i && !r_step_wv[0];
assign ecriture[1] = !r_step_wv[2] && !r_step_wv[1] && r_step_wv[0];
assign relecture[0] = read_enable && !r_step_rd[2] && !r_step_rd[1] && !r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[1] = read_enable && !r_step_rd[2] && !r_step_rd[1] && r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[2] = read_enable && !r_step_rd[2] && r_step_rd[1] && !r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[3] = read_enable && !r_step_rd[2] && r_step_rd[1] && r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[4] = read_enable && r_step_rd[2] && !r_step_rd[1] && !r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[5] = read_enable && r_step_rd[2] && !r_step_rd[1] && r_step_rd[0] && !busi_i && !r_standby && enable;
assign relecture[6] = busi_i || r_standby;

always @(posedge clk_ref or negedge rst)
  if(!rst)
       begin 
           rdaddr_o <= 'h0;
           wraddr_o <= 'h0;
           wen_o <= 1'b0;
           data_o <= 64'h0;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
  else if(soft_init)
       begin 
           rdaddr_o <= 'h0;
           wraddr_o <= 'h0;
           wen_o <= 1'b0;
           data_o <= 64'h0;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
//### CHARGEMENT Valeur WRADDR #######
  else if(charge_adr_w)
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= fp1_data_i;
           wen_o <= 1'b0;
           data_o <= 64'h0;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
//### CHARGEMENT Valeur RADDR #######
  else if(charge_adr_r)
       begin
           rdaddr_o <= fp1_data_i;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= 64'h0;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
//### ECRITURE EN MODE TEST #######
  else if(charge_test_data[0])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= fp1_data_i;
           wen_o <= 1'b0;
           data_o <= data_o;
           r_step_wv <= 3'b100;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
  else if(charge_test_data[1])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= (wen_o) ? wraddr_o + 1'b1 : wraddr_o;
           wen_o <= (r_step_wv == 3'b111) ? 1'b1 : 1'b0;
          case(r_step_wv)
             3'b100 : data_o <= {data_o[63:16],fp1_data_i};
             3'b101 : data_o <= {data_o[63:32],fp1_data_i,data_o[15:0]};
             3'b110 : data_o <= {data_o[63:48],fp1_data_i,data_o[31:0]};
             3'b111 : data_o <= {fp1_data_i,data_o[47:0]};           
          endcase
           r_step_wv <= (r_step_wv == 3'b111) ? 3'b100 : r_step_wv + 1'b1;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
  else if(charge_test_data[2])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= (wen_o) ? wraddr_o + 1'b1 : wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_o;
           r_step_wv <= r_step_wv;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
//### ECRITURE EN MODE VERIFICATION #######
  else if(ecriture[0])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= egal_un_i ? wraddr_o + 1'b1 : wraddr_o;
           wen_o <= 1'b1;
           data_o <= data_dut_i;
           r_step_wv <= egal_un_i ? 3'b0 : 3'b001;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
  else if(ecriture[1])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o + 1'b1;
           wen_o <= 1'b0;
           data_o <= data_o;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
//######## RE-LECTURE DES DONNEES #########
  else if(relecture[0])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b001;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end
  else if(relecture[1])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b010;
           r_dv_trce_o <= 1'b1;
           data_rd_o <= data_read_i[15:0];
           r_standby <= 1'b1;
       end
  else if(relecture[2])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b011;
           r_dv_trce_o <= 1'b1;
           data_rd_o <= data_read_i[31:16];
           r_standby <= 1'b1;
       end
  else if(relecture[3])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b100;
           r_dv_trce_o <= 1'b1;
           data_rd_o <= data_read_i[47:32];
           r_standby <= 1'b1;
       end
  else if(relecture[4])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b101;
           r_dv_trce_o <= 1'b1;
           data_rd_o <= data_read_i[63:48];
           r_standby <= 1'b1;
       end
    else if(relecture[5])
       begin
           rdaddr_o <= rdaddr_o + 1'b1;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b001;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= data_rd_o;
           r_standby <= 1'b1;
       end
  else if(relecture[6])
       begin
           rdaddr_o <= rdaddr_o;
           wraddr_o <= wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_dut_i;
           r_step_wv <= 3'b0;
           r_step_rd <= (read_enable && enable) ? r_step_rd : 3'b000;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= data_rd_o;
           r_standby <= (!busi_i) ? 1'b0 : 1'b1;
       end
  else
       begin
           rdaddr_o <= egaladdr ? 'b0 : rdaddr_o;
           wraddr_o <= egaladdr ? 'b0 : wraddr_o;
           wen_o <= 1'b0;
           data_o <= data_o;
           r_step_wv <= 3'b0;
           r_step_rd <= 3'b0;
           r_dv_trce_o <= 1'b0;
           data_rd_o <= 16'h0;
           r_standby <= 1'b0;
       end

endmodule
