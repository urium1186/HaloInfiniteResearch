import struct
from enum import IntFlag

#
# Resumen:
#     Controls the layout of an object when exported to unmanaged code.
from commons.debug_utils import *
from halo_infinite_tag_reader.headers.ver.file_header import FileHeader
from halo_infinite_tag_reader.varnames import getStrInMmr3Hash


class LayoutKind(IntFlag):
    #
    # Resumen:
    #     The members of the object are laid out sequentially, in the order in which they
    #     appear when exported to unmanaged memory. The members are laid out according
    #     to the packing specified in System.Runtime.InteropServices.StructLayoutAttribute.Pack,
    #     and can be noncontiguous.
    Sequential = 0,
    #
    # Resumen:
    #     The precise position of each member of an object in unmanaged memory is explicitly
    #     controlled, subject to the setting of the System.Runtime.InteropServices.StructLayoutAttribute.Pack
    #     field. Each member must use the System.Runtime.InteropServices.FieldOffsetAttribute
    #     to indicate the position of that field within the type.
    Explicit = 2,
    #
    # Resumen:
    #     The runtime automatically chooses an appropriate layout for the members of an
    #     object in unmanaged memory. Objects defined with this enumeration member cannot
    #     be exposed outside of managed code. Attempting to do so generates an exception.
    Auto = 3


class StructLayout:
    def __init__(self, pf, pSize=-1, playout_kind=LayoutKind.Explicit):
        self.Size = pSize
        self.layout_kind = playout_kind
        self.f = pf


class TagDependency(StructLayout):
    def __init__(self, pf):
        super(TagDependency, self).__init__(pf, 24)
        # [FieldOffset(0)]
        # self.GroupTag: int = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.GroupTag: str = struct.unpack('4s', self.f.read(4))[0]
        self.GroupTagReverse: str = self.GroupTag[::-1].decode("utf-8")

        # [FieldOffset(4)]
        # uint
        self.NameOffset: int = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(8)]
        # long
        self.AssetID: int = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(16)]
        self.GlobalID: int = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(20)]
        self.UnknownProperty: int = int.from_bytes(self.f.read(4), 'little', signed=True)
        main_key = self.UnknownProperty

        name_key = self.f.name.split('\\')[-1].split('.')[-1]
        fillDebugDict(main_key, name_key, debug_TagDependency)


class DataBlock(StructLayout):
    def __init__(self, pf):
        super(DataBlock, self).__init__(pf, 16)
        # uint
        self.Size = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(4)]
        # public short
        self.UnknownProperty = int.from_bytes(self.f.read(2), 'little', signed=True)

        # [FieldOffset(6)]
        # public short
        self.Section = int.from_bytes(self.f.read(2), 'little', signed=True)

        # [FieldOffset(8)]
        # public ulong
        self.Offset = int.from_bytes(self.f.read(8), 'little', signed=False)

        main_key = self.UnknownProperty

        name_key = self.f.name.split('\\')[-1].split('.')[-1]
        fillDebugDict(main_key, name_key, debug_DataBlock)


class TagStruct(StructLayout):
    def __init__(self, pf):
        super(TagStruct, self).__init__(pf, 32)
        # [FieldOffset(0)]
        # public long
        self.GUID1 = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(8)]
        # public long
        self.GUID2 = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(16)]
        # publicshort
        self.Type = int.from_bytes(self.f.read(2), 'little', signed=True)

        # [FieldOffset(18)]
        # publicshort
        self.UnknownProperty = int.from_bytes(self.f.read(2), 'little', signed=True)

        # [FieldOffset(20)]
        # publicint
        self.TargetIndex = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(24)]
        # publicint
        self.FieldBlock = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(28)]
        # publicuint
        self.FieldOffset = int.from_bytes(self.f.read(4), 'little', signed=False)

        main_key = self.UnknownProperty
        #name_key = self.f.name.split('\\')[-1].split('.')[-1]
        #name_key = f"{self.TargetIndex}<->{self.Type}"
        name_key = self.Type
        fillDebugDict(main_key, name_key, debug_TagStruct)

        if self.Type == 1 and self.UnknownProperty == 1:
            k = f"{self.TargetIndex}<->{self.UnknownProperty}"
            print(k)
            if True or k == '1<->1':
                print(self.f.name.split('\\')[-1])



