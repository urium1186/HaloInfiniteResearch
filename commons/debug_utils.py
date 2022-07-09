debug_TagStruct = {}
debug_TagStruct_Type = {}
debug_DataBlock = {}
debug_DataReference = {}
debug_TagDependency = {}
debug_dict = {}
debug_dict_1 = {}
debug_hash = {}


def fillDebugDict(main_key, name_key, p_debug_dict):
    if p_debug_dict.keys().__contains__(main_key):
        if p_debug_dict[main_key].keys().__contains__(name_key):
            p_debug_dict[main_key][name_key] += 1
        else:
            p_debug_dict[main_key][name_key] = 1
    else:
        p_debug_dict[main_key] = {name_key: 1}
