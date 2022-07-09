from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from halo_infinite_tag_reader.common_tag_types import TagInstance
from halo_infinite_tag_reader.varnames import Mmr3Hash_str, getStrInMmr3Hash


class RenderModel(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mode')
        self.json_str_base = '{"skeletons":[]}'

    def load(self):
        super().load()

    def toJson(self):
        super().toJson()
        self.json_base['skeletons'] = self.getBonesInfo()['skeletons']

    def getBonesInfo(self):
        bones = {'skeletons': []}
        i = 0
        for bone_inst in self.tag_parse.rootTagInst.childs[0]['nodes'].childs:
            b_name = bone_inst['name'].value
            b_name = getStrInMmr3Hash(b_name)
            bone = {'name': b_name,
                    'parent': bone_inst['parent node'].value,
                    'first_child_node': bone_inst['first child node'].value,
                    'next_sibling_node': bone_inst['next sibling node'].value,
                    'scl': [1, 1, 1],
                    'rotq': [bone_inst['default rotation'].x, bone_inst['default rotation'].y,
                             bone_inst['default rotation'].z, bone_inst['default rotation'].w],
                    'pos': [bone_inst['default translation'].x, bone_inst['default translation'].y,
                            bone_inst['default translation'].z],
                    'rot': [0, 0, 0],
                    }
            i += 1
            bones['skeletons'].append(bone)
        return bones

    def getMeshXLod(self):
        count = 0
        for entry in self.tag_parse.rootTagInst.childs[0]['meshes'].childs:
            count = count + entry['LOD render data'].childrenCount
        print(count)

    def onInstanceLoad(self, instance: TagInstance):

        if instance.tagDef.N == "regions":
            for ch in instance.childs:
                print(ch["name"].str_value)

        elif instance.tagDef.N == "material_index":
            if instance.parent.tagDef.N == 'parts':
                materials = instance.parent.parent.parent.parent.childs[0]['materials'].childs
                if instance.value != -1:
                    path = materials[instance.value]['material'].path
                    instance.extra_data = {'path': path}
                else:
                    debug = 1
        elif instance.tagDef.N == 'render_geometry':
            debug = 0
        elif instance.tagDef.N == "meshes":
            temp_dict = {}
            for i, mesh in enumerate(instance.childs):
                temp_dict[i] = \
                mesh['LOD_render_data'].childs[0]['parts'].childs[0]['material_index'].extra_data['path'].split('\\')[
                    -1]

            for region in self.tag_parse.rootTagInst.childs[0]['regions'].childs:
                permutations = region['permutations'].childs
                for permutation in permutations:
                    m_index = permutation['mesh_index'].value
                    if m_index == -1:
                        continue
                    clone_index = instance.childs[m_index]['clone_index'].value
                    if temp_dict.keys().__contains__(m_index):
                        del temp_dict[m_index]
                    if clone_index == -1:
                        continue
                    if temp_dict.keys().__contains__(clone_index):
                        del temp_dict[clone_index]
            keys = list(temp_dict.keys())
            res_dict = {}
            for k in keys:
                if str(temp_dict[k]).__contains__('mc117'):
                    del temp_dict[k]
                else:
                    core = temp_dict[k].split('_')[0]
                    if res_dict.keys().__contains__(core):
                        res_dict[core].append(temp_dict[k])
                    else:
                        res_dict[core] = [temp_dict[k]]
            print(list(temp_dict.keys()))
            debug = 1
        elif instance.tagDef.N == "compression_info":
            debug = 1
        pass
