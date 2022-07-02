from halo_infinite_tag_reader.base_template import BaseTemplate
from halo_infinite_tag_reader.tag_reader_utils import checkFileExistInUE5Project


class Swatch(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwsw')
        self.default_color_variant = ""
        self.json_str_base = '{"emissiveAmount": 0.0,\
                              "scratchRoughness": 0.0,\
                              "scratchBrightness": 0.0,\
                              "ior": 0.0,\
                              "colorVariant": {\
                                  "botColor": [],\
                                  "id": "",\
                                  "topColor": [],\
                                  "midColor": []\
                              },\
                              "normalPath": "",\
                              "normalTextureTransform": [],\
                              "scratchAlbedoTint": 0,\
                              "scratchColor": [],\
                              "metallic": 0.0,\
                              "scratchMetallic": 0.0,\
                              "roughnessBlack": 0.0,\
                              "colorVariantId": "",\
                              "scratchIor": 0.0,\
                              "roughnessWhite": 0.0,\
                              "roughness": 0.0,\
                              "groupName": "",\
                              "emissiveIntensity": 0.0,\
                              "colorGradientMap": "",\
                              "swatchId": ""\
                              }'

    def toJson(self):
        super().toJson()
        root = self.tag_parse.rootTagInst.childs[0]
        color_variant = None
        for color in root['color_variants'].childs:
            if color['name'].value == self.default_color_variant:
                color_variant = color
                break
        if color_variant is None:
            color_variant = root['color_variants'].childs[0]

        self.json_base["scratchRoughness"] = root['scratch_roughness'].value
        self.json_base["scratchBrightness"] = root['scratch_brightness'].value
        self.json_base["ior"] = root['ior'].value
        self.json_base["colorVariant"]["botColor"] = [color_variant['gradient_bottom_color'].r_value, color_variant['gradient_bottom_color'].g_value, color_variant['gradient_bottom_color'].b_value]
        self.json_base["colorVariant"]["topColor"] = [color_variant['gradient_top_color'].r_value, color_variant['gradient_top_color'].g_value, color_variant['gradient_top_color'].b_value]
        self.json_base["colorVariant"]["midColor"] = [color_variant['gradient_mid_color'].r_value, color_variant['gradient_mid_color'].g_value, color_variant['gradient_mid_color'].b_value]
        self.json_base["colorVariant"]["id"] = color_variant['name'].value
        self.json_base["normalPath"] = root['normal_detail_map'].path
        checkFileExistInUE5Project(self.json_base["normalPath"])
        self.json_base["normalTextureTransform"] = [root['normalTextureTransform'].x,root['normalTextureTransform'].y]
        self.json_base["scratchAlbedoTint"] = root['scratch_albedo_tint_spec'].value
        self.json_base["scratchColor"] = [root['scratch_color'].r_value,root['scratch_color'].g_value,root['scratch_color'].b_value]
        self.json_base["metallic"] = root['metallic'].value
        self.json_base["scratchMetallic"] = root['scratch_metallic'].value
        self.json_base["roughnessBlack"] = root['roughness_black'].value
        self.json_base["colorVariantId"] = color_variant['name'].value
        self.json_base["scratchIor"] = root['scratch_ior'].value
        self.json_base["roughnessWhite"] = root['roughness_white'].value
        #self.json_base["roughness"] = root['key'].value
        #self.json_base["groupName"] = root['key'].value
        #self.json_base["emissiveIntensity"] = root['key'].value
        self.json_base["colorGradientMap"] = root['color_gradient_map'].path
        checkFileExistInUE5Project(self.json_base["colorGradientMap"])
        #self.json_base["swatchId"] = root['key'].value
        #print("")

