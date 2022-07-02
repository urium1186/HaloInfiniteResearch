import unreal
import json
import sys

import utils
import materials_utils


"""
REF
    material = unreal.load_asset('/Game/coatings/matsys/hwp_cvw_matsys_.hwp_cvw_matsys_')
    prop = temp.get_editor_property("MaterialLayersFunctions.Background.Background")
    layer0 = default_layers.get_editor_property('layers')[0]
    mat_expre = unreal.MaterialEditingLibrary.get_material_property_input_node(material,unreal.MaterialProperty.MP_BASE_COLOR)
    default_layers = mat_expre_layers[0].get_editor_property('default_layers'
    unreal.MaterialEditingLibrary.recompile_material(material)
    
    temp = unreal.load_asset('/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l7_Generic1.hwp_cvw_matsys_l7_Generic1')
    print(help(temp))
    
    unreal.MaterialEditingLibrary.delete_material_expression(material,unreal.MaterialExpressionMaterialAttributeLayers)
    unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionMaterialAttributeLayers,500,100)
    
    
    From that tutorial...

    pip-installing matplotlib
    
    If you installed the embedded distribution, just move to the Plugins/UnrealEnginePython/Binaries/Win64 directory in your terminal, and run:
    
    ./python.exe -m pip install --target . matplotlib
    
    (the --target . ensures the modules are not installed into the Lib/site-packages subdirectory)
    
"""

def log_hello_unreal():
    """
    logs hello unreal to
    """
    unreal.log_warning("Hello unreal")

def log_event_materials(MT_file):
    """
    logs hello unreal to
    """
    print(f"Hello unreal {MT_file}")

#log_hello_unreal()

ue_shaders_path = '/Game/coatings/matsys/toDuplicate/'
ue_generated_shaders_path = '/Game/coatings/genereted/'


def createGenericAsset(asset_path='', unique_name=True, asset_class=None, asset_factory=None):
    if unique_name:
        asset_path, asset_name = unreal.AssetToolsHelpers.get_asset_tools().create_unique_asset_name(
            base_package_name=asset_path, suffix='')
    #print(f"asset_name: {asset_name} asset_path {asset_path}")
    #print(
    #    f"asset in : {unreal.AssetRegistryHelpers.is_valid(unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(asset_path))}")
    # if not unreal.find_asset(asset_name) is None:
    # if not unreal.EditorAssetLibrary().does_asset_exist(asset_path=asset_path):
    if not unreal.AssetRegistryHelpers.is_valid(
            unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(asset_path)):
        path = asset_path.rsplit('/', 1)[0]
        name = asset_path.rsplit('/', 1)[1]
        temp = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=name, package_path=path,
                                                                       asset_class=asset_class, factory=asset_factory)
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name=name + 'd', package_path=path,
                                                                          original_object=temp)

    return unreal.load_asset(asset_path)


def createGenericAssetWithName(package_path='', name='', asset_class=None, asset_factory=None):
    # if not unreal.find_asset(asset_name) is None:
    # if not unreal.EditorAssetLibrary().does_asset_exist(asset_path=asset_path):
    asset_path = package_path + name
    if not unreal.AssetRegistryHelpers.is_valid(
            unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(asset_path)):
        temp = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=name, package_path=package_path,
                                                                       asset_class=asset_class, factory=asset_factory)
        return temp

    return unreal.load_asset(asset_path)


def get_asset_dict(asset_type=None, asset_name_in = ''):
    asset_list = None
    if asset_type:
        asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class(asset_type)
    else:
        asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    asset_dict = {}
    for asset in asset_list:
        asset_name = str(asset.asset_name)
        obj_path = asset.object_path
        if asset_name not in asset_dict:
            asset_dict[asset_name] = [str(obj_path)]
        else:
            asset_dict[asset_name].append(str(obj_path))

    return asset_dict

olympus_texture_root_path = '/Game/__chore/gen__/pc__/objects/characters/spartan_armor/bitmaps/olympus/'

def get_asset_texture_dict(part = ''):
    asset_list = None
    part_fix = part.split('_')[-1]
    unreal.log_error(part_fix)
    if part_fix.__contains__('belt'):
        part_fix = 'torso'
        unreal.log_error(part_fix)
    pack_path = olympus_texture_root_path + '' + part_fix + '/'+part_fix+'_001'
    #unreal.log(pack_path)
    #
    filter_texture = unreal.ARFilter(package_paths=[pack_path], class_names=[unreal.Name('Texture2D')])
    asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets(filter_texture)
    asset_dict = {}
    for asset in asset_list:
        asset_name = str(asset.asset_name)
        obj_path = asset.object_path
        if asset_name not in asset_dict:
            asset_dict[asset_name] = [str(obj_path)]
        else:
            asset_dict[asset_name].append(str(obj_path))

    return asset_dict



"""
_asg_control
_mask_0_control
_mask_1_control
_normal
Texture2D'/Game/__chore/gen__/pc__/objects/characters/spartan_armor/bitmaps/olympus/armfor/armfor_001/olympus_spartan_armfor_001_s001_normal.olympus_spartan_armfor_001_s001_normal'
"""


def duplicate_asset_in_path(path, mi_name, mtl_folder):
    editor_asset_library = unreal.EditorAssetLibrary
    mi_full_path = mtl_folder + '/' + mi_name
    #unreal.log_warning(mi_full_path)
    base_mtl_obj = unreal.load_asset(path)

    if editor_asset_library.does_asset_exist(mi_full_path):
        mi_asset = editor_asset_library.find_asset_data(mi_full_path).get_asset()
        #unreal.log_warning("Asset already exists")
        #unreal.log_warning(f": {mi_asset}")
    else:

        mi_asset = unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(asset_name=mi_name,
                                                                              package_path=mtl_folder,
                                                                              original_object=base_mtl_obj)
        unreal.log("Asset not exists")
        unreal.log_warning(f"Create Asset {mi_asset}")
    return mi_asset

