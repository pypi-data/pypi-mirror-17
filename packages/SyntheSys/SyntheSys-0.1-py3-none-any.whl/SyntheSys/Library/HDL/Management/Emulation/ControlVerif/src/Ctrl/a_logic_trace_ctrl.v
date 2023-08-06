`define LENGTH_RAM_TRACE 13                 
`define PROF_RAM_TRACE 8192
`define FULL_RAM_TRACE 13'b1_1111_1111_0111  // Max -10

module a_logic_trace_ctrl(
//###### Identifiant #######
                   carte_i,
                   fpga_i,
                   id_i,
//### Signaux Commande
                   clk_ref,
                   rst,
                   fp1_data_i,
                   fp1_dv_i,
                   ctrl_trce_i,
                   
                   clk_user_i,


//### COMMANDE DETECTE POUR CONTROLEUR DE TRACE
//
                   enable_o,
                   detect_data_o,
                   w_addr_o,
                   r_addr_o,
                   write_test_data_o,
                   read_enable_o,
                   init_o

                   );
                 
input[3:0] id_i;
input carte_i;
input[3:0] fpga_i;
input[15:0] fp1_data_i;
input fp1_dv_i;

input clk_ref, rst, ctrl_trce_i;                 
input clk_user_i;

output w_addr_o, r_addr_o;
output write_test_data_o;
output read_enable_o;
output init_o;
output enable_o;
output detect_data_o;

wire[3:0] id_i;
wire carte_i;
wire[3:0] fpga_i;
wire[15:0] fp1_data_i;
wire fp1_dv_i;


wire clk_ref, rst;                 
wire clk_user_i;

reg w_addr_o, r_addr_o;
reg write_test_data_o;
reg read_enable_o;
reg init_o;

wire enable_o;
wire detect_data_o;

//##### DECLARATION DES SIGNAUX INTERNE #########
reg[1:0] prog_step;
wire standby_capture;
wire prog_add_wr, prog_add_rd, prog_rd_cmd, prog_wr_cmd, prog_init_cmd;

assign enable_o = ((id_i == fpga_i) && carte_i) ? 1'b1 : 1'b0;

//###############################################
//###### DECODAGE LOCAL                     #####
//### 0 ==>  prog addresse write            #####
//### 1 ==>  prog addresse read             #####
//### 2 ==> read_commande                   #####
//### 3 ==> write_commande                  #####
//### 15 ==>  init                          #####
//###############################################
//
assign detect_data_o = fp1_dv_i && ctrl_trce_i;
assign standby_capture = detect_data_o && !prog_step[0] && !prog_step[1];
assign prog_add_wr = fp1_data_i[0] && standby_capture;
assign prog_add_rd = fp1_data_i[1] && standby_capture;
assign prog_rd_cmd = fp1_data_i[2] && standby_capture;
assign prog_wr_cmd = fp1_data_i[3] && standby_capture;
assign prog_init_cmd = fp1_data_i[15] && standby_capture;

always @(posedge clk_ref or negedge rst)
  if(!rst)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b0;
       end
  else if(prog_add_wr)
       begin
           w_addr_o <= 1'b1;
//           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b01;
       end
  else if(prog_init_cmd)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b1;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b01;
       end
  else if(prog_add_rd)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b1;
//           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b01;
       end
  else if(prog_rd_cmd)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b1;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b10;
       end
  else if(prog_wr_cmd)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b1;
           prog_step <= 2'b10;
       end
  else if(!prog_step[0] && prog_step[1])
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= ctrl_trce_i ? read_enable_o : 1'b0;
           write_test_data_o <= ctrl_trce_i ? write_test_data_o : 1'b0;
           prog_step <= ctrl_trce_i ? prog_step : 2'b00;
       end
  else if(prog_step[0] && !prog_step[1] && !ctrl_trce_i)
       begin
           w_addr_o <= 1'b0;
           r_addr_o <= 1'b0;
           init_o <= 1'b0;
           read_enable_o <= 1'b0;
           write_test_data_o <= 1'b0;
           prog_step <= 2'b0;
       end


endmodule
