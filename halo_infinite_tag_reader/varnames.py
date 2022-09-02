import pathlib

from commons.debug_utils import debug_hash
from configs.config import Config
from halo_infinite_tag_reader.tag_reader_utils import createDirAltNameID

import pymmh3 as mmh3


def getMmr3HashIntFrom(str_in: str) -> str:
    return mmh3.hash(str_in, seed=0)


def getMmr3HashFrom(str_in: str) -> str:
    integer_val = mmh3.hash(str_in, seed=0)
    # print(integer_val)
    # converting int to bytes with length
    # of the array as 5 and byter order as
    # little
    hash_str = getMmr3HashFromInt(integer_val)

    # printing integer in byte representation
    return hash_str


def getMmr3HashFromInt(integer: int) -> str:
    unsigned_integer = integer
    if integer < 0:
        unsigned_integer = integer + 2 ** 32

    bytes_val = unsigned_integer.to_bytes(4, 'little')
    return bytes_val.hex().upper()


# print(getMmr3HashFrom('r_shoulderpad_legendary'))


def getStrInMmr3Hash(p_hash) -> str:
    if Mmr3Hash_str.keys().__contains__(p_hash):
        if not Mmr3Hash_str_iu.keys().__contains__(p_hash):
            hash_str = f'{p_hash}:{Mmr3Hash_str[p_hash]}'
            print(hash_str)
            Mmr3Hash_str_iu[p_hash] = Mmr3Hash_str[p_hash]
            path_to_hash = Config.ROOT_DIR + '\\halo_infinite_tag_reader\\hash\\in_use.txt'
            with open(path_to_hash, 'a') as f:
                f.write(hash_str+'\n')
        return Mmr3Hash_str[p_hash]
    else:
        if debug_hash.keys().__contains__(p_hash):
            debug_hash[p_hash] += 1
        else:
            debug_hash[p_hash] = 1
        return p_hash