def createMaterialISwatch(mi_name, mtl_folder, data):
    #unreal.log("---------------------------------------------------")
    mi_asset = duplicate_asset_in_path(ue_shaders_path + 'ML_WayPoint_Generic_Inst.ML_WayPoint_Generic_Inst', mi_name, mtl_folder)

    mi_asset = asignarMaterialISwatchBYData(mi_asset, data)
    # unreal.log_warning( dir(mi_asset))
    """
    unreal.log_warning(mi_asset.get_editor_property('parent'))
    unreal.log('vector_parameter_values')
    unreal.log_warning(mi_asset.get_editor_property('vector_parameter_values'))
    unreal.log('font_parameter_values')
    unreal.log_warning(mi_asset.get_editor_property('font_parameter_values'))
    unreal.log('scalar_parameter_values')
    # mi_asset.set_editor_property('scalar_parameter_values', [unreal.ScalarParameterValue(unreal.MaterialParameterInfo('metallic'),1)])
    unreal.log_warning(mi_asset.get_editor_property('scalar_parameter_values'))
    unreal.log('static_component_mask_parameter_values')
    unreal.log_warning(mi_asset.get_editor_property('static_component_mask_parameter_values'))
    unreal.log('static_switch_parameter_values')
    unreal.log_warning(mi_asset.get_editor_property('static_switch_parameter_values'))
    unreal.log('texture_parameter_values')
    unreal.log_warning(mi_asset.get_editor_property('texture_parameter_values'))
    unreal.log('parent')
    # unreal.log_warning( dir(mi_asset.get_editor_property('parent')))
    """
    return
    """
    MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mtl.get_asset())  # set parent material
    MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "metallic",
                                                                  1)
    """


global g_last_color_variants
g_last_color_variants = []

global default_color_variants
default_color_variants = []

def asignarMaterialISwatchBYData(m_swatch, data, association = unreal.MaterialParameterAssociation.GLOBAL_PARAMETER, index = -1):
    #unreal.log("---------------------------------------------------")
    #temps = f'association : {association}, index: {index}'
    #unreal.log(temps)

    #unreal.log("---------------------------------------------------")
    #unreal.log("---------asignarMaterialISwatchBYData--------------")
    """
     Set scalar values
    """
    scalar_keys = ['emissiveAmount', 'scratchRoughness', 'scratchBrightness', 'ior', 'emissiveAmount',
                   'scratchAlbedoTint', 'metallic', 'scratchMetallic', 'roughnessBlack', 'scratchIor',
                   'roughnessWhite', 'roughness', 'emissiveIntensity']
    scalar_values = []
    for i in range(len(scalar_keys)):
        scalar_values.append(unreal.ScalarParameterValue(unreal.MaterialParameterInfo(scalar_keys[i], association, index),
                                                         data[scalar_keys[i]]))
    m_swatch.set_editor_property('scalar_parameter_values', scalar_values)
    """
        Set texture values
       """
    texture_keys = ['normalPath', 'colorGradientMap']
    texture_params = []
    example = [
        '/Game/__chore/gen__/pc__/materials/generic/base/organic/dust/org_base_dust_01_normal.org_base_dust_01_normal',
        '/Game/__chore/gen__/pc__/materials/generic/base/organic/dust/org_base_dust_01_gradientmask.org_base_dust_01_gradientmask']

    for i in range(2):
        tex_path = data[texture_keys[i]]
        tex_path = tex_path.replace('.png', '')
        tex_path = '/Game/__chore/gen__/pc__/materials/generic/base/' + tex_path
        #unreal.log(f"Texture path: {tex_path}")
        #unreal.log_warning(f"Texture path: {example}")
        if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
            unreal.log_error("Can't find texture: " + tex_path)
            continue
        #unreal.log(f"Texture path: {tex_path} exist")
        tex_asset = unreal.EditorAssetLibrary.find_asset_data(tex_path).get_asset()
        texture_params.append(unreal.TextureParameterValue(unreal.MaterialParameterInfo(texture_keys[i], association, index), tex_asset))
        # unreal.TextureParameterValue(pi,unreal.Texture(outer=None, name='None'))

    m_swatch.set_editor_property('texture_parameter_values', texture_params)

    """
        Set Vector values
    """
    vector_params = []
    colorVariant_key = ['botColor', 'topColor', 'midColor']

    if 'colorVariant' in data.keys():
        colorVariants = data['colorVariant']
        g_last_color_variants.clear()
        for i in range(len(colorVariant_key)):
            temp_v = unreal.LinearColor(colorVariants[colorVariant_key[i]][0],
                                        colorVariants[colorVariant_key[i]][1],
                                        colorVariants[colorVariant_key[i]][2], 0
                                        )
            g_last_color_variants.append(temp_v)
            vector_params.append(unreal.VectorParameterValue(unreal.MaterialParameterInfo(colorVariant_key[i], association, index), temp_v))
    else:
        unreal.log_error('swatch Key colorVariant dont exist')
        unreal.log_error(g_last_color_variants)
        for i in range(len(colorVariant_key)):
            temp_v = g_last_color_variants[i]
            vector_params.append(
                unreal.VectorParameterValue(unreal.MaterialParameterInfo(colorVariant_key[i], association, index),
                                            temp_v))

    temp_v2 = unreal.LinearColor(
        data['normalTextureTransform'][0],
        data['normalTextureTransform'][1],
        0, 0)
    vector_params.append(unreal.VectorParameterValue(unreal.MaterialParameterInfo('normalTextureTransform', association, index),
                                                     temp_v2))
    m_swatch.set_editor_property('vector_parameter_values', vector_params)

    return m_swatch


