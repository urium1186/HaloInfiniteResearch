import os

from commons.tag_group_extension_map import map_ext
from configs.config import Config

map_CUID = {}


def getGUID(hex_string):
    temp_s = hex_string.upper()
    return '{' + temp_s[6:8] + temp_s[4:6] + temp_s[2:4] + temp_s[0:2] + "-" + temp_s[10:12] + temp_s[8:10] + "-" \
           + temp_s[12:16] + "-" + temp_s[16:20] + "-" + temp_s[21:32] + "}"


def resolvePathFile(path, grouptag, inSubPath=''):
    base_path = Config.BASE_UNPACKED_PATH
    if inSubPath != '':
        base_path = inSubPath
    path_to_find = base_path + path
    t_tag_group = grouptag.replace(' ', '')
    if not map_ext.keys().__contains__(t_tag_group):
        print(grouptag)
        print(path)
        print(path_to_find)
        return ''
    ext = map_ext[t_tag_group]
    plataform = '{pc}'
    path_to_find = path_to_find + '.' + ext
    if not os.path.isfile(path_to_find):
        if t_tag_group == 'bitm':
            path_to_find = f"{base_path}__chore\\pc__\\{path}{plataform}.{ext}"
            if not os.path.isfile(path_to_find):
                """
                print(grouptag)
                print(path)
                print(path_to_find)
                """
                debug = 1
            else:
                return path_to_find
        elif t_tag_group == 'shdv':
            path_to_find = f"{base_path}{path}{plataform}.{ext}"
            if not os.path.isfile(path_to_find):
                """
                print(grouptag)
                print(path)
                print(path_to_find)
                """
                debug = 1
            else:
                return path_to_find
        else:
            """
            print(grouptag)
            print(path)
            print(path_to_find)
            """
            debug = 1
    else:
        return path_to_find
    return ''