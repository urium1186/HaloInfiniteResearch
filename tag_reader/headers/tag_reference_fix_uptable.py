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

from tag_reader.headers.tag_ref_table import TagDependency
from tag_reader.headers.tag_struct_table import TagStruct
from tag_reader.tag_reader_utils import readStringInPlace


class TagReferenceFixup:

    def __init__(self):
        self.field_block = -1
        self.field_offset = -1
        self.name_offset = -1
        self.dependency_index = -1
        self.tag_dependency: TagDependency = None
        self.parent_struct: TagStruct = None
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

    def readStrings(self, f: BinaryIO, header, data_block_table, tag_struct_table, tag_dependency_table, verbose=False):
        # f.readline()
        f.seek(header.tag_reference_offset)
        for x in range(header.tag_reference_count):
            self.entries.append(TagReferenceFixup())
            self.entries[x].readIn(f, header)
            if self.entries[x].field_block >= len(data_block_table.entries):
                debug = True
                assert False
            db = data_block_table.entries[self.entries[x].field_block]
            for tag_i in tag_struct_table.entries:
                if tag_i.field_data_block == db:
                    self.entries[x].parent_struct = tag_i
                    break
            if self.entries[x].parent_struct is None:
                debug =True
            if self.entries[x].dependency_index != -1:
                self.entries[x].tag_dependency = tag_dependency_table.entries[self.entries[x].dependency_index]
                assert self.entries[x].name_offset == self.entries[x].tag_dependency.name_offset
            else:
                debug = True
            self.entries[x].parent_struct.l_tag_ref.append(self.entries[x])
        offset_1 = f.tell()
        lastPos = offset_1 + header.string_table_size
        while offset_1 < lastPos:
            self.strings.append(readStringInPlace(f, offset_1))
            offset_1 = f.tell()
