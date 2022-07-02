#from dataclasses import dataclass, fields, field
from enum import IntFlag, Enum

#import numpy as np
import gf
#import binascii
#from typing import List
import os
import copy

import json


unpack_directory = "J:/Games/Halo Infinite Stuf/Extracted/HI/models/beta 1"
#unpack_directory = "C:/Users/Jorge/Downloads/Compressed/deploy1/HI/HaloInfiniteUnpack"
materials_dir = 'objects\characters\spartan_armor\materials/'
directory = f"{unpack_directory}/{materials_dir}"
directory = directory.replace("\\", "/")
out_path = "J:/Games/Halo Infinite Stuf/Extracted/HI/textures/unpaked/"



map_texture_parameter = {
    "_asg_control": {"path":'shaders\\default_bitmaps\\bitmaps\\default_diff',"control": False},
    "_mask_0_control": {"path":'shaders\\default_bitmaps\\bitmaps\\color_black',"control": False},
    "_mask_1_control": {"path":'shaders\\default_bitmaps\\bitmaps\\color_black',"control": False},
    "_normal": {"path":'shaders\\default_bitmaps\\bitmaps\\default_normal',"control": False},
    "_cubehdr": {"path":'shaders\\default_bitmaps\\bitmaps\\black_cubehdr',"control": False},
}

class FileTypes(Enum):
    # *.materialpalette
    MATERIALSTYLES = "materialstyles"
    BITMAPS = "bitmap" #{pc}.bitmap
    PALETTES = "materialpalette"
    SHADERS = "shadervariant"
    MATERIALS = "material"
    COATINGMATERIALSETS = "coatingmaterialset"
    MATERIALSWATCH = "materialswatch"
    MATERIALVISORSWATCH = "materialvisorswatch"

class ShaderType(IntFlag):
    DEFAULT = 0 # _matsys
    TYPE_1 =  1 # cvw_matsys
    TYPE_2 =  2 # cvw_ld_matsys
    CHORE  =  3 #__chore
    OBJ_2Space = 4
    OBJ_1Space = 5
    OBJ_LITERAL = 6
    OBJ_2Space_2 = 7
    MAT_LITERAL = 8

shaderTypesValues = [
    b"\x5f\x6d\x61\x74\x73\x79\x73", # _matsys
    b"\x63\x76\x77\x5f\x6d\x61\x74\x73\x79\x73", # cvw_matsys
    b"\x63\x76\x77\x5f\x6c\x64\x5f\x6d\x61\x74\x73\x79\x73", # cvw_ld_matsys
    b"\x5f\x5f\x63\x68\x6f\x72\x65\x5c", # __chore\
    b"\x00\x00",
    b"\x00",
    b"\x6f\x62\x6a\x65\x63\x74\x73\x5c", # objects\
    b"\x00\x02",
    b"\x6d\x61\x74\x65\x72\x69\x61\x6c\x73\x5c" # materials\
]

class HIFile:

    unique_files = {
        FileTypes.MATERIALS: [],
        FileTypes.MATERIALSWATCH: [],
        FileTypes.MATERIALVISORSWATCH: [],
        FileTypes.PALETTES: [],
        FileTypes.COATINGMATERIALSETS: [],
        FileTypes.MATERIALSTYLES: [],
        FileTypes.SHADERS: [],
        FileTypes.BITMAPS: [],
    }
    def __init__(self):
        self.path = ""
        self.obj_path = ""
        self.files_paths: [str] = []
        self.name = []
        self.ext = ".*"

    def loadUnique(self, obj_path="") -> bool:
        if self not in self.unique_files[self.getFileType()]:
            self.unique_files[self.getFileType()].append(self)
            self.load()
            return True

        return False

    def load(self, obj_path=""):
        self.files_paths.append(obj_path)
        if self not in self.unique_files[self.getFileType()]:
            self.unique_files[self.getFileType()].append(self)

        print(f"Cargado {type(self)} from {self.path}")


    def __str__(self):
        return f"Clase {type(self)} from {self.path}"

    def __eq__(self, other):
        return self.path == other.path

    def getFileType(self)-> FileTypes:
        raise ValueError("No Implementado")


