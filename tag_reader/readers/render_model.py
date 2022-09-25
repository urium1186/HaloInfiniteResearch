import json

from tag_reader.readers.base_template import BaseTemplate
from tag_reader.tag_instance import TagInstance
from tag_reader.var_names import  getStrInMmr3Hash


class RenderModel(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mode')
        self.json_str_base = '{"skeletons":[]}'

    def load(self):
        super().load()

    def toJson(self):
        super().toJson()
        self.json_base = self.tag_parse.rootTagInst.toJson()['items'][0]
        self.json_base['skeletons'] = self.getBonesInfo()['skeletons']
        """
        self.json_base['name'] = self.tag_parse.rootTagInst.childs[0]['name'].toJson()
        self.json_base['name'] = self.tag_parse.rootTagInst.childs[0]['name'].toJson()
        regions = []
        regions_json = self.tag_parse.rootTagInst.childs[0]['regions'].toJson()
        # regions_json = self.tag_parse.rootTagInst.toJson()
        meshes = self.tag_parse.rootTagInst.childs[0]['meshes'].toJson()

        self.json_base['regions'] = regions_json
        self.json_base['meshes'] = meshes
        """
        self.json_str_base = json.dumps(self.json_base)
        return self.json_base

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
        #print(count)

    def onInstanceLoad(self, instance: TagInstance):
        super(RenderModel, self).onInstanceLoad(instance)
        if instance.tagDef.N == 'mesh lod chunks':
            xml = instance.content_entry.strXml()
            for funct in instance.childs:
                if funct['chunks'].byteLengthCount > 0:
                    with open(self.full_filepath, 'rb') as f:
                        funct['chunks'].readBinData(f)
                    temp = int.from_bytes(funct['chunks'].bin_data, byteorder="little", signed=True)
                    funct['chunks'].extra_data['value'] = temp

            debug = True

        elif instance.tagDef.N == "material index":
            if instance.parent.tagDef.N == 'parts':
                materials = instance.parent.parent.parent.parent.childs[0]['materials'].childs
                if instance.value != -1:
                    path = materials[instance.value]['material'].path
                    instance.extra_data = {'path': path}
                else:
                    debug = 1
        elif instance.tagDef.N == 'render geometry':
            debug = 0
        elif instance.tagDef.N == "meshes":
            debug = True
        elif instance.tagDef.N == "compression info":
            debug = 1
        pass