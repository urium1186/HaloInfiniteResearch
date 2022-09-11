import os

import numpy as np

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
    t_tag_group = grouptag # .replace(' ', '')
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
        elif t_tag_group == 'shdv' or t_tag_group == 'shbc':
            path_to_find = f"{base_path}{path}{plataform}.{ext}"
            if not os.path.isfile(path_to_find):
                path_to_find = path_to_find.replace('__chore\\gen__\\','__chore\\gen__\\pc__\\')
                if not os.path.isfile(path_to_find):
                    debug = 1
                else:
                    return path_to_find
                """
                print(grouptag)
                print(path)
                print(path_to_find)
                """
                debug = 1
            else:
                return path_to_find

        elif t_tag_group == 'mwsy':
            extra = '{ct}'
            path_to_find = f'{base_path}__chore\\gen__\\{path}{extra}.{ext}'
            if not os.path.isfile(path_to_find):
                return ''
            else:
                return path_to_find
        else:
            path_to_find = f'{base_path}__chore\\gen__\\{path}.{ext}'
            if not os.path.isfile(path_to_find):
                return ''
            else:
                return path_to_find
            debug = 1
    else:
        return path_to_find


    return ''


"""
point = [x,y,z] and ref = [x,y,z] and the radius should be a float.
"""


def inSphere(point, ref, radius):
    # Calculate the difference between the reference and measuring point
    diff = np.subtract(point, ref)

    # Calculate square length of vector (distance between ref and point)^2
    dist = np.sum(np.power(diff, 2))

    # If dist is less than radius^2, return True, else return False
    return dist < radius ** 2
