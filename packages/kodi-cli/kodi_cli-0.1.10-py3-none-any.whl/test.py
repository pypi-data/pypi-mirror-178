from kodi_interface import KodiObj
from kodi_help_tester import get_input
import sys

def process_block(base_key: str, dict_block: dict, param_dict: dict, indent: int = 0):
    # print(f'  key: {base_key} dict_block: {dict_block}')
    for key, value in dict_block.items():
        if base_key:
            cur_key = f'{base_key}.{key}'
        else:
            cur_key = key
        key_type = str(type(value))
        key_type = key_type.replace("<class '","")
        key_type = key_type.replace("'>","")
        dict_key = f'{cur_key}!{indent}!{key_type}'
        # print(dict_key)
        if dict_key not in param_dict:
            print(f' Adding key: {dict_key}')
            param_dict[dict_key] = 0
        param_dict[dict_key] += 1
        # print(f'    cur_key: {cur_key}  value: {value}')
        if type(value) is str or type(value) is list:
            pass
        elif type(value) is dict:
            # print(f'  RECURSE: {cur_key}')
            process_block(cur_key, value, param_dict, indent+1)

def merge_to_master_dict(master_dict: dict, minor_dict):
    for key, value in minor_dict.items():
        if key not in master_dict:
            master_dict[key] = 0
        master_dict[key] += value

def output_key_list(key_dict: dict, caption: str):
    print()
    print(f'Keys for {caption}')
    print(f'  {"ref":5} {"type":8} {"key"}')
    print(f'  {"-"*5} {"-"*8} {"-"*50}')
    sorted_dict = dict(sorted(key_dict.items()))
    for key,value in sorted_dict.items():
        token = key.split("!")
        key_name = token[0]
        indent   = int(token[1])
        spacer = " "*(indent*2)
        val_type = token[2]
        print(f'  {value:5} {val_type:8} {spacer}{key_name}')
        # print(f'{key}')

def process_namespaces():
    parameter_keys = {}
    kodi_obj = KodiObj()
    namespaces = kodi_obj.get_namespace_list()
    for ns in namespaces:
        methods = kodi_obj.get_namespace_method_list(ns)
        ns_parameter_keys = {}
        for method in methods:
            method_definition = kodi_obj._namespaces[ns][method]
            parameters_list = method_definition.get('params', [])
            p_names = kodi_obj._get_parameter_names(parameters_list)
            print(f'Processing {ns}.{method}({p_names})')
            for param_item in parameters_list:
                process_block("", param_item, ns_parameter_keys)

        # load master list
        merge_to_master_dict(parameter_keys, ns_parameter_keys)
        print()
    output_key_list(parameter_keys, "Namespaces")

def process_references():
    print('Processing References...')
    parameter_keys = {}
    kodi_obj = KodiObj()
    references = kodi_obj._kodi_references
    reference_keys = {}
    process_block("", references, reference_keys)
    output_key_list(reference_keys, "References")

process_namespaces()
process_references()