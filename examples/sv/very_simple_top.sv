// This file is public domain, it can be freely copied without restrictions.
// SPDX-License-Identifier: CC0-1.0

`timescale 1us/1us

module top();
  logic clk = 0;
  logic din,dout;

  block block_i(clk, din, dout);

  initial begin
    forever begin
      #10 clk <= ~clk;
    end
  end

endmodule

module block (
  input logic clk, din,
  output logic dout
);

  reg [10:0] ctr = 0;

  always @(posedge clk) begin
    ctr <= ctr + 1;

    if (ctr !== 40)
      dout <= din;
  end

  assert property(@(negedge clk) din == dout);

endmodule
