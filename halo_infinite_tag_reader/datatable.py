import struct


class DataTableEntry:

    def __init__(self):
        self.offset_type = -1
        self.offset = -1
        self.offset_fill = -1
        self.size = -1
        self.size_fill = -1
        self.offset_plus = -1

    def readIn(self, f, header=None):
        self.size = struct.unpack('i', f.read(4))[0]
        self.size_fill = struct.unpack('H', f.read(2))[0]
        self.offset_type = struct.unpack('H', f.read(2))[0]
        self.offset = struct.unpack('i', f.read(4))[0]
        self.offset_fill = struct.unpack('i', f.read(4))[0]
        self.offset_plus = self.offset + header.data_offset


class DataTable:

    def __init__(self):
        self.entries = []
        pass

    def readTable(self, f, header):
        f.seek(header.data_table_offset)
        for x in range(header.data_table_count):
            entry = DataTableEntry()
            # print(offset)
            entry.readIn(f, header)
            self.entries.append(entry)
        return
