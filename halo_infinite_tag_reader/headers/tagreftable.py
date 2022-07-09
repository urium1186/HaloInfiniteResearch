import struct


class TagDependency:

    def __init__(self):
        self.tagGroup = ""
        self.name_offset = -1
        self.ref_id_sub = None  # AssetID l = 8
        self.ref_id_center = None
        self.global_id = None
        self.unknown_property = -1
        pass


class TagDependencyTable:

    def __init__(self) -> None:
        self.entries = []
        pass
    """
    char tagGroup[4];
        int string_offset;
        byte ref_id_sub[4];
        byte ref_id_center[4];
        byte ref_id[4];
        int parent;
    """
    def readTable(self, f, header):
        f.seek(header.dependency_count_offset)
        for x in range(header.dependency_count):
            #offset = header.tagref_table_offset + x * 24
            entry = TagDependency()
            entry.tagGroup = struct.unpack('4s', f.read(4))[0]
            entry.name_offset = struct.unpack('i', f.read(4))[0]#int.from_bytes(buffer, 'little')
            entry.ref_id_sub = f.read(4).hex().upper()
            entry.ref_id_center = f.read(4).hex().upper()
            entry.global_id = f.read(4).hex().upper()
            entry.unknown_property = struct.unpack('i', f.read(4))[0]
            if entry.unknown_property !=-1:
                debug = 0
            self.entries.append(entry)
