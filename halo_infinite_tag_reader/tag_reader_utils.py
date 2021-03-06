import os
import pathlib
import json
import shutil
import sys

from configs.config import Config


def createDirAltNameID(in_dir: str):
    dict_return = {}
    for path in pathlib.Path(in_dir).rglob('info_*.json'):
        with open(path, 'rb') as f:
            data = json.load(f)
            filename = path.stem.split('info_')[-1]
            if data['CommonData']['Type'] != "ArmorCoating":
                continue
            altName = data['CommonData']['AltName']
            key = filename.split('-')[2] + "____" + altName
            if not dict_return.keys().__contains__(key):
                dict_return[key] = filename
            else:
                debug = ""

            f.close()

    return dict_return


def compareRegion(region_ko: {}, region_ok: {}):
    if region_ko['material'] != region_ok['material']:
        return False
    if region_ko['layers'].__len__() != region_ok['layers'].__len__():
        return False

    for i in range(region_ko['layers'].__len__()):
        s_p_t_ko = region_ko['layers'][i]['swatch']
        s_p_t_ok = region_ok['layers'][i]['swatch'].replace(".png", "")
        if s_p_t_ko.find(s_p_t_ok) == -1:
            return False

    return True


def getBinaryRepresentation(bytes):
    a = bytearray(bytes)
    b = bin(int.from_bytes(a, byteorder=sys.byteorder))
    print(b)
    return b

def access_4bits(data, num):
    # access 4 bits from num-th position in data
    # c = access_4bits(b, 4)
    return bin(int(data, 2) >> num & 0b1111)


def replaceSwatchIdByTex(json_data):
    dict_id_tax = {}
    for swatch in json_data['swatches']:
        dict_id_tax[swatch['swatchId']] = swatch['normalPath']

    for reg_key in json_data['regionLayers']:
        for layer_i in range(json_data['regionLayers'][reg_key]['layers'].__len__()):
            if dict_id_tax.keys().__contains__(json_data['regionLayers'][reg_key]['layers'][layer_i]['swatch']):
                json_data['regionLayers'][reg_key]['layers'][layer_i]['swatch'] = dict_id_tax[
                    json_data['regionLayers'][reg_key]['layers'][layer_i]['swatch']]

    return json_data


def search_regions_names():
    path = "J:\\Games\\Halo Infinite Stuf\\Web-Json\\analizar\\"
    corre = "corre_002-001-olympus-81647ac6.json"
    error = "error_002-001-olympus-81647ac6.json"
    data_ok = None
    data_ko = None
    with open(path + corre, 'rb') as f:
        data_ok = json.load(f)
        f.close()
    with open(path + error, 'rb') as f:
        data_ko = json.load(f)
        f.close()
    map_names = {"ko": "ok"}
    asd = [""]
    asd.__contains__("kjklj")
    regions_name = data_ok['regionLayers'].keys()
    data_ko = replaceSwatchIdByTex(data_ko)
    data_ok = replaceSwatchIdByTex(data_ok)
    for region_name_ko in data_ko['regionLayers']:
        if not regions_name.__contains__(region_name_ko):
            for region_name_ok in data_ok['regionLayers']:
                if not regions_name.__contains__(region_name_ko):
                    if compareRegion(data_ko['regionLayers'][region_name_ko], data_ok['regionLayers'][region_name_ok]):
                        map_names[region_name_ko] = region_name_ok

    print(map_names)
    print("________----------________")


def checkFileExistInUE5Project(path):
    full_path = Config.UE5_PROJECT_IMPORTED_PC_PATH + path + '.uasset'
    if not os.path.isfile(full_path):
        print(full_path)
        texture_path = Config.EXPORTED_TEXTURE_PATH + path + '{pc}.bitmap.tga'
        if os.path.isfile(texture_path):
            tempTempTextPath = Config.EXPORTED_TEXTURE_PATH + "tempMove\\"
            new_texture_path = tempTempTextPath + path + '.tga'
            if not os.path.isfile(new_texture_path):
                new_dir_path = new_texture_path.replace(new_texture_path.split("\\")[-1], '')
                if not os.path.exists(new_dir_path):
                    os.makedirs(new_dir_path, exist_ok=True)
                shutil.copyfile(texture_path, new_texture_path)
                print(new_texture_path)
    else:
        debug = 1


def getContentEntryByRefIndex(conten: [], ref_index):
    count = 0
    entry_found = None
    for i, entry in enumerate(conten):
        if entry.ref_index == ref_index:
            count = count + 1
            entry_found = i
    if count > 1:
        print(count)
    return entry_found


def createTree(entries: [], index_parent):
    for i, entry in enumerate(entries):
        print(entry)


def analizarCabecera(fh, execute=False):
    if not execute:
        return
    types_map = {}
    a = []
    a.__len__()
    content_tree = {}
    root = None
    dict_type = {}
    createTree(fh.content_table.entries, -1)
    return
    for index_ref in range(fh.data_table.entries.__len__()):
        temp = getContentEntryByRefIndex(fh.content_table.entries, index_ref)
        if fh.data_table.entries[index_ref].offset_type == 2:
            debug = 1
        if dict_type.keys().__contains__(fh.data_table.entries[index_ref].offset_type):
            dict_type[fh.data_table.entries[index_ref].offset_type].append(fh.data_table.entries[index_ref])
        else:
            dict_type[fh.data_table.entries[index_ref].offset_type] = [fh.data_table.entries[index_ref]]

    debug = 2

    for entry in fh.content_table.entries:
        key = entry.hash.guid + ' -- ' + str(entry.parent_index)
        if entry.parent_index != -1:
            p_i = getContentEntryByRefIndex(fh.content_table.entries, entry.parent_index)
            fh.content_table.entries[p_i].childs.append(entry)
            fh.content_table.entries[entry.parent_index].childs2.append(entry)
        else:
            root = entry
        if types_map.keys().__contains__(key):
            types_map[key].append(entry)
        else:
            types_map[key] = [entry]

    for entry in fh.content_table.entries:
        k = 1

    print('asd')
