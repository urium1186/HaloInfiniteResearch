import io

from commons.exception.read_tag_struct_exception import ReadTagStructException
from tag_reader.headers.general_class import PreLoadSections
from tag_reader.headers.tag_struct_table import TagStructTable
from tag_reader.headers.data_reference_table import DataReferenceTable
from tag_reader.headers.data_block_table import DataBlockTable
from tag_reader.headers.header import Header
from tag_reader.headers.tag_reference_fix_uptable import TagReferenceFixupTable
from tag_reader.headers.tag_ref_table import TagDependencyTable
from tag_reader.headers.zone_set import ZoneSet


class TagBaseReader:

    def __init__(self, p_read_ref_data = False):
        self.file_header = Header()
        self.tag_dependency_table = TagDependencyTable()
        self.data_block_table = DataBlockTable()
        self.tag_struct_table = TagStructTable()
        self.data_reference_table = DataReferenceTable()
        self.tag_reference_fixup_table = TagReferenceFixupTable()  # string_table
        self.zone_set = None
        self.read_ref_entry_data = p_read_ref_data

    def readIn(self, f):
        self.file_header.readHeader(f)
        self.tag_dependency_table.readTable(f, self.file_header)
        self.data_block_table.readTable(f, self.file_header)
        try:
            self.tag_struct_table.readTable(f, self.file_header, self.data_block_table)
        except ReadTagStructException as e:
            print(f"ReadTagStructException in {e.file_name} on {e.tag_struct} ")
        self.data_reference_table.readTable(f, self.file_header,self.data_block_table,self.tag_struct_table, self.read_ref_entry_data)
        self.tag_reference_fixup_table.readStrings(f, self.file_header, self.data_block_table, self.tag_struct_table,self.tag_dependency_table)

        bin_stream = io.BytesIO(self.file_header.header_zone_set_bin_data)
        self.zone_set = ZoneSet(bin_stream)

    def readInOnlyHeader(self, f):
        self.file_header.readHeader(f, PreLoadSections(s_all=False))

