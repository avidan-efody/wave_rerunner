from rerun_args.customize import *

def read_wave(clean_sig_list):
    # get file postfix check if supported
    
    wavefile = read_argument('wavefile')
    wave_type = wavefile.split('.')[-1]

    supported_wave_formats = ['vcd', 'fsdb']

    if wave_type not in supported_wave_formats:
        raise ValueError("Wavefile type: ", wave_type, " is currently not supported. Supported formats are: ", supported_wave_formats)

    # optional args
    sigs_directions = read_argument('sigs_directions')

    data = None

    if wave_type == 'vcd':
        from wave.vcd_reader import VcdReader
        data = VcdReader(clean_sig_list, wavefile, sigs_directions)
    elif wave_type == 'fsdb':
        from wave.fsdb_reader import FsdbReader
        data = FsdbReader(clean_sig_list, wavefile, sigs_directions)

    return data     
