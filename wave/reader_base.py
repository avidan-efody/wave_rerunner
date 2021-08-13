
class ScopeNotFound(Exception):
    pass

class ReaderBase:
    def __init__(self, clean_sig_list, wave_file, sigs_directions):  
        self.sigs_directions = sigs_directions if sigs_directions != None else True

        self.signal_values = self.extract_values_from_wave(clean_sig_list, self.sigs_directions)
        self.signal_changes = self.extract_events(self.signal_values)


    def extract_values_from_wave(self, clean_sig_list, sigs_directions):
    	pass

    def extract_events(self, signal_values):
        all_changes = []

        for sig_name, sig_values in signal_values.items():
            all_changes.extend(sig_values)

        change_times = sorted(list(set([change[0] for change in all_changes])))

        return change_times

    def get_next_event(self, sim_time):
        next_time = next((change_time for change_time in self.signal_changes if change_time > sim_time), None)
        return next_time

    def get_values_at(self, sim_time):
        current_values = {}
        for sig_name, sig_values in self.signal_values.items():
            current_values[sig_name] = next((sig_value[1] for sig_value in sig_values[::-1] if sig_value[0] <= sim_time), None)

        return current_values  