Mmr3Hash_str = {}
Mmr3Hash_str_save = {
    '0A5BDF43': 'torso_belt',
    '580AAD54': 'mp_visor',
    '0F9BB6DC': 'l_armup',
    '6A56DD67': 'l_knee',
    'DD8D3E8E': 'l_kneepad',
    'E98D4937': 'r_kneepad',
    'AA98D35D': 'neck',
    'FD8B5467': 'r_armup',
    'DCA0D157': 'r_knee',
    '5F847ED3': 'helmet',
    'B49FE137': 'l_thigh',
    'BBBE9470': 'l_shoulderpad',
    '352BF79E': 'l_boot',
    'FBDD12B4': 'r_boot',
    'D03377BB': 'r_armfor',
    '139AED84': 'r_shin',
    'E965807C': 'r_glove',
    '64E065A0': 'r_shoulderpad',
    '3B3D0B0F': 'r_thigh',
    'FF6A3A29': 'l_shin',
    '29930562': 'l_glove',
    '6AAF913F': 'l_armfor',
    'B4CD1980': 'torso',
    'AC92D0CE': 'r_shoulderpad_legendary',
    'A0A506D7': 'l_shoulderpad_legendary',
    '7519B3BC': 'l_glove_legendary',
    '1AA603D1': 'r_glove_legendary',
    # bones names
    '2FB6CA56': 'masterchief_world',
    '18BD3017': 'b_pedestal',
    'C377784D': 'b_aim_pitch',
    'A5B711FB': 'b_aim_yaw',
    'A067308A': 'b_pelvis',
    'F3E999A2': 'b_spine1',
    '529170DD': 'b_spine2',
    '607A7192': 'b_spine3',
    'BBA5B49B': 'b_neck0',
    '5EA0CE6E': 'b_neck1',
    '599329A3': 'b_head',
    '97A9A6F7': 'b_helmet',
    '65901585': 'b_neck1_twist',
    '6926D6C2': 'b_neck0_twist',
    '0E56E963': 'b_l_clav',
    'A630345C': 'b_l_upperarm',
    'CA4ED531': 'b_l_forearm',
    '6EB51F62': 'b_l_hand',
    '20CF0B5D': 'b_l_thumb1',
    'F6CAB399': 'b_l_thumb2',
    'DBB9C7E2': 'b_l_thumb3',
    'A7EF31CE': 'b_l_index1',
    '65F019AD': 'b_l_index2',
    '4DD5BE60': 'b_l_index3',
    'C487664E': 'b_l_middle1',
    '46C04FD7': 'b_l_middle2',
    '51B364D8': 'b_l_middle3',
    'BFC9F01F': 'b_l_ring1',
    'CA72783B': 'b_l_ring2',
    '9E165C9F': 'b_l_ring3',
    'AD4DD846': 'b_l_pinky0',
    '31280A06': 'b_l_pinky1',
    '940A0F47': 'b_l_pinky2',
    '12B873DD': 'b_l_pinky3',
    'AB219BEB': 'b_l_wrist_fixup',
    '1EEFDBCE': 'b_l_grip',
    'CD589AE1': 'b_l_hand_helper3',
    '2F7055FF': 'b_l_hand_helper4',
    '3CD83F1F': 'b_l_hand_helper1',
    '4ED006EF': 'b_l_hand_helper2',
    '0A6ADA5A': 'b_l_forearm_fixup',
    '2A172BD2': 'b_l_hand_twist',
    '4072E109': 'b_l_forearm_helper4',
    '284B0F4D': 'b_l_forearm_helper3',
    '39F60DCD': 'b_l_forearm_helper2',
    '6472316D': 'b_l_forearm_helper1',
    '6599D3B4': 'b_l_hand_ctwist',
    'AFD8D42C': 'b_l_elbow_fixup',
    '77AA58C6': 'b_l_elbow_armor',
    '3BA284D1': 'b_l_upperarm_fixup',
    '2AE2AC27': 'b_l_shoulder_fixup',
    '5D662063': 'b_l_shoulder_helper1',
    'B142FD37': 'b_l_shoulder_helper2',
    '054C106F': 'b_l_shoulder_helper3',
    '03425E79': 'b_l_shoulder_helper4',
    '099B5C3A': 'b_l_upperarm_ctwist',
    'AF9C3392': 'b_r_clav',
    'CACF0402': 'b_r_upperarm',
    '23FC3166': 'b_r_forearm',
    'BB913FBE': 'b_r_hand',
    'B4FF6752': 'b_r_index1',
    '5C03C4CB': 'b_r_index2',
    '96454254': 'b_r_index3',
    '681B58B9': 'b_r_middle1',
    'A70737F6': 'b_r_middle2',
    '580E036F': 'b_r_middle3',
    'D96C39F8': 'b_r_pinky0',
    '03C28844': 'b_r_pinky1',
    'F785A450': 'b_r_pinky2',
    '08CC8B3E': 'b_r_pinky3',
    '7D40B492': 'b_r_ring1',
    '02BAFF97': 'b_r_ring2',
    'E140268F': 'b_r_ring3',
    '1E96208E': 'b_r_thumb1',
    '81E8AC03': 'b_r_thumb2',
    '534D4B6A': 'b_r_thumb3',
    '96FE4AF8': 'b_r_wrist_fixup',
    'B5A59E99': 'b_r_grip',
    '4A1A3D03': 'b_r_hand_helper1',
    'BD009B8D': 'b_r_hand_helper2',
    '9770F9E7': 'b_r_hand_helper3',
    '3300BAC7': 'b_r_hand_helper4',
    '4B670344': 'b_r_hand_twist',
    '8B84DF79': 'b_r_forearm_fixup',
    'C686B04C': 'b_r_hand_ctwist',
    '0DD3E974': 'b_r_forearm_helper4',
    'C20370D6': 'b_r_forearm_helper3',
    '6A9F45EB': 'b_r_forearm_helper2',
    'F85C7CF9': 'b_r_forearm_helper1',
    'D62A7F32': 'b_r_elbow_fixup',
    '0AB47925': 'b_r_elbow_armor',
    '3842C58A': 'b_r_shoulder_fixup',
    '7A752A16': 'b_r_upperarm_fixup',
    'C9157555': 'b_r_shoulder_helper1',
    '64C3C56B': 'b_r_shoulder_helper2',
    '34DCBB6F': 'b_r_shoulder_helper3',
    '8A4EF90A': 'b_r_shoulder_helper4',
    '01B07FDD': 'b_r_upperarm_ctwist',
    'EC688A83': 'b_torso',
    '5C400F38': 'b_backpack',
    'E6BEA875': 'b_l_scap1',
    '14D5BB42': 'b_l_scap2',
    '85EB7C59': 'b_l_scap3',
    '39943D4F': 'b_r_scap1',
    'B4543038': 'b_r_scap2',
    '952293E8': 'b_r_scap3',
    'E336E32A': 'b_l_lowerback_armor',
    '0CE26AF5': 'b_abarmor',
    '339D9B1E': 'b_backarmor',
    '4F1F6BA5': 'b_r_lowerback_armor',
    '5593C579': 'b_camera',
    '46390949': 'b_neck0_ik',
    'F4C22D5B': 'b_neck1_ik',
    'BD6DC8E5': 'b_head_ik',
    '2BFCA19A': 'b_head_ik_eff',
    '5CAB0D2B': 'b_head_ctwist',
    '2F1A3303': 'b_spine2_twist',
    'D88DA08D': 'b_spine1_twist',
    '082F4F0C': 'b_l_thigh',
    '5E199603': 'b_l_calf',
    '8A157010': 'b_l_foot',
    '627716DE': 'b_l_toe',
    'CFE06087': 'b_l_calf_jiggle',
    'E704BFFE': 'b_l_upperleg_jiggle',
    '17DD8361': 'b_l_knee_fixup',
    '7F8AEE57': 'b_l_thigh_helper',
    'F1C52FFB': 'b_r_thigh',
    '2EEDDA0E': 'b_r_calf',
    'BD2B9572': 'b_r_foot',
    '37C1E5DB': 'b_r_toe',
    '459D6A9B': 'b_r_calf_jiggle',
    '32604D33': 'b_r_upperleg_jiggle',
    '5E3B1EAC': 'b_r_knee_fixup',
    'AD3C1AF8': 'b_r_thigh_helper',
    'D5329D4B': 'b_r_thigh_ctwist',
    'C7874F6A': 'b_l_thigh_ctwist',
    'B337624C': 'b_l_glut_ctwist',
    'CDF6AF4E': 'b_r_glut_ctwist',
    'CA7CDD59': 'b_spine1_ik',
    'BD911494': 'b_spine2_ik',
    '50EE2EF7': 'b_spine3_ik',
    'A8F94A77': 'b_spine3_ik_eff',
    'D6B89A01': 'b_spine_ctwist',

    # RenderModel Regions

    '2BF0F7E5': 'c_helmet',
    '35661A2A': 'torso_debug_-error-35661A2A',
    '24102F6B': 'c_neck',
    '9582814A': 'c_torso',
    '83B4A472': 'c_waist',
    '326AE329': 'l_thigh-error-326AE329',
    '9F67C942': 'default',
    '02D225AB': 'l_armfor-error-02D225AB',
    '02D225AA': 'l_kneepad-error-02D225AA',
    'B9D69A59': 'l_knee-error-B9D69A59',
    '3C859084': 'l_leg',
    'C650BFA3': 'l_shoulder',
    'A8426F00': 'l_shoulder_pad',
    '01672774': 'l_glove-error-01672774',
    '01672771': 'r_armfor-error-01672771',
    '0D8D0788': 'r_kneepad-error-0D8D0788',
    '6AAD6699': 'r_knee-error-6AAD6699',
    '07838F43': 'r_leg',
    '21A8914E': 'r_shoulder',
    '96274AB6': 'r_shoulder_pad',
    '9D353C2C': 'l_glove_1-error-9D353C2C',

    # permutations
    'EFB1F099': 'chief',
    '000F3C92': 'fp_body_default',

    # other
    'D25A559B': '__default__',
}

