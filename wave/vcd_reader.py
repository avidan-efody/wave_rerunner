import os
import sys
import re

# wip: better structured vcd reader
from wave.reader_base import ReaderBase

class VcdReader(ReaderBase):
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):
        self.vcd_path = wave_file #self.check_file_names_are_valid(wave_file)
        self.excluded_sigs = excluded_sigs
        self.replay_blocks = replay_blocks

        self.scope_begin_match = r"^\$scope\s*([^ ]+)\s*([^ ]+)\s*\$end"
        self.scope_end_match = r"\$upscope\s*\$end"
        self.definitions_end_match = r"\$enddefinitions.*"

        self.signal_match = r"\$var.*\$end"
        self.simple_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*\$end"
        self.vector_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*(\[[0-9]+\:[0-9]+\]*)\s*\$end"

        self.dumpvars_match = r"^\$dumpvars.*"
        self.new_time_match = r"^#([0-9]+)"
        self.sig_value_match = r"^[b]{0,1}([zx10]+)[ ]{0,1}(.*)"

        super().__init__(replay_blocks, wave_file, excluded_sigs, inputs_only)

    def extract_values_from_wave(self, replay_blocks, excluded_sigs, inputs_only):
        self.sigs_values = {}

        self.extract_vcd_file(self.vcd_path)

        return self.sigs_values

    def extract_vcd_file(self, valid_path):
        with open(valid_path, "r") as vcd_file:
            self.sig_name_2_vcd_name = {}
            self.vcd_name_2_sig_name = {}
            self.extract_scopes(vcd_file)
            print(self.sig_name_2_vcd_name)
            self.extract_sig_values(vcd_file)

    def extract_scopes(self, vcd_file, current_scope=""):
        while vcd_file:
            vcd_line = vcd_file.readline()
            if (vcd_line == "" ):
                return

            scope_begin = re.match(self.scope_begin_match, vcd_line)
            scope_end = re.match(self.scope_end_match, vcd_line)
            sig = re.match(self.signal_match, vcd_line)
            simple_sig = re.search(self.simple_sig_match, vcd_line)
            vector_sig = re.search(self.vector_sig_match, vcd_line)
            definitions_end = re.search(self.definitions_end_match, vcd_line)

            if definitions_end:
                if (current_scope != ""):
                    raise ValueError("Definitions terminated in the middle of scope: ", current_scope)
                return

            if scope_begin:
                new_scope_name = scope_begin.group(2)
                prefix = current_scope + "." if current_scope != "" else ""
                print("going into scope: ", prefix + new_scope_name)
                self.extract_scopes(vcd_file, prefix + new_scope_name)

            if scope_end:
                print("going out of scope: ", current_scope)
                return

            if current_scope not in self.replay_blocks:
                # just read the lines
                continue

            if sig and simple_sig:
                self.update_sig_tables(current_scope, simple_sig)

            if sig and vector_sig:
                self.update_sig_tables(current_scope, vector_sig)


            if (not (vector_sig or simple_sig or scope_begin or scope_end)):
                pass
                #print("Unsupported line: ", vcd_line)

    def update_sig_tables(self, current_scope, signal_match):
        vcd_name = signal_match.group(1)
        sig_name = signal_match.group(2)

        full_sig_name = current_scope + "." + sig_name
        print(full_sig_name)

        if full_sig_name in self.excluded_sigs:
            return

        self.sig_name_2_vcd_name[full_sig_name] = vcd_name
        self.vcd_name_2_sig_name[vcd_name] = full_sig_name        


    def extract_sig_values(self, vcd_file):
        for sig_name in self.sig_name_2_vcd_name.keys():
            self.sigs_values[sig_name] = []

        dumpvars_found = False

        while vcd_file:
            vcd_line = vcd_file.readline()
            if (vcd_line == "" ):
                return

            dumpvars = re.match(self.dumpvars_match, vcd_line)
            new_time = re.match(self.new_time_match, vcd_line)
            sig_value = re.match(self.sig_value_match, vcd_line)

            if dumpvars:
                dumpvars_found = True
                current_time = 0

            if not dumpvars_found:
                continue

            if new_time:
                current_time = new_time.group(1)

            if sig_value:
                signal_value = sig_value.group(1)
                signal_vcd_name = sig_value.group(2)
                if signal_vcd_name in self.vcd_name_2_sig_name:
                    signal_name = self.vcd_name_2_sig_name[signal_vcd_name]
                    self.sigs_values[signal_name].append((int(current_time), signal_value))
                else:
                    # we currently get here for expended vector signals (i.e. [x[3]])
                    continue 



            

        
