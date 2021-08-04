import os
import sys
import re

from reader_base import ReaderBase

class VcdReader(ReaderBase):
    def __init__(self, replay_block, wave_file,signal_list=[]):
        self.vcd_path = self.check_file_names_are_valid(wave_file)
        self.signal_list = signal_list
        super().__init__(replay_block, wave_file)


    def check_file_names_are_valid(self, path):
        def find(file_name, search_dir):
            for root, dirs, files in os.walk(search_dir):
                if file_name in files:
                    return os.path.join(root, file_name)

        # print (sys.argv[1].rsplit("/",1))
        if '/' in path:
            name , dir_n = path.rsplit("/", 1)[1], path.rsplit("/", 1)[0]
        else:
            name = path
            dir_n = sys.path[0]
            # print (dir_n)

        res_or_path = find(name, dir_n)
        if res_or_path == None:
            print('ERROR finding file name %s in dir %s\nPlease make sure the VCD file full path you enter is valid' % (
                name, dir_n))
            exit()
        else:
            return res_or_path

    def extract_values_from_wave(self, replay_block):
        def extract_lines_from_vcd_file(valid_path):
            f = open(valid_path, "r")
            wave_str_block = f.readlines()
            f.close()
            return wave_str_block

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
            heiracy = ""
            scope_h = extract_scope_module_name(scope_hier)
            for line in vcd_str_b:
                if "$scope" in line:
                    line_s = line.split(" ")
                    if heiracy == "":
                        heiracy += line_s[-2]
                    else:
                        heiracy += "." + line_s[-2]
                    if scope_h in line:
                        found_hier = 1
                        scope_index = vcd_str_b.index(line)
                        break
            if found_hier == 0 or scope_index is None:
                print("Error wrong scope name, Please Fix and rerun")
                exit()
            #    print (vcd_str_b[scope_index])
            print('signals extract from heiracy - ' + heiracy)
            return heiracy, scope_index

        def var2dict(vcd_str_b, scope_index):
            var_dict = {}
            index = 1
            while "$var" in vcd_str_b[scope_index + index]:
                var_s = vcd_str_b[scope_index + index].split(" ")
                if ":" in var_s[-2]:
                    var_dict[var_s[-4]] = var_s[-3]
                else:
                    var_dict[var_s[-3]] = var_s[-2]
                index += 1
            print('signals VCD symbols dictionary:')
            print(var_dict)
            return var_dict

        def singlas_record2hash(vcd_str_b, heiracy, var_dict):
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
                                    cureent_key = heiracy + "." + var_dict[key]
                                    # print (cureent_key)
                                    if cureent_key not in signals_hash.keys():
                                        signals_hash[cureent_key] = list()
                                    # print (line.replace(key,""))
                                    new_item = int(current_time), line.replace(key, "").replace(" ", "")
                                    signals_hash[cureent_key].append(new_item)
                                    # print (new_item)
                if "dumpvars" in line:
                    start_hash_record = 1
            # print (signals_hash)
            return signals_hash

        def remove_the_unselected_signals(var_d, signal_l):
            if signal_l:
                for key, value in dict(var_d).items():
                    if value not in signal_l:
                        del var_d[key]
                        print('{', key, ':', value, '} deleted from hash')

        def extract_hash_from_wave_str(vcd_list, scope_hier, signal_l):
            vcd_j = "".join(vcd_list)
            vcd_s = vcd_j.split("\n")
            heiracy, scope_index = scope_finder(vcd_s, scope_hier)
            var_dict = var2dict(vcd_s, scope_index)
            remove_the_unselected_signals(var_dict, signal_l)
            signals_h = singlas_record2hash(vcd_s, heiracy, var_dict)
            return signals_h

        # scope = self.vcd.scope_by_name(replay_block)
        wave_str_block = extract_lines_from_vcd_file(self.vcd_path)
        s_hash = extract_hash_from_wave_str(wave_str_block, self.replay_block, self.signal_list)
        print('signals hash:')
        print(s_hash)
        return s_hash