import codecs
import io
import json
import os.path
import pathlib
from collections import OrderedDict

from commons.common_utils import resolvePathFile
from commons.debug_utils import *
from commons.tag_group_extension_map import map_ext_not
from configs.config import Config

from tag_reader.headers.ver.tag import Tag
from tag_reader.readers.bitmap import Bitmap
from tag_reader.readers.material import Material
from tag_reader.readers.materialpalette import MaterialPalette
from tag_reader.readers.materialstyles import MaterialStyles
from tag_reader.readers.model import Model
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.readers.render_model import RenderModel
from tag_reader.readers.stringlist import StringList
from tag_reader.readers.swatch import Swatch
from tag_reader.tag_reader_utils import readStringInPlace
from tag_reader.var_names import map_alt_name_id, getMmr3HashFromInt, TAG_NAMES, getMmr3HashIntFrom


def evaluateTag(p_tag):
    #if p_tag.ZoneSetInfoHeader.ZoneSetCount1 == 1:
    #    return True
    return False
    if p_tag.header.ZoneSetSize - 16 < 80:
        return True

    rest_l_data = p_tag.header.ZoneSetSize - 16

    if rest_l_data == 16:
        return True

    ref_4_l = p_tag.ZoneSetInfoHeader.ZoneSetCount1 * 16
    if rest_l_data == ref_4_l + 4:
        return True

    if p_tag.ZoneSetInfoHeader.ZoneSetListOffset1 != 0:
        return True

    r_d = rest_l_data - ref_4_l
    #count_ = divmod(r_d, p_tag.ZoneSetInfoHeader.ZoneSetListOffset)

    ref_pair_l = p_tag.ZoneSetInfoHeader.ZoneSetListOffset * 8

    if count_[1] == 0:
        return True
    return False
    if p_tag.ZoneSetInfoHeader.ZoneSetListOffset1 == 1:
        return True

    if p_tag.ZoneSetInfoHeader.ZoneSetListOffset1 != 0:
        return True
    return False


def recursiveTags(p_tag: Tag, p_filename: str, p_tag_zone_list, recursive_list: [], pcount):
    pcount.append(1)
    ##print(pcount.__len__())
    if pcount.__len__() == 1933:
        debug = True
    if p_tag.TagDependencyList.__len__()>0:
        for dep in p_tag.TagDependencyList:

            bin_stream = io.BytesIO(p_tag.StringTable)
            path = readStringInPlace(bin_stream, dep.NameOffset, True)
            path_full = resolvePathFile(path,dep.GroupTagReverse)
            if path_full != '':
                key = path_full.split('\\')[-1]
                if p_tag_zone_list.keys().__contains__(key):
                    continue
                if recursive_list.__contains__(key):
                    continue

                with open(path_full, 'rb') as f:
                    in_tag = Tag(f)
                    f.close()
                parse_g = ReaderFactory.create_reader(path_full.replace(Config.BASE_UNPACKED_PATH,''))
                parse_g.load()

                recursiveTags(in_tag, path_full, p_tag_zone_list, recursive_list, pcount)

            debug = 1
    else:
        key = p_filename.split('\\')[-1]
        """ 
        if key.__contains__('bitmap'):
            temp_bitm = Bitmap(p_filename.replace(Config.BASE_UNPACKED_PATH,''))
            temp_bitm.load()
        """
        #int_hash = getMmr3HashIntFrom(key)
        if not recursive_list.__contains__(key):
            recursive_list.append(key)

        if evaluateTag(p_tag):
            return

        p_tag_zone_list[p_filename.split('\\')[-1]] = (
        f"{p_tag.ZoneSetInfoHeader.ZoneSetCount}-{p_tag.ZoneSetInfoHeader.ZoneSetCount1}-" \
        f"{p_tag.ZoneSetInfoHeader.ZoneSetListOffset}-{p_tag.ZoneSetInfoHeader.ZoneSetListOffset1}" \
        f" | ZL: {p_tag.header.ZoneSetSize - 16} DC: {p_tag.header.DependencyCount} TRC: {p_tag.header.TagReferenceCount}" \
        f"--- NRxDC: {p_tag.ZoneSetInfoHeader.ZoneSetListOffset >= p_tag.header.DependencyCount}" \
        f"--- NRxTRC: {p_tag.ZoneSetInfoHeader.ZoneSetListOffset <= p_tag.header.TagReferenceCount}" \
        f"--- NRx0: {p_tag.ZoneSetInfoHeader.ZoneSetListOffset == 0} : " \
        f"{p_tag.ZoneSetInfoHeader.ZoneSetListOffset == p_tag.header.TagReferenceCount == p_tag.header.DependencyCount == 0}"
        , p_tag)



