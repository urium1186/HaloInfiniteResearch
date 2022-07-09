import io

from halo_infinite_tag_reader.headers.tagstructtable import TagStructTable
from halo_infinite_tag_reader.headers.data_reference_table import DataReferenceTable
from halo_infinite_tag_reader.headers.datablocktable import DataBlockTable
from halo_infinite_tag_reader.headers.header import Header
from halo_infinite_tag_reader.headers.tagreferencefixuptable import TagReferenceFixupTable
from halo_infinite_tag_reader.headers.tagreftable import TagDependencyTable
from halo_infinite_tag_reader.headers.ver.tag import Tag
from halo_infinite_tag_reader.headers.zoneset import ZoneSet


class TagBaseReader:

    def __init__(self):
        self.file_header = Header()
        self.tag_dependency_table = TagDependencyTable()
        self.data_block_table = DataBlockTable()
        self.tag_struct_table = TagStructTable()
        self.data_reference_table = DataReferenceTable()
        self.tag_reference_fixup_table = TagReferenceFixupTable()  # string_table
        self.zone_set = None

    def readIn(self, f):
        self.file_header.readHeader(f)
        self.tag_dependency_table.readTable(f, self.file_header)
        self.data_block_table.readTable(f, self.file_header)
        self.tag_struct_table.readTable(f, self.file_header, self.data_block_table)
        self.data_reference_table.readTable(f, self.file_header)
        self.tag_reference_fixup_table.readStrings(f, self.file_header)

        bin_stream = io.BytesIO(self.file_header.header_zone_set_bin_data)
        self.zone_set = ZoneSet(bin_stream)