Mmr3Hash_str_dupl = {}
Mmr3Hash_str_iu = {}


def loadInUseHashNamesFile():
    path_to_hash = Config.ROOT_DIR + '\\halo_infinite_tag_reader\\hash\\in_use.txt'
    with open(path_to_hash, 'rb') as f:
        hash_lines = f.readlines()
        for h_l in hash_lines:
            values = str(h_l).replace('\\r\\n\'', '').split(':')
            if len(values) < 2:
                continue
            Mmr3Hash_str_iu[str(values[0]).replace("b'", "")] = values[1]

    debug = True


def loadAlternativeHashNamesFiles():
    return
    path_to_hash = Config.ROOT_DIR + '\\halo_infinite_tag_reader\\hash\\'
    for path in pathlib.Path(path_to_hash).rglob('*.txt'):
        #if not (path.name.__contains__('asdtag') or path.name.__contains__('in_use')):
        #    continue
        with open(path, 'rb') as f:
            hash_lines = f.readlines()
            for h_l in hash_lines:
                values = str(h_l).replace('\\r\\n\'','').split(':')
                if len(values)<2:
                    continue
                h_i = getMmr3HashFrom(values[1])
                if Mmr3Hash_str.keys().__contains__(h_i):
                    if not Mmr3Hash_str[h_i] == values[1]:
                        debug = Mmr3Hash_str[h_i]
                        b = values[1]
                        if Mmr3Hash_str[h_i].__contains__(f'-error-{h_i}'):
                            Mmr3Hash_str[h_i] = values[1]
                        else:
                            Mmr3Hash_str_dupl[h_i] = values[1]
                            if not Mmr3Hash_str_dupl[h_i] == values[1]:
                                debug = 1
                    #assert Mmr3Hash_str[h_i] == values[1], 'Los hash deberian dar el mismo valor'

                else:
                    Mmr3Hash_str[h_i] = values[1]


loadInUseHashNamesFile()
loadAlternativeHashNamesFiles()
map_alt_name_id = createDirAltNameID(Config.INFOS_PATH)

debug = ""