class DataReference(StructLayout):
    def __init__(self, pf):
        super(DataReference, self).__init__(pf, 20)

        # [FieldOffset(0)]
        # public int
        self.ParentStructIndex = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(4)]
        # public int
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(8)]
        # public int
        self.TargetIndex = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(12)]
        # public int
        self.FieldBlock = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(16)]
        # public uint
        self.FieldOffset = int.from_bytes(self.f.read(4), 'little', signed=False)

        main_key = self.UnknownProperty
        name_key = self.f.name.split('\\')[-1].split('.')[-1]
        fillDebugDict(main_key, name_key, debug_DataReference)


class TagReferenceFixup(StructLayout):
    def __init__(self, pf):
        super(TagReferenceFixup, self).__init__(pf, 16)

        # [FieldOffset(0)]
        # public int
        self.FieldBlock = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(4)]
        # public uint
        self.FieldOffset = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(8)]
        # public uint
        self.NameOffset = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(12)]
        # public int
        self.DepdencyIndex = int.from_bytes(self.f.read(4), 'little', signed=True)


class StringID(StructLayout):
    def __init__(self, pf):
        super(StringID, self).__init__(pf, 8)
        # [FieldOffset((0)]
        ## public uint
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset((4)]
        ## public uint
        self.StringOffset = int.from_bytes(self.f.read(4), 'little', signed=False)


class ZoneSetInformationHeader(StructLayout):
    def __init__(self, pf):
        super(ZoneSetInformationHeader, self).__init__(pf, 16)
        # [FieldOffset((0)]
        # long
        self.ZoneSetCount = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.ZoneSetCount1 = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset((8)]
        # long
        self.ZoneSetListOffset = int.from_bytes(self.f.read(4), 'little',
                                                signed=True)  # cantidad de Dependencia no repetidas
        self.ZoneSetListOffset1 = int.from_bytes(self.f.read(4), 'little', signed=True)


class ZoneSetInformationHeaderIn(StructLayout):
    def __init__(self, pf):
        super(ZoneSetInformationHeaderIn, self).__init__(pf, 16)
        # [FieldOffset((0)]
        # long
        temp_debug_pos = self.f.tell()
        # self.TadId = struct.unpack('4s', self.f.read(4))[0]
        # self.TadId = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.TadId = self.f.read(4).hex().upper()
        self.TadIdStr = getStrInMmr3Hash(self.TadId)

        self.TadIdCount1 = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset((8)]
        # long
        self.unk0 = int.from_bytes(self.f.read(4), 'little',
                                   signed=True)  # cantidad de Dependencia no repetidas
        self.unk1 = int.from_bytes(self.f.read(4), 'little', signed=True)

        self.ZoneSetTagList_1: [ZoneSetTag] = []
        for i in range(self.TadIdCount1):
            self.ZoneSetTagList_1.append(ZoneSetTag(self.f))

        self.ZoneSetTagList_ID: [ZoneSetTag] = []
        # if self.unk0 != 0:
        #    print(self.unk0)
        for i in range(self.unk0):
            self.ZoneSetTagList_ID.append(int.from_bytes(self.f.read(4), 'little', signed=True))

        self.ZoneSetTagList_2: [ZoneSetTag] = []
        # if self.unk1 != 0:
        #    print(self.unk1)
        for i in range(self.unk1):
            self.ZoneSetTagList_2.append(ZoneSetTag(self.f))

    # [StructLayout(LayoutKind.Explicit, Size = 40)]


class ZoneSetEntry(StructLayout):
    def __init__(self, pf):
        super(ZoneSetEntry, self).__init__(pf, 40)
        # [FieldOffset(0)]
        # public int
        self.StringID = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(4)]
        # public int
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(8)]
        # public long
        self.UnknownProperty2 = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(16)]
        # public long
        self.UnknownProperty3 = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(24)]
        # public long
        self.TagCount = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(32)]
        # public ulong
        self.TagListOffset = int.from_bytes(self.f.read(8), 'little', signed=False)


