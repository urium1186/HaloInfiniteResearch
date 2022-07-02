import copy
from enum import Enum, IntFlag

# drillsergeant_backplate_unsc_001
# iron_eagle_spartan_helmet_001_s001
# mc117_spartan_helmet_006_decal_s001
# olympus_spartan_glove_decal_009_s001
# reach_spartan_gear_004_s001
# samurai_spartan_gemstone_001_s001
#


coreTypesString = [
    "drillsergeant",
    "iron_eagle_spartan",
    "mc117_spartan",
    "olympus_spartan",
    "reach_spartan",
    "samurai_spartan",
    "lone_wolves_spartan",
    "_"
]

coreCustomParts = {
    "l_armfor": 40,
    "r_armfor": 83,
    "l_armup": 54,
    "r_armup": 96,
    "l_kneepad": 122,
    "r_kneepad": 130,
    "l_shoulderpad": 49,
    "r_shoulderpad": 92,
    "helmet": 11,
    "visor": 11
}

PartsW0BonesNames = {
    "l_armfor": 'b_l_forearm_fixup',
    "r_armfor": 'b_r_forearm_fixup',
    "l_armup": 'b_l_shoulder_helper4',
    "r_armup": 'b_r_shoulder_helper4',
    "l_kneepad": 'b_l_calf_jiggle',
    "r_kneepad": 'b_r_calf_jiggle',
    "l_shoulderpad": 'b_l_upperarm_fixup',
    "r_shoulderpad": 'b_r_upperarm_fixup',
    "helmet": 'b_helmet',
    "visor": 'b_helmet'
}

core_parts = {
    "parts": {
        "neck": {
            "asg": "neck"
        },
        "torso": {
            "asg": "torso"},
        "belt": {
            "asg": "belt"
        },
        "abPlate": {
            "asg": "torso"
        },
        "lBicep": {
            "asg": "armup"
        },
        "rBicep": {
            "asg": "armup"
        },
        "lElbow": {
            "asg": "armfor"
        },
        "rElbow": {
            "asg": "armfor"
        },
        "lForearm": {
            "asg": "armfor"
        },
        "rForearm": {
            "asg": "armfor"
        },
        "lThigh": {
            "asg": "thigh"
        },
        "rThigh": {
            "asg": "thigh"
        },
        "lKnee": {
            "asg": "knee"
        },
        "rKnee": {
            "asg": "knee"
        },
        "lShin": {
            "asg": "shin"
        },
        "rShin": {
            "asg": "shin"
        },
        "lFoot": {
            "asg": "boot"
        },
        "rFoot": {
            "asg": "boot"
        },
        "lBoot": {
            "asg": "boot"
        },
        "rBoot": {
            "asg": "boot"
        }
    },
    "configurable": {
        "lShoulder": {
            "asg": "armup",
            "optionKeys": [
                "body-a",
                "body-b",
                "body-c"
            ]
        },
        "rShoulder": {
            "asg": "armup",
            "optionKeys": [
                "body-a",
                "body-b",
                "body-c"
            ]
        },
        "techsuit": {
            "asg": "torso",
            "optionKeys": [
                "body-a",
                "body-b",
                "body-c"
            ]
        },
    },
    "prosthesis": {
        "lBicep": {
            "asg": "armup"
        },
        "rBicep": {
            "asg": "armup"
        },
        "lElbow": {
            "asg": "armfor"
        },
        "rElbow": {
            "asg": "armfor"
        },
        "lForearm": {
            "asg": "armfor"
        },
        "rForearm": {
            "asg": "armfor"
        },
        "lKnee": {
            "asg": "knee-prosthetic"
        },
        "rKnee": {
            "asg": "knee-prosthetic"
        },
        "lShin": {
            "asg": "shin-prosthetic"
        },
        "rShin": {
            "asg": "shin-prosthetic"
        },
        "lFoot": {
            "asg": "boot"
        },
        "rFoot": {
            "asg": "boot"
        },
        "lBoot": {
            "asg": "boot-prosthetic"
        },
        "rBoot": {
            "asg": "boot-prosthetic"
        },
        "lShoulder": {
            "asg": "armup"
        },
        "rShoulder": {
            "asg": "armup"
        }
    }
}

