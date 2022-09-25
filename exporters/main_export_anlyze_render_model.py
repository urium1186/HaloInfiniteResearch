import codecs
import pathlib
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

from tag_reader.readers.bitmap import Bitmap
from tag_reader.readers.model import Model
from tag_reader.readers.render_model import RenderModel

print(time.time())
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

filenames = [
    'objects\\characters\\spartan_armor\\spartan_armor.render_model',
    'objects\\characters\\spartans\\spartans.render_model',
    'objects\\characters\\storm_fp\\storm_fp.render_model',
    'objects\\weapons\\pistol\\magnum\\magnum.render_model',

]

#path_to_r_m = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\objects\\characters\\"
path_to_r_m = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\campaign\\__chore\\gen__\\objects\\characters\\"

for path in pathlib.Path(path_to_r_m).rglob('*.render_model'):
    #filename = str(path).replace("J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\","")
    filename = str(path).replace("J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\campaign\\","")
    print(filename)
    parse_render_model = RenderModel(filename)
    parse_render_model.load()
    exporter = RenderModelExporter(parse_render_model)
    exporter.debugAnalyzeMeshInfo()

print(artifact_on_all_comp)

print(time.time())
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)