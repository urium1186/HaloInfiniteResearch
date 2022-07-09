import struct


class DataReference:

    def __init__(self):
        self.parent_struct_index = None
        self.unknown_property = None
        self.target_index = None
        self.field_block = None
        self.field_offset = None

    def readIn(self, f, header=None):
        self.parent_struct_index = struct.unpack('i', f.read(4))[0]
        self.unknown_property = struct.unpack('i', f.read(4))[0]
        if self.unknown_property !=0:
            debug = 1
        self.target_index = struct.unpack('i', f.read(4))[0]
        self.field_block = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]
        #self.offset_plus = self.offset + header.data_offset


class DataReferenceTable:

    def __init__(self):
        self.entries = []
        pass

    def readTable(self, f, header):
        f.seek(header.data_reference_offset)
        for x in range(header.data_reference_count):
            entry = DataReference()
            # print(offset)
            entry.readIn(f, header)
            self.entries.append(entry)
        return
