import struct


class ZoneSetTag:
    def __init__(self, pf):
        self.f = pf
        self.StringIndex = int.from_bytes(self.f.read(4), 'little', signed=False)

        try:
            self.StringID = self.f.read(4).hex().upper()  # int.from_bytes(self.f.read(4), 'little', signed=False)
            # self.StringID = struct.unpack('4s', self.f.read(4))[0]
        except:
            debug = 1


class ZoneSetInformationHeaderIn:
    def __init__(self, pf):
        self.f = pf
        # self.tag_id = struct.unpack('4s', self.f.read(4))[0]
        # self.tag_id = int.from_bytes(self.f.read(4), 'little', signed=False)
        self.tag_id = self.f.read(4).hex().upper()
        self.tag_id_count_1 = int.from_bytes(self.f.read(4), 'little', signed=True)

        self.tag_id_count_2 = int.from_bytes(self.f.read(4), 'little',
                                             signed=True)  # cantidad de Dependencia no repetidas
        self.tag_id_count_3 = int.from_bytes(self.f.read(4), 'little', signed=True)

        self.zone_set_tag_list_1: [ZoneSetTag] = []
        for i in range(self.tag_id_count_1):
            self.zone_set_tag_list_1.append(ZoneSetTag(self.f))

        self.zone_set_tag_list_2: [ZoneSetTag] = []

        for i in range(self.tag_id_count_2):
            self.zone_set_tag_list_2.append(int.from_bytes(self.f.read(4), 'little', signed=True))

        self.zone_set_tag_list_3: [ZoneSetTag] = []

        for i in range(self.tag_id_count_3):
            self.zone_set_tag_list_3.append(ZoneSetTag(self.f))


class ZoneSetInformationHeader:
    def __init__(self, pf):
        self.f = pf
        # [FieldOffset((0)]
        # long
        self.zone_set_count = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.zone_set_count_1 = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset((8)]
        # long
        self.zone_set_list_offset = int.from_bytes(self.f.read(4), 'little',
                                                   signed=True)  # cantidad de Dependencia no repetidas
        self.zone_set_list_offset_1 = int.from_bytes(self.f.read(4), 'little', signed=True)


class ZoneSet:
    def __init__(self, pf):
        self.f = pf
        self.zone_set_info_header = ZoneSetInformationHeader(self.f)
        self.zone_set_infos = []
        for i in range(self.zone_set_info_header.zone_set_count_1):
            self.zone_set_infos.append(ZoneSetInformationHeaderIn(self.f))