class ZoneSetTag(StructLayout):
    def __init__(self, pf):
        super(ZoneSetTag, self).__init__(pf, 8)
        # [FieldOffset(0)]
        # public uint
        # self.GlobalID = int.from_bytes(self.f.read(4), 'little', signed=False)
        self.StringIndex = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(4)]
        # public int
        # self.StringID = int.from_bytes(self.f.read(4), 'little', signed=True)
        try:
            # self.StringID = struct.unpack('4s', self.f.read(4))[0]
            # self.StringID = int.from_bytes(self.f.read(4), 'little', signed=True)
            self.StringID = self.f.read(4).hex().upper()
        except:
            debug = 1


class TagBlock(StructLayout):
    def __init__(self, pf):
        super(TagBlock, self).__init__(pf, 28)
        # [FieldOffset(0)]
        # public ulong
        self.Elements = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(8)]
        # public ulong
        self.TypeInfo = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(16)]
        # public int
        self.Count = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(20)]
        # public int
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(24)]
        # public int
        self.UnknownProperty2 = int.from_bytes(self.f.read(4), 'little', signed=True)


class TagReference(StructLayout):
    def __init__(self, pf):
        super(TagReference, self).__init__(pf, 28)
        # [FieldOffset(0)]
        # public ulong
        self.TypeInfo = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(8)]
        # public int
        self.GlobalID = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(12)]
        # public long
        self.AssetID = int.from_bytes(self.f.read(8), 'little', signed=True)

        # [FieldOffset(20)]
        # public int
        # self.GroupTag = int.from_bytes(self.f.read(4), 'little', signed=True)
        self.GroupTag: str = struct.unpack('4s', self.f.read(4))[0]
        self.GroupTagReverse: str = self.GroupTag[::-1].decode("utf-8")

        # [FieldOffset(24)]
        # public int
        self.LocalHandle = int.from_bytes(self.f.read(4), 'little', signed=True)

        # public override string ToString()
        #   return GlobalID + " " + Utilities.GetClassID(GroupTag)


class DataReferenceField(StructLayout):
    def __init__(self, pf):
        super(DataReferenceField, self).__init__(pf, 24)
        # [FieldOffset(0)]
        # public ulong
        self.Data = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(8)]
        # public ulong
        self.TypeInfo = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(16)]
        # public int
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=True)

        # [FieldOffset(20)]
        # public uint
        self.Size = int.from_bytes(self.f.read(4), 'little', signed=False)

        # public override string ToString()
        #   return "Data Size:" + Size


class PageableResource(StructLayout):
    def __init__(self, pf):
        super(PageableResource, self).__init__(pf, 16)
        # [FieldOffset(0)]
        # public ulong
        self.TypeInfo = int.from_bytes(self.f.read(8), 'little', signed=False)

        # [FieldOffset(8)]
        # public uint
        self.Handle = int.from_bytes(self.f.read(4), 'little', signed=False)

        # [FieldOffset(12)]
        # public int
        self.UnknownProperty = int.from_bytes(self.f.read(4), 'little', signed=True)


class RealBounds(StructLayout):
    def __init__(self, pf):
        super(RealBounds, self).__init__(pf, 8)
        # [FieldOffset(0)]
        # public float
        self.MinBound = round(struct.unpack('f', self.f.read(4))[0], 4)

        # [FieldOffset(4)]
        # public float
        self.MaxBound = round(struct.unpack('f', self.f.read(4))[0], 4)

        # public override string ToString()
        #   return MinBound + " " + MaxBound


class RealVector3D(StructLayout):
    def __init__(self, pf):
        super(RealVector3D, self).__init__(pf, 12)
        # [FieldOffset(0)]
        # public float
        self.I = round(struct.unpack('f', self.f.read(4))[0], 4)

        # [FieldOffset(4)]
        # public float
        self.J = round(struct.unpack('f', self.f.read(4))[0], 4)

        # [FieldOffset(8)]
        # public float
        self.K = round(struct.unpack('f', self.f.read(4))[0], 4)

        # public override string ToString()

        # return I + " " + J + " " + K


