class StringID:
    def __init__(self):
        # public uint
        self.unknown_property = -1

        # [FieldOffset((4)]
        # public uint
        self.string_offset = -1


class StringIDTable:
    def __init__(self):
        self.entries = []

    def readTable(self, f, header):
        f.seek(header.dependency_count_offset)
        for x in range(header.dependency_count):
            entry = StringID()
            entry.unknown_property = int.from_bytes(self.f.read(4), 'little', signed=False)
            entry.string_offset = int.from_bytes(self.f.read(4), 'little', signed=False)
            self.entries.append(entry)