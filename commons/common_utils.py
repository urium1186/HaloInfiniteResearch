import os
import pathlib

import numpy as np

from commons.logs import Log
from commons.tag_group_extension_map import map_ext, map_ext_not
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
    t_tag_group = grouptag  # .replace(' ', '')
    if not map_ext.keys().__contains__(t_tag_group):
        Log.Print(grouptag)
        print(path)
        print(path_to_find)
        map_ext_not[grouptag] = path
        return ''
    ext = map_ext[t_tag_group]
    path_to_find_ext = path_to_find + '.' + ext
    if os.path.isfile(path_to_find_ext):
        return path_to_find_ext

    path_f = path.replace('\\', '/')
    split = path_f.rpartition('/')
    if split is None:
        return ''
    base_path_r = base_path.replace('\\', '/')
    filter_gen_pc = f"{base_path_r}{split[0]}{split[1]}"
    for path in pathlib.Path(filter_gen_pc).rglob(f'{split[2]}*.{ext}'):
        if not (path.name.__contains__(split[2])):
            continue
        else:
            debug = True
            return str(path)
    if path_f.__contains__('gen__/'):
        gen_pc = split[0].replace('gen__/','gen__/pc__/')

        filter_gen_pc =  f"{base_path_r}{gen_pc}{split[1]}"
        for path in pathlib.Path(filter_gen_pc).rglob(f'{split[2]}*.{ext}'):
            if not (path.name.__contains__(split[2])):
                continue
            else:
                debug = True
                return str(path)
    else:
        filter_pc = f"{base_path_r}__chore/gen__/{split[0]}{split[1]}"
        for path in pathlib.Path(filter_pc).rglob(f'{split[2]}*.{ext}'):
            if not (path.name.__contains__(split[2])):
                continue
            else:
                return str(path)

        filter_pc = f"{base_path_r}__chore/pc__/{split[0]}{split[1]}"
        for path in pathlib.Path(filter_pc).rglob(f'{split[2]}*.{ext}'):
            if not (path.name.__contains__(split[2])):
                continue
            else:
                return str(path)






    print(f"not found {path_f}")
    return ''


def resolvePathFile_v1(path, grouptag, inSubPath=''):
    base_path = Config.BASE_UNPACKED_PATH
    if inSubPath != '':
        base_path = inSubPath
    path_to_find = base_path + path
    t_tag_group = grouptag  # .replace(' ', '')
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
                path_to_find = path_to_find.replace('__chore\\gen__\\', '__chore\\gen__\\pc__\\')
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