def createFile(fileType:FileTypes = None) -> HIFile:
    if fileType == FileTypes.MATERIALS:
        return HIMaterial()
    elif fileType == FileTypes.SHADERS:
        return HIShaderVariant()
    elif fileType == FileTypes.BITMAPS:
        return HIBitmap()
    elif fileType == FileTypes.PALETTES:
        return HIMaterialPalette()
    elif fileType == FileTypes.COATINGMATERIALSETS:
        return HICoatingMaterialSet()
    elif fileType == FileTypes.MATERIALSTYLES:
        return HIMStyle()
    elif fileType == FileTypes.MATERIALSWATCH:
        return HIMaterialSwatch()
    elif fileType == FileTypes.MATERIALVISORSWATCH:
        return HIMaterialVisorSwatch()
    else:
        return None

def tryCreateFile(object_path) -> HIFile:
    bitmap_handle = f"{unpack_directory}/{object_path}"
    bitmap_handle = bitmap_handle.replace("\\", "/")
    bitmap_handle = bitmap_handle.replace("/", "\\")
    for fileType in FileTypes:
        filePath = f"{bitmap_handle}.{fileType.value}"
        if os.path.isfile(filePath):
            tempFile = createFile(fileType)
            #print(filePath)
            #print(fileType.value)
            tempFile.obj_path = object_path
            tempFile.name = object_path.replace('\\', '/').split('/')[-1]
            tempFile.path = filePath
            #print(fileType.name)
            return tempFile
        else:
            if fileType == FileTypes.MATERIALSTYLES:
                tempExt ="{ct}.materialstyles"
                filePath = f"{unpack_directory}/__chore\gen__\{object_path}"
                filePath = filePath.replace("\\", "/")
                filePath = filePath.replace("/", "\\")
                filePath = f"{filePath}{tempExt}"
                if os.path.isfile(filePath):
                    tempFile = createFile(fileType)
                    print(filePath)
                    print(fileType.value)
                    tempFile.obj_path = object_path
                    tempFile.name = object_path.replace('\\', '/').split('/')[-1]
                    tempFile.path = filePath
                    print(fileType.name)
                    return tempFile
            elif fileType == FileTypes.SHADERS:
                tempExt = "{pc}.shadervariant"
                filePath = f"{bitmap_handle}{tempExt}"
                if not "pc__\\" in filePath:
                    filePath = filePath.replace("gen__\\", "gen__\\pc__\\")
                if os.path.isfile(filePath):
                    tempFile = createFile(fileType)
                    print(filePath)
                    print(fileType.value)
                    tempFile.obj_path = object_path
                    tempFile.name = object_path.replace('\\', '/').split('/')[-1]
                    tempFile.path = filePath
                    print(fileType.name)
                    return tempFile
                tempExt = ".shader"
                filePath = f"{bitmap_handle}{tempExt}"
                if os.path.isfile(filePath):
                    tempFile = createFile(fileType)
                    print(filePath)
                    print(fileType.value)
                    tempFile.obj_path = object_path
                    tempFile.name = object_path.replace('\\', '/').split('/')[-1]
                    tempFile.path = filePath
                    print(fileType.name)
                    return tempFile
            elif fileType == FileTypes.BITMAPS:
                tempExt = "{pc}.bitmap"
                filePath = f"{unpack_directory}\__chore\pc__\{object_path}{tempExt}"
                filePath = filePath.replace("\\", "/")
                filePath = filePath.replace("/", "\\")
                if os.path.isfile(filePath):
                    tempFile = createFile(fileType)
                    print(filePath)
                    print(fileType.value)
                    tempFile.obj_path = object_path
                    tempFile.name = object_path.replace('\\', '/').split('/')[-1]
                    tempFile.path = filePath
                    print(fileType.name)
                    return tempFile
    return None



class HIBitmap(HIFile):

    def __init__(self):
        self.m_name = ""
        self.ext = "{pc}.bitmap"
        self.files_paths: [str] = []

    def getFileType(self) -> FileTypes:
        return FileTypes.BITMAPS

