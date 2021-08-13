#!/usr/bin/csh

setenv PYTHONPATH ../:$PYTHONPATH

# required by cocotb
setenv MODULE test_dut
#setenv MODULE cocotb.ipython_support
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

vcs -top top  +acc+1 +vpi -P $WAVE_RERUNNER/examples/common/pli.tab +define+COCOTB_SIM=1 -sverilog -timescale=1ns/1ps -full64 -debug -debug_access -kdb -load libcocotbvpi_vcs.so $WAVE_RERUNNER/examples/sv/less_simple_top.sv

./simv +define+COCOTB_SIM=1 -full64 -ucli -do dump.cmd
