module a_clock_gen_rs232_prot8 (
                                  rst_n,
                                  clk_ref,
                                  r_di,
                                  dv_i,
                                  
                                  data_demi,
                                  dv_demi,
                                  
                                  valeur_comp,
                                  dv_data,
                                  data,

                                  clk_rcpt,
                                  clk_rcpt_general,
                                  clk_send,

                                  error_p8,
                                  send_sync_o,
                                  sync_o
                                  );

input rst_n, clk_ref;
input r_di, dv_i;
input dv_data;
input[15:0] data;
input[71:0] valeur_comp;
input[7:0] data_demi;
input dv_demi;

output clk_rcpt, clk_send, clk_rcpt_general;
output sync_o,error_p8, send_sync_o;

wire rst_n, clk_ref;
wire r_di, dv_i;
wire dv_data;
wire[15:0] data;
wire[71:0] valeur_comp;
wire[7:0] data_demi;
wire dv_demi;
wire send_sync_o;
reg clk_rcpt;
reg clk_send;
wire flag_0, sync_o, flag_demi;
wire clk_rcpt_general;
// ########## DECLARATION SIGNAUX INTERNE #######
reg pipe_sync_o;
reg enable_o;
reg[11:0] cpt_h_rclk, cpt_h_send;
reg[4:0] cpt_pulse;
reg r_start;
reg[4:0] r_cpt_data;

wire[11:0] div_freq_trans;



wire[11:0] div_freq_rec_0;
wire flag_p8_1, error_p8_1, flag_p8_2, error_p8_2, flag_p8_3, error_p8_3, error_p8_4;
wire error_p8, error_demi;
wire rst_global;
wire timeout;
// --- Dectecteur de frequence ------
//

assign clk_rcpt_general = clk_rcpt & flag_0;
assign rst_global = rst_n & !error_p8 & !timeout;
assign send_sync_o = sync_o & !pipe_sync_o;

a_calcul_freq u_calcul_freq0(
                            .rst_n(rst_global),
                            .clk_ref(clk_ref),
                            .r_di(r_di),
                            .valeur_comp(valeur_comp[7:0]),
                            .val_div(4'd8),
                            
                            .div_freq_rec(div_freq_rec_0),
                            .flag_first(flag_demi)
                            );

a_timeout_rs232 u_timeout_rs232(
                               .rst_n(rst_global),
                               .clk_ref(clk_ref),
                               .start(flag_demi),
                               .fin_timeout(flag_0),
                       
                               .error(timeout)
                               );

a_compare_val u_comp_val_demi(
                          .rst_n(rst_global),
                          .clk_ref(clk_ref),
                          .enable(flag_demi),
                          .comp_val({10'b0,valeur_comp[7:0]}),

                          .data_valid(dv_demi),
                          .data({10'b0,data_demi}),
                            
                          .flag(flag_0),
                          .error(error_demi)
                          );

// Decode protocole 8 bits

a_compare_val u_comp_val_0(
                          .rst_n(rst_global),
                          .clk_ref(clk_ref),
                          .enable(flag_0),
                          .comp_val({1'b0,valeur_comp[23:16],1'b0,valeur_comp[15:8]}),

                          .data_valid(dv_data),
                          .data({1'b0,data[15:8],1'b0,data[7:0]}),
                            
                          .flag(flag_p8_1),
                          .error(error_p8_1)
                          );

a_compare_val u_comp_val_1(
                          .rst_n(rst_global),
                          .clk_ref(clk_ref),
                          .enable(flag_p8_1),
                          .comp_val({1'b1,valeur_comp[39:32],1'b1,valeur_comp[31:24]}),

                          .data_valid(dv_data),
                          .data({1'b1,data[15:8],1'b1,data[7:0]}),
                            
                          .flag(flag_p8_2),
                          .error(error_p8_2)
                          );

a_compare_val u_comp_val_2(
                          .rst_n(rst_global),
                          .clk_ref(clk_ref),
                          .enable(flag_p8_2),
                          .comp_val({1'b1,valeur_comp[55:48],1'b1,valeur_comp[47:40]}),

                          .data_valid(dv_data),
                          .data({1'b1,data[15:8],1'b1,data[7:0]}),
                            
                          .flag(flag_p8_3),
                          .error(error_p8_3)
                          );

a_compare_val u_comp_val_3(
                          .rst_n(rst_global),
                          .clk_ref(clk_ref),
                          .enable(flag_p8_3),
                          .comp_val({1'b1,valeur_comp[71:64],1'b1,valeur_comp[63:56]}),

                          .data_valid(dv_data),
                          .data({1'b1,data[15:8],1'b1,data[7:0]}),
                            
                          .flag(sync_o),
                          .error(error_p8_4)
                          );

assign error_p8 = error_p8_1 | error_p8_2 | error_p8_3 | error_p8_4 | error_demi;

assign div_freq_trans = div_freq_rec_0;


// ## GENERATION DE L'HORLOGES DU BUS SERIE EN RECEPTION ##
always @(posedge clk_ref or negedge rst_global)

if(!rst_global)
    begin
        pipe_sync_o <= 1'b0;
    end
else
    begin 
        pipe_sync_o <= sync_o;
    end

always @(posedge clk_ref or negedge rst_global)

if(!rst_global)
    begin
       clk_rcpt <= 1'b0;
       cpt_h_rclk <= 12'hfc0;
       cpt_pulse <= 5'b0;
       enable_o <= 1'b1;
    end
else if(cpt_h_rclk == div_freq_rec_0)
    begin
       clk_rcpt <= (cpt_pulse == 5'b0_1000) ? 1'b0 : 1'b1;
       cpt_h_rclk <= 12'b0;
       cpt_pulse <= cpt_pulse + 1'b1;
       enable_o <= (cpt_pulse == 5'b0_1000) ? 1'b1 : 1'b0;
    end
else if(!enable_o)
    begin
       clk_rcpt <= 1'b0;
       cpt_h_rclk <= cpt_h_rclk + 1'b1;
       cpt_pulse <= cpt_pulse;
       enable_o <= 1'b0;
    end
else 
    begin
       clk_rcpt <= 1'b0;
       cpt_h_rclk <= 12'hfc0;
       cpt_pulse <= 5'b0;
       enable_o <= flag_demi ? r_di : 1'b1;
    end


// ## GENERATION DE L'HORLOGES DU BUS SERIE EN EMMISSION ## 

always @(posedge clk_ref or negedge rst_global)
                                                                                                    
if(!rst_global)
    begin
       clk_send <= 1'b0;
       cpt_h_send <= 12'b0;
       r_start <= 1'b0;
       r_cpt_data <= 5'b0;
    end
else if(dv_i | send_sync_o)
    begin
       clk_send <= 1'b0;
       cpt_h_send <= 12'b0;
       r_start <= 1'b1;
       r_cpt_data <= r_cpt_data;
    end
else if(cpt_h_send == div_freq_trans)
    begin
       clk_send <= 1'b1;
       cpt_h_send <= 12'b0;
       r_start <= (r_cpt_data == 5'd19) ? 1'b0 : 1'b1;
       r_cpt_data <= (r_cpt_data == 5'd19) ? 5'b0 : (r_cpt_data + 1'b1);
    end
else
    begin
       clk_send <= 1'b0;
       cpt_h_send <= r_start ? (cpt_h_send + 1'b1) : 1'b0;
       r_start <= r_start;
       r_cpt_data <= r_cpt_data;
    end

endmodule