parst_bones_rel = {
    "parts_neck_model": ['skel:b_spine3', 'skel:b_neck0_twist', 'skel:b_head', 'skel:b_neck1_twist'],
    "parts_torso_model": ['skel:b_spine3'],
    "parts_belt_model": ['skel:b_pelvis', 'skel:b_spine1_twist', 'skel:b_spine2_twist'],
    "parts_abPlate_model": ['skel:b_spine3'],
    "parts_lBicep_model": ['skel:b_l_shoulder_helper4'],
    "parts_rBicep_model": ['skel:b_r_shoulder_helper4'],
    "parts_lElbow_model": ['skel:b_l_upperarm', 'skel:b_l_forearm'],
    "parts_rElbow_model": ['skel:b_r_forearm', 'skel:b_r_upperarm'],
    "parts_lForearm_model": ['skel:b_l_forearm_fixup'],
    "parts_rForearm_model": ['skel:b_r_forearm_fixup'],
    "parts_lThigh_model": ['skel:b_l_upperleg_jiggle'],
    "parts_rThigh_model": ['skel:b_r_upperleg_jiggle'],
    "parts_lKnee_model": ['skel:b_l_thigh', 'skel:b_l_knee_fixup', 'skel:b_l_calf'],
    "parts_rKnee_model": ['skel:b_r_thigh', 'skel:b_r_knee_fixup', 'skel:b_r_calf'],
    "parts_lShin_model": ['skel:b_l_calf_jiggle'],
    "parts_rShin_model": ['skel:b_r_calf_jiggle'],
    "parts_lFoot_model": ['skel:b_l_toe', 'skel:b_l_foot', 'skel:b_l_calf'],
    "parts_rFoot_model": ['skel:b_r_toe', 'skel:b_r_foot', 'skel:b_r_calf'],
    "parts_lBoot_model": ['skel:b_l_foot'],
    "parts_rBoot_model": ['skel:b_r_foot'],
    "configurable_lShoulder_models_body-a": ['skel:b_spine3', 'skel:b_l_clav', 'skel:b_l_shoulder_helper1',
                                             'skel:b_l_shoulder_helper4', 'skel:b_l_shoulder_helper2'],
    "configurable_rShoulder_models_body-a": ['skel:b_spine3', 'skel:b_r_clav', 'skel:b_r_shoulder_helper1',
                                             'skel:b_r_shoulder_helper4', 'skel:b_r_shoulder_helper2'],
    "configurable_techsuit_models_body_a": ['skel:b_spine3', 'skel:b_neck0_twist', 'skel:b_pelvis',
                                            'skel:b_spine1_twist', 'skel:b_l_thigh', 'skel:b_l_thigh_ctwist',
                                            'skel:b_spine2_twist', 'skel:b_r_thigh', 'skel:b_r_thigh_helper',
                                            'skel:b_r_glut_ctwist'],
    "parts_lGlovepad_model": ['skel:b_l_hand'],
    "parts_lGlove_model": ['skel:b_l_pinky3', 'skel:b_l_pinky2', 'skel:b_l_pinky1', 'skel:b_l_hand', 'skel:b_l_pinky0',
                           'skel:b_l_ring1', 'skel:b_l_ring3', 'skel:b_l_ring2', 'skel:b_l_middle1', 'skel:b_l_index3',
                           'skel:b_l_index2', 'skel:b_l_index1', 'skel:b_l_hand_twist', 'skel:b_l_thumb1',
                           'skel:b_l_thumb2', 'skel:b_l_thumb3', 'skel:b_l_middle3', 'skel:b_l_middle2'],
    "parts_rGlovepad_model": ['skel:b_r_hand'],
    "parts_rGlove_model": ['skel:b_r_pinky3', 'skel:b_r_pinky2', 'skel:b_r_pinky1', 'skel:b_r_pinky0', 'skel:b_r_hand',
                           'skel:b_r_ring1', 'skel:b_r_ring3', 'skel:b_r_ring2', 'skel:b_r_middle1', 'skel:b_r_index3',
                           'skel:b_r_index2', 'skel:b_r_index1', 'skel:b_r_hand_twist', 'skel:b_r_thumb1',
                           'skel:b_r_thumb2', 'skel:b_r_thumb3', 'skel:b_r_middle3', 'skel:b_r_middle2'],
    "parts_helmet_model": ['skel:b_helmet'],
    "parts_lKneepad_model": ['skel:b_l_calf_jiggle'],
    "parts_rKneepad_model": ['skel:b_r_calf_jiggle'],
    "parts_lShoulderpad_model": ['skel:b_l_upperarm_fixup'],
    "parts_rShoulderpad_model": ['skel:b_r_upperarm_fixup'],
}

