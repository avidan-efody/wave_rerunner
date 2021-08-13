#!/usr/bin/csh

setenv PYTHONPATH ../:$PYTHONPATH

# required by cocotb
setenv MODULE injector.wave_rerunner
#setenv MODULE cocotb.ipython_support
setenv TESTCASE ''
setenv TOPLEVEL post_uvm_top 
setenv TOPLEVEL_LANG verilog

# those don't work (vcs crash)
# -debug_access+all -debug_region=2,post_uvm_top.vip0 -debug_region=2,post_uvm_top.apb0

vcs -lca -kdb -sverilog -timescale=1ns/1ns +vpi -debug_access+all -debug_region=2,post_uvm_top.vip0 -debug_region=2,post_uvm_top.apb0 -debug_region=2,post_uvm_top.ctl +define+UVM_OBJECT_MUST_HAVE_CONSTRUCTOR +incdir+$UVM_HOME/src $UVM_HOME/src/uvm.sv $UVM_HOME/src/dpi/uvm_dpi.cc -CFLAGS -DVCS  +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/vip +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/ +incdir+$WAVE_RERUNNER/examples/sv/integrated/apb  $WAVE_RERUNNER/examples/sv/integrated/codec/codec_pkg.sv $WAVE_RERUNNER/examples/sv/integrated/codec/post_uvm/post_uvm_top.sv -full64 -load libcocotbvpi_vcs.so

./simv -full64 +define+COCOTB_SIM=1 +UVM_VERBOSITY=UVM_HIGH +UVM_TESTNAME=post_uvm_test -l replayed_run.log -ucli -do post_dump.cmd
