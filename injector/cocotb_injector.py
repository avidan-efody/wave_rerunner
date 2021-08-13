from cocotb.binary import BinaryValue
from cocotb.handle import Force

from cocotb.handle import ModifiableObject, HierarchyObject, HierarchyArrayObject, NonHierarchyIndexableObject

from injector.injector_base import InjectorBase

from rerun_args.customize import *

from functools import reduce

# This class will get all signals in cocotb dut in the 

# 3 use cases:
# A. fsdb only for block, we're loading entire design in rerun: in this case cocotb TOPLEVEL is top.block
# B. fsdb for entire design, cocotb injects only on a given block. use wave_prefix to add path to block
# C. fsdb for top1.x, cocotb runs on top2.x (postuvm). use wave_prefix == "top1", design_prefix "top2" to replace top1 with top2

# note postuvm doesn't work on this branch for now because cocotb doesn't iterate over vpiInterface

class CocotbDesignExplorer():
    def __init__(self, cocotb_dut):
        self.coco_dut = cocotb_dut

        wave_prefix = read_argument('wave_prefix', True)
        self.prefix = wave_prefix if wave_prefix != None else ''
        
        self.replay_blocks = read_argument('replay_block')
        if not isinstance(self.replay_blocks, list):
            self.replay_blocks = [self.replay_blocks]
        
        self.basic_sigs = {} # hash containing path relative to coccotb dut, and the signal object
        for replay_block in self.replay_blocks:
            self.get_basic_sigs(replay_block)

        excluded_sigs = read_argument('excluded_sigs', True)
        excluded_sigs = excluded_sigs if excluded_sigs != None else {}

        clean_basic_sigs = {}
        for key, value in self.basic_sigs.items():
            if key not in excluded_sigs:
                clean_basic_sigs[self.prefix + key] = value

        self.basic_sigs = clean_basic_sigs

    def get_basic_sigs(self, replay_block):
        element = self.get_cocotb_element(replay_block)
        self.get_basic_sigs_recursive(element)


    def get_basic_sigs_recursive(self,coco_element):
        coco_element._discover_all()
        for sig_name, coco_sig in coco_element._sub_handles.items():

            # any normal signal. structs, struct arrays, unpacked vectors are not modifiable
            if isinstance(coco_sig, ModifiableObject):
                print("Adding signal: ", coco_sig._path)
                self.basic_sigs[coco_sig._path] = coco_sig

            # unpacked vector (but not of structs)
            if (coco_sig._type == 'GPI_ARRAY'):
                if (isinstance(coco_sig[coco_sig._range[1]], ModifiableObject)):
                    print("Adding unpacked array: ", coco_sig._path)
                    self.basic_sigs[coco_sig._path] = coco_sig

            # struct
            if (coco_sig._type == 'GPI_STRUCTURE'):
                self.get_basic_sigs_recursive(coco_sig)

            # struct array
            if (coco_sig._type == 'GPI_ARRAY'): 
                if (coco_sig[coco_sig._range[1]]._type == 'GPI_STRUCTURE'):
                    for coco_sig_element in coco_sig:
                        self.get_basic_sigs_recursive(coco_sig_element) 

    # our cocotb dut points to some internal block. when we get the signal name from wave, we need to remove a prefix
    def remove_prefix(self, str, prefix):
        if str.startswith(self.prefix):
            return str[len(self.prefix):]
        return str  # or whatever

    def get_cocotb_element(self,element_name):
        print(element_name.split('.')[1:])
        return reduce(getattr, element_name.split('.')[1:], self.coco_dut)

    def get_sig(self, name_with_prefix):
        return self.basic_sigs[self.remove_prefix(name_with_prefix)]


class CocotbInjector(InjectorBase):
    def __init__(self, design_explorer):
        # replay_blocks is a problem: currently through test_customization.py
        self.design_explorer = design_explorer
        self.error_signals = []
        self.previous_values = None

        super().__init__()

    def inject_values(self, current_values):
        values = self.filter_unchanged(current_values)
        
        for sig_name, value in values.items():

            if sig_name in self.error_signals:
                pass
                #continue

            coco_sig = self.design_explorer.basic_sigs[sig_name]

            bin_value = None

            try: 
                # unpacked vector
                if ((coco_sig._type == 'GPI_ARRAY') and isinstance(coco_sig[0], ModifiableObject)):
                    for idx, coco_sig_element in enumerate(coco_sig):
                        coco_sig_element <= Force(BinaryValue(value[idx]))
                else:
                    coco_sig <= Force(BinaryValue(value))
            except ValueError:
                if sig_name not in self.error_signals:
                    self.error_signals.append(sig_name)
                    print("Value error. Signal is: ", sig_name, " value is: ", value)#, "\n the values requested to inject are: ", values)
            except TypeError:
                if sig_name not in self.error_signals:
                    self.error_signals.append(sig_name)
                    print("Type error. Signal is: ", sig_name, " value is: ", value)#, "\n the values requested to inject are: ", values)


    def filter_unchanged(self, current_values):
        if self.previous_values == None:
            self.previous_values = current_values
            return current_values


        changed_values = {}
        for sig, value in current_values.items():
            if sig in self.previous_values.keys():
                if self.previous_values[sig] != value:
                    changed_values[sig] = value

        self.previous_values = current_values

        return changed_values