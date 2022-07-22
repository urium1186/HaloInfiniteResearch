from commons.enums_struct_def import TagStructType
from halo_infinite_tag_reader.common_tag_types import *
from halo_infinite_tag_reader.headers.tagbasereader import TagBaseReader
from halo_infinite_tag_reader.headers.ver.tag import Tag
from halo_infinite_tag_reader.tag_reader_utils import analizarCabecera
from halo_infinite_tag_reader.tag_struct import TagStruct

from halo_infinite_tag_reader.taglayouts import TagLayouts


class Event(object):

    def __init__(self):
        self.__eventhandlers = []

    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)


class TagParseControl:

    def __init__(self, filename: str, tagLayoutTemplate: str):
        self.tag = None
        self.tagLayout = None
        self.f: BinaryIO = None
        self.rootTagInst: TagInstance = None
        self.filename = filename
        self.tagLayoutTemplate = tagLayoutTemplate
        self.full_header = TagBaseReader()
        self.content_data_index = 0
        self.OnInstanceLoad = Event()

    def readFile(self):
        with open(self.filename, 'rb') as self.f:
            self.full_header.readIn(self.f)
            analizarCabecera(self.full_header)

            self.tagLayout = TagLayouts.Tags(self.tagLayoutTemplate)
            root_tag = TagLayouts.C('TagStructBlock', 'Root', self.tagLayout, p_P={"g": "true"})
            self.rootTagInst = TagInstance(tag=root_tag, addressStart=self.full_header.tag_struct_table.entries
            [0].data_reference.offset_plus, offset=0)
            self.rootTagInst.content_entry = self.full_header.tag_struct_table.entries[0]
            self.readTagsAndCreateInstances(self.rootTagInst)
            self.f.close()
            # print("debug")

    def hasTagBlock(self, tagDefinitions) -> bool:
        for entry in tagDefinitions:
            if tagDefinitions[entry].T == "Tagblock":
                return True
        return False

    def readTagDefinition(self, parent, parcial_address=0, f=None):
        tagInstanceTemp = {}
        tagBlocks = []
        tagDefinitions = parent.tagDef.B
        if f is None:
            f = self.f
        f.seek(parcial_address)
        for entry in tagDefinitions:
            # print(tagDefinitions[entry].T)
            # key = parent_property_name + "_" + tagDefinitions[entry].N + "_" + str(i)
            key = tagDefinitions[entry].N
            if tagInstanceTemp.keys().__contains__(key):
                key = key + '_'
            if key == 'index buffer index':
                debug = 0
            tagInstanceTemp[key] = tagInstanceFactoryCreate(tag=tagDefinitions[entry], addressStart=parcial_address,
                                                            offset=entry)
            tagInstanceTemp[key].readIn(f, self.full_header)
            if tagDefinitions[entry].T == "TagStructData":
                if tagInstanceTemp[key].__class__ == TagStructData:
                    tagInstanceTemp[key].__class__ = TagStructData
                    if tagInstanceTemp[key].generateEntry:
                        tagBlocks.append(tagInstanceTemp[key])

            elif tagDefinitions[entry].T == "Tagblock":
                tagBlocks.append(tagInstanceTemp[key])
            elif tagDefinitions[entry].T == "ResourceHandle":
                tagBlocks.append(tagInstanceTemp[key])
            else:
                tagInstanceTemp[key].parent = parent
                self.OnInstanceLoad(tagInstanceTemp[key])
        return {"parent": tagInstanceTemp, "child_array": tagBlocks}

    def readTagsAndCreateInstances(self, instance_parent: TagInstance):
        tagBlocks = []
        instance_parent.content_entry.field_name = instance_parent.tagDef.N
        if instance_parent.tagDef.T == 'TagStructData':
            typue_d = instance_parent.content_entry.type_id
            name_1 = instance_parent.content_entry.field_name
            bool_some = instance_parent.content_entry.unknown_property_bool_0_1
            debug = True

        if instance_parent.content_entry.unknown_property_bool_0_1 != 0:
            typue_d = instance_parent.content_entry.type_id
            name_1 = instance_parent.content_entry.field_name
            debug = True

        if instance_parent.content_entry.type_id == 4:
            name_1 = instance_parent.content_entry.field_name
            bool_some = instance_parent.content_entry.unknown_property_bool_0_1
            debug= True
        if instance_parent.content_entry.data_reference is None:
            #print("Error")
            self.OnInstanceLoad(instance_parent)
            return
        if instance_parent.content_entry.data_reference.unknown_property != 0:
            debug = True

        n_items = -1
        read_result = {"parent": {}, "child_array": []}
        for data in instance_parent.content_entry.bin_datas:
            bin_stream = io.BytesIO(data)
            read_result = self.readTagDefinition(instance_parent, f=bin_stream)
            instance_parent.childs.append(read_result['parent'])
            tagBlocks = tagBlocks + read_result['child_array']
            n_items = read_result['child_array'].__len__()
            #print("debug")

        if instance_parent.content_entry.type_id == TagStructType.ResourceHandle and read_result['parent'] == {}:
            self.OnInstanceLoad(instance_parent)
            return

        if n_items == -1:
            if instance_parent.content_entry.childs.__len__() != 0:
                debug = 1
        elif n_items == 0:
            if instance_parent.content_entry.childs.__len__() != 0:
                debug = 'error'
        else:
            if instance_parent.content_entry.childs.__len__() != 0:
                count = divmod(instance_parent.content_entry.childs.__len__(), n_items)
                if instance_parent.content_entry.type_id != TagStructType.ExternalFileDescriptor:
                    if count[1] != 0:
                        debug = "pposible error"
                    if count[0] != instance_parent.content_entry.bin_datas.__len__():
                        debug = "pposible error"
                else:
                    debug = True

        for i, entry in enumerate(instance_parent.content_entry.childs):
            tag_child_inst = tagBlocks[i]

            tag_child_inst.content_entry = entry
            tag_child_inst.parent = instance_parent
            self.readTagsAndCreateInstances(tag_child_inst)
        """
        if instance_parent.content_entry.hash.guid == '{FE51FDAC-4778-FF62-5430-3A86CA923A0}':
            print(' Scale data Block ')
        if instance_parent.content_entry.hash.guid == '{4A81849D-42B4-EEFB-AC56-9A3180F53E6}':
            print(' Mesh data Block ')
        if instance_parent.content_entry.hash.guid == '{67FAC497-4E7D-3D88-A2F7-4B7F893FF8D}':
            print(' Mesh meta data block ')
        if instance_parent.content_entry.hash.guid == '{10DD7329-4880-7FE0-9AB7-BBCEE273225}':
            print(' entry for the parts ')
        #print(self.__class__)
        """
        self.OnInstanceLoad(instance_parent)

    def readTagsAndCreateInstances_1(self, instance_parent: TagInstance, loopCount=1):
        tagInstanceArrayTemp: [{}] = []
        tagBlocks = []
        key = ''
        if instance_parent.content_entry.data_reference is None:
            self.OnInstanceLoad(instance_parent)
            #print("Error")
            return
        address = instance_parent.content_entry.data_reference.offset_plus
        for i in range(loopCount):
            parcial_address = address + (i * instance_parent.tagDef.S)
            result = self.readTagDefinition(instance_parent.tagDef.B, parcial_address)
            instance_parent.childs.append(result['parent'])
            tagBlocks = tagBlocks + result['child_array']
        paren_p_name = instance_parent.tagDef.N

        if tagBlocks.__len__() != instance_parent.content_entry.childs.__len__():
            debug = 'error'
        parentcontent_info_1 = instance_parent.content_entry.readTagBlokInfo(self.f)
        parentcontent_info_2 = instance_parent.content_entry.readTagBlokInfo(self.f)
        for i, entry in enumerate(instance_parent.content_entry.childs):
            content_info = entry.readTagBlokInfo(self.f)
            if i >= tagBlocks.__len__():
                debug = 0
                continue
            tag_child_inst = tagBlocks[i]
            child_name = tag_child_inst.tagDef.N

            if child_name == 'render geometry':
                debug = 1
            entry_size = 0 if entry.target_index == -1 else entry.data_reference.size
            if tag_child_inst.tagDef.T == 'ResourceHandle':
                tag_child_inst.tagDef.S = entry_size
                continue
            tag_block_size = tag_child_inst.childrenCount * tag_child_inst.tagDef.S
            if tag_block_size != entry_size:
                debug = 'error'
                continue
            else:
                tag_child_inst.content_entry = entry
                tag_child_inst.parent = instance_parent
                if entry_size != 0:
                    if entry.data_reference.unknown_property_bool_0_1 != 0:
                        continue
                    if entry.data_reference.section != 1:
                        continue
                    self.readTagsAndCreateInstances(tag_child_inst, tag_child_inst.childrenCount)
                print('algo')

            debug = 'error'
        debug = 0

    def readTagsAndCreateControls(self, tagStruct: TagStruct = None, startingTagOffset: int = -1,
                                  tagDefinitions: {} = {}, address: int = -1,
                                  parent_property_name="", loopCount=1, parent=None,
                                  absolute_address_chain: str = ""):
        tagInstanceArrayTemp: [{}] = []
        tagBlocks = []
        key = ''
        if parent is None:
            # tagDefinitions.content_data = self.full_header.content_table.entries[0]
            self.content_data_index = self.content_data_index + 1
        parcial_address = address
        p_p_name = parent_property_name
        for i in range(loopCount):
            prevEntry = 0
            tagInstanceTemp = {}
            if not parent is None:
                parcial_address = address + (i * parent.tagDef.S)

            result = self.readTagDefinition(tagDefinitions, parcial_address)
            tagInstanceArrayTemp.append(result['parent'])
            tagBlocks = tagBlocks + result['child_array']

        if parent is None:
            self.TagInstance = tagInstanceArrayTemp
        else:
            parent.TagInstance = tagInstanceArrayTemp
            self.f.seek(address + parent.tagDef.S * loopCount)
        p_p_name = parent_property_name
        for t_i, tag_inst in enumerate(tagBlocks):
            debug_parameter_name = tag_inst.tagDef.N
            if debug_parameter_name == 'render geometry':
                debug = 0
            if tag_inst.tagDef.T == 'Comment':
                bo = self.hasTagBlock(tag_inst.tagDef.B)
            n_childs = tag_inst.childrenCount
            t_size = tag_inst.tagDef.S
            tag_inst.tagDef.content_data = self.full_header.tag_struct_table.entries[self.content_data_index]
            tag_inst.content_entry = tag_inst.tagDef.content_data
            full_size = t_size * n_childs
            error = False
            sum = True
            debug_before = self.full_header.tag_struct_table.entries[self.content_data_index - 1]
            actual = self.full_header.tag_struct_table.entries[self.content_data_index]
            debug_next = self.full_header.tag_struct_table.entries[self.content_data_index + 1]
            if full_size == 0 and not (tag_inst.tagDef.content_data.data_reference is None):
                error = True
            if tag_inst.tagDef.content_data.data_reference is None:
                error = (full_size != 0)
                if error:
                    debug = 0
            elif full_size != tag_inst.tagDef.content_data.data_reference.size:

                error = True
                if tag_inst.tagDef.T == 'Comment':
                    if tag_inst.tagDef.N == 'mesh package':
                        sum = False

            if sum:
                self.content_data_index = self.content_data_index + 1
            else:
                if tag_inst.tagDef.T == 'ResourceHandle':
                    self.content_data_index = self.content_data_index + 1

            if n_childs <= 0:
                continue
            iterate_address = self.f.tell()
            if tag_inst.tagDef.content_data.data_reference.size_fill != 0:
                debug = 0
            if tag_inst.tagDef.content_data.data_reference.offset_type == 2:
                continue
            else:
                iterate_address = tag_inst.tagDef.content_data.data_reference.offset_plus

                # debug_address = address + tag_inst.tagDef.content_data.data_reference.offset
            # print(f"cantidad de elementos {n_childs}, tamano unitario {t_size}, tamano bloque {n_childs * t_size}")
            self.readTagsAndCreateControls(tagDefinitions=tag_inst.tagDef.B, address=iterate_address,
                                           parent_property_name=tag_inst.tagDef.N, loopCount=n_childs, parent=tag_inst)

    def AddSubscribersForOnInstanceLoad(self, objMethod):
        self.OnInstanceLoad += objMethod

    def RemoveSubscribersOnInstanceLoad(self, objMethod):
        self.OnInstanceLoad -= objMethod
