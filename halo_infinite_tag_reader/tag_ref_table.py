import struct


class TagRegTableEntry:

    def __init__(self):
        self.tagGroup = ""
        self.string_offset = -1
        self.ref_id_sub = None
        self.ref_id_center = None
        self.ref_id = None
        self.parent = -1
        pass


class TagRefTable:

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
        f.seek(header.tagref_table_offset)
        for x in range(header.tagref_table_count):
            #offset = header.tagref_table_offset + x * 24
            entry = TagRegTableEntry()
            entry.tagGroup = struct.unpack('4s', f.read(4))[0]
            entry.string_offset = struct.unpack('i', f.read(4))[0]#int.from_bytes(buffer, 'little')
            entry.ref_id_sub = f.read(4).hex().upper()
            entry.ref_id_center = f.read(4).hex().upper()
            entry.ref_id = f.read(4).hex().upper()
            entry.parent = struct.unpack('i', f.read(4))[0]
            self.entries.append(entry)
