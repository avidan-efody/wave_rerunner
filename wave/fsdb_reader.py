from pynpi import npisys
from pynpi import waveform

from wave.reader_base import ReaderBase, ScopeNotFound

class FsdbReader(ReaderBase):
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):
        npisys.init(["anything"])

        self.fsdb = waveform.open(wave_file)

        if not self.fsdb:
            raise FileNotFoundError("Error. Failed to open file: ", wave_file, " or it isn't an fsdb")

        super().__init__(replay_blocks, wave_file, excluded_sigs, inputs_only)

    def extract_values_from_wave(self, replay_blocks, excluded_sigs = [], inputs_only=True):
        sig_list = []
        for block in replay_blocks:
            scope = self.fsdb.scope_by_name(block)
            if not scope:
                raise ScopeNotFound("Can't find scope: ", block, " in fsdb")
            sig_list.extend(scope.sig_list())

        signal_values = {}
        for sig in sig_list:
            if (sig.full_name() in excluded_sigs):
                continue

            if (inputs_only) and (sig.direction() != waveform.DirType_e.DirInput):
                continue

            print("extracting values for: ", sig.full_name())
            signal_values[sig.full_name()] = waveform.sig_hdl_value_between(sig,0,self.fsdb.max_time(),waveform.VctFormat_e.BinStrVal)

        return signal_values