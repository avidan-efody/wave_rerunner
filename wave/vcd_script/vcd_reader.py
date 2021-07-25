#!/usr/intel/bin/python

import sys
import os 
import re 


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def check_file_names_are_valid(name,dir_n):
    #print (sys.argv[1].rsplit("/",1))
    res_or_path = find (name,dir_n)
    if res_or_path == None:
      print ('ERROR finding file name %s in dir %s\nPlease make sure the VCD file full path you enter is valid' % (name,dir_n))
      exit()
    else:
      return res_or_path

def extract_scope_module_name(scope_hier):    
    scope_s = scope_hier.split('.')
    if '.' in scope_hier:    
      #print (scope_s)
      if '' is scope_hier.split('.')[-1]:
        scope_h = scope_hier.split('.')[-2]
      else: 
        scope_h = scope_hier.split('.')[-1]
    else:
      scope_h = scope_hier
    #print (scope_h)
    return scope_h


def scope_finder(vcd_str_b,scope_hier):    
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
    if found_hier == 0:
      print ("Error wrong scope name, Please Fix and rerun")
#    print (vcd_str_b[scope_index])
    print ('signals extract from heiracy - ' + heiracy)
    return heiracy , scope_index

def var2dict(vcd_str_b,scope_index):
    var_dict = {}
    index = 1
    while "$var" in vcd_str_b[scope_index+index]:
        var_s = vcd_str_b[scope_index+index].split(" ")
        if ":" in var_s[-2]:
          var_dict[var_s[-4]] = var_s[-3] 
        else:
          var_dict[var_s[-3]] = var_s[-2] 
        index += 1
    print ('signals VCD symbols dictionary:')
    print (var_dict)
    return var_dict

def singlas_record2hash(vcd_str_b,heiracy,var_dict):
    current_time = 0
    signals_hash = {}
    start_hash_record = 0
    for line in vcd_str_b:
      m = re.search("^#",line)
      if m:
        current_time = line.replace("#","")
        #print (current_time)
      else:
        if start_hash_record:
          for key in var_dict.keys():
            if "end" not in line:
              if key in line:
                cureent_key = heiracy+"."+var_dict[key]
                #print (cureent_key)
                if cureent_key not in signals_hash.keys():
                  signals_hash[cureent_key] = list()
                #print (line.replace(key,""))
                new_item  = int(current_time) , line.replace(key,"").replace(" ","") 
                signals_hash[cureent_key].append(new_item) 
                #print (new_item)
      if "dumpvars" in line:
        start_hash_record = 1
    #print (signals_hash)
    return signals_hash

def remove_the_unselected_signals(var_d,signal_l):
    if signal_l:
      for key,value in dict(var_d).items():
         if value not in signal_l:
           del var_d[key]
           print '{',key,':',value,'} deleted from hash'
         
    

def extract_hash_from_wave_str(vcd_list,scope_hier,signal_l):
    vcd_j = "".join(vcd_list)
    vcd_s = vcd_j.split("\n")
    heiracy ,scope_index =  scope_finder(vcd_s,scope_hier)
    var_dict = var2dict(vcd_s,scope_index)
    remove_the_unselected_signals(var_dict,signal_l)
    signals_h = singlas_record2hash(vcd_s,heiracy,var_dict)
    return signals_h

def extract_lines_from_vcd_file(valid_path):
    f = open(valid_path,"r")
    wave_str_block = f.readlines()
    f.close()
    return wave_str_block

def help_f():
    print ('\nthe script must get 2 values\n')
    print ('-path or -p for full path to VCD file')
    print ('-scope or -s for scope scope.\ncan be any of the type below -\nblock_i/top.block_i./top.block_i\n')
    print ('additional feature:')
    print ('-signal or -sig for specific signals hash (-sig per signal)\n')
    print ('example for script cmd line-\n')
    print ('vcd_reader.py -p /path/sample.vcd -s sub_block\n')
    print ('vcd_reader.py -p /path/sample.vcd -s sub_block -sig clk -sig din\n')

    
def ui():
     if ('-h' or '-help') in sys.argv[1]:
       help_f()
     else:
      if ('-s' or '-scope') in sys.argv:
        #print (sys.argv[sys.argv.index('-s' or '-scope')+1])
        scope = sys.argv[sys.argv.index('-s' or '-scope')+1]
      else:
        print ("Error user didn't enter scope.\nPlesea see -h or -help for more detial")
        exit()
      if ('-p' or '-path') in sys.argv:
        #print (sys.argv[sys.argv.index('-p' or '-path')+1])
        path = sys.argv[sys.argv.index('-p' or '-path')+1]
      else:
        print ("Error user didn't enter path to VCD file.\nPlesea see -h or -help for more detial")
        exit()
      signal_list = list()
      for arg in sys.argv:
        if ('-sig' or '-signal') in arg:
          #print (sys.argv[sys.argv.index(arg)+1])
          signal_list.append(sys.argv[sys.argv.index(arg)+1])
      return scope , path , signal_list

        


def main():
    print("execute vcd reader")
    scope , path , signal_list = ui()
    valid_path = check_file_names_are_valid(path.rsplit("/",1)[1],path.rsplit("/",1)[0])
    print ('full path ' + valid_path + ' is valid')    
    wave_str_block = extract_lines_from_vcd_file(valid_path)
    s_hash = extract_hash_from_wave_str(wave_str_block,scope,signal_list)
    print ('signals hash:') 
    print s_hash
    print("vcd reader finish")

if __name__ == "__main__":
    main()            