"""
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l1_Generic.hwp_cvw_matsys_l1_Generic'
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l4_Generic.hwp_cvw_matsys_l4_Generic'
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l7_Generic.hwp_cvw_matsys_l7_Generic'
        MaterialFunctionMaterialLayerInstance'/Game/coatings/matsys/toDuplicate/ML_WayPoint_Generic_Inst.ML_WayPoint_Generic_Inst'
        MaterialFunctionMaterialLayerBlendInstance'/Game/coatings/matsys/toDuplicate/MLB_WayPoint_Generic_Inst.MLB_WayPoint_Generic_Inst'
        
        MaterialInstanceConstant'/Game/coatings/matsys/News/test/hwp_cvw_matsys_l1_Generic.hwp_cvw_matsys_l1_Generic'
"""
map_layer_ueasset = {
    "cvw_1_layered": '/Game/coatings/matsys/News/test/hwp_cvw_matsys_l1_Generic.hwp_cvw_matsys_l1_Generic',
    "cvw_4_layered": '/Game/coatings/matsys/News/test/hwp_cvw_matsys_l4_Generic.hwp_cvw_matsys_l4_Generic',
    "cvw_7_layered": '/Game/coatings/matsys/News/test/hwp_cvw_matsys_l7_Generic.hwp_cvw_matsys_l7_Generic',
    "layer_blend_instance": ""
}

class CoatingGeneralData:
    def __init__(self):
        self.grimeSwatch = ""
        self.emissiveAmount = 0.0
        self.grimeAmount = 0.0
        self.scratchAmount = 0.0
        self.swatches = []
        self.regionLayers = []
        self.name = ""