coreCustomPartsConfig = {
    "helmet": "Helmets",
    "visor": "Visors",
    "l_shoulderpad": "LeftShoulderPads",
    "r_shoulderpad": "RightShoulderPads",
    "glove": "Gloves",
    "kneepad": "KneePads",
    "chestattachments": "ChestAttachments",
    "wristattachments": "WristAttachments",
    "hipattachments": "HipAttachments"
}

code_info_types = {
    "002": "Coatings",
    "005": "Helmets",
    "004": "HelmetAttachments",
    "012": "Visors",
    "008": "LeftShoulderPads",
    "009": "RightShoulderPads",
    "003": "Gloves",
    "006": "KneePads",
    "001": "ChestAttachments",
    "011": "WristAttachments",
    "010": "HipAttachments",
    "013": "Emblems",
    "015": "ArmorFx",
    "016": "MythicFx",
    "007": "ArmorTheme",
    "017": "CoreType"
}

types_info_code = {
    "ArmorVisor": "012",
    "ArmorHelmet": "005",
    "ArmorLeftShoulderPad": "008",
    "ArmorGlove": "003",
    "ArmorKneePad": "006",
    "ArmorRightShoulderPad": "009",
    "ArmorHelmetAttachment": "004",
    "ArmorHipAttachment": "010",
    "ArmorChestAttachment": "001",
    "ArmorWristAttachment": "011",
    "ArmorEmblem": "013",
    "ArmorCoating": "002",
    "AiColor": "301",
    "AiModel": "302",
    "AiTheme": "303",
    "WeaponCharm": "201",
    "WeaponEmblem": "205",
    "WeaponCoating": "203",
    "VehicleEmblem": "405",
    "VehicleCoating": "404",
    "SpartanActionPose": "101",
    "SpartanBackdropImage": "103",
    "SpartanVoice": "105",
    "SpartanEmblem": "104",
    "ArmorTheme": "007",
    "ArmorFx": "015",
    "ArmorMythicFx": "016",
    "WeaponTheme": "207",
    "WeaponDeathFx": "204",
    "WeaponAlternateGeometryRegion": "210",
    "VehicleTheme": "408",
    "VehicleAlternateGeometryRegion": "401"
}

Platform = 'pc'
map_part_materials = [
    'neck',
    'torso',
    'torso_belt',
    'torso',
    'l_armup',
    'r_armup',
    'l_armfor',
    'r_armfor',
    'l_armfor',
    'r_armfor',
    'l_thigh',
    'r_thigh',
    'l_knee',
    'r_knee',
    'l_shin',
    'r_shin',
    'l_boot',
    'r_boot',
    'l_boot',
    'r_boot',
    'l_armup',
    'r_armup',
    'torso',
    'l_glove',
    'l_glove',
    'r_glove',
    'r_glove',
    'helmet',
    'l_kneepad',
    'r_kneepad',
    'l_shoulderpad',
    'r_shoulderpad'
]

map_materials_name_parts = {
    'unique_names': {"name": 0},
    '_neck_': ["parts_neck_model"],
    '_belt_': ["parts_belt_model"],
    '_torso_': ["parts_torso_model", "configurable_techsuit_models_"],
    '_l_armup_': ["parts_lBicep_model", "configurable_lShoulder_models"],
    '_r_armup_': ["parts_rBicep_model", "configurable_rShoulder_models"],
    '_l_armfor_': ["parts_lForearm_model", "parts_lElbow_model"],
    '_r_armfor_': ["parts_rForearm_model", "parts_rElbow_model"],
    '_l_thigh_': ["parts_lThigh_model"],
    '_r_thigh_': ["parts_rThigh_model"],
    '_l_knee_': ["parts_lKneepad_model", "parts_lKnee_model"],
    '_r_knee_': ["parts_rKneepad_model", "parts_rKnee_model"],
    '_l_shin_': ["parts_lShin_model"],
    '_r_shin_': ["parts_rShin_model"],
    '_l_boot_': ["parts_lBoot_model"],
    '_r_boot_': ["parts_rBoot_model"],
    '_l_glove_': ["parts_lGlove_model"],
    '_r_glove_': ["parts_rGlove_model"],
    '_helmet_': ["parts_helmet_model"],
    '_l_kneepad_': ["parts_lKneepad_model"],
    '_r_kneepad_': ["parts_rKneepad_model"],
    '_l_shoulderpad_': ["parts_lShoulderpad_model"],
    '_r_shoulderpad_': ["parts_rShoulderpad_model"]
}

