from typing import BinaryIO

from halo_infinite_tag_reader.taglayouts import TagLayouts
from halo_infinite_tag_reader.headers.tagstructtable import TagStruct


class TagInstance:

    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        self.tagDef = tag
        self.content_entry: TagStruct = None
        self.childs: [TagInstance] = []
        self.parent: TagInstance = None
        self.addressStart = addressStart
        self.offset = offset
        self.inst_parent_offset = -1
        self.inst_address = -1
        self.extra_data = {}
        pass

    def readIn(self, f: BinaryIO, header=None):
        self.inst_address = f.tell()
        self.inst_parent_offset = self.inst_address - self.addressStart

    def getFirstChild(self):
        if len(self.childs) > 0:
            return self.childs[0]
        else:
            return None

    def getGlobalAddress(self):
        if self.data_reference is not None:
            return self.data_reference.field_data_block.offset_plus
        else:
            return -1

    def toJson(self):
        dict = {'extra_data': self.extra_data,
                'items': []}
        for ch in self.childs:
            temp_dict = {}
            if ch.__class__ == {}.__class__:
                for key in ch.keys():
                    temp_dict[key] = ch[key].toJson()
                dict['items'].append(temp_dict)
            else:
                dict['items'].append(ch.toJson())
        return dict
