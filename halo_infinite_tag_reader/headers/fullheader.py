from halo_infinite_tag_reader.headers.contenttable import ContentTable
from halo_infinite_tag_reader.headers.data_block_table import DataBlockTable
from halo_infinite_tag_reader.headers.datatable import DataTable
from halo_infinite_tag_reader.headers.header import Header
from halo_infinite_tag_reader.headers.stringtable import StringTable
from halo_infinite_tag_reader.headers.tag_ref_table import TagRefTable


class FullHeader:

    def __init__(self):
        self.file_header = Header()
        self.tag_ref_table = TagRefTable()
        self.data_table = DataTable()
        self.content_table = ContentTable()
        self.data_block_table = DataBlockTable()
        self.string_table = StringTable()

    def readIn(self, f):
        self.file_header.readHeader(f)
        self.tag_ref_table.readTable(f, self.file_header)
        self.data_table.readTable(f, self.file_header)
        self.data_block_table.readTable(f, self.file_header)
        self.content_table.readTable(f, self.file_header, self.data_table)
        self.string_table.readStrings(f, self.file_header)

