import os
import sys
import re

# wip: better structured vcd reader

class VcdReader:
    def __init__(self, valid_path):
        self.scope_begin_match = r"^\$scope\s*([^ ]+)\s*([^ ]+)\s*\$end"
        self.scope_end_match = r"\$upscope\s*\$end"

        self.signal_match = r"\$var.*\$end"
        self.simple_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*\$end"
        self.vector_sig_match = r"([^ ]+)\s*([a-zA-Z0-9_]+)\s*(\[[0-9]+\:[0-9]+\]*)\s*\$end"

        self.new_time_match = r"^#([0-9]+)"
        self.sig_value_match = 

        self.extract_vcd_file(valid_path)

    def extract_vcd_file(self, valid_path):
        with open(valid_path, "r") as vcd_file:
            self.sig_name_2_vcd_name = {}
            self.vcd_name_2_sig_name = {}
            self.extract_scopes(vcd_file)
            print(self.sig_name_2_vcd_name)

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

            if scope_begin:
                new_scope_name = scope_begin.group(2)
                prefix = current_scope + "." if current_scope != "" else ""
                self.extract_scopes(vcd_file, prefix + new_scope_name)

            if scope_end:
                return

            if sig and simple_sig:
                vcd_name = simple_sig.group(1)
                sig_name = simple_sig.group(2)
                self.sig_name_2_vcd_name[current_scope + "." + sig_name] = vcd_name
                self.vcd_name_2_sig_name[vcd_name] = current_scope + "." + sig_name

            if sig and vector_sig:
                vcd_name = vector_sig.group(1)
                sig_name = vector_sig.group(2)
                self.sig_name_2_vcd_name[current_scope + "." + sig_name] = vcd_name
                self.vcd_name_2_sig_name[vcd_name] = current_scope + "." + sig_name

            if (not (vector_sig or simple_sig or scope_begin or scope_end)):
                pass
                #print("Unsupported line: ", vcd_line)

    def extract_values(self):
        pass
