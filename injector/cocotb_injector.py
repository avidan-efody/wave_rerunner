from cocotb.binary import BinaryValue
from cocotb.handle import Force

from cocotb.handle import NonHierarchyIndexableObject

from injector.injector_base import InjectorBase

from functools import reduce

class CocotbInjector(InjectorBase):
    def __init__(self, dut, prefix = ""):
        self.coco_dut = dut
        self.prefix = prefix
        self.error_signals = []

        super().__init__()

    def remove_prefix(self, str, prefix):
        if str.startswith(prefix):
            return str[len(prefix):]
        return str  # or whatever

    def get_cocotb_sig(self,sig_name):
         return reduce(getattr, self.remove_prefix(sig_name, self.prefix).split('.')[1:], self.coco_dut)


    def inject_values(self, values):
        for sig_name, value in values.items():
            # structs/arrays injection not supported yet.
            if '{' in value:
                print("skipping hier signal?: ", sig_name)
                continue

            if sig_name in self.error_signals:
                continue

            coco_sig = self.get_cocotb_sig(sig_name)

            bin_value = BinaryValue(value)
            # sometimes cocotb sees an object as idexable, but it is just a plain vector? 
            #if isinstance(coco_sig, NonHierarchyIndexableObject):
            #    bin_value = [BinaryValue(v) for v in list(value)]
                #print("skipping list signal: ", sig_name)
                #continue
            #else:
            #    bin_value = BinaryValue(value)

            #print("assigning sig: ", sig_name)
    
            try:
                coco_sig <= Force(bin_value)
            except ValueError:
                print("Value error. The values requested to inject are: ", values)
            except TypeError:
                self.error_signals.append(sig_name)
                print("Type error. Signal name is: ", sig_name, " sig value: ", value)