

vcs -kdb -sverilog -timescale=1ns/1ns -debug_access+r +vpi +define+UVM_OBJECT_MUST_HAVE_CONSTRUCTOR +incdir+$UVM_HOME/src $UVM_HOME/src/uvm.sv $UVM_HOME/src/dpi/uvm_dpi.cc -full64 -CFLAGS -DVCS  +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/vip +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/ +incdir+$WAVE_RERUNNER/examples/sv/integrated/apb  $WAVE_RERUNNER/examples/sv/integrated/codec/codec_pkg.sv $WAVE_RERUNNER/examples/sv/integrated/codec/tb_top.sv

./simv -full64 +UVM_VERBOSITY=UVM_HIGH +UVM_TESTNAME=codec_test -l original_run.log -ucli -do dump.cmd
