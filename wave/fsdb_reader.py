from pynpi import npisys
from pynpi import waveform

from wave.reader_base import ReaderBase, ScopeNotFound

class FsdbReader(ReaderBase):
    def __init__(self, clean_sig_list, wave_file, sigs_directions):
        npisys.init(["anything"])

        self.fsdb = waveform.open(wave_file)

        if not self.fsdb:
            raise FileNotFoundError("Error. Failed to open file: ", wave_file, " or it isn't an fsdb")

        super().__init__(clean_sig_list, wave_file, sigs_directions)

    def extract_values_from_wave(self, clean_sig_list, sigs_directions):
        signal_values = {}
        for sig in clean_sig_list:
            fsdb_sig = self.fsdb.sig_by_name(sig)

            if not fsdb_sig:
                raise ValueError("Signal: ", sig, " doesn't exist in fsdb")

            fsdb_directions = list(map(self.convert_to_fsdb_direction,sigs_directions))

            if len(fsdb_directions) and (fsdb_sig.direction() not in fsdb_directions):
                continue

            print("extracting values for: ", fsdb_sig.full_name())
            signal_values[sig] = waveform.sig_hdl_value_between(fsdb_sig,0,self.fsdb.max_time(),waveform.VctFormat_e.BinStrVal)
            print("values extracted: ", signal_values[sig])

        return signal_values

    def convert_to_fsdb_direction(self, generic_direction):
        if generic_direction == generic_direction.input:
            return waveform.DirType_e.DirInput
        if generic_direction == generic_direction.output:
            return waveform.DirType_e.DirOutput

