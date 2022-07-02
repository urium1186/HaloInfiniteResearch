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
        self.huid = GUID()
        self.data_table_count = -1
        self.data_table_offset = -1
        self.tagref_table_count = -1
        self.tagref_table_offset = 0x50  # always starts directly after the header
        self.content_table_count = -1
        self.content_table_offset = -1
        self.string_offset = -1
        self.string_count = -1
        self.string_length = -1
        self.data_block_table_count = -1
        self.data_block_table_offset = -1
        self.data_offset = -1
        self.data_len = -1  # Length of the data that is part of the usual data structure and gets referenced by the tables
        self.other_data_len = -1  # Length of additional data, in other formats
        self.some_field_length = -1  # Length of the field after the strings (unknown purpose)
        pass

    def checkMagic(self, f):
        f.seek(0x0)
        if f.read(4) != b'ucsh':
            self.magic = False
            return False
        else:
            self.magic = True
            return True

    def readHeader(self, f):
        self.huid.readIn(f)
        f.seek(0x18)  # Beta n -> 0x18 Beta 1-> 0x38
        # Table 1 data (unknown purpose, but needed to calculate offsets)
        # entry size 0x18
        self.tagref_table_offset = 0x50  # fixed, directly after the header
        self.tagref_table_count = int.from_bytes(f.read(4), 'little')  # 0x18

        # Data Table (contains offsets and sizes of data blocks, referenced by content table)
        # size 0x10
        self.data_table_offset = self.tagref_table_offset + self.tagref_table_count * 0x18  #
        self.data_table_count = int.from_bytes(f.read(4), 'little')  # 0x1c

        # Content Table (contains references to data table entries and a hash to identify the type of entry)
        # size 0x20
        self.content_table_offset = self.data_table_offset + self.data_table_count * 0x10
        self.content_table_count = int.from_bytes(f.read(4), 'little')  # 0x20

        # Data Block Table (contains offsets to model data blocks)
        # size 0x14
        self.data_block_table_offset = self.content_table_offset + self.content_table_count * 0x20
        self.data_block_table_count = int.from_bytes(f.read(4), 'little')  # 0x24

        # String stuff
        self.string_offset = self.data_block_table_offset + self.data_block_table_count * 0x14
        self.string_count = int.from_bytes(f.read(4), 'little')  # 0x28
        self.string_length = int.from_bytes(f.read(4), 'little')  # 0x2c

        self.some_field_length = int.from_bytes(f.read(4), 'little')  # 0x30

        # Data offset
        f.seek(0x38)
        self.data_offset = int.from_bytes(f.read(4), 'little')  # 0x38
        self.data_len = int.from_bytes(f.read(4), 'little')  # 0x3c

    def getOtherData(self, f):
        data_start = self.string_offset + self.string_length + self.some_field_length
        data_len = self.data_offset - data_start
        f.seek(data_start)
        return f.read(data_len)