def run_recursive_tag_in_paths():
    global p, filename, tag, f, parse_g
    for p in test_path_r:
        filename = Config.BASE_UNPACKED_PATH + p
        tag = None
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                tag = Tag(f)
                f.close()
            recursiveTags(tag, filename, tag_zone_list, r_path_list, count)
        else:
            print(f'no existe {filename}')



def run_recursive_reader_in_paths():
    global p, filename, tag, f, parse_g
    for p in test_path_r:
        filename = Config.BASE_UNPACKED_PATH + p
        tag = None
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                tag = Tag(f)
                f.close()
            parse_g = ReaderFactory.create_reader(filename.replace(Config.BASE_UNPACKED_PATH, ''))
            parse_g.load_recursive = True
            parse_g.load()
            continue
        else:
            print(f'no existe {filename}')

def onInstanceLoad(instance):
    if instance.tagDef.N == 'marker groups':
        for  child in instance.childs:
            for sub_ch in child['markers'].childs:
                r_i = sub_ch['region index'].value
                p_i = sub_ch['permutation index'].value
                n_i = sub_ch['node index'].value
                if n_i == -1:
                    debug = True
                if r_i != -1:
                   if not (p_i == n_i == -1):
                       debug = True
                elif p_i != -1:
                   if not (r_i == n_i == -1):
                       debug = True
                elif n_i != -1:
                   if not (r_i == p_i == -1):
                       debug = True



        #print(instance)

""""""


def run_in_paths():
    global p, filename, tag, f, parse_g
    for p in test_path:
        filename = Config.BASE_UNPACKED_PATH + p
        tag = None
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                tag = Tag(f)
                f.close()
            parse_g = ReaderFactory.create_reader(filename.replace(Config.BASE_UNPACKED_PATH, ''))
            parse_g.load()
            key = filename.split('\\')[-1]
            # int_hash = getMmr3HashIntFrom(key)
            if not r_path_list.__contains__(key):
                r_path_list.append(key)
            if evaluateTag(tag):
                continue
        else:
            print(f'no existe {filename}')



filename = '__chore\\gen__\\compositions\\mainmenu_customization\\camera{g}.camera_animation_graph'
filename = '__chore\\gen__\\compositions\\mainmenu_customization\\mainmenu_customization{trim}.composition'
filename = 'objects\\characters\\spartan_armor\\spartan_armor.model_animation_graph'
filename = 'objects\\characters\\storm_masterchief\\damage_effects\\wraith_board_melee.effect'
#filename = 'objects\\vehicles\\forerunner\\forerunner_vtol\\fx\\boarding\parts\\boarding_bits.particle'
filename = '__chore\\pc__\\shaders\\default_bitmaps\\arrays\white{pc}.bitmap'

filename = 'objects\\characters\\spartan_armor\\spartan_armor.model_animation_graph'
filename = 'objects\\coatings\\materials\\cvw_7_layered.material'

#
filename = '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles'
filename = '__chore\\gen__\\shaders\\bytecode\\3a4\\f04d0c92e2c0fb434bcbbadaa51bc.shader_root_signature'
filename = '__chore\\gen__\\shaders\\bytecode\\ffe\\9549cd680282f0b704a503b96b920_pc.shader_bytecode'
filename = 'objects\\weapons\\pistol\\magnum\\magnum.render_model'
filename = '__chore\\gen__\\pc__\\shaders\\surfaces\\cvw\\matsys\\cvw_matsys_l7{10}_448{pc}.shadervariant'
filename = '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.render_model'
filename = '__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.render_model'