class RegionLayerParameterValues:
    def __init__(self):
        self.scalar_values = []
        self.texture_params = []
        self.vector_params = []
        self.sw_color_blend = True
        self.sw_ignore_texel_density = []
        self.sw_normal_blend = []
        self.material_instance = []
        self.coating_common_info = CoatingGeneralData()
        self.numbres_of_layers = 1

    def applyParameterValues(self):
        self.material_instance.set_editor_property('scalar_parameter_values', self.scalar_values)
        self.material_instance.set_editor_property('texture_parameter_values', self.texture_params)
        self.material_instance.set_editor_property('vector_parameter_values', self.vector_params)

    def stackParameterValuesInGrime(self, grimeSwid = None , swatches = None):
        if grimeSwid is None:
            grimeSwid = self.coating_common_info.grimeSwatch
        if swatches is None:
            swatches = self.coating_common_info.swatches

        temp_sw = get_swatch_in_by_id(swatches, grimeSwid)
        if temp_sw != {}:
            self.stackLayersISwatchBYData(data=temp_sw, index=7)
        else:
            unreal.log_error(f'En la capa grime, swatch con id: {grimeSwid} no existe !!!!!!!')
            parameter = unreal.MaterialParameterInfo('Amount', unreal.MaterialParameterAssociation.BLEND_PARAMETER,
                                                     6)
            self.scalar_values.append(unreal.ScalarParameterValue(parameter, 0))


    def stackParameterValuesInLayers(self, layers, swatches):
        for i in range(len(layers)):
            swid = layers[i]['swatch']
            sw_color_blend = layers[i]['colorBlend']
            sw_ignore_texel_density = layers[i]['ignoreTexelDensity']
            sw_normal_blend = layers[i]['normalBlend']
            temp_sw = get_swatch_in_by_id(swatches, swid)

            if temp_sw != {}:
                self.stackLayersISwatchBYData(data=temp_sw, index=i)
            else:
                unreal.log_error(f'En la capa {i}, swatch con id: {swid} no existe !!!!!!!')
                parameter = unreal.MaterialParameterInfo('Amount', unreal.MaterialParameterAssociation.BLEND_PARAMETER,
                                                         i-1)
                self.scalar_values.append(unreal.ScalarParameterValue(parameter, 0))

            if i > 0:
                parameterIndex = unreal.MaterialParameterInfo('Index',
                                                              unreal.MaterialParameterAssociation.BLEND_PARAMETER, i-1)
                self.scalar_values.append(unreal.ScalarParameterValue(parameterIndex, i))

        act_lay = len(layers)

        #unreal.log_warning(mi_asset.get_editor_property('static_switch_parameter_values'))
        if self.numbres_of_layers > act_lay:
            for j in range(self.numbres_of_layers-len(layers)):
                parameterAmount = unreal.MaterialParameterInfo('Amount', unreal.MaterialParameterAssociation.BLEND_PARAMETER, act_lay-1 + j)
                self.scalar_values.append(unreal.ScalarParameterValue(parameterAmount, 0))




    def stackLayersISwatchBYData(self, data, association = unreal.MaterialParameterAssociation.LAYER_PARAMETER, index = -1):
        #if (index == 4):
            #unreal.log_warning('Debug Data')
            #unreal.log_warning(data)
        """
         Set scalar values
        """
        scalar_keys = ['emissiveAmount', 'scratchRoughness', 'scratchBrightness', 'ior', 'emissiveAmount',
                       'scratchAlbedoTint', 'metallic', 'scratchMetallic', 'roughnessBlack', 'scratchIor',
                       'roughnessWhite', 'roughness', 'emissiveIntensity']
        scalar_values = []
        for i in range(len(scalar_keys)):
            scalar_values.append(
                unreal.ScalarParameterValue(unreal.MaterialParameterInfo(scalar_keys[i], association, index),
                                            data[scalar_keys[i]]))
        self.scalar_values += scalar_values

        """
            Set texture values
           """
        texture_keys = ['normalPath', 'colorGradientMap']
        texture_params = []
        example = [
            '/Game/__chore/gen__/pc__/materials/generic/base/organic/dust/org_base_dust_01_normal.org_base_dust_01_normal',
            '/Game/__chore/gen__/pc__/materials/generic/base/organic/dust/org_base_dust_01_gradientmask.org_base_dust_01_gradientmask']

        for i in range(2):
            tex_path = data[texture_keys[i]]
            tex_path = tex_path.replace('.png', '')
            tex_path = '/Game/__chore/gen__/pc__/materials/generic/base/' + tex_path
            #unreal.log(f"Texture path: {tex_path}")
            #unreal.log_warning(f"Texture path: {example}")
            if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
                unreal.log_error("Can't find texture: " + tex_path)
                continue
            #unreal.log(f"Texture path: {tex_path} exist")
            tex_asset = unreal.EditorAssetLibrary.find_asset_data(tex_path).get_asset()
            texture_params.append(
                unreal.TextureParameterValue(unreal.MaterialParameterInfo(texture_keys[i], association, index),
                                             tex_asset))
            # unreal.TextureParameterValue(pi,unreal.Texture(outer=None, name='None'))

        self.texture_params += texture_params

        """
            Set Vector values
        """
        vector_params = []
        colorVariant_key = ['botColor', 'topColor', 'midColor']
        unreal.log_warning('---- Staked Layer Vector Parameters ----')
        if 'colorVariant' in data.keys():
            g_last_color_variants.clear()
            colorVariants = data['colorVariant']

            for i in range(len(colorVariant_key)):
                temp_v = unreal.LinearColor(colorVariants[colorVariant_key[i]][0],
                                            colorVariants[colorVariant_key[i]][1],
                                            colorVariants[colorVariant_key[i]][2], 0
                                            )
                g_last_color_variants.append(temp_v)
                vector_params.append(
                    unreal.VectorParameterValue(unreal.MaterialParameterInfo(colorVariant_key[i], association, index),
                                                temp_v))
        else:
            unreal.log_error('Stak layers Key colorVariant dont exist')
            unreal.log_error(g_last_color_variants)
            for i in range(len(colorVariant_key)):
                temp_v = g_last_color_variants[i]
                vector_params.append(
                    unreal.VectorParameterValue(unreal.MaterialParameterInfo(colorVariant_key[i], association, index),
                                                temp_v))
        if 'scratchColor' in data.keys():
            temp_v1 = unreal.LinearColor(data['scratchColor'][0],
                                        data['scratchColor'][1],
                                        data['scratchColor'][2], 0
                                        )
            vector_params.append(
                unreal.VectorParameterValue(unreal.MaterialParameterInfo('scratchColor', association, index),
                                            temp_v1))

        temp_v2 = unreal.LinearColor(
            data['normalTextureTransform'][0],
            data['normalTextureTransform'][1],
            0, 0)
        vector_params.append(
            unreal.VectorParameterValue(unreal.MaterialParameterInfo('normalTextureTransform', association, index),
                                        temp_v2))

        self.vector_params += vector_params


def get_swatch_in_by_id(swatches, swid):
    for i in range(len(swatches)):
        if swatches[i]['swatchId'] == swid:
            return swatches[i]

    return {}


def create_material_by_region_in_path(region_layer, path, coating_common_info, swatches = []):
    name = region_layer['bodyPart']
    material = region_layer['material']
    layers: [] = region_layer['layers']
    material_editing_library = unreal.MaterialEditingLibrary

    mi_asset = duplicate_asset_in_path(map_layer_ueasset[material], name, path)

    #mi_asset_parent = duplicate_asset_in_path(map_layer_ueasset[material], material+'_base', path)
    #mi_asset.set_editor_property('parent',mi_asset_parent)
    #unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, mi_asset_parent)
    """"""
    regionLayres = RegionLayerParameterValues()
    regionLayres.coating_common_info = coating_common_info
    regionLayres.material_instance = mi_asset
    regionLayres.numbres_of_layers = int(str(material).split('_')[1])
    unreal.log(f'Region name: {name}')
    regionLayres.stackParameterValuesInLayers(layers, swatches)
    regionLayres.stackParameterValuesInGrime()
    regionLayres.applyParameterValues()
    mi_asset = regionLayres.material_instance

    material_editing_library.set_material_instance_scalar_parameter_value(mi_asset, "scratchAmount",
                                                                          coating_common_info.scratchAmount)
    material_editing_library.set_material_instance_scalar_parameter_value(mi_asset, "grimeAmount",
                                                                          coating_common_info.grimeAmount)
    material_editing_library.set_material_instance_scalar_parameter_value(mi_asset, "emissiveAmount",
                                                                          coating_common_info.emissiveAmount)
    #unreal.log('Textures Names')
    """
    textures = get_asset_texture_dict(name)
    for tex_name in textures:
        #unreal.log(textures[tex_name][0])
        tex_asset = unreal.EditorAssetLibrary.find_asset_data(textures[tex_name][0]).get_asset()
        if str(tex_name).__contains__('_asg_control'):
            #print('_asg_control: ' + tex_name)
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, '_asg_control', tex_asset)
        elif str(tex_name).__contains__('_mask_0_control'):
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, '_mask_0_control', tex_asset)
            #print('_mask_0_control: ' + tex_name)
        elif str(tex_name).__contains__('_mask_1_control'):
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, '_mask_1_control', tex_asset)
            #print('_mask_1_control: ' + tex_name)
        elif str(tex_name).__contains__('_normal'):
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, '_normal', tex_asset)
            #print('_normal: ' + tex_name)
    """
    #unreal.MaterialEditingLibrary.recompile_material(mi_asset)
    return mi_asset