sklMap = {
    3: 4,
    14: 117,
    5: 118,
    6: 126,
    19: 7,
    39: 13,
    11: 123,
    12: 131,
    54: 10,
    51: 12,
    16: 124,
    10: 119,
    9: 127,
    8: 132,
    20: 122,
    17: 130,
    18: 120,
    29: 121,
    22: 128,
    23: 129,
    21: 116,
    7: 133,
    34: 15,
    58: 16,
    38: 57,
    50: 58,
    15: 135,
}

filterList = [
    "olympus_spartan_helmet_001_s001",
    "olympus_spartan_l_armfor_001_s001",
    "olympus_spartan_l_armfor_001_s001",
    "olympus_spartan_l_armup_001_s001",
    "olympus_spartan_l_armup_001_s001",
    "olympus_spartan_l_boot_001_s001",
    "olympus_spartan_l_glove_001_s001",
    "olympus_spartan_l_knee_001_s001",
    "olympus_spartan_l_kneepad_002_s001",
    "olympus_spartan_l_shoulderpad_001_s001",
    "olympus_spartan_l_thigh_001_s001",
    "olympus_spartan_neck_001_s001",
    "olympus_spartan_r_armfor_prosthetic_001_s001",
    "olympus_spartan_r_armfor_prosthetic_001_s001",
    "olympus_spartan_r_armup_prosthetic_001_s001",
    "olympus_spartan_r_boot_001_s001",
    "olympus_spartan_r_glove_prosthetic_001_s001",
    "olympus_spartan_r_knee_001_s001",
    "olympus_spartan_r_kneepad_002_s001",
    "olympus_spartan_r_shoulderpad_001_s001",
    "olympus_spartan_torso_001_s001",
    "olympus_spartan_torso_001_s001",
    "olympus_spartan_torso_001_s001",
    "olympus_spartan_torso_001_s001",
    "olympus_spartan_torso_001_s001",
    "olympus_spartan_torso_001_s001"
]


class Mesh:
    def __init__(self):
        self.vert_pos = []
        self.vert_uv0 = []
        self.vert_uv1 = []
        self.vert_norm = []
        self.vert_tangent = []
        self.faces = []
        self.name = ""
        self.weight_indices = []
        self.weights = []
        self.weight_pairs = []
        self.bones = []
        self.parts = []


class Part:

    def __init__(self):
        self.material_index = -1
        self.index_offset = -1
        self.index_count = -1
        self.vertex_count = -1
        self.material_path = ""
        self.mat_string = ""
        self.material = None

class CoreArmor(IntFlag):
    DRILLSERGEANT = 0
    IRON_EAGLE_SPARTAN = 1
    MC117_SPARTAN = 2
    OLYMPUS_SPARTAN = 3
    REACH_SPARTAN = 4
    SAMURAI_SPARTAN = 5
    LONE_WOLVES_SPARTAN = 6
    ALL = 7

    def getString(self):
        return coreTypesString[self]


def getFiltersListByArmorTheme(armor_theme_json):
    filterListTemp = []
    for key in code_info_types.keys():
        temp_k = code_info_types[key]
        if temp_k in armor_theme_json.keys():
            if 'DefaultOptionPath' in armor_theme_json[temp_k].keys():
                default_opt = armor_theme_json[temp_k]['DefaultOptionPath']
                print(default_opt)
                if default_opt == '':
                    continue
                if 'OptionPaths' in armor_theme_json[temp_k].keys():
                    index = armor_theme_json[temp_k]['OptionPaths'].index(default_opt)
                    print(f'index {index}')
                elif 'Options' in armor_theme_json[temp_k].keys():
                    array_opt = armor_theme_json[temp_k]['Options']
                    for i in range(len(array_opt)):
                        if array_opt[i]['HelmetPath'] == default_opt:
                            index = i
                            break
                    print(f'index {index}')
            else:
                print(f'key info no default {temp_k}')
    return filterListTemp