class HIShader(HIFile):

    def __init__(self):
        self.sh_name = ""
        self.obj_path = ""
        self.files_paths: [str] = []
        self.textures : [HIFile] = []
        self.ext = ".shader"

    def getFileType(self) -> FileTypes:
        return FileTypes.SHADERS

    def load(self, obj_path = ""):
        """
        print(self)
        print(f"shader name {self.sh_name}")
        # pc__\
        if not "pc__\\" in self.path:
            self.path = self.path.replace("gen__\\", "gen__\\pc__\\")
        """
        if not os.path.isfile(self.path):
            print(f"No file shader {self.path}")
            return
        fb = open(self.path, "rb").read()
        ini_offset = fb.find(shaderTypesValues[ShaderType.CHORE])
        if ini_offset == -1:
            print("debug no variant shader")
            return

        bin_end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space],ini_offset) + 2

        text_end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space],bin_end_offset)-2
        sub_array = fb[bin_end_offset:text_end_offset].split(shaderTypesValues[ShaderType.OBJ_1Space])
        for obj_p in sub_array:
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.textures.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")


class HIShaderVariant(HIShader):
    def __init__(self):
        self.sh_name = ""
        self.obj_path = ""
        self.files_paths: [str] = []
        self.textures: [HIFile] = []
        self.ext = "{pc}.shadervariant"

class HIMaterial(HIFile):
    def __init__(self):
        self.m_name = ""
        self.shader = None
        self.files_paths: [str] = []
        self.textures: [HIFile] = []
        self.style : HIMStyle = None
        self.ext = ".material"

    def getFileType(self) -> FileTypes:
        return FileTypes.MATERIALS

    def load(self, obj_path=""):
        #   offset = fb.find(b"\x63\x76\x77\x5f\x6c\x64\x5f\x6d\x61\x74\x73\x79\x73\x7b\x31\x30\x7d\x5f\x30")
        #   offset = fb.find(b"\x63\x76\x77\x5f\x6c\x64\x5f\x6d\x61\x74\x73\x79\x73") # cvw_ld_matsys
        #   offset = fb.find(b"\x63\x76\x77\x5f\x6d\x61\x74\x73\x79\x73") # cvw_matsys
        if not os.path.isfile(self.path):
            print(f"No file maps {self.path}")
            return

        fb = open(self.path, "rb").read()

        init_offset = fb.find(shaderTypesValues[ShaderType.CHORE])
        end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2],init_offset)

        temp_array = fb[init_offset:end_offset]
        temp_array = temp_array.split(shaderTypesValues[ShaderType.OBJ_1Space])

        for obj_p in temp_array:
            if obj_p == b'\00' or obj_p == b'':
                continue
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.textures.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")

        if len(self.textures)>0 and (type(self.textures[0]) is HIShader or type(self.textures[0]) is HIShaderVariant):
            self.shader = self.textures.pop(0)

        if len(self.textures)>0 and type(self.textures[-1]) is HIMStyle:
            self.style = self.textures.pop()