filename = '__chore\\gen__\\shaders\\bytecode\\ffe\\9549cd680282f0b704a503b96b920_pc.shader_bytecode'
filename = 'ui\\olympus\\hud\\weapons\\brute\\disruptor\\hip_reticle_disruptor.cui_screen'
filename = 'objects\\characters\\spartan_armor\\spartan_armor.biped'
#filename = '__chore/ds__/shaders/default_bitmaps/bitmaps/color_black{ds}.bitmap'
filename = '__chore/pc__/shaders/default_bitmaps/bitmaps/color_black{pc}.bitmap'
#filename = 'fx/library_olympus/levels/mp/nar/sn_02/mp02_200/_parts/nar_m02200_sun_particle_flare.particle'
filename = 'objects\\characters\\spartan_armor\\spartan_armor.render_model'
filename = 'levels\\design\\example_room\\devices\\control_example_2\\control_example_2.render_model'
#filename = 'objects\\characters\\spartan_armor\\customization\\samurai.customizationthemeconfiguration'
#filename = 'objects\\characters\\spartan_armor\\customization\\olympus.customizationthemeconfiguration'
#filename = 'objects\\characters\\spartan_armor\\customization\\reach.customizationthemeconfiguration'
#filename = 'objects\\characters\\spartan_armor\\materials\\samurai\\shoulderpad\\shoulderpad_004\\samurai_spartan_r_shoulderpad_004_s001.material'
#filename = 'objects\\characters\\spartan_armor\\spartan_armor.frame_event_list'
#filename = 'objects\\characters\\spartan_armor\\spartan_armor.model_animation_graph'
#filename = 'objects\\characters\\spartan_armor\\spartan_armor.biped'
#filename = 'objects\\characters\\spartan_armor\\spartan_armor.biped'
#filename = 'objects\\characters\\drill_sergeant_with_face\\drill_sergeant_with_face.biped'
#filename = '__chore\\gen__\\objects\\characters\\drill_sergeant_with_face\\2c57aca7124a4d7b{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\drill_sergeant_with_face\\2c57aca7124a4d7b{g}.render_model'
print(getMmr3HashIntFrom("samurai_004_render:samurai_spartan_r_shoulderpad_004_s001MatSG"))
print(getMmr3HashIntFrom("Title"))

parse = ReaderFactory.create_reader(filename)
# 1073741824
#tag_inst = parse.readParameterByName('global tag ID')
#hash = getMmr3HashFromInt(tag_inst.value)
#if TAG_NAMES.keys().__contains__(hash):
#    debu = TAG_NAMES[hash]

#parse.load_recursive = True
parse.AddSubForOnInstanceLoad(onInstanceLoad)
parse.load()
exit(0)
#json_temp = parse.toJson(True)
for anim in parse.first_child['animations'].childs:
    parse.readAnimationFuctionData(anim)

