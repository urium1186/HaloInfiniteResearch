from halo_infinite_tag_reader.base_template import BaseTemplate
from halo_infinite_tag_reader.common_tag_types import TagInstance
from configs.config import Config
from halo_infinite_tag_reader.render_model import RenderModel


class Model(BaseTemplate):

    def __init__(self, filename, p_render_model=None):
        super().__init__(filename, 'hlmt')
        self.debug = False
        self.json_str_base = '{"root":[]}'
        self.render_model = p_render_model

    def load(self):
        super().load()

    def loadRenderModel(self):
        filename = Config.BASE_UNPACKED_PATH + self.tag_parse.rootTagInst.childs[0]['render model'].path +'.render_model'
        self.render_model = RenderModel(filename)
        self.render_model.load()


    def onInstanceLoad(self, instance: TagInstance):
        variants = {}
        if instance.tagDef.N == 'variants':
            if not self.debug:
                return 
            temp_mesh_s = None
            temp_mesh_r = None
            if not (self.render_model is None):
                temp_mesh_s = self.render_model.tag_parse.rootTagInst.childs[0]['meshes'].childs
                temp_mesh_r = self.render_model.tag_parse.rootTagInst.childs[0]['regions'].childs

            for ch in instance.childs:
                variants[ch['name'].str_value] = {}
                regions = ch['regions'].childs
                for region in regions:
                    region_name = region['region name']
                    variants[ch['name'].str_value][region_name.str_value] = []
                    temp_mesh_r_i = -1
                    for rn in temp_mesh_r:
                        if rn['name'].value == region_name.value:
                            temp_mesh_r_i = rn['permutations'].childs
                            break
                    for per in region['permutations'].childs:
                        runtime_permutation = []
                        per_mesh_index = per['runtime permutation index'].value
                        if temp_mesh_s is None:
                            runtime_permutation.append(str(per_mesh_index))
                        else:
                            if per_mesh_index != -1 and not (temp_mesh_r_i is None):
                                per_mesh_index_1 =temp_mesh_r_i[per_mesh_index]['mesh_index'].value
                                for p in temp_mesh_s[per_mesh_index_1]['LOD_render_data'].childs[0]['parts'].childs:
                                    runtime_permutation.append(p['material_index'].extra_data['path'].split('\\')[-1])

                            else:
                                runtime_permutation.append(str(per_mesh_index))

                        variants[ch['name'].str_value][region_name.str_value].append((per['permutation name'].str_value, runtime_permutation))

            debug = 1