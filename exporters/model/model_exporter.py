import io
import os

import numpy as np
import mathutils
import utils
from commons.debug_utils import vertx_data_arrays, fillDebugDict
from exporters.base_exporter import BaseExporter
from exporters.domain.domain_types import *
from exporters.model.render_model_exporter import RenderModelExporter
from exporters.to.fbx.export_to_fbx import FbxModel
from halo_infinite_tag_reader.readers.model import Model


class ModelExporter(BaseExporter):

    def __init__(self, model: Model):
        super(ModelExporter, self).__init__()
        self.render_model_exporter = None
        self.model = model
        self.render_model_inst = None
        self.filepath_export = 'J:/Games/Halo Infinite Stuf/Extracted/Converted/RE_OtherGames/HI/models/'

    def export(self):
        super(ModelExporter, self).export()
        if not self.model.is_loaded():
            self.model.load()
        if self.model.render_model is None:
            return
        
        nodes_data = self.model.render_model.getBonesInfo()
        instance = self.model.tag_parse.rootTagInst.childs[0]['variants']
        if self.render_model_exporter is None:
            self.render_model_exporter = RenderModelExporter(self.model.render_model)
        for ch in instance.childs:
            if not ch['name'].str_value == 'chief':
                continue
            fbx_model = FbxModel(p_skl_data=nodes_data)
            
            mesh_list = self.render_model_exporter.getMeshListByVariant(ch)

            for mesh in mesh_list:
                fbx_model.add(mesh)

            temp_str = self.model.full_filepath.split('\\')[-1].replace('.', '_')
            sub_dir = f"{temp_str}/variants/"
            os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
            save_path = f"{self.filepath_export}{sub_dir}{ch['name'].str_value}.fbx"
            fbx_model.export(save_path, True)
            print(f"Saved model to {save_path}")

        print('end Export')