""" 
        shader_obj_path = gf.offset_to_string_mem(fb, init_offset)
        print(str(shader_obj_path))
        shader_name = str(shader_obj_path).split("\\")[-1]
        tempShader = tryCreateFile(shader_obj_path)
        # if "{" in shader_name:
        #    tempShader = HIShaderVariant()

        tempShader.loadUnique()
        self.shader = tempShader
        firstTexture = gf.offset_to_string_mem(fb, init_offset + len(shader_obj_path) + 2)
        # print(firstTexture)
        tempFile1 = tryCreateFile(firstTexture)
        tempFile1.loadUnique()
        self.textures.append(tempFile1)
        temp = '!'
        tempOffset = init_offset + len(shader_obj_path) + 2 + len(firstTexture) + 1
        tempTexName = firstTexture
        while tempTexName != '\x02':
            tempTexName = gf.offset_to_string_mem(fb, tempOffset)
            tempOffset = tempOffset + len(tempTexName) + 1
            if tempTexName != '\x02' and tempTexName != "":
                if "" == tempTexName:
                    print("Parar")
                tempFile = tryCreateFile(tempTexName)
                if tempFile is None:
                    print(f"Debug error in {tempTexName}")
                elif type(tempFile) is HIBitmap:
                    tempFile.loadUnique()
                    self.textures.append(tempFile)
                elif type(tempFile) is HIMStyle:
                    self.style = tempFile
                    self.style.loadUnique()
                else:
                    print(f"Debug error in {tempTexName} other type {type(tempFile)}")
        style_obj_path = ""

        print(f"Materials textures")
        for x in self.textures:
            print(x)
"""
class HIMaterialPalette(HIFile):
    def __init__(self):
        self.mp_name = ""
        self.materials_p: [HIFile] = []
        self.files_paths: [str] = []
        self.style: HIMStyle = None
        self.ext = ".materialpalette"  #.materialpalette

    def getFileType(self) -> FileTypes:
        return FileTypes.PALETTES

    def load(self, obj_path=""):

        if not os.path.isfile(self.path):
            print(f"No file HIMaterialPalette {self.path}")
            return
        fb = open(self.path, "rb").read()
        print(f"HIMaterialPalette file path {self.path}")
        init_offset = fb.find(shaderTypesValues[ShaderType.MAT_LITERAL])
        if init_offset == -1:
            print(f"No material in HIMaterialPalette. Code: {shaderTypesValues[ShaderType.MAT_LITERAL]}")
            return
        end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2], init_offset)
        temp_array = fb[init_offset:end_offset]
        temp_array = temp_array.split(shaderTypesValues[ShaderType.OBJ_1Space])

        for obj_p in temp_array:
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.materials_p.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")


class HICoatingMaterialSet(HIFile):
    def __init__(self):
        self.c_name = ""
        self.materials_cs: [HIFile] = []
        self.files_paths: [str] = []
        self.ext = ".coatingmaterialset"  # .coatingmaterialset

    def getFileType(self) -> FileTypes:
        return FileTypes.COATINGMATERIALSETS

    def load(self, obj_path=""):

        if not os.path.isfile(self.path):
            print(f"No file HICoatingMaterialSet {self.path}")
            return
        fb = open(self.path, "rb").read()
        print(f"HICoatingMaterialSet file path {self.path}")
        init_offset = fb.find(shaderTypesValues[ShaderType.OBJ_LITERAL])
        if init_offset == -1:
            print(f"No object in HICoatingMaterialSet. Code: {shaderTypesValues[ShaderType.OBJ_LITERAL]}")
            return
        end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2], init_offset)
        temp_array = fb[init_offset:end_offset]
        temp_array = temp_array.split(shaderTypesValues[ShaderType.OBJ_1Space])

        for obj_p in temp_array:
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.materials_cs.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")


class HIMaterialSwatch(HIFile):
    def __init__(self):
        self.msw_name = ""
        self.materials_l: [HIFile] = []
        self.files_paths: [str] = []
        self.style: HIMStyle = None
        self.ext = ".materialswatch"  #.materialswatch

    def getFileType(self) -> FileTypes:
        return FileTypes.MATERIALSWATCH

    def load(self, obj_path=""):

        if not os.path.isfile(self.path):
            print(f"No file HIMaterialSwatch {self.path}")
            return
        fb = open(self.path, "rb").read()
        print(f"HIMaterialSwatch file path {self.path}")
        init_offset = fb.find(shaderTypesValues[ShaderType.MAT_LITERAL])
        if init_offset == -1:
            print(f"No material in style. Code: {shaderTypesValues[ShaderType.MAT_LITERAL]}")
            return
        end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2],init_offset)
        temp_array = fb[init_offset:end_offset]
        temp_array = temp_array.split(shaderTypesValues[ShaderType.OBJ_1Space])

        for obj_p in temp_array:
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.materials_l.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")


