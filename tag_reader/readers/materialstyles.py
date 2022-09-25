
from tag_reader.readers.base_template import BaseTemplate
from configs.config import Config
from tag_reader.readers.materialpalette import MaterialPalette
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.var_names import Mmr3Hash_str, getStrInMmr3Hash


class MaterialStyles(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwsy')
        self.default_style = 0
        self.json_str_base = '{"grimeSwatch": "",' \
                             '"name": "",' \
                             '"emissiveAmount": 0,' \
                             '"swatches": [],' \
                             '"grimeAmount": 0,' \
                             '"regionLayers": {},' \
                             '"scratchAmount": 0' \
                             '}'

    def toJson(self):
        super().toJson()
        root = self.tag_parse.rootTagInst.childs[0]
        regions_names = []
        for entry in root['regions'].childs:
            regions_names.append(entry['name'].value)
        style_select = root['style'].childs[self.default_style]
        self.json_base["grimeSwatch"] = style_select['grime_type'].value
        self.json_base["name"] = style_select['palette'].path.split('\\')[-1]
        self.json_base["emissiveAmount"] = style_select['emissive_amount'].value
        self.json_base["grimeAmount"] = style_select['grime_amount'].value
        self.json_base["scratchAmount"] = style_select['scratch_amount'].value
        parse_mwpl = ReaderFactory.create_reader(style_select['palette'].path+".materialpalette") # Config.BASE_UNPACKED_PATH +
        parse_mwpl.load()
        parse_mwpl.toJson()
        self.json_base["swatches"] = parse_mwpl.json_base['swatches']
        regionLayers = {}
        for entry in style_select['regions'].childs:
            layers = []
            for lay in entry['layers'].childs:
                lay_d = {}
                lay_d['colorBlend'] = bool(lay['Color_Blend'].selected_index)
                lay_d['swatch'] = lay['name'].value
                lay_d['ignoreTexelDensity'] = bool(lay['Ignore_Texel_Density_Scalar'].selected_index)
                lay_d['normalBlend'] = bool(lay['Normal_Blend'].selected_index)
                """
                if lay_d['swatch'] == "00000000":
                    lay_d['swatch'] = ""
                """
                layers.append(lay_d)
            material = root['coatingMaterialSets'].childs[entry['Coating Material Set'].value]['coatingMaterialSet'].path
            material = material.split('\\')[-1]
            r_name = entry['name'].str_value
            regionLayers[r_name] = {"layers": layers,
                                     "material": material,
                                     "bodyPart": r_name,
                                        "name_data":entry['name'].toJson()
                                     }

        self.json_base["regionLayers"] = regionLayers
        #print(root)

    def onInstanceLoad(self, instance):
        super(MaterialStyles, self).onInstanceLoad(instance)
