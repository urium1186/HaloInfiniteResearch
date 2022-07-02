from exporters.model.model_exporter import ModelExporter
from configs.config import Config
from halo_infinite_tag_reader.model import Model

"""
filename = Config.BASE_UNPACKED_PATH + 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist'
parse_string_list = StringList(filename)
parse_string_list.load()

filename = Config.BASE_UNPACKED_PATH + MultilingualUnicodeStringList.test_path
parse_mult_lang_string_list = MultilingualUnicodeStringList(filename)
parse_mult_lang_string_list.load()


filename = Config.BASE_UNPACKED_PATH + 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist[3_string_list_resource]'
parse_string_list_r = StringListResource(filename)
parse_string_list_r.load()



filename = Config.BASE_UNPACKED_PATH + 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist[0_string_list_resource]'
full_header = FullHeader()
with open(filename, 'rb') as f:
    full_header.readIn(f)
    f.close()
"""
"""
filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartan_armor\\spartan_armor.render_model'
parse_render_model = RenderModel(filename)
parse_render_model.load()

filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartan_armor\\spartan_armor.model'
parse_model = Model(filename, parse_render_model)
parse_model.load()

exporter = ModelExporter(parse_model)
exporter.export()


filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartans\\spartans.render_model'
parse_render_model = RenderModel(filename)
parse_render_model.load()


filename = Config.BASE_UNPACKED_PATH + 'objects\\characters\\spartans\\spartans.model'
parse_model = Model(filename, parse_render_model)
parse_model.load()
exporter = RenderModelExporter(parse_render_model)
exporter.export_by_regions = True
exporter.export()

exporter = ModelExporter(parse_model)
exporter.export()
"""

filename = Config.BASE_UNPACKED_PATH + '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model'
filename = Config.BASE_UNPACKED_PATH + '__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.model'
#filename = Config.BASE_UNPACKED_PATH + '__chore\\gen__\\objects\\characters\\marine\\9b04ff325d614e30{g}.model'
parse_model = Model(filename)
parse_model.load()
parse_model.loadRenderModel()

"""
exporter = RenderModelExporter(parse_model.render_model)
exporter.export_by_regions = True
exporter.export()
"""
exporter = ModelExporter(parse_model)
exporter.export()
# parse_mat.toJson
#if __name__ == "__main__":

#exporter = RenderModelExporter(parse_render_model)
#exporter.export()
# parse_mat.toJson()
print("parse_mode")