#!/usr/bin/csh

setenv MODULE replay_wave
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

./simv +define+COCOTB_SIM=1  -full64 -ucli -do post_dump.cmd
