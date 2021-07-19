#!/usr/bin/csh

setenv PYTHONPATH ../:$PYTHONPATH

# required by cocotb
setenv MODULE replay_wave
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

./simv +define+COCOTB_SIM=1  -full64 -ucli -do $WAVE_RERUNNER/examples/common/post_dump.cmd
