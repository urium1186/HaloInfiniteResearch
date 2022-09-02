import codecs
from datetime import datetime
import json
import os
import shutil
import time

import configs
from commons.debug_utils import normal_artifact_files, Intersection_meth3, Difference_meth3, artifact_on_all_comp, \
    vertx_data_arrays
from exporters.model.bitmap_exporter import BitmapExporter
from exporters.model.model_exporter import ModelExporter
from configs.config import Config
from exporters.model.render_model_exporter import RenderModelExporter
from exporters.to.fbx.import_from_fbx import FbxModelImporter
from exporters.to.image.export_to_img_pillow import ExportImgPillowImpl

from halo_infinite_tag_reader.readers.bitmap import Bitmap
from halo_infinite_tag_reader.readers.model import Model
from halo_infinite_tag_reader.readers.render_model import RenderModel

print(time.time())
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
"""
#filename = '__chore\\gen__\\objects\\characters\\jacob_keyes\\5c7777b9614e46b3{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\inquisitor\\889eab6be2c9348f{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\halsey\\d80c3413b6b7139d{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\cortana\\4bb7743c2a8ef0a9{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\civilian_mother\\66034be81ab43bdc{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\brute_atriox\\dc3fefb59fe7509b{g}.model'
filename = '__chore\\gen__\\objects\\characters\\brute\\d84ff668256ab6e8{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\pilot\\810314e64aa263ae{g}.model'
parse_model = Model(filename)
parse_model.load()

exporter = ModelExporter(parse_model)
exporter.export()

filename = 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist'
parse_string_list = StringList(filename)
parse_string_list.load()

filename = MultilingualUnicodeStringList.test_path
parse_mult_lang_string_list = MultilingualUnicodeStringList(filename)
parse_mult_lang_string_list.load()


filename = 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist[3_string_list_resource]'
parse_string_list_r = StringListResource(filename)
parse_string_list_r.load()



filename = 'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist[0_string_list_resource]'
full_header = FullHeader()
with open(filename, 'rb') as f:
    full_header.readIn(f)
    f.close()



# filename = 'objects\\characters\\spartan_armor\\spartan_armor.render_model'
filename = '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.render_model'
parse_render_model = RenderModel(filename)
parse_render_model.load()"""
"""
parse_render_model.toJson()
saveTo = Config.MODEL_EXPORT_PATH + 'spartan_armor_render_model.json'
with open(saveTo, 'wb') as fw:
    json.dump(parse_render_model.json_base, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
    fw.close()

exporter = RenderModelExporter(parse_render_model)

exporter.export()
"""
"""
# exporter.debugAnalyzeMeshInfo()
"""
filename = 'objects\\characters\\spartan_armor\\spartan_armor.model'
filename = '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model'

parse_model = Model(filename)
parse_model.load()
"""
parse_model.toJson()
saveTo = Config.MODEL_EXPORT_PATH + 'spartan_armor_model.json'
with open(saveTo, 'wb') as fw:
    json.dump(parse_model.json_base, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
    fw.close()
"""
exporter = ModelExporter(parse_model)
exporter.export()
"""
print(vertx_data_arrays)
debug = True


filename = 'objects\\characters\\spartans\\spartans.render_model'
parse_render_model = RenderModel(filename)
parse_render_model.load()

exporter = RenderModelExporter(parse_render_model)
exporter.export_by_regions = True
exporter.debugAnalyzeMeshInfo()
#exporter.export()


filename = 'objects\\characters\\spartans\\spartans.model'
parse_model = Model(filename, parse_render_model)
parse_model.load()

exporter = ModelExporter(parse_model)
exporter.export()

filename = '__chore\\gen__\\objects\\characters\\spartan_dinh\\28ca8142b9ac566d{g}.model'
filename = '__chore\\gen__\\objects\\characters\\spartan_eklund\\cf5c5fd3383d7f8c{g}.model'
#filename = '__chore\\gen__\\objects\\characters\\marine\\9b04ff325d614e30{g}.model'
parse_model = Model(filename)
parse_model.load()
parse_model.loadRenderModel()


exporter = RenderModelExporter(parse_model.render_model)
exporter.export_by_regions = True
exporter.export()

exporter = ModelExporter(parse_model)
exporter.export()
# parse_mat.toJson
"""
# if __name__ == "__main__":

# exporter = RenderModelExporter(parse_render_model)
# exporter.export()
# parse_mat.toJson()
"""
filename = '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_02\\hum_base_fabric_oriental_pattern_02_normal{pc}.bitmap'

parse_bitm = Bitmap(filename)
parse_bitm.load()

exporter = BitmapExporter(parse_bitm)
exporter.export()

filename = '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_01\\hum_base_fabric_oriental_pattern_01_gradientmask{pc}.bitmap'

parse_bitm = Bitmap(filename)
parse_bitm.load()

exporter = BitmapExporter(parse_bitm)
exporter.export()


"""
"""
filename = '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_01\\hum_base_fabric_oriental_pattern_01_normal{pc}.bitmap'

parse_bitm = Bitmap(filename)
parse_bitm.load()

exporter = BitmapExporter(parse_bitm)
exporter.export()

filename = '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\wrinkles\\hum_base_fabric_wrinkles_01_color{pc}.bitmap'
parse_bitm = Bitmap(filename)
parse_bitm.load()
exporter = BitmapExporter(parse_bitm)
exporter.export()

"""

"""
with open('../normals_posible_error_unpacked_nocompresed.txt') as f:
    faltan = f.readlines()
no_repeat = []
for p in faltan:
    pat =  p.replace('/','\\').replace('\n','').split('[')[0]
    pat = pat.replace(Config.BASE_UNPACKED_PATH,'')
    if no_repeat.__contains__(pat):
        continue
    no_repeat.append(pat)

    parse_bitm = Bitmap(pat)
    parse_bitm.load()
    exporter = BitmapExporter(parse_bitm)
    exporter.export()

artifact_on_no_comp = list(normal_artifact_files.keys())

difference = Difference_meth3(no_repeat, artifact_on_no_comp)
# print(inters)
print("parse_mode")

#normal_artifact_files = {}
mydir = Config.EXPORTED_TEXTURE_PATH_BASE + 'DDS\\'
shutil.rmtree(mydir)
mydir = Config.EXPORTED_TEXTURE_PATH_BASE + 'TGA\\'
shutil.rmtree(mydir)

path = 'J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\campaign\\__chore\\pc__\\materials\\generic\\base\\'
p = [os.path.join(dp, f)[len(path):].replace("\\", "/") for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn if f.endswith(".bitmap") and ".chunk" not in f and ".dds" not in f and "normal" in f ]

for path in p:
    x = path.replace('/','\\')
    temp_p = f"__chore\\pc__\\materials\\generic\\base\\{x}"
    parse_bitm = Bitmap(temp_p)
    parse_bitm.load()
    exporter = BitmapExporter(parse_bitm)
    exporter.export()
    """
"""
for path in artifact_on_all_comp:
    temp_p = path
    parse_bitm = Bitmap(temp_p)
    parse_bitm.load()
    exporter = BitmapExporter(parse_bitm)
    exporter.export()


difference_1 = Difference_meth3(artifact_on_all_comp, artifact_on_no_comp)
difference_1_2 = Difference_meth3(artifact_on_no_comp, artifact_on_all_comp)
difference_2 = Difference_meth3(artifact_on_all_comp, no_repeat)
difference_2_1 = Difference_meth3( no_repeat, artifact_on_all_comp )
difference_3 = Difference_meth3(difference_2, difference)
"""
print(artifact_on_all_comp)

print(time.time())
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)