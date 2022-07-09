import os
import struct


class GUID:
    def __init__(self):
        self.guid = "{00000000-0000-0000-0000-000000000000}"
        pass

    def readIn(self, f, header=None):
        temp_s = f.read(16).hex().upper()
        self.guid = '{' + temp_s[6:8] + temp_s[4:6] + temp_s[2:4] + temp_s[0:2] + "-" + temp_s[10:12] + temp_s[8:10] + \
                    "-" + temp_s[12:16] + "-" + temp_s[16:20] + "-" + temp_s[21:32] + "}"


def getGUID(hex_string):
    temp_s = hex_string.upper()
    return '{' + temp_s[6:8] + temp_s[4:6] + temp_s[2:4] + temp_s[0:2] + "-" + temp_s[10:12] + temp_s[8:10] + "-" \
           + temp_s[12:16] + "-" + temp_s[16:20] + "-" + temp_s[21:32] + "}"


class Header:

    def __init__(self):
        self.file_size = 0
        self.zone_set_offset = -1
        self.string_table_offset = -1
        self.isMagic = False
        self.magic = ''
        self.unknown_property_4 = -1
        self.section_3_alignment = -1
        self.section_2_alignment = -1
        self.tag_data_alignment = -1
        self.header_alignment = -1
        self.section_3_size = -1
        self.section_2_size = -1
        self.unknown_desc_info_type = -1
        self.huid = ''
        self.asset_checksum = -1
        self.data_block_count = -1
        self.data_block_offset = -1
        self.dependency_count = -1
        self.dependency_count_offset = 0x50  # always starts directly after the header
        self.tag_struct_count = -1
        self.tag_struct_offset = -1
        self.tag_reference_offset = -1
        self.tag_reference_count = -1
        self.string_table_size = -1
        self.data_reference_count = -1
        self.data_reference_offset = -1
        self.header_size = -1
        self.data_size = -1  # Length of the data that is part of the usual data structure and gets referenced by the tables
        self.zone_set_size = -1  # Length of the field after the strings (unknown purpose)

        self.section_0_bin_data = b''
        self.header_str_bin_data = b''
        self.header_zone_set_bin_data = b''
        self.section_1_bin_data = b''
        self.section_2_bin_data = b''
        self.section_3_bin_data = b''

    def checkMagic(self, f):
        f.seek(0x0)
        if f.read(4) != b'ucsh':
            self.isMagic = False
            f.seek(0x0)
            return False
        else:
            self.isMagic = True
            f.seek(0x0)
            return True

    def readHeader(self, f):
        # self.huid.readIn(f)
        bytes_unk = f.read(16)
        # self.Magic = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.magic = struct.unpack('4s', bytes_unk[0:4])[0]

        # [FieldOffset(4)]
        self.version = int.from_bytes(bytes_unk[4:8], 'little', signed=True)

        # [FieldOffset(8)]
        # ulong

        bytes_unk_str = bytes_unk[8:16].hex()

        # self.GUID = getGUID(bytes_unk_str)
        self.huid = bytes_unk_str
        self.asset_checksum = int.from_bytes(f.read(8), 'little', signed=False)
        # f.seek(0x18)  # Beta n -> 0x18 Beta 1-> 0x38
        # Table 1 data (unknown purpose, but needed to calculate offsets)
        # entry size 0x18
        self.dependency_count_offset = 0x50  # fixed, directly after the header
        self.dependency_count = int.from_bytes(f.read(4), 'little')  # 0x18

        # Data Table (contains offsets and sizes of data blocks, referenced by content table)
        # size 0x10
        self.data_block_offset = self.dependency_count_offset + self.dependency_count * 0x18  #
        self.data_block_count = int.from_bytes(f.read(4), 'little')  # 0x1c

        # Content Table (contains references to data table entries and a hash to identify the type of entry)
        # size 0x20
        self.tag_struct_offset = self.data_block_offset + self.data_block_count * 0x10
        self.tag_struct_count = int.from_bytes(f.read(4), 'little')  # 0x20

        # Data Block Table (contains offsets to model data blocks)
        # size 0x14
        self.data_reference_offset = self.tag_struct_offset + self.tag_struct_count * 0x20
        self.data_reference_count = int.from_bytes(f.read(4), 'little')  # 0x24

        # String stuff
        self.tag_reference_offset = self.data_reference_offset + self.data_reference_count * 0x14
        self.tag_reference_count = int.from_bytes(f.read(4), 'little')  # 0x28
        self.string_table_offset = self.tag_reference_offset + (self.tag_reference_count * 0x10)
        self.string_table_size = int.from_bytes(f.read(4), 'little')  # 0x2c
        self.zone_set_offset = self.string_table_offset + self.string_table_size
        self.zone_set_size = int.from_bytes(f.read(4), 'little')  # 0x30

        self.unknown_desc_info_type = int.from_bytes(f.read(4), 'little', signed=False)

        self.header_size = int.from_bytes(f.read(4), 'little')  # 0x38
        self.data_size = int.from_bytes(f.read(4), 'little')  # 0x3c
        # [FieldOffset(64)]
        # uint
        self.section_2_size = int.from_bytes(f.read(4), 'little', signed=True)

        # [FieldOffset(68)]
        self.section_3_size = int.from_bytes(f.read(4), 'little', signed=True)

        # [FieldOffset(72)]
        # byte
        self.header_alignment = int.from_bytes(f.read(1), 'little', signed=True)

        # [FieldOffset(73)]
        # byte
        self.tag_data_alignment = int.from_bytes(f.read(1), 'little', signed=True)

        # [FieldOffset(74)]
        # byte
        self.section_2_alignment = int.from_bytes(f.read(1), 'little', signed=True)

        # [FieldOffset(75)]
        # byte
        self.section_3_alignment = int.from_bytes(f.read(1), 'little', signed=True)

        # [FieldOffset(76)]
        self.unknown_property_4 = int.from_bytes(f.read(4), 'little', signed=True)

        f.seek(0)
        self.section_0_bin_data = f.read(self.header_size)
        self.section_1_bin_data = f.read(self.data_size)
        self.section_2_bin_data = f.read(self.section_2_size)
        self.section_3_bin_data = f.read(self.section_3_size)
        self.file_size = self.header_size + self.data_size + self.section_2_size + self.section_3_size
        if os.path.getsize(f.name) != self.file_size:
            debug=True
        f.seek(self.string_table_offset)
        self.header_str_bin_data = f.read(self.string_table_size)
        self.header_zone_set_bin_data = f.read(self.zone_set_size)


    def getOtherData(self, f):
        data_start = self.tag_reference_offset + self.string_table_size + self.zone_set_size
        data_len = self.header_size - data_start
        f.seek(data_start)
        return f.read(data_len)
