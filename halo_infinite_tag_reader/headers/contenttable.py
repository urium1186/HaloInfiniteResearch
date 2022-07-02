import struct

from halo_infinite_tag_reader.headers.datatable import DataTableEntry
from halo_infinite_tag_reader.headers.header import GUID


class ContentTableEntry:

    def __init__(self):
        self.hash = GUID()
        self.space = -1
        self.ref_index = -1
        self.parent_index = -1
        self.parent_offset = -1
        self.data_reference : DataTableEntry = None
        self.data_parent: DataTableEntry = None
        self.parent: ContentTableEntry = None
        self.childs: [ContentTableEntry] = []
        self.parent_entry_index = -1
        self.entry_index = -1
        self.bin_datas = []
        self.bin_datas_hex = []
        self.type = 'Tagblock'
        self.property_name = ''

    def readIn(self, f, header=None):
        self.hash.readIn(f, header)
        self.space = struct.unpack('i', f.read(4))[0]
        self.ref_index = struct.unpack('i', f.read(4))[0]
        self.parent_index = struct.unpack('i', f.read(4))[0]
        self.parent_offset = struct.unpack('i', f.read(4))[0]

    def readTagBlokInfo(self, f):
        address = -1 #isTagblock=True
        info = {"property_addres": address,
                "type": 'Tagblock',
                "addres_dir_1": -1,
                "n_sub": -1,
                "n_p_chls":-1,
                "n_childs": -1
                }
        address_to_back = f.tell()
        if self.parent is not None and self.data_parent is not None:
            address = self.data_parent.offset_plus + self.parent_offset
            f.seek(address)
            info = {"property_addres": address,
                    "type": 'Tagblock',
                    "addres_dir_1": struct.unpack('Q', f.read(8))[0],
                    "n_sub": struct.unpack('i', f.read(4))[0],
                    "n_p_chls": struct.unpack('i', f.read(4))[0],
                    "n_childs": -1
                    }

            try:
                info["n_childs"] = struct.unpack('i', f.read(4))[0]
            except:
                info["n_childs"] = -1

            if info['n_p_chls'] > -1:
                info["n_childs"] = info['n_p_chls']
                info["type"] = "ResourceHandle"
                debug = info['n_p_chls']  # Is HandleResource
                f.seek(address_to_back)
                return info
            else:
                if info['n_childs'] < -1:
                    if self.data_reference is None:
                        info["type"] = "NoDataStartBlock"
                        f.seek(address_to_back)
                        return info
                else:
                    f.seek(address_to_back)
                    return info
                debug = info['n_p_chls']  # Error o Desconocido

                f.seek(address_to_back)
                return None


        f.seek(address_to_back)
        if self.data_reference is not None:
            if self.data_reference.size_fill != 0:
                info["n_p_chls"] = self.data_reference.size_fill
                info["type"] = "RawBlock"
                return info
            if self.data_reference.offset_type != 1:
                info["n_p_chls"] = self.data_reference.offset_type
                info["type"] = "RawBlock"
                return info
            if self.entry_index == 0:
                info["n_childs"] = 1
                info["type"] = "Root"
                return info
        return None

    def readDataEntry(self, f):
        blocks = []
        info = self.readTagBlokInfo(f=f)
        pos_on_init = f.tell()
        ns_child = -1
        if info is None:
            info['debug'] = 1

        self.type = info["type"]

        if self.type == "NoDataStartBlock":
            return blocks
        if self.type == "RawBlock":
            return blocks

        ns_child = info['n_childs']
        if ns_child < 0:
            debug = ns_child
            if info['n_p_chls'] > -1:
                ns_child = info['n_p_chls']
                debug = info['n_p_chls']  # Is HandleResource
            else:
                debug = info['n_p_chls']  # Error o Desconocido
        if ns_child < 0:
            debug = 'Error pq despues del ajsute dio negativo'
        else:
            if ns_child == 0:
                if self.data_reference is not None:
                    debug = 'Posible error, pq tonces no seria un hijo'
                    if self.type =='ResourceHandle':
                        f.seek(self.data_reference.offset_plus)
                        blocks.append(f.read(self.data_reference.size))
                        f.seek(pos_on_init)
                        return blocks
                    else:
                        debug = 'Posible error, pq tonces no seria un ResourceHandle'
                return blocks
            else:
                if self.data_reference is None:
                    if self.parent is not None:
                        debug = 'Otro Error pq los datareference None es cuando no tiene Hijos'
                else:
                    count = divmod(self.data_reference.size, ns_child)

                    if count[1] != 0:
                        debug = ' Deberia ser 0 siempre el resto'
                    else:
                        if self.data_reference.size != 0:
                            if self.data_reference.size_fill != 0:
                                f.seek(pos_on_init)
                                return blocks
                            if self.data_reference.offset_type != 1:
                                f.seek(pos_on_init)
                                return blocks
                        f.seek(self.data_reference.offset_plus)
                        sub_block_size = count[0]
                        for k in range(ns_child):
                            blocks.append(f.read(sub_block_size))
                        f.seek(pos_on_init)
                        return blocks
        return blocks

    def readAllIn(self, f, header=None)->{}:
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


class ContentTable:
    def __init__(self) -> None:
        self.entries: [ContentTableEntry] = []
        pass

    def readTable(self, f, header, data_table):
        f.seek(header.content_table_offset)
        for x in range(header.content_table_count):
            # offset = header.content_table_offset + x * 0x20
            entry = ContentTableEntry()
            entry.readIn(f, header)

            if header.data_table_count > entry.ref_index > -1:
                entry.data_reference = data_table.entries[entry.ref_index]

            if header.data_table_count > entry.parent_index > -1:
                entry.data_parent = data_table.entries[entry.parent_index]

                p_i = self.getContentEntryByRefIndex(entry.parent_index)
                if p_i is not None:
                    entry.parent_entry_index = p_i
                    entry.parent = self.entries[p_i]
                    self.entries[p_i].childs.append(entry)

            entry.entry_index = self.entries.__len__()
            entry.bin_datas = entry.readDataEntry(f)
            for data in  entry.bin_datas:
                entry.bin_datas_hex.append(data.hex())
            self.entries.append(entry)

    def getContentEntryByRefIndex(self, ref_index):
        count = 0
        entry_found = None
        for i, entry in enumerate(self.entries):
            if entry.ref_index == ref_index:
                count = count + 1
                entry_found = i
                return entry_found
        if count > 1:
            print(count)
        return entry_found

