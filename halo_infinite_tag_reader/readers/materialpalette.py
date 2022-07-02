from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from configs.config import Config
from halo_infinite_tag_reader.readers.swatch import Swatch


class MaterialPalette(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwpl')
        self.json_str_base = '{"swatches":[]}'

    def load(self):
        super().load()

        for i, key in enumerate(self.tag_parse.rootTagInst.childs[0]['swatches'].childs):
            key['swatch'].path = self.tag_parse.full_header.string_table.entries[i].str_path


    def toJson(self):
        super().toJson()
        i = 0
        swatches = []
        for key in self.tag_parse.rootTagInst.childs[0]['swatches'].childs:
            parse_mwsw = Swatch(Config.BASE_UNPACKED_PATH + key['swatch'].path+'.materialswatch')
            parse_mwsw.load()
            parse_mwsw.default_color_variant = key['color'].value
            parse_mwsw.toJson()
            parse_mwsw.json_base['swatchId'] = key['name'].value
            parse_mwsw.json_base['emissiveAmount'] = key['emissiveAmount'].value
            parse_mwsw.json_base['emissiveIntensity'] = key['emissiveIntensity'].value
            parse_mwsw.json_base['roughness'] = key['roughnessOverride'].selected_index
            swatches.append(parse_mwsw.json_base)
        self.json_base['swatches'] = swatches