class HIMaterialVisorSwatch(HIFile):
    def __init__(self):
        self.msw_name = ""
        self.materials_sw: [HIFile] = []
        self.files_paths: [str] = []
        self.style: HIMStyle = None
        self.ext = ".materialvisorswatch"  #.materialvisorswatch

    def getFileType(self) -> FileTypes:
        return FileTypes.MATERIALVISORSWATCH

    def load(self, obj_path=""):

        if not os.path.isfile(self.path):
            print(f"No file HIMaterialVisorSwatch {self.path}")
            return
        fb = open(self.path, "rb").read()
        print(f"HIMaterialVisorSwatch file path {self.path}")
        init_offset = fb.find(shaderTypesValues[ShaderType.MAT_LITERAL])
        if init_offset == -1:
            print(f"No material in style. Code: {shaderTypesValues[ShaderType.MAT_LITERAL]}")
            return
        end_offset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2],init_offset)
        temp_array = fb[init_offset:end_offset]
        temp_array = temp_array.split(shaderTypesValues[ShaderType.OBJ_1Space])

        for obj_p in temp_array:
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.materials_sw.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")

class HIMStyle(HIFile):
    def __init__(self):
        self.s_name = ""
        self.files_paths: [str] = []
        self.coatings: [HIFile] = []
        self.palettes: [HIFile] = []
        self.visor: [HIFile] = []
        self.materials: [HIFile] = []
        self.ext = "{ct}.materialstyles"

    def getFileType(self) -> FileTypes:
        return FileTypes.MATERIALSTYLES

    def load(self, obj_path=""):
        print(self)
        print(f"style name {self.s_name}")
        # pc__\
        if obj_path != "":
            self.obj_path = obj_path

        self.path = f"{unpack_directory}/__chore\gen__\{self.obj_path}{self.ext}"
        self.path = self.path.replace("\\", "/")
        self.path = self.path.replace("/", "\\")
        """
        if not "pc__\\" in self.path:
            self.path = self.path.replace("gen__\\", "gen__\\pc__\\")
        """
        if not os.path.isfile(self.path):
            print(f"No file style {self.path}")
            return
        fb = open(self.path, "rb").read()
        print(f"Style file path {self.path}")

        object_offset = fb.find(shaderTypesValues[ShaderType.OBJ_LITERAL])
        if object_offset == -1:
            print(f"No object in style. Code: {shaderTypesValues[ShaderType.OBJ_LITERAL]}")
            return
        last_oofset = fb.find(shaderTypesValues[ShaderType.OBJ_2Space_2],object_offset)
        print("Primer array style:")
        f_array = fb[object_offset:last_oofset].split(shaderTypesValues[ShaderType.OBJ_2Space])
        if len(f_array) != 2:
            print(f"Debug error in {self.path}")

        for obj_p in f_array[0].split(shaderTypesValues[ShaderType.OBJ_1Space]):
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p+b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                if tempFile.getFileType() == FileTypes.COATINGMATERIALSETS:
                    self.coatings.append(tempFile)
                elif tempFile.getFileType() == FileTypes.PALETTES:
                    self.palettes.append(tempFile)
                else:
                    self.visor.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")
        # HICoatingMaterialSet 9
        # HIMaterialPalette 82
        # HIMaterialVisorSwatch 1
        for obj_p in f_array[1].split(shaderTypesValues[ShaderType.OBJ_1Space]):
            if obj_p == b'':
                continue
            self.files_paths.append(gf.offset_to_string_mem(obj_p + b"\00", 0))
            tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p+b"\00", 0))
            if tempFile is not None:
                tempFile.loadUnique()
                self.materials.append(tempFile)
            else:
                # tempFile = tryCreateFile(gf.offset_to_string_mem(obj_p + b"\00", 0))
                print(f"Debug error in {obj_p}")
        # HIMaterialSwatch 9
        print("Style coatings")
        print(self.coatings)

        print("Style materials")
        print(self.materials)


def load_material(material_path, x=''):
    material = tryCreateFile(material_path)
    if material is None:
        return None
    material.loadUnique()
    if "olympus_spartan_torso_001_s001" in material.path:
        print(filter)
    if material.path == "C:\\Users\\Jorge\\Downloads\\Compressed\\deploy1\\HIU\\objects\\characters\\spartan_armor\\materials\\olympus\\torso\\torso_001\\olympus_spartan_torso_001_belt_s001.material":
        print("fin")
        tempMs = []
        tempMsV = []
        for m in material.unique_files[FileTypes.MATERIALS]:
            if m.shader.path == "C:\\Users\\Jorge\\Downloads\\Compressed\\deploy1\\HIU\\__chore\\gen__\\pc__\\shaders\\surfaces\\cvw\\cvw_ld_matsys{10}_0{pc}.shadervariant":
                tempMs.append(m)
            else:
                tempMsV.append(m)
        print(tempMs)

    print(material)
    return material



    # print(gf.offset_to_string_mem(fb,offset))
    # print(chr(fb[fb.find(b"\x63\x76\x77\x5f\x6c\x64\x5f\x6d\x61\x74\x73\x79\x73\x7b\x31\x30\x7d\x5f\x30")]))