def createCoatoingMaterials(data):
    t_mtl_folder = ue_generated_shaders_path + data['name']
    t_mtl_folder_swatches = t_mtl_folder + '/swatches'
    t_mtl_folder_region_layers = t_mtl_folder + '/regionLayers'
    unreal.EditorAssetLibrary.make_directory(t_mtl_folder)
    unreal.EditorAssetLibrary.make_directory(t_mtl_folder_swatches)
    unreal.EditorAssetLibrary.make_directory(t_mtl_folder_region_layers)
    coating_common_info = CoatingGeneralData()
    coating_common_info.name = data['name']
    coating_common_info.grimeSwatch = data['grimeSwatch']
    coating_common_info.emissiveAmount = data['emissiveAmount']
    coating_common_info.grimeAmount = data['grimeAmount']
    coating_common_info.scratchAmount = data['scratchAmount']
    coating_common_info.swatches = data['swatches']
    coating_common_info.regionLayers = data['regionLayers']

    #for x in data.keys():
        #unreal.log_warning(x)

    for i in range(len(data['swatches'])):
        name = ''
        if i < 10:
            name = '0' + str(i)
        else:
            name = str(i)
        name = name + '_' + data['swatches'][i]['swatchId']
       # unreal.log_warning(name)
        createMaterialISwatch(name, t_mtl_folder_swatches, data['swatches'][i])
    for k in data['regionLayers'].keys():
        create_material_by_region_in_path(data['regionLayers'][k], t_mtl_folder_region_layers, coating_common_info, data['swatches'])


    return

def recompileShader():
    #material = unreal.load_asset('/Game/coatings/matsys/hwp_cvw_matsys.hwp_cvw_matsys')
    material = unreal.load_asset('/Game/coatings/matsys/News/hwp_cvw_matsys.hwp_cvw_matsys')
    unreal.MaterialEditingLibrary.recompile_material(material)

def loadAndCreateCoatings(coating_name = 'oly_20yhalo_h1_mc'):
    # MaterialFunctionMaterialLayer'/Game/Temp_move_later/Base_Material_Layer.Base_Material_Layer'
    #unreal.log_warning("Hello Coatings")
    # f = open('data.json')
    unreal.EditorLevelLibrary.save_current_level()
    coating_data_root_path = 'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/'
    if coating_name == '':
        return
    #coating_name = 'oly_mil_nara'
    #coating_name = 'oly_mil_ghost_grey'
    #coating_name = 'oly_20yhalo_h1_mc'
    coating_data_path = coating_data_root_path + coating_name + '.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_mil_ghost_grey.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/gen_mil_darkred.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/gen_mil_hcs_summer.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_mil_ghost_grey.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_mil_sirocco.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_win_hohoho.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_esports_navi.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_esports_fnatic.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_esports_faze.json'
        #'H:/GameDev/games-tool/  _!ExtraerModelsHalo/HaloInfinite/HaloInfiniteModelExtractor-main/coatings/oly_esports_eunited.json'
    f = open(coating_data_path)
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list

    # Closing file
    f.close()
    unreal.EditorLevelLibrary.select_nothing()

    allActors = unreal.EditorLevelLibrary.get_all_level_actors()
    sklActor = None
    for x in allActors:
        if x.get_actor_label() ==  coating_name:
            sklActor = x
            break
        print(x.get_actor_label())

    if sklActor is None:
        skeletalMeshPath = '/Game/Temp_move_later/SkeletalMesh/united.united'
        skeletalMesh = unreal.EditorAssetLibrary.find_asset_data(skeletalMeshPath).get_asset()
        sklActor = unreal.EditorLevelLibrary.spawn_actor_from_object(skeletalMesh,
                                                                     unreal.Vector(x=-240.0, y=-50.0, z=20.0),
                                                                     unreal.Rotator(roll=0.0, pitch=0.0, yaw=90.00))
        sklActor.set_actor_label(coating_name)

    #get_actor_label()
    unreal.EditorLevelLibrary.set_selected_level_actors([sklActor])
    createCoatoingMaterials(data)
    asignarCoatingToSelectedMesh(coating_name)
    unreal.EditorLevelLibrary.select_nothing()
    save_all_dirts()
    #unreal.EditorLevelLibrary.destroy_actor(actors[0])


def save_all_dirts():
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(True, True)
    unreal.EditorLevelLibrary.save_current_level()


def createGenericAsset_EXAMPLER():
    base_path = '/Game/GenericAssets/'
    generic_assets = [
        [base_path + 'sequence', unreal.LevelSequence, unreal.LevelSequenceFactoryNew()],
        [base_path + 'material', unreal.Material, unreal.MaterialFactoryNew()],
        [base_path + 'MaterialLayer', unreal.MaterialFunctionMaterialLayer,
         unreal.MaterialFunctionMaterialLayerFactory()],
        [base_path + 'MaterialLayerBlend', unreal.MaterialFunctionMaterialLayerBlend,
         unreal.MaterialFunctionMaterialLayerBlendFactory()],
        # [base_path + 'MaterialLayerI', unreal.MaterialFunctionMaterialLayerInstance, unreal.MaterialFunctionMaterialLayerInstanceFactory()]
    ]
    """
    for asset in generic_assets:
        print(createGenericAsset(asset[0], True, asset[1], asset[2]))
    """

