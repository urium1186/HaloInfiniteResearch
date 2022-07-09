import struct

from commons.common_utils import getGUID
from commons.debug_utils import debug_TagStruct, fillDebugDict, debug_TagStruct_Type
from commons.enums_struct_def import TagStructType
from halo_infinite_tag_reader.headers.datablocktable import DataBlock


class TagStruct:

    def __init__(self):
        # self.hash = GUID()
        self.info = {}
        self.GUID = ''
        self.GUID1 = ''
        self.GUID2 = ''
        self.type_id = -1
        self.unknown_property_bool_0_1 = -1
        self.target_index = -1
        self.field_block = -1
        self.field_offset = -1
        self.data_reference: DataBlock = None
        self.data_parent: DataBlock = None
        self.parent: TagStruct = None
        self.childs: [TagStruct] = []
        self.parent_entry_index = -1
        self.entry_index = -1
        self.bin_datas = []
        self.bin_datas_hex = []
        self.type_ = 'Tagblock'
        self.field_name = ''

    def readIn(self, f, header=None):
        # self.hash.readIn(f, header)
        self.GUID1 = f.read(8).hex()
        self.GUID2 = f.read(8).hex()
        self.GUID = getGUID(self.GUID1 + self.GUID2)
        self.type_id = struct.unpack('H', f.read(2))[0]
        self.unknown_property_bool_0_1 = struct.unpack('H', f.read(2))[0]
        self.target_index = struct.unpack('i', f.read(4))[0]
        self.field_block = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]

        main_key = self.type_id

        name_key = f.name.split('\\')[-1]
        fillDebugDict(main_key, name_key, debug_TagStruct)

    def readTagStructInfo(self, f):
        address_to_back = f.tell()
        address = -1
        info = {"property_addres": 0,
                "n_childs": -1
                }
        if self.type_id == TagStructType.Root:
            info = {"property_addres": 0,
                    "n_childs": 1
                    }
            if self.field_block != -1:
                raise Exception("Root no debe pertenecer a otro campo")
        elif self.type_id == TagStructType.Tagblock:
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 16)
            info = {"property_addres": address,
                    "n_childs": struct.unpack('i', f.read(4))[0]
                    }
        elif self.type_id == TagStructType.ExternalFileDescriptor:
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 12)
            info = {"property_addres": address,
                    "n_childs": struct.unpack('i', f.read(4))[0]
                    }
            if info["n_childs"] != 0:
                raise Exception("ExternalFileDescriptor no debe tener hijos, ya que estan en archivo aparte")

        elif self.type_id == TagStructType.ResourceHandle:
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 12)
            info = {"property_addres": address,
                    "n_childs": struct.unpack('i', f.read(4))[0]
                    }

        elif self.type_id == TagStructType.NoDataStartBlock:
            address = self.data_parent.offset_plus + self.field_offset
            if self.target_index != -1:
                raise Exception("NoDataStartBlock significa q no tiene informacion")
            f.seek(address)
            info = {"property_addres": address,
                    "n_childs": struct.unpack('i', f.read(4))[0]
                    }

        f.seek(address_to_back)
        return info

    def readDataEntry(self, f):
        blocks = []
        pos_on_init = f.tell()
        self.info = self.readTagStructInfo(f=f)
        if self.type_id == TagStructType.NoDataStartBlock:
            return blocks
        elif self.type_id == TagStructType.ExternalFileDescriptor:
            if self.info["n_childs"] != 0:
                raise Exception("Error de interpretacion de Datos, ya q son externos")
            f.seek(self.data_reference.offset_plus)
            blocks.append(f.read(self.data_reference.size))
            f.seek(pos_on_init)
            return blocks
        else:
            if self.info["n_childs"] == 0:
                if self.target_index != -1:
                    raise Exception("Si no tiene hijos, el refernce deberia ser -1")
                return blocks
            else:
                count = divmod(self.data_reference.size, self.info["n_childs"])

                if count[1] != 0:
                    raise Exception(' Deberia ser 0 siempre el resto')
                else:
                    if self.data_reference.size == 0:
                        raise Exception(
                            ' Deberia ser moyor q 0, de lo contrario seria un bloke vacio, error division 0')
                    f.seek(self.data_reference.offset_plus)
                    sub_block_size = count[0]
                    for k in range(self.info["n_childs"]):
                        blocks.append(f.read(sub_block_size))
                    f.seek(pos_on_init)
                    return blocks
    """
    def readAllIn(self, f, header=None) -> {}:
        result = {"entry_data": None,
                  "child_datas": {}}
        if self.childs.__len__() != 0:
            for entry in self.childs:
                result["entry_data"] = self.readDataEntry(f)
                result["child_datas"][entry] = entry.readAllIn(f, header)
            return result
        else:
            result["entry_data"] = self.readDataEntry(f)
            return result
    """

class TagStructTable:
    def __init__(self) -> None:
        self.entries: [TagStruct] = []
        pass

    def readTable(self, f, header, data_table):
        f.seek(header.tag_struct_offset)
        for x in range(header.tag_struct_count):
            # offset = header.content_table_offset + x * 0x20
            entry = TagStruct()
            entry.readIn(f, header)

            if header.data_block_count > entry.target_index > -1:
                entry.data_reference = data_table.entries[entry.target_index]

            if header.data_block_count > entry.field_block > -1:
                entry.data_parent = data_table.entries[entry.field_block]

                p_i = self.getContentEntryByRefIndex(entry.field_block)
                if p_i is not None:
                    entry.parent_entry_index = p_i
                    entry.parent = self.entries[p_i]
                    self.entries[p_i].childs.append(entry)

            entry.entry_index = self.entries.__len__()
            entry.bin_datas = entry.readDataEntry(f)
            for data in entry.bin_datas:
                entry.bin_datas_hex.append(data.hex())
            self.entries.append(entry)

    def getContentEntryByRefIndex(self, ref_index):
        count = 0
        entry_found = None
        for i, entry in enumerate(self.entries):
            if entry.target_index == ref_index:
                count = count + 1
                entry_found = i
                return entry_found
        if count > 1:
            print(count)
        return entry_found