def getTextureParameterData(mat):
    result = None
    if len(mat.files_paths) == 0 or not mat.files_paths[0].__contains__('shaders'):
        print('Posible error')
    elif mat.files_paths[0].__contains__('cvw_ld_matsys{10}_0'):
        # and len(mat.files_paths) < 7
        # and not mat.files_paths[2].__contains__('default_normal')
        tempo = mat.files_paths[1:-1]
        temp_map = copy.deepcopy(map_texture_parameter)
        for k in map_texture_parameter.keys():
            for i in range(len(tempo)):
                if tempo[i].__contains__(k) or tempo[i].__contains__(map_texture_parameter[k]['path'].split('\\')[-1]):
                    temp_path = tempo.pop(i)
                    temp_map[k]['path'] = temp_path
                    temp_map[k]['control'] = True
                    break

        if len(tempo) > 0:

            for j in range(len(tempo)):
                for k in map_texture_parameter.keys():
                    if temp_map[k]['control'] == False:
                        temp_map[k]['path'] = tempo[j]
                        temp_map[k]['control'] = True
                        break
            #debug_list.append({"mat": mat, "temp_map": temp_map, "extr": tempo})

        result = temp_map
    return result

def all_from_directory():
    global folder
    last_mat = None
    p = [os.path.join(dp, f)[len(directory):].replace("\\", "/") for dp, dn, fn in os.walk(os.path.expanduser(directory)) for f in fn if ".material" in f and ".chunk" not in f and ".dds" not in f ]
    for path in p:
        x = path.split('/')[-1]
        folder = directory + path.replace(x, "")

        last_mat =load_material(materials_dir+path.replace('.'+x.split('.')[-1],''), x)
    return last_mat


if __name__ == "__main__":
    # deploy1\IU\objects\characters\spartan_armor\materials\mc117\glove\glove_006\ C:\Users\Jorge\Downloads\Compressed\deploy1\IU\objects\characters\spartan_armor\materials\
    # if the code isnt working try replacing all the backslashes with forward slashes in every directory
    last_mat = all_from_directory().unique_files
    if not last_mat is None:
        debug_list = []
        for mat in last_mat[FileTypes.MATERIALS]:
            if mat.obj_path.__contains__(''):
            #if mat.obj_path.__contains__('objects\\characters\\spartan_armor\\materials'):
                print(mat.name)
                if len(mat.files_paths) == 0 or not mat.files_paths[0].__contains__('shaders'):
                    print('Posible error')
                elif mat.files_paths[0].__contains__('cvw_ld_matsys{10}_0')  :
                    #and len(mat.files_paths) < 7
                    #and not mat.files_paths[2].__contains__('default_normal')
                    tempo= mat.files_paths[1:-1]
                    temp_map = copy.deepcopy(map_texture_parameter)
                    for k in  map_texture_parameter.keys():
                        for i in range(len(tempo)):
                            if tempo[i].__contains__(k) or tempo[i].__contains__(map_texture_parameter[k]['path'].split('\\')[-1]):
                                temp_path = tempo.pop(i)
                                temp_map[k]['path'] = temp_path
                                temp_map[k]['control'] = True
                                break

                    if len(tempo)>0:

                        for j in range(len(tempo)):
                            for k in  map_texture_parameter.keys():
                                if temp_map[k]['control'] == False:
                                    temp_map[k]['path'] = tempo[j]
                                    temp_map[k]['control'] = True
                                    break
                        debug_list.append({"mat": mat, "temp_map": temp_map, "extr": tempo})

                    print('new shader')

                elif not len(mat.files_paths) == 7:
                    print('Posible error en longitud')
                else:
                    print('Correct')
    print('fin')