# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:46:19 2023

@author: Naz
"""

import os
import re

origin = os.getcwd()
work_folder = os.path.join(origin,"../db/outputs")

def role_check(file_name):
    if re.match(r"^e[0-9]+",file_name):
        if re.match(r"^e[0-9]+m",file_name):
            role = "electrophile-anion"
        elif re.match(r"^e[0-9]+$",file_name):
            role = "electrophile-neutral"
        else:
            role = "electrophile"
    elif re.match(r"^nu[0-9]+",file_name):
        if re.match(r"^nu[0-9]+p",file_name):
            role = "nulceophile-cation"
        elif re.match(r"^nu[0-9]+$",file_name):
            role = "nucleophile-neutral"
        else:
            role = "electrophile"
    else:
        role = "na"
    return role

def append_dictionary(dictionary, key, text_list):
    if  key not in dictionary.keys():
        dictionary[key] = []        
        dictionary[key].append(text_list)
    else :
        dictionary[key].append(text_list)
    # print(dictionary)

def get_fragments(file_name, string_list):
    result = {}
    with open(file_name,"r") as file:
        status = "search"
        active = -1
        buffer = []
        for idx, line in enumerate(file):
            if status == "search":
                for i in range(len(string_list)):
                    start = string_list[i][0]
                    if start in line:  
                        status = "write"
                        active = i
                        start_idx = idx
 
            if status == "write" and idx != start_idx:
                if string_list[active][1] not in line:
                    buffer.append(line)
                else:                     
                    append_dictionary(result, string_list[active][0], buffer)
                    
                    with open ("buffer.txt","a") as f:
                        f.write(str(start_idx))
                        f.write(" ".join(buffer))
                        f.write("\n\n")
                    print(buffer)
                    buffer.clear()
                    status = "search"
    return result

               
       
for root, dirs, files in os.walk(work_folder):
    for name in files:
         if "e951a.log" in name:
            full_name = os.path.join(root,name)
            string_list = [
                           ("NATURAL BOND ORBITAL ANALYSIS",
                            "-------------------------------------------------------------------"),
                           ("NHO Directionality and ",
                            "Threshold for printing:")
                           ]
            fragment_dictionary = get_fragments(full_name, string_list)
            start = string_list[0][0]
            # print(start)
            # print(fragment_dictionary)
            items_number = len(fragment_dictionary)
            # l = fragment_dictionary.get(start)[0][1]
            # print(l)
            # for i in range(len(l)):   
            #     print(l[i])

            