def set_mi_texture(mi_asset, param_name, tex_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
        unreal.log_warning("Can't find texture: " + tex_path)
        return False
    tex_asset = unreal.EditorAssetLibrary.find_asset_data(tex_path).get_asset()
    return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, param_name, tex_asset)




def deleteSelectedActors():
    temp_sel_assets = unreal.EditorLevelLibrary.get_selected_level_actors()
    for sm_asset in temp_sel_assets:
        unreal.EditorLevelLibrary.destroy_actor(sm_asset)
    unreal.EditorLevelLibrary.save_current_level()

def delete_generated_folder():
    if unreal.EditorAssetLibrary.does_directory_exist('/Game/coatings/genereted'):
        if unreal.EditorAssetLibrary.delete_directory('/Game/coatings/genereted'):
            save_all_dirts()


def unloadPakages():
    skeletalMeshPath = '/Game/Temp_move_later/SkeletalMesh/united.united'
    skeletalMesh_data = unreal.EditorAssetLibrary.find_asset_data(skeletalMeshPath)
    skeletalMesh = skeletalMesh_data.get_asset()

    unreal.EditorLoadingAndSavingUtils.unload_packages([unreal.find_package(skeletalMesh_data.package_name)])

def rename_reference():
    #MaterialInstanceConstant'/Game/coatings/genereted/oly_mil_arctic/regionLayers/temp/mp_visor.mp_visor'

    #'/Game/coatings/matsys/News/ML_WayPoint_Generic_Inst.ML_WayPoint_Generic_Inst'

    #'/Game/coatings/genereted/oly_mil_arctic/swatches/02_9573a92c43b04541ac4e509bb2e55263.02_9573a92c43b04541ac4e509bb2e55263'
    ad = unreal.EditorAssetLibrary.find_asset_data(
        '/Game/coatings/genereted/oly_mil_arctic/regionLayers/temp/mp_visor.mp_visor')
    ad.get_asset()
    print(unreal.EditorAssetLibrary.find_package_referencers_for_asset('/Game/coatings/genereted/oly_mil_arctic/regionLayers/temp/mp_visor.mp_visor'))
    return


    print(ad.package_name)
    pkg = unreal.find_package(ad.package_name)
    print(pkg)
    #return
    old =  unreal.SoftObjectPath('/Game/coatings/matsys/News/ML_WayPoint_Generic_Inst.ML_WayPoint_Generic_Inst')
    new =  unreal.SoftObjectPath('/Game/coatings/genereted/oly_mil_arctic/swatches/02_9573a92c43b04541ac4e509bb2e55263.02_9573a92c43b04541ac4e509bb2e55263')
    map = {old : new}
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    AssetTools.rename_referencing_soft_object_paths([pkg], map)


def copy_texture_parameter(mi_asset, from_asset):
    unreal.log_warning(from_asset)
    for k in materials_utils.map_texture_parameter.keys():
        tex_asset = from_asset.get_texture_parameter_value(k)
        unreal.log_warning(tex_asset)
        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, k, tex_asset)


    return mi_asset


"""
MaterialInstanceConstant'/Game/coatings/genereted/oly_mil_sirocco/regionLayers/helmet.helmet'
"""
def asignarCoatingToSelectedMesh(coating):
    #unreal.log("---------------------------------------------------")
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    MaterialEditingLibrary = unreal.MaterialEditingLibrary
    EditorAssetLibrary = unreal.EditorAssetLibrary
    EditorLevelLibrary = unreal.EditorLevelLibrary

    sel_assets = unreal.EditorLevelLibrary.get_selected_level_actors()
    mtl_folder = '/Game/coatings/genereted/'
    materials = []
    for sm_asset in sel_assets:
        if sm_asset.get_class().get_name() != "SkeletalMeshActor":
            continue  # skip non-static-meshes

        skle_asset = sm_asset.skeletal_mesh_component
        m_slot_names = skle_asset.get_material_slot_names()
        skle_asset_materials = []
        for mat_asset in skle_asset.get_materials():
            skle_asset_materials.append(mat_asset)

        regions_materilas = EditorAssetLibrary.list_assets( mtl_folder +coating+'/regionLayers')
        print(regions_materilas)
        with unreal.ScopedEditorTransaction("My Transaction Set Coating") as trans:
            for m_slot_name in m_slot_names:
                for i in range(len(regions_materilas)):
                    region_name = regions_materilas[i].split('.')[-1]
                    if str(m_slot_name).__contains__('_belt_') and region_name == 'torso_belt':
                        mi_full_path = regions_materilas[i]
                        mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
                        mat_index = skle_asset.get_material_index(m_slot_name)
                        mi_asset = copy_texture_parameter(mi_asset, skle_asset_materials[mat_index])
                        skle_asset_materials[mat_index] = (mi_asset)
                        print('region belt')
                        break
                    elif str(m_slot_name).__contains__(region_name):
                        mi_full_path = regions_materilas[i]
                        mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
                        mat_index= skle_asset.get_material_index(m_slot_name)
                        mi_asset = copy_texture_parameter(mi_asset, skle_asset_materials[mat_index])
                        skle_asset_materials[mat_index] = (mi_asset)


            #SkeletalMaterial
            skle_asset.set_editor_property('override_materials', skle_asset_materials)
            sm_asset.set_actor_label(coating)

    #skle_asset.set_editor_property('override_materials', materials)
    #unreal.log(sel_assets)

