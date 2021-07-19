from pynpi import npisys
from pynpi import waveform

from wave.reader_base import ReaderBase

class FsdbReader(ReaderBase):
    def __init__(self, replay_block, wave_file):
        npisys.init(["anything"])

        self.fsdb = waveform.open("novas.fsdb")

        if not self.fsdb:
            print("Error. Failed to open file")

        super().__init__(replay_block, wave_file)

    def extract_values_from_wave(self, replay_block):
        scope = self.fsdb.scope_by_name(replay_block)

        signal_values = {}

        for sig in scope.sig_list():
            if sig.direction() == waveform.DirType_e.DirInput:
                print("extracting values for: ", sig.full_name())
                signal_values[sig.full_name()] = waveform.sig_hdl_value_between(sig,0,self.fsdb.max_time(),waveform.VctFormat_e.DecStrVal)

        return signal_values