def splitMeshByParts(mesh):
    mesh_list = []
    if len(mesh.parts) == 1:
        return [mesh]
    for p, part in enumerate(mesh.parts):
        if part.material_path.__contains__('helmet') or part.material_path.__contains__(
                'glove') or part.material_path.__contains__('gear'):
            return [mesh]
        m = Mesh()
        m.parts = [part]
        m.faces = copy.deepcopy(
            mesh.faces[int(part.index_offset / 3):int((part.index_offset + part.index_count) / 3)])

        dsort = set()
        for face in m.faces:
            for f in face:
                dsort.add(f)
        dsort = sorted(dsort)

        # Moves all the faces down to start at 0
        d = dict(zip(dsort, range(max(dsort) + 1)))
        for j in range(len(m.faces)):
            for k in range(3):
                m.faces[j][k] = d[m.faces[j][k]]

        m.vert_pos = trim_verts_data(mesh.vert_pos, dsort)
        m.vert_uv0 = trim_verts_data(mesh.vert_uv0, dsort)
        """
        m.weight_indices = trim_verts_data(mesh.weight_indices, dsort)
        m.weights = trim_verts_data(mesh.weights, dsort)
        createSkinInfo(m)"""
        if mesh.weight_pairs:
            m.weight_pairs = trim_verts_data(mesh.weight_pairs, dsort)
        if mesh.vert_uv1:
            m.vert_uv1 = trim_verts_data(mesh.vert_uv1, dsort)
        if mesh.vert_norm:
            m.vert_norm = trim_verts_data(mesh.vert_norm, dsort)

        # if (len(m.getBonesAffected()) < 0):
        #   continue

        if part.mat_string:
            m.name = mesh.name + part.mat_string.split('/')[-1] + f"_{p}"
        else:
            m.name = mesh.name + f"_{p}"

        mesh_list.append(m)

    return mesh_list

def trim_verts_data(verts, dsort):
    v_new = []
    for i in dsort:
        v_new.append(verts[i])
    return v_new


def getFaceMaterialIndex(indexFace, mesh):
    if len(mesh.parts) > 1:
        for p, part in enumerate(mesh.parts):
            if indexFace >= int(part.index_offset / 3) and indexFace <= int((part.index_offset + part.index_count) / 3):
                return p
    else:
        return 0


def isLeft(vertes):
    negative = False
    positive = False
    for i, vert in enumerate(vertes):
        if vert[1] * 254 > -0.01 and vert[1] * 254 < 0.01:
            k = 0
        elif vert[1] * 254 >= 0.01:
            positive = True
        elif vert[1] * 254 <= -0.01:
            negative = True

        if positive and negative:
            print("Centrado")
            return "C"
    if positive:
        print("Left")
        return "L"
    if negative:
        print("Rigth")
        return "R"


def hayVerticesRepetidos(listaVertice):
    repetidos = []
    for i in range(len(listaVertice) - 1):
        for j in range(i + 1, len(listaVertice), 1):
            if listaVertice[i] == listaVertice[j]:
                repetidos.append([i, j])

    print(f"repetido {len(repetidos)} en {repetidos}")


def get_bin(x, n=0):
    """
    Get the binary representation of x.

    Parameters
    ----------
    x : int
    n : int
        Minimum number of digits. If x needs less digits in binary, the rest
        is filled with zeros.

    Returns
    -------
    str
    """
    return format(x, 'b').zfill(n)


def get_flipped_value_of(number):
    orig_bin = get_bin(number, n=8)
    flip_bin = orig_bin[4:8] + orig_bin[0:4]
    # flip_bin = orig_bin[::-1]
    result = int(flip_bin, 2)
    return result


def getBonesIn(mesh):
    bones = []
    if len(mesh.weight_pairs)<1:
        return mesh.bones
    for pair in mesh.weight_pairs:
        for b in pair[0]:
            if not bones.__contains__(b):
                bones.append(b)
    return bones


def getNamePart(mesh):
    temp_name = mesh.name
    if not len(mesh.parts) < 1:
        part = mesh.parts[0]
        mat_name = part.mat_string.split('/')[-1]
        core_name = mat_name.split('_')[0]
        for k in map_materials_name_parts.keys():
            if mat_name.__contains__(k):
                if len(mesh.bones) > 1:
                    number_part = mat_name.split(k)[1].split('_')[0]
                    if k == '_belt_':
                        number_part = mat_name.split(k)[0].split('_')[-1]

                    temp_name = f'{core_name}_{map_materials_name_parts[k][-1]}_{number_part}'
                    break
                else:
                    number_part = mat_name.split(k)[1].split('_')[0]
                    temp_name = f'{core_name}_{map_materials_name_parts[k][0]}_{number_part}'
                    break
    if map_materials_name_parts['unique_names'].__contains__(temp_name):
        map_materials_name_parts['unique_names'][temp_name] = map_materials_name_parts['unique_names'][temp_name] + 1
    else:
        map_materials_name_parts['unique_names'][temp_name] = 1
    temp_name = f'{temp_name}_{map_materials_name_parts["unique_names"][temp_name]}'
    return temp_name