def asignarMaterialsToSelectedMesh():
    #unreal.log("---------------------------------------------------")
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    MaterialEditingLibrary = unreal.MaterialEditingLibrary
    EditorAssetLibrary = unreal.EditorAssetLibrary
    base_mtl = unreal.EditorAssetLibrary.find_asset_data("/Game/Environment/Cave/Materials/M_CaveBase")

    # Iterate over selected meshes
    sel_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    for sm_asset in sel_assets:
        if sm_asset.get_class().get_name() != "StaticMesh":
            continue  # skip non-static-meshes

        asset_name = sm_asset.get_name()
        if asset_name.startswith("S_"):
            asset_name = asset_name[2:]  # Store mesh name without prefix
        asset_folder = unreal.Paths.get_path(sm_asset.get_path_name())
        base_folder = asset_folder[:-7]  # get base folder (subtract "Meshes" from base path)
        mtl_folder = base_folder + "/Materials/"
        tex_folder = base_folder + "/Textures/"

        # create folder for materials if not exist
        if not unreal.EditorAssetLibrary.does_directory_exist(mtl_folder):
            unreal.EditorAssetLibrary.make_directory(mtl_folder)
        # name of material instance for this mesh
        mi_name = "MI_" + asset_name
        mi_full_path = mtl_folder + mi_name
        # Check if material instance already exists
        if EditorAssetLibrary.does_asset_exist(mi_full_path):
            mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
            #unreal.log("Asset already exists")
        else:
            mi_asset = AssetTools.create_asset(mi_name, mtl_folder, unreal.MaterialInstanceConstant,
                                               unreal.MaterialInstanceConstantFactoryNew())
            # set material instance parameters!
        MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mtl.get_asset())  # set parent material
        MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "Desaturation",
                                                                            0.3)  # set scalar parameter
        # find textures for this mesh
        set_mi_texture(mi_asset, "Base Color", tex_folder + "T_" + asset_name + "_basecolor")
        set_mi_texture(mi_asset, "Masks Map", tex_folder + "T_" + asset_name + "_masks")
        set_mi_texture(mi_asset, "Normal", tex_folder + "T_" + asset_name + "_normal")
        set_mi_texture(mi_asset, "BentNormal", tex_folder + "T_" + asset_name + "_Bentnormal")

        # ToDo
        """
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l1_Generic.hwp_cvw_matsys_l1_Generic'
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l4_Generic.hwp_cvw_matsys_l4_Generic'
        MaterialInstanceConstant'/Game/coatings/matsys/toDuplicate/hwp_cvw_matsys_l7_Generic.hwp_cvw_matsys_l7_Generic'
        MaterialFunctionMaterialLayerInstance'/Game/coatings/matsys/toDuplicate/ML_WayPoint_Generic_Inst.ML_WayPoint_Generic_Inst'
        MaterialFunctionMaterialLayerBlendInstance'/Game/coatings/matsys/toDuplicate/MLB_WayPoint_Generic_Inst.MLB_WayPoint_Generic_Inst'
        olympus_spartan_shoulderpad_010_s001_mask_0_control
        "-control-0.png"
        "-control-1.png"
        "-asg.png"
        "-normal.png"
        """

        # set new material instance on static mesh
        sm_asset.set_material(0, mi_asset)

def setUpNormalsCOnfigInTextures():
    print('setUpNormalsCOnfigInTextures')
    root_path = '/Game/__chore/gen__/pc__/'
    filter_texture = unreal.ARFilter(package_paths=[root_path], class_names=[unreal.Name('Texture2D')], recursive_paths = True)
    asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets(filter_texture)
    asset_dict = {}
    for asset_data in asset_list:
        asset_name = str(asset_data.asset_name)
        if asset_name.__contains__('_normal'):
            asset = asset_data.get_asset()
            if not asset.compression_settings == unreal.TextureCompressionSettings.TC_NORMALMAP:
                asset.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP)
                print(f'Exist {asset_name}')
    save_all_dirts()



