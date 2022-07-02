import struct


class DataBlockTableEntry:

    def __init__(self):
        self.type = None
        self.type_fill = None
        self.parent_index = None
        self.parent_index_fill = None
        self.offset = None

    def readIn(self, f, header=None):
        self.type = struct.unpack('i', f.read(4))[0]
        self.type_fill = struct.unpack('i', f.read(4))[0]
        self.parent_index = struct.unpack('i', f.read(4))[0]
        self.parent_index_fill = struct.unpack('i', f.read(4))[0]
        self.offset = struct.unpack('i', f.read(4))[0]
        #self.offset_plus = self.offset + header.data_offset


class DataBlockTable:

    def __init__(self):
        self.entries = []
        pass

    def readTable(self, f, header):
        f.seek(header.data_block_table_offset)
        for x in range(header.data_block_table_count):
            entry = DataBlockTableEntry()
            # print(offset)
            entry.readIn(f, header)
            self.entries.append(entry)
        return