def createSkinInfo(mesh):
    m = mesh
    # Dealing with weights if they exist

    if m.weight_indices:
        for i in range(len(m.weight_indices)):
            if not m.bones.__contains__(m.weight_indices[i]):
                m.bones.append(m.weight_indices[i])
            if m.weights:
                n_w = normalizeWeightsInfoV3(m.weight_indices[i], m.weights[i], i)
                if len(n_w[0]) > 2:
                    a = 0
                m.weight_pairs.append(n_w)
                # m.weight_pairs = [[[m.weight_indices[i][j], m.weights[i][j]] for j in range(4) if m.weights[i][j] != 0] for i in range(len(m.weight_indices))]
                a = 0
            else:
                m.weight_pairs.append([[m.weight_indices[i][0]], [0.]])
                a = 0
    else:
        for veri in range(len(mesh.vert_pos)):
            for key in coreCustomParts.keys():
                if (mesh.name.__contains__(key)):
                    mesh.weight_pairs.append([[coreCustomParts[key]], [1]])
        mesh.bones = [coreCustomParts[key]]
    return m


def normalizeWeightsInfoV2(sub_weight_indices, sub_weights):
    proc_ind = []
    proc_wei = []
    for j in range(4):
        pass
    if not proc_ind.__contains__(sub_weight_indices[j]):
        proc_ind.append(sub_weight_indices[j])
        proc_wei.append(sub_weights[j])
    else:
        t_j = proc_ind.index(sub_weight_indices[j])
        proc_wei[t_j] = proc_wei[t_j] + sub_weights[j]

    s1 = sum(proc_wei)
    s = 256

    if s1 != 0:
        norm_weights = [x / s1 for x in proc_wei]
    else:
        norm_weights = [0 for x in proc_wei]

    ind = []
    wei = []
    for j in range(len(proc_ind)):
        if norm_weights[j]:
            ind.append(proc_ind[j])
            wei.append(norm_weights[j])
    return [ind, wei]


def normalizeWeightsInfoV3(sub_weight_indices, sub_weights, vertex=0):
    proc_ind = []
    proc_wei = []
    for j in range(4):
        if not proc_ind.__contains__(sub_weight_indices[j]):
            proc_ind.append(sub_weight_indices[j])
            proc_wei.append(sub_weights[j])
        else:
            t_j = proc_ind.index(sub_weight_indices[j])
            proc_wei[t_j] = proc_wei[t_j] + sub_weights[j]

    s1 = sum(proc_wei)
    s = 255

    if s1 != 0:
        norm_weights = [x / s1 for x in proc_wei]
    else:
        norm_weights = [1 for x in proc_wei]

    ind = []
    wei = []
    for j in range(len(proc_ind)):
        if norm_weights[j]:
            ind.append(proc_ind[j])
            wei.append(norm_weights[j])
    return [ind, wei]


def normalizeWeightsInfoV4(sub_weight_indices, sub_weights):
    proc_ind = []
    proc_wei = []
    for j in range(4):
        if not proc_ind.__contains__(sub_weight_indices[j]):
            proc_ind.append(sub_weight_indices[j])
            proc_wei.append(sub_weights[j])
        else:
            t_j = proc_ind.index(sub_weight_indices[j])
            proc_wei[t_j] = proc_wei[t_j] + sub_weights[j]

    s1 = sum(proc_wei)
    s = 256

    if s1 != 0:
        norm_weights = [x / s1 for x in proc_wei]
    else:
        norm_weights = [1 for x in proc_wei]

    ind = []
    wei = []
    for j in range(len(proc_ind)):
        if norm_weights[j]:
            ind.append(proc_ind[j])
            wei.append(norm_weights[j])
    return [ind, wei]


def normalizeWeightsInfo(sub_weight_indices, sub_weights):
    s1 = sum(sub_weights)
    s = 256

    if s1 != 0:
        norm_weights = [x / s for x in sub_weights]
    else:
        norm_weights = [1, 1, 1, 1]
    ind = []
    wei = []
    for j in range(4):
        if norm_weights[j]:
            ind.append(sub_weight_indices[j])
            wei.append(norm_weights[j])
    return [ind, wei]


def normalize_material_name(name):
    result = 'MI_' + name.replace('{', '_').replace('}', '_')
    return result
