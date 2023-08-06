module a_rd_cross_x2_ram(
                     ctrl_i,

                     data_i_0,
                     data_i_1,

                     dv_i_0,
                     dv_i_1,

                     data_o,
                     dv_o
                     );

input ctrl_i;
input[15:0] data_i_0, data_i_1;
input dv_i_0, dv_i_1;

output[15:0] data_o;
output dv_o;

wire ctrl_i;
wire[15:0] data_i_0, data_i_1;
wire dv_i_0, dv_i_1;

wire[15:0] data_o;
wire dv_o;

assign dv_o = ctrl_i ? dv_i_1 : dv_i_0;
assign data_o = ctrl_i ? data_i_1 : data_i_0;

endmodule
