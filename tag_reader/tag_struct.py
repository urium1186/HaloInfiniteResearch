from enum import IntFlag

from tag_reader.tag_layouts import TagLayouts


class TagStruct:

    def __init__(self):
        self.Datnum = ''
        self.ObjectId = ''
        self.TagGroup = ''
        self.TagData = 0
        self.TagTypeDesc = ''
        self.TagFullName = ''
        self.TagFile = ''
        self.unloaded = False


class GroupTagStruct:

    def __init__(self):
        self.TagGroupDesc = ''
        self.TagGroupName = ''
        self.TagGroupDefinitition = ''
        self.TagExtraType = ''
        self.TagExtraName = ''
        self.TagCategory = None  # public TreeViewItem TagCategory;


class TagEditorDefType(IntFlag):
    TagEditorDefinition = 0
    TED_TagRefGroup = 1


class TagEditorDefinition:

    def __init__(self):
        self.TEDType = TagEditorDefType.TagEditorDefinition
        self.MemoryType = ''
        self.OffsetOverride = ''
        self.TagDef: TagLayouts.C = None
        self.TagStruct: TagStruct = None
        self.DatNum = ''
        self.TagId = ''

    def GetTagOffset(self):
        if self.OffsetOverride is not None:
            return self.OffsetOverride
        return self.TagDef.AbsoluteTagOffset

    def __int__(self, ted):
        self.MemoryType = ted.MemoryType
        self.OffsetOverride = ted.OffsetOverride
        self.TagDef = ted.TagDef
        self.TagStruct = ted.TagStruct
        self.DatNum = ted.DatNum
        self.TagId = ted.TagId

class TED_TagRefGroup(TagEditorDefinition):
    def __init__(self):
        self.TagGroup = ''
        super()
        self.TEDType = TagEditorDefType.TED_TagRefGroup

    
