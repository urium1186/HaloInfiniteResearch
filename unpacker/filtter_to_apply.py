FILE_TYPE_EXT_FILTTER = {
    'max_size_to_load': 15,
    'min_size_to_load': 15,
}

count_file_mapped = []
count_file_mapped_not = []
count_file_mapped_exp = []
count_file_mapped_error = []
map_tag_names = {}

def validString(in_string: str) -> bool:
    # if (temp.__contains__('spartan_armor') or temp.__contains__('gear')):
    # if (temp.__contains__('pc__/objects/characters/spartan_armor/bitmaps/')):
    # if (temp.__contains__('materials/generic/')):
    # if (temp.__contains__('__chore/pc__/shaders/')):
    # if (temp.__contains__('coatings')):
    # if (temp.__contains__('objects')) or (temp.__contains__('pc__')):
    # if (temp.__contains__('objects/characters')):
    # if (temp.__contains__('string')):
    # if (temp.__contains__('brute_atriox')):
    #return in_string.__contains__('color_black{pc}.bitmap')
    #return (not (in_string.__contains__('[') and in_string.__contains__(']'))) and (not (in_string.__contains__('{') and in_string.__contains__('}'))) # not in_string.__contains__('{ds}')
    #return (not (in_string.__contains__('[') and in_string.__contains__(']'))) and ((in_string.__contains__('{') and in_string.__contains__('}'))) # not in_string.__contains__('{ds}')
    return (not (in_string.__contains__('[') and in_string.__contains__(']'))) and (in_string.__contains__('weapons\\rifle\\provoker\\provoker'))





def isInRange(in_value, in_init_min=0, in_init_max=1000000000):
    min = in_init_min
    max = in_init_max + 20
    return min <= in_value <= max