def generateAllMaterials():
    # 'objects\\characters\\spartan_armor\\materials/mc117/armfor/armfor_006/mc117_spartan_l_armfor_006_s001'
    last_mat = materials_utils.all_from_directory().unique_files
    root_path = '/Game/__chore/gen__/pc__/'
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    editor_asset_library = unreal.EditorAssetLibrary
    material_editing_library = unreal.MaterialEditingLibrary
    # TODO Shaders MaterialFactoryNew

    for mat in last_mat[materials_utils.FileTypes.SHADERS]:
        temp_path = root_path + mat.obj_path.replace('\\', '/').replace('__chore/gen__/', '')
        temp_name = temp_path.split('/')[-1]
        #if not temp_path.__contains__('objects/characters/spartan_armor/materials'):
            #continue
        mtl_folder = temp_path.replace('/'+temp_name,'')
        # create folder for materials if not exist
        if not editor_asset_library.does_directory_exist(mtl_folder):
            editor_asset_library.make_directory(mtl_folder)

        # name of material instance for this mesh
        if not temp_path.__contains__('iron_eagle'):
            continue
        mi_name = temp_name
        mi_full_path = temp_path.replace('{', '_').replace('}', '_')
        # Check if material instance already exists
        if editor_asset_library.does_asset_exist(mi_full_path):
            mi_asset = editor_asset_library.find_asset_data(mi_full_path).get_asset()
            # unreal.log("Asset already exists")
        else:
            mi_asset = asset_tools.create_asset(mi_name.replace('{', '_').replace('}', '_'), mtl_folder, unreal.Material,
                                               unreal.MaterialFactoryNew())
            # set material instance parameters!
        #MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mtl.get_asset())  # set parent material

    # TODO MATERIALS  MaterialInstanceConstantFactoryNew

    for mat in last_mat[materials_utils.FileTypes.MATERIALS]:
        temp_path = root_path + mat.obj_path.replace('\\', '/').replace('__chore/gen__/', '')
        temp_name = temp_path.split('/')[-1]
        if not temp_path.__contains__('iron_eagle'):
            continue

        #if not temp_path.__contains__('olympus_spartan_helmet_014_s001'):
        #    continue
        #print('olympus_spartan_helmet_014_s001')
        if len(mat.files_paths) == 0 or not mat.files_paths[0].__contains__('shaders'):
            print('Posible error')
        elif mat.files_paths[0].__contains__('cvw_ld_matsys{10}_0'):
            #print('debug cvw_ld_matsys')
            parent_path = root_path + mat.files_paths[0].replace('\\', '/').replace('__chore/gen__/', '').replace('{', '_').replace('}', '_')
            parent_asset = None

            if editor_asset_library.does_asset_exist(parent_path):
                parent_asset = editor_asset_library.find_asset_data(parent_path).get_asset()
            else:
                print(f'debug no existe parent {parent_path}')
                continue
            temp = materials_utils.getTextureParameterData(mat)
            if not temp is None:
                temp_path = root_path + mat.obj_path.replace('\\', '/').replace('__chore/gen__/', '')
                temp_name = temp_path.split('/')[-1]
                # if not temp_path.__contains__('objects/characters/spartan_armor/materials'):
                # continue
                mtl_folder = temp_path.replace('/' + temp_name, '')
                # create folder for materials if not exist
                if not editor_asset_library.does_directory_exist(mtl_folder):
                    editor_asset_library.make_directory(mtl_folder)

                # name of material instance for this mesh
                mi_name = utils.normalize_material_name(temp_name)
                mi_full_path = temp_path.replace(temp_name, mi_name)
                # Check if material instance already exists
                if editor_asset_library.does_asset_exist(mi_full_path):
                    mi_asset = editor_asset_library.find_asset_data(mi_full_path).get_asset()
                    # unreal.log("Asset already exists")
                else:
                    mi_asset = asset_tools.create_asset(mi_name, mtl_folder,
                                                        unreal.MaterialInstanceConstant,
                                                        unreal.MaterialInstanceConstantFactoryNew())
                # set material instance parameters!
                material_editing_library.set_material_instance_parent(mi_asset, parent_asset)  # set parent material
                for k in temp.keys():
                    texture_path1 = root_path + temp[k]['path'].replace('\\', '/').replace('__chore/gen__/', '')
                    texture_path = texture_path1
                    print('init texture_path')
                    print(texture_path)
                    print('key k ')
                    print(k)
                    if texture_path.__contains__(materials_utils.map_texture_parameter[k]['path'].split('\\')[-1]):
                        texture_path =  mi_full_path.replace('materials', 'bitmaps').replace('MI_', '').replace('visor','helmet').replace('_l_','_').replace('_r_', '_') + k
                        print('texture_path')
                        print(texture_path)
                    if not editor_asset_library.does_asset_exist(texture_path):
                        if not editor_asset_library.does_asset_exist(texture_path1):
                            continue
                        else:
                            texture_path = texture_path1
                    print('texture_path final')
                    print(texture_path)
                    tex_asset = unreal.EditorAssetLibrary.find_asset_data(texture_path).get_asset()
                    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, k, tex_asset)
                    print(f'ASignacion correcta in path {mi_full_path}')

    save_all_dirts()



def reviewAllMaterials():
    last_mat = materials_utils.all_from_directory().unique_files
    root_path = '/Game/__chore/gen__/pc__/'
    for mat in last_mat[materials_utils.FileTypes.BITMAPS]:
        temp_path = root_path + mat.obj_path.replace('\\','/')
        if unreal.EditorAssetLibrary.does_asset_exist(temp_path):
            text = f'Exist {mat.name}'
            mi_tex_asset = unreal.EditorAssetLibrary.find_asset_data(temp_path).get_asset()

            if mi_tex_asset.blueprint_get_size_x() <= 128 and mat.obj_path.__contains__('materials\\generic\\base\\'):
                print('-----------------------------------------------------------')
                print(text)
                print('x:' + str(mi_tex_asset.blueprint_get_size_x()))
                print('y:' + str(mi_tex_asset.blueprint_get_size_y()))

            if mat.obj_path.__contains__('_normal'):
                if not mi_tex_asset.compression_settings == unreal.TextureCompressionSettings.TC_NORMALMAP:
                    mi_tex_asset.compression_settings = unreal.TextureCompressionSettings.TC_NORMALMAP
                    print(f'Exist {mat.name}')
        else:
            if not mat.obj_path.__contains__('_gear_'):
                unreal.log_error(f'Dont Exist {mat.name}')

def createPartsMaterialsIn(path='C:\\Users\\Jorge\\Downloads\\Compressed\\deploy1\\HIU\objects\\characters\\spartan_armor\\materials\\'):
    # TODO Create materiasl base
    print('TODO')

#loadAndCreateCoatings()
#unreal.log(sys.argv[0])