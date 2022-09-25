import io
import os
import re
import struct

from commons.tag_group_extension_map import ma_guid_ext_no_magic, ma_guid_ext_resource, map_ext, ma_guid_ext
from configs.config import Config
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.var_names import getMmr3HashFromInt, TAG_NAMES
from unpacker import filtter_to_apply
from unpacker.dao import tag_group_ext
from unpacker.filtter_to_apply import count_file_mapped_not, count_file_mapped, map_tag_names, count_file_mapped_error, \
    count_file_mapped_exp

"""

{'aset': 'objects\\weapons\\rifle\\provoker\\provoker',
 'vmed': 'fx\\library_olympus\\sandbox\\objects\\material_effects\\object_metal',
 'smed': 'sound\\005_sandbox\\013_physics\\013_physics\\_sound_material_effects_definitions\\013_phy_objects_unique_fusioncoil',
 'past': 'fx\\particles\\assets\\energy_sword_edge_01\\energy_sword_edge_01',
 'samp': 'ui\\olympus\\hud\\widgets\\reticle\\reticle'}
"""

def getMapExtension(decomp_save_data, t1e):
    f_t = io.BytesIO(decomp_save_data)
    bytes_unk = f_t.read(16)
    Magic = struct.unpack('4s', bytes_unk[0:4])[0]
    ext = t1e.save_path.split('.')[-1]
    if Magic != b'ucsh':
        if not ext.__contains__('chunk'):
            debug = 1
        ext1 = t1e.save_path.split('/')[-1].split('[')[1].split('.')[0]
        ext1 = ext1[ext1.index('_') + 1:]
        ext = t1e.save_path.split('/')[-1].split('[')[0].split('.')[-1]
        if ext1 == "bitmap_resource_handle]":
            print(f"bitmap_resource_handle] in {t1e.save_path}")
        key_ext = f"{ext1}|{ext}"
        if not ma_guid_ext_no_magic.__contains__(key_ext):
            ma_guid_ext_no_magic.append(key_ext)
            debug = True

        return
    bytes_unk_str = bytes_unk.hex()

    GUID_t = bytes_unk[8:16].hex()  # getGUID(bytes_unk_str)

    if ext.__contains__('['):
        ext = ext.split('[')[-1]  # .replace(']', '')
        ext = ext[ext.index('_') + 1:-1]

        if ma_guid_ext_resource.keys().__contains__(GUID_t):
            if not ma_guid_ext_resource[GUID_t].__contains__(ext):
                ma_guid_ext_resource[GUID_t].append(ext)
                debug = True

        else:
            ma_guid_ext_resource[GUID_t] = [ext]
        return
    tag_key = t1e.tag[::-1].decode("utf-8").replace(' ', '')
    if tag_key == 'aset':
        debug = True
    if map_ext.keys().__contains__(tag_key):
        if map_ext[tag_key] != ext:
            debug = True

    else:
        map_ext[tag_key] = ext

    if ma_guid_ext.keys().__contains__(GUID_t):
        if ma_guid_ext[GUID_t] != ext:
            debug = True

    else:
        if list(ma_guid_ext.values()).__contains__(ext):
            debug = True
        ma_guid_ext[GUID_t] = ext

    if ma_guid_ext[GUID_t] != map_ext[tag_key]:
        debug = True
    """
    with open(t1e.save_path, "wb") as f:
        f.write(decomp_save_data)
    """
def getPlataformExtra(t1e):
    result = re.findall(r'{(.+?)}', t1e.save_path)
    print(result)
    assert (t1e.save_path.__contains__('gen__/') or t1e.save_path.__contains__('pc__/') or t1e.save_path.__contains__('ds__/'))
    pass

def asd(decomp_save_data, t1e):
    filename = t1e.save_path.replace(Config.BASE_UNPACKED_PATH, '')
    hash_temp = t1e.hash_global_hex
    if filename.__contains__('color_black{'):
        debug = True
    if hash_temp == 'FFFFFFFF':
        return
    if hash_temp == 'F1D28FF0':
        return
    if TAG_NAMES.keys().__contains__(hash_temp):
        count_file_mapped.append(filename)
    else:
        count_file_mapped_not.append(filename)



    if map_tag_names.keys().__contains__(hash_temp):
        count_file_mapped_error.append(f"{hash_temp} - {filename} - {map_tag_names[hash_temp]}")
    else:
        map_tag_names[hash_temp] = filename
        if os.path.isfile(t1e.save_path):
            count_file_mapped_exp.append(f"{hash_temp} : {filename}" + '\n')

def asd_save(decomp_save_data, t1e):
    filename = t1e.save_path.replace(Config.BASE_UNPACKED_PATH, '')
    if filename.__contains__('{ds}'):
        debug = True
    try:
        parse = ReaderFactory.create_reader(filename)
        parse.tag_parse.byte_stream = io.BytesIO(decomp_save_data)
        tag_inst = parse.readParameterByName('global tag ID')
        parse.tag_parse.byte_stream.close()
        hash_temp = getMmr3HashFromInt(tag_inst.value)

        if TAG_NAMES.keys().__contains__(hash_temp):
            maped_path = TAG_NAMES[hash_temp]
            if maped_path != filename:
                debug = True
                filtter_to_apply.count_file_mapped_error.append(filename)
            else:
                if hash_temp == t1e.hash_global_hex:
                    debug = True
                filtter_to_apply.count_file_mapped.append(filename)
        else:
            filtter_to_apply.count_file_mapped_not.append(filename)

    except Exception as e:
        #print(e)
        if not (filename.__contains__('[') and filename.__contains__(']')):
            filtter_to_apply.count_file_mapped_exp.append(filename)
