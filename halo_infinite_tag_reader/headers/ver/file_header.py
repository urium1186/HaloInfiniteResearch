import os
import struct

from commons.common_utils import getGUID, map_CUID
from commons.debug_utils import debug_dict_1, debug_dict


class FileHeader:

    def __init__(self, pf):
        debug = False
        self.f = pf
        name = self.f.name.split('\\')[-1]
        self.f.seek(0x0)  #
        # [FieldOffset(0)]
        bytes_unk = self.f.read(16)
        #self.Magic = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.Magic = struct.unpack('4s', bytes_unk[0:4])[0]

        # [FieldOffset(4)]
        self.Version = int.from_bytes(bytes_unk[4:8], 'little', signed=True)

        # [FieldOffset(8)]
        # ulong

        bytes_unk_str = bytes_unk[8:16].hex()

        #self.GUID = getGUID(bytes_unk_str)
        self.GUID = bytes_unk_str
        """
        ext_key = self.f.name.split('.')[-1]
        if map_CUID.keys().__contains__(self.GUID):
            if not map_CUID[self.GUID].__contains__(ext_key):
                map_CUID[self.GUID].append(ext_key)
        else:
            map_CUID[self.GUID] = [ext_key]
            print(f"'{self.GUID}': '{ext_key}',")
        """
        # [FieldOffset(16)]
        # ulong
        self.AssetChecksum = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(24)]
        self.DependencyCount = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(28)]
        self.DataBlockCount = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(32)]
        self.TagStructCount = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(36)]
        self.DataReferenceCount = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(40)]
        self.TagReferenceCount = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(44)]
        # uint
        self.StringTableSize = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(48)]
        self.ZoneSetSize = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(52)]
        # uint
        self.ZoneSetType = int.from_bytes(self.f.read(4), 'little', signed=False)
        if self.ZoneSetType>4:
            debug = True
        key = self.ZoneSetType
        value_key = name.split(".")[-1]
        if debug_dict_1.keys().__contains__(key):
            if not debug_dict_1[key].__contains__(value_key):
                debug_dict_1[key].append(value_key)
        else:
            debug_dict_1[key] = [value_key]


        # [FieldOffset(56)]
        # uint
        self.HeaderSize = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(60)]
        # uint
        self.DataSize = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(64)]
        # uint
        self.Section2Size = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(68)]
        self.Section3Size = int.from_bytes(self.f.read(4), 'little', signed=True)
        if self.Section3Size !=0:
            debug = True

        # [FieldOffset(72)]
        # byte
        self.HeaderAlignment = int.from_bytes(self.f.read(1), 'little', signed=True)
        if self.HeaderAlignment != 0:
            debug = True

        # [FieldOffset(73)]
        # byte
        self.TagDataAlignment = int.from_bytes(self.f.read(1), 'little', signed=True)

        # [FieldOffset(74)]
        # byte
        self.Section2Alignment = int.from_bytes(self.f.read(1), 'little', signed=True)

        #key = f"{self.TagDataAlignment}"
        key = f"{ self.Section2Size} - {self.Section2Alignment}"

        if name.split('.')[-1] == 'material':
            if self.Section2Size != 0:
                debug = True
            if self.Section2Alignment == 0:
                debug = True

        if key == '0 - 0' and name.split('.')[-1] == 'material':
            debug = True
        else:
            if key != '0 - 0' and name.split('.')[-1] != 'material':
                debug = True
        if debug_dict.keys().__contains__(key):
            if not debug_dict[key].__contains__(name):
                debug_dict[key].append(name)
        else:
            debug_dict[key] = [name]


        # [FieldOffset(75)]
        # byte
        self.Section3Alignment = int.from_bytes(self.f.read(1), 'little', signed=True)

        # [FieldOffset(76)]
        self.UnknownProperty4_bitmap = int.from_bytes(self.f.read(4), 'little', signed=True)
        if self.UnknownProperty4_bitmap !=0:
            debug = True
        self.FileSize = self.HeaderSize + self.DataSize + self.Section3Size + self.Section2Size
        if os.path.getsize(self.f.name) != self.FileSize:
            debug = True
        if debug:
            #print(f"{self.UnknownProperty2}-{self.UnknownProperty3}-{self.UnknownProperty4}")
            #print(self.f.name)
            debug = False


