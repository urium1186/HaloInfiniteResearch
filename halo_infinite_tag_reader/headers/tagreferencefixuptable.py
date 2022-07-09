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


class TagReferenceFixup:

    def __init__(self):
        self.field_block = -1
        self.field_offset = -1
        self.name_offset = -1
        self.dependency_index = -1
        self.str_path = ""
        pass

    def readIn(self, f, header=None):
        self.field_block = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]
        self.name_offset = struct.unpack('i', f.read(4))[0]
        self.dependency_index = struct.unpack('i', f.read(4))[0]
        temp_offset = (header.tag_reference_offset + (header.tag_reference_count * 0x10)) + self.name_offset
        self.str_path = readStringInPlace(f, temp_offset, True)


class TagReferenceFixupTable:

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
        f.seek(header.tag_reference_offset)
        for x in range(header.tag_reference_count):
            self.entries.append(TagReferenceFixup())
            self.entries[x].readIn(f, header)

        offset_1 = f.tell()
        lastPos = offset_1 + header.string_table_size
        while offset_1<lastPos:
            self.strings.append(readStringInPlace(f, offset_1))
            offset_1 = f.tell()

