# introduction
 
This repo contains code to read various wave formats (fsdb, shm, vcd, wlf) into python and then reinject selected parts into selected parts of the design. The applications in the examples directory show how this can be used to:

* [Rerun SVA assertions without rerunning the whole RTL](examples/sva_rerun/README.md)
* [Rerun UVM checkers, coverage and RAL monitor without any RTL](examples/uvm_rerun/README.md)

Refer to above links for detailed description of each application.

# structure

* wave/ - contains python modules that read wave files in various formats (fsdb, vcd, shm, wlf) into python data structure. Currently fsdb is fully supported, vcd partially supported, and others are not supported yet. Refer to support matrix for more info.
* injector/ - contains python modules to re-inject data from the python data structures back into a design. Also contains a generic cocotb test (wave_rerunner.py) that will take the data read from the wave files, and re-apply it at the given scopes
* examples/ - examples showing how these capabilities could be applied to common verification tasks such as SVA assertion replay or UVM checkers/coverage replay both without or with only limited part of original RTL

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

![alt-text](https://github.com/avidan-efody/assertion_rerun/blob/main/examples/sva_rerun/assertion-rerun.gif)

## UVM rerun

replace vendor with your favorite vendor (currently only "snps")

```
cd examples/[vendor]/setup
source sourceme.[vendor]
cd ../../uvm_rerun/[vendor]
source run.csh
source rerun.csh
```
