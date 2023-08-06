module a_timeout_rs232 (
                       rst_n,
                       clk_ref,
                       start,
                       fin_timeout,
                       
                       error
                       );


input rst_n, clk_ref;
input start;
input fin_timeout;

output error;

wire rst_n, clk_ref;
wire start;
wire fin_timeout;

wire error;

reg pipe_start;
wire demarre_cpt;
reg[26:0] cpt_timeout; //0.5seconde pour clkref 1ghz
reg compte;

assign error = (cpt_timeout == 27'd100000);

always @(posedge clk_ref or negedge rst_n)
if(!rst_n)
    begin
        pipe_start <= 1'b0;
    end
else
    begin
        pipe_start <= start;
    end

assign demarre_cpt = start & !pipe_start;

always @(posedge clk_ref or negedge rst_n)
if(!rst_n)
    begin
        cpt_timeout <= 27'b0;
        compte      <= 1'b0;
    end
else if(demarre_cpt || compte)
    begin
        cpt_timeout <= cpt_timeout + 1'b1;
        compte      <= !fin_timeout;
    end

endmodule