class Tag:
    def __init__(self, pf):
        self.header = FileHeader(pf)
        self.TagDependencyList: [TagDependency] = []
        self.DataBlockList: [DataBlock] = []
        self.TagStructList: [TagStruct] = []
        self.DataReferenceList: [DataReference] = []
        self.TagReferenceFixupList: [TagReferenceFixup] = []
        self.StringIDList: [StringID] = []  # Not a thing in Infinite?
        self.StringTable: bytes = None
        self.ZoneSetInfoHeader: ZoneSetInformationHeader = None
        self.ZoneSetEntryList: [ZoneSetEntry] = []
        self.ZoneSetTagList: [ZoneSetTag] = []
        self.ZoneSetData = bytes
        self.ZoneSetDataStr = ''
        self.TagData: bytes = None
        self.ResourceData: bytes = None
        self._initRead()

    def _initRead(self):
        for i in range(self.header.DependencyCount):
            self.TagDependencyList.append(TagDependency(self.header.f))

        for i in range(self.header.DataBlockCount):
            self.DataBlockList.append(DataBlock(self.header.f))

        for i in range(self.header.TagStructCount):
            self.TagStructList.append(TagStruct(self.header.f))

        for i in range(self.header.DataReferenceCount):
            self.DataReferenceList.append(DataReference(self.header.f))

        for i in range(self.header.TagReferenceCount):
            self.TagReferenceFixupList.append(TagReferenceFixup(self.header.f))

        self.StringTable = self.header.f.read(self.header.StringTableSize)
        temp_pos = self.header.f.tell()
        self.ZoneSetInfoHeader = ZoneSetInformationHeader(self.header.f)
        temp_list = []
        # try:
        for i in range(self.ZoneSetInfoHeader.ZoneSetCount1):
            temp_list.append(ZoneSetInformationHeaderIn(self.header.f))
        temp_pos_1 = self.header.f.tell()
        self.ZoneSetData = self.header.f.read(temp_pos + self.header.ZoneSetSize - temp_pos_1)
        if len(self.ZoneSetData) != 0:
            debug = True
        div_mod = divmod(len(self.ZoneSetData), 8)
        if div_mod[1] != 0 and self.ZoneSetData != b'\x00\x00\x00\x00':
            debug = 1
        else:
            if div_mod[0] != 0:
                print(divmod(len(self.ZoneSetData), 8)[0])
                print(
                    f"{self.ZoneSetInfoHeader.ZoneSetCount}-{self.ZoneSetInfoHeader.ZoneSetCount1}-" \
                    f"{self.ZoneSetInfoHeader.ZoneSetListOffset}-{self.ZoneSetInfoHeader.ZoneSetListOffset1}" \
                    f" | ZL: {self.header.ZoneSetSize - 16} DC: {self.header.DependencyCount} TRC: {self.header.TagReferenceCount}" \
                    f"--- NRxDC: {self.ZoneSetInfoHeader.ZoneSetListOffset >= self.header.DependencyCount}" \
                    f"--- NRxTRC: {self.ZoneSetInfoHeader.ZoneSetListOffset <= self.header.TagReferenceCount}" \
                    f"--- NRx0: {self.ZoneSetInfoHeader.ZoneSetListOffset == 0} : " \
                    f"{self.ZoneSetInfoHeader.ZoneSetListOffset == self.header.TagReferenceCount == self.header.DependencyCount == 0}"
                )
                print(self.header.f)

        self.ZoneSetDataStr = self.ZoneSetData.hex()

        self.TagData = self.header.f.read(self.header.DataSize)
        """
        except:
            print(
                f"{self.ZoneSetInfoHeader.ZoneSetCount}-{self.ZoneSetInfoHeader.ZoneSetCount1}-" \
                f"{self.ZoneSetInfoHeader.ZoneSetListOffset}-{self.ZoneSetInfoHeader.ZoneSetListOffset1}" \
                f" | ZL: {self.header.StringIDCount - 16} DC: {self.header.DependencyCount} TRC: {self.header.TagReferenceCount}" \
                f"--- NRxDC: {self.ZoneSetInfoHeader.ZoneSetListOffset >= self.header.DependencyCount}" \
                f"--- NRxTRC: {self.ZoneSetInfoHeader.ZoneSetListOffset <= self.header.TagReferenceCount}" \
                f"--- NRx0: {self.ZoneSetInfoHeader.ZoneSetListOffset == 0} : " \
                f"{self.ZoneSetInfoHeader.ZoneSetListOffset == self.header.TagReferenceCount == self.header.DependencyCount == 0}"
            )
            print(self.header.f)
            debug = 1
        
        """
