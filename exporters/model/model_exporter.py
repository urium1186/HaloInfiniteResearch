import io
import json
import os

import numpy as np
import mathutils
import utils
from commons.debug_utils import vertx_data_arrays, fillDebugDict
from configs.config import Config
from exporters.base_exporter import BaseExporter
from exporters.domain.domain_types import *
from exporters.model.render_model_exporter import RenderModelExporter
from exporters.to.fbx.export_to_fbx import FbxModel
from exporters.to.fbx.import_from_fbx import FbxModelImporter
from tag_reader.readers.model import Model
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.readers.render_model import RenderModel
from tag_reader.var_names import getMmr3HashFromInt, Mmr3Hash_str_iu


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
            temp_filename = f'{self.model.tag_parse.rootTagInst.childs[0]["render model"].path}.render_model'
            self.model.render_model = ReaderFactory.create_reader(temp_filename)
            # self.model.render_model.load_recursive = True
            self.model.render_model.load()

        
        nodes_data = self.model.render_model.getBonesInfo()
        instance = self.model.tag_parse.rootTagInst.childs[0]['variants']
        if self.render_model_exporter is None:
            self.render_model_exporter = RenderModelExporter(self.model.render_model)

        for ch in instance.childs:
            if False and not ch['name'].str_value == 'chief':
                continue
            if ch['regions'].childs[0]['parent variant'].value != -1:
                deb = True
            fbx_model = FbxModel(p_skl_data=nodes_data)
            runtime_regions = self.model.tag_parse.rootTagInst.childs[0]['runtime regions'].childs
            mesh_list = self.render_model_exporter.getMeshListByVariant(ch, runtime_regions)

            for mesh in mesh_list:
                mesh.bones_data = nodes_data
                fbx_model.add(mesh)

            temp_str = self.model.full_filepath.split('\\')[-1].replace('.', '_')
            sub_dir = f"{temp_str}/variants/"
            os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
            save_path = f"{self.filepath_export}{sub_dir}{ch['name'].str_value}.fbx"
            fbx_model.export(save_path, True)
            print(f"Saved model to {save_path}")
            #break

        print('end Export')

    def exportByJson(self, json_path):
        if not self.model.is_loaded():
            self.model.load()
        if self.model.render_model is None:
            temp_filename = f'{self.model.tag_parse.rootTagInst.childs[0]["render model"].path}.render_model'
            self.model.render_model = ReaderFactory.create_reader(temp_filename)
            # self.model.render_model.load_recursive = True
            self.model.render_model.load()

        nodes_data = self.model.render_model.getBonesInfo()
        with open(json_path, 'rb') as f:
            data = json.load(f)
        for k, v in data.items():
            if isinstance(v, dict):
                if v.keys().__contains__('IsRequired'):
                    if v['IsRequired']:
                        if v.keys().__contains__('DefaultOptionPath') and v['DefaultOptionPath'] != '':
                            file_name = v['DefaultOptionPath'].split('/')[-1]
                            temp_json_path = Config.WEB_DOWNLOAD_DATA+f'seasson 2\\info_{file_name}'
                            if os.path.exists(temp_json_path):
                                with open(temp_json_path, 'rb') as sub_f:
                                    sub_data = json.load(sub_f)
                                    if isinstance(sub_data, dict):
                                        if sub_data.keys().__contains__('RegionData'):
                                            region_data = sub_data['RegionData']
                                            data['CoreRegionData']['BaseRegionData'].extend(region_data)

        tag_id = data['TagId']
        tag_id_hash = getMmr3HashFromInt(data['TagId'])
        print(f"tag id hash {tag_id_hash}")
        variant_name_hash = getMmr3HashFromInt(data['VariantId']['m_identifier'])
        variant_name = variant_name_hash
        if Mmr3Hash_str_iu.keys().__contains__(variant_name_hash):
            variant_name = Mmr3Hash_str_iu[variant_name_hash]

        if self.render_model_exporter is None:
            self.render_model_exporter = RenderModelExporter(self.model.render_model)

        mesh_list = self.render_model_exporter.getMeshListByJson(data)
        fbx_model = FbxModel(p_skl_data=nodes_data)
        for mesh in mesh_list:
            mesh.bones_data = nodes_data
            fbx_model.add(mesh)
        file_name_temp= json_path.split('\\')[-1].replace('.json','')
        temp_str = self.model.full_filepath.split('\\')[-1].replace('.', '_')
        sub_dir = f"{temp_str}/variants/"
        os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
        save_path = f"{self.filepath_export}{sub_dir}{variant_name}_{file_name_temp}.fbx"
        fbx_model.export(save_path, True)
        print(f"Saved model to {save_path}")