print(filename)
print(len(map_ext_not))
exit(0)
test_path = [
    '__chore\\gen__\\compositions\\mainmenu_customization\\camera{g}.camera_animation_graph',
    '__chore\\gen__\\compositions\\mainmenu_customization\\mainmenu_customization{trim}.composition',
    'objects\\characters\\spartan_armor\\spartan_armor.model_animation_graph',
    'objects\\characters\\storm_masterchief\\damage_effects\\wraith_board_melee.effect',
    'objects\\vehicles\\forerunner\\forerunner_vtol\\fx\\boarding\parts\\boarding_bits.particle',
    '__chore\\pc__\\shaders\\default_bitmaps\\arrays\white{pc}.bitmap',
    'objects\\characters\\spartan_armor\\materials\\olympus\\armfor\\armfor_001\\olympus_spartan_l_armfor_001_s001.material',
    'objects\\characters\\spartan_armor\\spartan_armor.model_animation_graph',
    'objects\\coatings\\materials\\cvw_7_layered.material',

    '__chore\\gen__\\pc__\\shaders\\surfaces\\cvw\\matsys\\cvw_matsys_l7{10}_448{pc}.shadervariant',
    '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles',
    '__chore\\gen__\\shaders\\bytecode\\3a4\\f04d0c92e2c0fb434bcbbadaa51bc.shader_root_signature',
    '__chore\\gen__\\shaders\\bytecode\\ffe\\9549cd680282f0b704a503b96b920_pc.shader_bytecode',
    'objects\\weapons\\pistol\\magnum\\magnum.render_model',

    '__chore\\gen__\\shaders\\bytecode\\ffe\\9549cd680282f0b704a503b96b920_pc.shader_bytecode',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_01\\hum_base_fabric_oriental_pattern_01_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_04\\hum_base_fabric_oriental_pattern_04_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_09\\hum_base_fabric_oriental_pattern_09_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\leather\\leather_bomber\\hum_base_leather_bomber_gradientmask{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_rohg{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_gradientmask{pc}.bitmap',
    'materials\\generic\\base\\___blank\\___blank___.materialswatch',
    'objects\\characters\\spartan_armor\\coatings\\olympus\\oly_mil_stone_green.materialpalette',
    '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles',
    'objects\\characters\\spartan_armor\\materials\\olympus\\armfor\\armfor_001\\olympus_spartan_l_armfor_001_s001.material',
    'objects\\characters\\spartans\\spartans.render_model',
    'objects\\characters\\storm_fp\\storm_fp.render_model',
    'objects\\weapons\\pistol\\magnum\\magnum.render_model',
    'objects\\characters\\spartan_armor\\spartan_armor.render_model',
    '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles',
    '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model',
    '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.render_model',
    '__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.model',
    '__chore\\gen__\\objects\\characters\\marine\\9b04ff325d614e30{g}.model',
    'objects\\characters\\spartans\\spartans.model',
    'objects\\characters\\spartans\\spartans.render_model',
    'objects\\characters\\spartan_armor\\spartan_armor.model',
    'objects\\characters\\spartan_armor\\spartan_armor.render_model',
    'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist',
]

test_path_r = [
    'objects\\characters\\spartan_armor\\spartan_armor.model',
    #'objects\\characters\\spartans\\spartans.model',
    #'objects\\characters\\storm_fp\\storm_fp.model',
    'objects\\weapons\\pistol\\magnum\\magnum.render_model',
    '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model',
    #'__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.model',
    'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist'
             ]
tag_zone_list = {}

filename = 'objects\\characters\\spartans\\spartans.render_model'
render_model_0 = RenderModel(filename)
#render_model_0.load()

filename = 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist'

parse_string_list = StringList(filename)
#parse_string_list.load()





r_path_list = []
count = []

#run_recursive_tag_in_paths()
#exit(0)

#run_in_paths()
run_recursive_reader_in_paths()
# search_regions_names()
"""
#print(' Scale data Block : ' + getGUID('ACFD51FE7847FF625430C3A86CA923A0'))
#print(' Mesh data Block : ' + getGUID('9D84814AB442EEFBAC56C9A3180F53E6'))
#print(' Mesh meta data block : ' + getGUID('97c4fa677D4E3D88a2f794b7f893ff8d'))
#print(' Entry for the parts : ' + getGUID('2973dd1080487fe09ab78bbcee273225'))
"""
#print(len(map_CUID))
#print(len(debug_dict))
#print(len(debug_dict_1))
#print(len(debug_hash))

_debug_DataBlock = OrderedDict(sorted(debug_DataBlock.items()))
_debug_TagStruct = OrderedDict(sorted(debug_TagStruct.items()))
_debug_DataReference = OrderedDict(sorted(debug_DataReference.items()))
_debug_TagDependency = OrderedDict(sorted(debug_TagDependency.items()))
_debug_data_ref_zoneInfo = OrderedDict(sorted(debug_data_ref_zoneInfo.items()))


filename = 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist'

parse_string_list = StringList(filename)
parse_string_list.load()
"""
'__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model',
'__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.model',
'__chore\\gen__\\objects\\characters\\marine\\9b04ff325d614e30{g}.model',
'objects\\characters\\spartans\\spartans.model',
"""
filename = 'objects\\characters\\spartans\\spartans.render_model'
render_model_0 = RenderModel(filename)
render_model_0.load()

filename = '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model'
parse_model = Model(filename)
parse_model.load()

filename = '__chore\\pc__\\shaders\\default_bitmaps\\bitmaps\\color_red{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()

filename = '__chore\\pc__\\materials\\generic\\base\\human\\leather\\leather_bomber\\hum_base_leather_bomber_gradientmask{pc}.bitmap'
tag_bitm = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_bitm = Tag(f)
    f.close()

parse_bitm = Bitmap(filename)
parse_bitm.load()
"""
# parse_bitm.toJson()
#print("parse_bitm")
"""

filename = '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_normal{pc}.bitmap'
tag_bitm_1 = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_bitm_1 = Tag(f)
    f.close()

parse_bitm_1 = Bitmap(filename)
parse_bitm_1.load()
"""
# parse_bitm.toJson()
#print("parse_bitm")
"""
filename = '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_rohg{pc}.bitmap'
tag_bitm_2 = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_bitm_2 = Tag(f)
    f.close()

parse_bitm_2 = Bitmap(filename)
parse_bitm_2.load()
# parse_bitm.toJson()
#print("parse_bitm")


filename = '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_gradientmask{pc}.bitmap'
parse_bitm_3 = Bitmap(filename)
parse_bitm_3.load()
# parse_bitm.toJson()
#print("parse_bitm")
"""

"""
filename = 'materials\\generic\\base\\___blank\\___blank___.materialswatch'
tag_mwsw = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_mwsw = Tag(f)
    f.close()
parse_mwsw = Swatch(filename)
parse_mwsw.load()
# parse_mwsw.toJson()
#print("parse_mwsw")

filename = 'objects\\characters\\spartan_armor\\coatings\\olympus\\oly_mil_stone_green.materialpalette'
tag_mwpl = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_mwpl = Tag(f)
    f.close()
parse_mwpl = MaterialPalette(filename)
parse_mwpl.load()
# parse_mwpl.toJson()
#print("parse_mwpl")

filename = '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles'
tag_mwsy = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_mwsy = Tag(f)
    f.close()
parse_mwsy = MaterialStyles(filename)
parse_mwsy.load()
#print("parse_mwsy")

# search_regions_names()

filename = 'objects\\characters\\spartan_armor\\materials\\olympus\\armfor\\armfor_001\\olympus_spartan_l_armfor_001_s001.material'
#tag_mat = None
#with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
#    tag_mat = Tag(f)
#    f.close()
parse_mat_1 = Material(filename)
parse_mat_1.load()
# parse_mat.toJson()
#print("parse_mat")


filename = 'objects\\characters\\spartans\\spartans.render_model'
tag_mode = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_mode = Tag(f)
    f.close()
parse_mode = RenderModel(filename)
parse_mode.load()
#parse_mode.getMeshXLod()
# parse_mat.toJson()
#print("parse_mode")



filename = 'objects\\characters\\storm_fp\\storm_fp.render_model'
tag_mode_1 = None
#with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
#    tag_mode_1 = Tag(f)
#    f.close()
parse_mode = RenderModel(filename)
parse_mode.load()
# parse_mat.toJson()
#print("parse_mode")

filename = 'objects\\weapons\\pistol\\magnum\\magnum.render_model'
tag_mode_2 = None
with open(Config.BASE_UNPACKED_PATH + filename, 'rb') as f:
    tag_mode_2 = Tag(f)
    f.close()
parse_mode_2 = RenderModel(filename)
parse_mode_2.load()
# parse_mat.toJson()
#print("parse_mode")

filename = 'objects\\characters\\spartan_armor\\spartan_armor.render_model'
parse_mode_3 = RenderModel(filename)
parse_mode_3.load()
"""
"""
# parse_mat.toJson()
#print("parse_mode")
_bitmap_id_usage = OrderedDict(sorted(bitmap_id_usage.items()))

filename = '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles'
dict_core = {
        'iron_eagle_spartan_style{ct}': "eag",
        'lone_wolves_spartan_style{ct}': "wlv",
        'mc117_spartan_style{ct}': "mc117",
        'olympus_spartan_style{ct}': "olympus",
        'reach_spartan_style{ct}': "reach",
        'samurai_spartan_style{ct}': "samurai"

    }

##print(debug_hash)
##print(debug_TagStruct)
_debug_TagStruct_Type = OrderedDict(sorted(debug_TagStruct_Type.items()))
for path in pathlib.Path(Config.SPARTAN_STYLE_PATH).rglob('*spartan_style{ct}.materialstyles'):
    #continue
    with open(path, 'rb') as f:
        filename = str(path).replace(Config.BASE_UNPACKED_PATH, '')

        parse_mwsy = ReaderFactory.create_reader(filename)
        parse_mwsy.load()
        ##print("------------------------" + dict_core[path.stem] + "------------------------")

        for i in range(parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childrenCount):
            temp_palette = parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childs[i]

            # #print(temp_palette['palette'].path)

            parse_mwsy.default_style = i
            parse_mwsy.toJson()
            coat_file_name = dict_core[path.stem] + '____' + parse_mwsy.json_base['name']

            if map_alt_name_id.keys().__contains__(coat_file_name):
                coat_file_name = map_alt_name_id[coat_file_name]
            else:
                depo = 1
            saveTo = Config.EXPORT_JSON+'coating\\' + coat_file_name + '.json'
            with open(saveTo, 'wb') as fw:
                json.dump(parse_mwsy.json_base, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
                fw.close()

        f.close()
#print("parse_mwsy")
print("fin")

if __name__ == "__main__":
    print('comienzo')