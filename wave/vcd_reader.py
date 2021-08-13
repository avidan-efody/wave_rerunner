import os
import sys
import re

from wave.reader_base import ReaderBase

class VcdReader(ReaderBase):
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):
        self.vcd_path = wave_file #self.check_file_names_are_valid(wave_file)
        super().__init__(replay_blocks, wave_file, excluded_sigs, inputs_only)

    def extract_lines_from_vcd_file(self, valid_path):
        f = open(valid_path, "r")
        wave_str_block = f.readlines()
        f.close()
        return wave_str_block

    def extract_values_from_wave(self, replay_blocks, excluded_sigs, inputs_only):
        def extract_scope_module_name(scope_hier):
            scope_s = scope_hier.split('.')
            if '.' in scope_hier:
                # print (scope_s)
                if '' == scope_hier.split('.')[-1]:
                    scope_h = scope_hier.split('.')[-2]
                else:
                    scope_h = scope_hier.split('.')[-1]
            else:
                scope_h = scope_hier
            # print (scope_h)
            return scope_h

        def scope_finder(vcd_str_b, scope_hier):
            scope_index = None
            found_hier = 0
            hierarchy = ""
            scope_h = extract_scope_module_name(scope_hier)
            for line in vcd_str_b:
                if "$scope" in line:
                    line_s = line.split(" ")
                    if hierarchy == "":
                        hierarchy += line_s[-2]
                    else:
                        hierarchy += "." + line_s[-2]
                    if scope_h in line:
                        found_hier = 1
                        scope_index = vcd_str_b.index(line)
                        break
            if found_hier == 0 or scope_index is None:
                print("Error wrong scope name, Please Fix and rerun")
                exit()
            #    print (vcd_str_b[scope_index])
            print('signals extract from hierarchy - ' + hierarchy)
            return hierarchy, scope_index

        # scope_index holds the line # in which the scope starts
        def var2dict(vcd_str_b, scope_index):
            var_dict = {}
            index = 1
            while "$var" in vcd_str_b[scope_index + index]:
                var_s = vcd_str_b[scope_index + index].split()
                if ":" in var_s[-2]:
                    var_dict[var_s[-4]] = var_s[-3]
                else:
                    var_dict[var_s[-3]] = var_s[-2]
                index += 1
            print('signals VCD symbols dictionary:')
            print(var_dict)
            return var_dict

        def singlas_record2hash(vcd_str_b, hierarchy, var_dict):
            current_time = 0
            signals_hash = {}
            start_hash_record = 0
            for line in vcd_str_b:
                m = re.search("^#", line)
                if m:
                    current_time = line.replace("#", "")
                    # print (current_time)
                else:
                    if start_hash_record:
                        for key in var_dict.keys():
                            if "end" not in line:
                                if key in line:
                                    cureent_key = hierarchy + "." + var_dict[key]
                                    # print (cureent_key)
                                    if cureent_key not in signals_hash.keys():
                                        signals_hash[cureent_key] = list()
                                    # print (line.replace(key,""))
                                    new_item = int(current_time), line.replace(key, "").replace(" ", "").replace("b","")
                                    signals_hash[cureent_key].append(new_item)
                                    # print (new_item)
                if "dumpvars" in line:
                    start_hash_record = 1
            # print (signals_hash)
            return signals_hash

        def extract_hash_from_wave_str(vcd_list, scope_hier, excluded_sigs):
            vcd_j = "".join(vcd_list)
            vcd_s = vcd_j.split("\n")
            hierarchy, scope_index = scope_finder(vcd_s, scope_hier)
            sig_list = var2dict(vcd_s, scope_index)
            for sig in excluded_sigs:
                print("Removing excluded sig: ", sig, " from the list of signals to get from vcd")
                sig_list.pop(sig, None)         
            signals_h = singlas_record2hash(vcd_s, hierarchy, sig_list)
            return signals_h

        # scope = self.vcd.scope_by_name(replay_block)
        vcd_str = self.extract_lines_from_vcd_file(self.vcd_path)
        signal_values = {}

        for replay_block in replay_blocks:
            signal_values.update(extract_hash_from_wave_str(vcd_str, replay_block, excluded_sigs))

        print('signals hash:')
        print(signal_values)
        return signal_values