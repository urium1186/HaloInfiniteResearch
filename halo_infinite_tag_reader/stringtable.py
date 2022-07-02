"""
class StringTableEntry:
    local
    int
    init_offset = FTell();
    int
    unknown_0x0;
    int
    tag_ref;
    FSeek(init_offset + 0x8);
    int
    string_offset;
    int
    string_index;
    const
    int
    temp_offset = (header.string_offset + (header.string_count * 0x10)) + string_offset;
    const
    string
    str = ReadString(temp_offset);
"""
import struct

from typing.io import BinaryIO

from halo_infinite_tag_reader.common_tag_types import readStringInPlace


class StringTableEntry:

    def __init__(self):
        self.unknown_0x0 = -1
        self.unknown_0x1 = -1
        self.string_offset = -1
        self.string_index = -1
        self.str_path = ""
        pass

    def readIn(self, f, header=None):
        self.unknown_0x0 = struct.unpack('i', f.read(4))[0]
        self.unknown_0x1 = struct.unpack('i', f.read(4))[0]
        self.string_offset = struct.unpack('i', f.read(4))[0]
        self.string_index = struct.unpack('i', f.read(4))[0]
        temp_offset = (header.string_offset + (header.string_count * 0x10)) + self.string_offset
        self.str_path = readStringInPlace(f, temp_offset, True)


class StringTable:

    def __init__(self):
        self.entries = []
        self.strings = []
        pass


        """
        while True:
            char = f.read(1)
            if char == b'\x00':
                return "".join(string)
            string.append(char.decode("utf-8"))
        """


    def readStrings(self,f:BinaryIO,header,verbose=False):
        #f.readline()
        f.seek(header.string_offset)
        for x in range(header.string_count):
            self.entries.append(StringTableEntry())
            self.entries[x].readIn(f, header)

        offset_1 = f.tell()
        lastPos = offset_1 + header.string_length
        while offset_1<lastPos:
            self.strings.append(readStringInPlace(f, offset_1))
            offset_1 = f.tell()

