import os
import struct

from tag_reader.headers.data_block_table import DataBlock
from tag_reader.headers.tag_struct_table import TagStruct


class DataReference:

    def __init__(self):
        self.parent_struct_index = None
        self.parent_struct: TagStruct = None
        self.unknown_property = None
        # self.target_index = None
        self.field_data_block_index = None
        self.field_data_block: DataBlock = None
        # self.field_block = None
        self.parent_field_data_block_index = None
        self.field_offset = None
        self.bin_data = b''
        self.bin_data_hex = ""
        self.loaded_bin_data = False
        self.path_file = ''

    def readIn(self, f, header=None):
        self.path_file = f.name
        self.parent_struct_index = struct.unpack('i', f.read(4))[0]
        assert self.parent_struct_index < header.tag_struct_count
        self.unknown_property = struct.unpack('i', f.read(4))[0]
        if self.unknown_property != 0:
            debug = 1

        self.field_data_block_index = struct.unpack('i', f.read(4))[0]
        self.parent_field_data_block_index = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]
        # self.offset_plus = self.offset + header.data_offset

    def readBinData(self, f=None, header=None):
        if self.field_data_block_index != -1:
            f_close = False
            if f is None:
                f = open(self.path_file, 'rb')
                f_close = True
            pos_on_init = f.tell()
            f.seek(self.field_data_block.offset_plus)
            self.bin_data = f.read(self.field_data_block.size)
            f.seek(pos_on_init)
            if f_close:
                f.close()
            self.bin_data_hex = self.bin_data.hex()
        self.loaded_bin_data = True


class DataReferenceTable:

    def __init__(self):
        self.entries = []

        pass

    def readTable(self, f, header, data_block_table, tag_struct_table, read_entry_data=False):

        f.seek(header.data_reference_offset)
        for x in range(header.data_reference_count):
            entry = DataReference()
            # print(offset)
            entry.readIn(f, header)
            entry.parent_struct = tag_struct_table.entries[entry.parent_struct_index]
            if entry.field_data_block_index != -1:
                entry.field_data_block = data_block_table.entries[entry.field_data_block_index]
                if read_entry_data:
                    entry.readBinData(f, header)
                else:
                    entry.bin_data = [None] * entry.field_data_block.size

            entry.parent_struct.l_function.append(entry)
            self.entries.append(entry)
        return

    def getContentEntryByRefIndex(self, ref_index):
        count = 0
        entry_found = None
        for i, entry in enumerate(self.entries):
            if entry.field_data_block_index == ref_index:
                count = count + 1
                entry_found = i
                return entry_found
        if count > 1:
            print(count)
        return entry_found
