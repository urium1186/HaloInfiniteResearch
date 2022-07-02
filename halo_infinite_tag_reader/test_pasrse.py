import codecs
import json
import pathlib

from configs.config import Config
from halo_infinite_tag_reader.readers.materialstyles import MaterialStyles
from halo_infinite_tag_reader.varnames import map_alt_name_id

# search_regions_names()
"""
print(' Scale data Block : ' + getGUID('ACFD51FE7847FF625430C3A86CA923A0'))
print(' Mesh data Block : ' + getGUID('9D84814AB442EEFBAC56C9A3180F53E6'))
print(' Mesh meta data block : ' + getGUID('97c4fa677D4E3D88a2f794b7f893ff8d'))
print(' Entry for the parts : ' + getGUID('2973dd1080487fe09ab78bbcee273225'))

filename = Config.BASE_UNPACKED_PATH + '__chore\\pc__\\materials\\generic\\base\\human\\leather\\leather_bomber\\hum_base_leather_bomber_gradientmask{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()
# parse_bitm.toJson()
print("parse_bitm")


filename = Config.BASE_UNPACKED_PATH + '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_normal{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()
# parse_bitm.toJson()
print("parse_bitm")

filename = Config.BASE_UNPACKED_PATH + '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_rohg{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()
# parse_bitm.toJson()
print("parse_bitm")


filename = Config.BASE_UNPACKED_PATH + '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_gradientmask{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()
# parse_bitm.toJson()
print("parse_bitm")



filename = Config.BASE_UNPACKED_PATH + 'materials\\generic\\base\\___blank\\___blank___.materialswatch'
#parse_mwsw = Swatch(filename)
#parse_mwsw.load()
# parse_mwsw.toJson()
print("parse_mwsw")

filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartan_armor\\coatings\\olympus\\oly_mil_stone_green.materialpalette'
#parse_mwpl = MaterialPalette(filename)
#parse_mwpl.load()
# parse_mwpl.toJson()
print("parse_mwpl")

filename = Config.BASE_UNPACKED_PATH + '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles'
#parse_mwsy = MaterialStyles(filename)
#parse_mwsy.load()
print("parse_mwsy")

# search_regions_names()

filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartan_armor\\materials\\olympus\\armfor\\armfor_001\\olympus_spartan_l_armfor_001_s001.material'
#parse_mat = Material(filename)
#parse_mat.load()
# parse_mat.toJson()
print("parse_mat")


filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartans\\spartans.render_model'
parse_mode = RenderModel(filename)
#parse_mode.load()
#parse_mode.getMeshXLod()
# parse_mat.toJson()
print("parse_mode")

filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\storm_fp\\storm_fp.render_model'
parse_mode = RenderModel(filename)
#parse_mode.load()
# parse_mat.toJson()
print("parse_mode")

filename = Config.BASE_UNPACKED_PATH + 'objects\\weapons\\pistol\\magnum\\magnum.render_model'
parse_mode = RenderModel(filename)
#parse_mode.load()
# parse_mat.toJson()
print("parse_mode")

filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartan_armor\\spartan_armor.render_model'
parse_mode = RenderModel(filename)
parse_mode.load()
"""
# parse_mat.toJson()
print("parse_mode")


filename = Config.BASE_UNPACKED_PATH + '__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\olympus\\olympus_spartan_style{ct}.materialstyles'

dict_core = {
    'iron_eagle_spartan_style{ct}': "eag",
    'lone_wolves_spartan_style{ct}': "wlv",
    'mc117_spartan_style{ct}': "mc117",
    'olympus_spartan_style{ct}': "olympus",
    'reach_spartan_style{ct}': "reach",
    'samurai_spartan_style{ct}': "samurai"

}

for path in pathlib.Path(Config.SPARTAN_STYLE_PATH).rglob('*spartan_style{ct}.materialstyles'):
    #continue
    with open(path, 'rb') as f:
        filename = path

        parse_mwsy = MaterialStyles(filename)
        parse_mwsy.load()
        print("------------------------" + dict_core[path.stem] + "------------------------")

        for i in range(parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childrenCount):
            temp_palette = parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childs[i]

            # print(temp_palette['palette'].path)

            parse_mwsy.default_style = i
            parse_mwsy.toJson()
            coat_file_name = dict_core[path.stem] + '____' + parse_mwsy.json_base['name']

            if map_alt_name_id.keys().__contains__(coat_file_name):
                coat_file_name = map_alt_name_id[coat_file_name]
            else:
                depo = 1
            saveTo = Config.EXPORT_JSON + coat_file_name + '.json'
            with open(saveTo, 'wb') as fw:
                json.dump(parse_mwsy.json_base, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
                fw.close()

        f.close()
print("parse_mwsy")
