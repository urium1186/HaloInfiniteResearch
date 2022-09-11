import struct

from commons.debug_utils import debug_DataBlock, fillDebugDict


class DataBlock:

    def __init__(self):
        self.section = -1
        self.offset = -1
        self.size = -1
        self.unknown_property = -1
        self.offset_plus = -1

    def readIn(self, f, header=None):
        self.size = struct.unpack('i', f.read(4))[0]
        self.unknown_property = struct.unpack('H', f.read(2))[0]  # only change in render_model
        self.section = struct.unpack('H', f.read(2))[0]
        self.offset = struct.unpack('Q', f.read(8))[0]
        if self.section == 1:
            self.offset_plus = self.offset + header.header_size
        elif self.section == 2:
            self.offset_plus = self.offset + header.header_size + header.data_size
        elif self.section == 3:
            self.offset_plus = self.offset + header.header_size + header.data_size + header.section_2_size
        else:
            debug = True

        main_key = self.unknown_property
        if self.unknown_property !=0:
            debug = True
            header.data_reference_count


        name_key = f.name.split('\\')[-1]
        fillDebugDict(main_key, name_key, debug_DataBlock)



class DataBlockTable:

    def __init__(self):
        self.entries = []
        pass

    def readTable(self, f, header):
        f.seek(header.data_block_offset)
        for x in range(header.data_block_count):
            entry = DataBlock()
            # print(offset)
            entry.readIn(f, header)
            self.entries.append(entry)
        return
