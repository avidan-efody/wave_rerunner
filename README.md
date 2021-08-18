# introduction
 
This repo contains code to read various wave formats (fsdb, shm, vcd, wlf) into python and then reinject selected parts into selected parts of the design. A typical use case for this code would be:

* A test takes very long, because it runs a big RTL and testbench
* You've only changed a UVM checker or an assertion
* You'd like to check the modified UVM checker or assertion without rerunning the big RTL

The applications in the examples directory, described in detail below, show how to do exactly that:

* [Rerun UVM checkers, coverage and RAL monitor without any RTL](https://github.com/avidan-efody/wave_rerunner#uvm-rerun)
* [Rerun SVA assertions without rerunning the whole RTL](https://github.com/avidan-efody/wave_rerunner#sva-rerun)

# structure

* wave/ - contains python modules that read wave files in various formats (fsdb, vcd, shm, wlf) into python data structure. Currently fsdb is fully supported, vcd partially supported, and others are not supported yet. Refer to support matrix for more info.
* injector/ - contains python modules to re-inject data from the python data structures back into a design. Also contains a generic cocotb test (wave_rerunner.py) that will take the data read from the wave files, and re-apply it at the given scopes
* examples/ - examples showing how these capabilities could be applied to common verification tasks such as SVA assertion replay or UVM checkers/coverage replay both without or with only limited part of original RTL

# Operation

wave_rerunner is a special cocotb python test that the user loads during simulation. This test reads wave data (currently FSDB, some VCD, planned SHM) from a user configured file into python data structures. It then re-injects the values read from the wave into a user configured design scope. Note, that unlike some solution available from vendors it *doesn't generate any SV/Verilog code*, but rather uses the original code. Unlike other vendor soutions, it does run a simulation even during rerun, but the simulation is much faster since a lot of the RTL and testbench are removed.

## UVM rerun

Assume you have run a regression with a (state-of-the-art) simulation top called tb_top that contains:
* your DUT
* some SV interfaces connected to DUT IO, say apb_if, and serial_if
* UVM code to initialize virtual interfaces from interface instance
* UVM call to run_test()
* Some clock/reset generators

You have only modified one of your UVM checkers or have added some coverage, and you would prefer not to rerun the whole regression again just to see some results. All the more so since you expect a few iterations until you get it straight.

To achieve this using wave_rerunner you could create a new top with the following minor modifications:
* Your DUT instantiation removed
* Your agents configured to passive mode

And then ask wave_rerunner to replay only the signals inside your SV interface instances by specifying:

```replay_blocks = ["tb_top.apb_if", "tb_top.serial_if"]```

Since these interfaces hold all the signals your coverage and checkers ever see, you should get exactly the same transaction from your monitors, and exactly the same results from your checkers and coverage. However, since you're not running any RTL now, you'll be iterating much faster. You could obtain even better speedup and get less noise by replaying only the interfaces your checker cares about, and disabling all other checkers. 

Note that your new top can still inject the clocks. There's little point, and quite a bit of performance/memory penalty to reading and replaying those.

![alt-text](https://github.com/avidan-efody/assertion_rerun/blob/main/examples/uvm_rerun/uvm_rerun.png)

## SVA rerun

Assume you have run a regression with a simulation top called cluster_top and saved relevant FSDBs with all or a few levels down recorded. You have now modified an assertion inside cluster_top.block_top.subblock_top, and you would prefer not to rerun the whole cluster just to check it, all the more so since you're not sure of the assertion, and think it might take a few iterations.

To get going quickly you could run your original cluster_top in vcs loading cocotb as a VPI library (assuming you have cocotb installed, this is just a simulator switch). Cocotb will kick off the default wave_rerunner test, which will look for a file containing some parameters on your PYTHONPATH. These parameters include the fsdb you would like to rerun, and the scope that you would like to rerun, which in this case is cluster_top. It will then read all inputs to cluster_top from the FSDB and re-inject them, reproducing the original test result.

This configuration will likely give you a good speed-up already because your testbench is much lighter. However, your RTL is still running in full, when all you really need to run is subblock_top.

To improve that you could tell wave_rerunner to extract and reinject only the inputs to cluster_top, provided that you have logged them in your wave file. You'll do this by specifying ```replay_blocks = ["cluster_top.block_top.subblock_top"]```. This will make wave_rerunner extract signals belonging to this block only, and reinject only those. Now your simulator will likely run much faster because everything except for cluster_top.block_top.subblock_top (and the blocks it drives), is not seeing much activity and hence not taking much simulation time. Still, you'll be running a lot that you're not actually using.

A further improvement would be to load subblock_top as your simulation top. To adapt the path from your FSDB path you could use the wave_prefix configuration argument and set it to: wave_prefix = "cluster_top.block_top". Now wave rerunner will pick the values for cluster_top.block_top.subblock_top inputs (because that is what you specified in replay_blocks), but instead of trying to inject them at cluster_top.block_top.subblock_top.my_input, it will remove the prefix and inject them at subblock_top.my_input. Now you'll be rerunning only subblock_top, which is likely to give an even better speedup.

You can obtain even faster runtime by creating a module that contains only your assertions, and binding it at runtime into subblock_top. This is not only a generally recommanded pattern for packaging and encapsulating assertions, but would also allow you to rerun without any RTL at all, since you could now simply replay the inputs of the binded assertions block.

Finally, if your wave file contains clocks, you could obtain faster run-time and smaller memory foot-print, by not replaying those from the wave file, but rather, keeping the original clock generators in the rerun setup. Since this technique is common to SVA rerun and UVM rerun, it is covered elsewhere.

![alt-text](https://github.com/avidan-efody/assertion_rerun/blob/main/examples/sva_rerun/assertion-rerun.gif)

## Detailed operation

TBD

# pre-requisites

* cocotb (currently required for injecting anything back)
* reading commercial wave formats (fsdb, shm, wlf) requires the matching simulator
* rerunning SVA/UVM requires commercial simulator

# running the examples

## SVA rerun

replace *vendor* with your favorite vendor (currently either "snps" or "cdns")

```
cd examples/[vendor]/setup
source sourceme.[vendor]
cd ../../sva_rerun/[vendor]/
source run.csh 
source rerun.csh
```

## UVM rerun

replace vendor with your favorite vendor (currently only "snps")

```
cd examples/[vendor]/setup
source sourceme.[vendor]
cd ../../uvm_rerun/[vendor]
source run.csh
source rerun.csh
```
