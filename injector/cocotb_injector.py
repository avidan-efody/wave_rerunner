from cocotb.binary import BinaryValue

from injector.injector_base import InjectorBase

from functools import reduce

class CocotbInjector(InjectorBase):
    def __init__(self, dut):
        self.coco_dut = dut

        super().__init__()

    def get_cocotb_sig(self,sig_name):
         return reduce(getattr, sig_name.split('.')[1:], self.coco_dut)

    def inject_values(self, values):
        for sig_name, value in values.items():
            coco_sig = self.get_cocotb_sig(sig_name)
            coco_sig <= BinaryValue(value)