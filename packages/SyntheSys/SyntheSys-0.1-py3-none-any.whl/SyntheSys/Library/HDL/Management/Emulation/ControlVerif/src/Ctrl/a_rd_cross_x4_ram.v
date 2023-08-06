module a_rd_cross_x4_ram(
                     ctrl_i,

                     data_i_0,
                     data_i_1,
                     data_i_2,
                     data_i_3,

                     dv_i_0,
                     dv_i_1,
                     dv_i_2,
                     dv_i_3,

                     data_o,
                     dv_o
                     );

input[2:0] ctrl_i;
input[15:0] data_i_0, data_i_1, data_i_2, data_i_3 ;
input dv_i_0, dv_i_1, dv_i_2, dv_i_3;

output[15:0] data_o;
output dv_o;

wire[2:0] ctrl_i;
wire[15:0] data_i_0, data_i_1, data_i_2, data_i_3;
wire dv_i_0, dv_i_1, dv_i_2, dv_i_3;

wire[15:0] data_o;
wire dv_o;

assign dv_o   = ctrl_i[2] ? dv_i_3   : ctrl_i[1] ? dv_i_2   : ctrl_i[0] ? dv_i_1   : dv_i_0  ;
assign data_o = ctrl_i[2] ? data_i_3 : ctrl_i[1] ? data_i_2 : ctrl_i[0] ? data_i_1 : data_i_0;

endmodule
