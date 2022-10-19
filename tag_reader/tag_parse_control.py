import os
import pathlib
from builtins import range

from commons.enums_struct_def import TagStructType
from configs.config import Config
from tag_reader.common_tag_types import *
from tag_reader.headers.tag_base_reader import TagBaseReader
from tag_reader.tag_reader_utils import analizarCabecera
from tag_reader.tag_struct import TagStruct
from tag_reader.tag_instance import TagInstance
from tag_reader.tag_layouts import TagLayouts
from commons.classes import Event

class TagParseControl:

    def __init__(self, filename: str, tagLayoutTemplate: str = '', p_tagLayout=None):
        if tagLayoutTemplate == '':
            if p_tagLayout is None:
                raise Exception('Debe tener o una ext o tagLayout')
        if p_tagLayout is None:
            if tagLayoutTemplate == '':
                raise Exception('Debe tener o una ext o tagLayout')
        self.tag = None
        self.tagLayout = p_tagLayout
        self.f: BinaryIO = None
        self.rootTagInst: TagInstance = None
        self.filename = filename
        self.tagLayoutTemplate = tagLayoutTemplate
        self.full_header = TagBaseReader()
        self.content_data_index = 0
        self.OnInstanceLoad = Event()
        self.hasFunction = 0
        self.byte_stream = None

    def reset(self):
        self.tag = None
        self.f: BinaryIO = None
        self.rootTagInst: TagInstance = None
        self.full_header = TagBaseReader()
        self.content_data_index = 0
        self.OnInstanceLoad = Event()
        self.hasFunction = 0

    def readFile(self):
        try:
            with open(self.filename, 'rb') as self.f:
                if Config.VERBOSE:
                    Log.Print(f"Reading {self.filename} ")
                self.full_header.readIn(self.f)
                analizarCabecera(self.full_header)
                if self.tagLayout is None:
                    self.tagLayout = TagLayouts.Tags(self.tagLayoutTemplate)
                root_tag = TagLayouts.C('TagStructBlock', 'Root', self.tagLayout, p_P={"g": "true"})
                self.rootTagInst = TagInstance(tag=root_tag, addressStart=self.full_header.tag_struct_table.entries
                [0].field_data_block.offset_plus, offset=0)
                self.rootTagInst.content_entry = self.full_header.tag_struct_table.entries[0]
                self.readTagsAndCreateInstances(self.rootTagInst)
                self.f.close()
                if Config.VERBOSE:
                    Log.Print(f"Read end in {self.filename} ")
                if self.hasFunction == 0:
                    assert self.full_header.file_header.data_reference_count == 0
                else:
                    assert self.hasFunction <= self.full_header.file_header.data_reference_count
                    assert self.hasFunction == self.full_header.file_header.data_reference_count
        except FileNotFoundError as e:
            if Config.VERBOSE:
                Log.Print(f"Can not read file {self.filename} not found. Exception {e.__class__} {e.args}")

    def hasTagBlock(self, tagDefinitions) -> bool:
        for entry in tagDefinitions:
            if tagDefinitions[entry].T == "Tagblock":
                return True
        return False

    def readTagDefinitionByNamePathSelfAddress(self, name_path, is_only_name=True):
        try:
            if self.byte_stream is not None:
                self.f = self.byte_stream
            else:
                self.f = open(self.filename, 'rb')

            if Config.VERBOSE:
                Log.Print(f"Reading {self.filename} name path {name_path} ")
            self.full_header.readInOnlyHeader(self.f)
            if self.tagLayout is None:
                self.tagLayout = TagLayouts.Tags(self.tagLayoutTemplate)
            root_tag = TagLayouts.C('TagStructBlock', 'Root', self.tagLayout, p_P={"g": "true"})
            self.rootTagInst = TagInstance(tag=root_tag, addressStart=self.full_header.file_header.section_1_offset,
                                           offset=0)
            t_i = self.readTagsAndCreateInstancesBySelfAddress(self.rootTagInst, name_path, is_only_name)
            self.f.close()
            return t_i



        except FileNotFoundError as e:
            if Config.VERBOSE:
                Log.Print(f"Can not read file {self.filename} not found. Exception {e.__class__} {e.args}")

    def readTagDefinitionSelfAddress(self, parent, parcial_address=0, f=None, ref_it={'i': 0, 'f': 0, 'r': 0}):
        tagInstanceTemp = {}
        tagBlocks = []
        tagDefinitions = parent.tagDef.B
        if f is None:
            f = self.f
        f.seek(parcial_address)
        for entry in tagDefinitions:
            key = tagDefinitions[entry].N
            if tagInstanceTemp.keys().__contains__(key):
                key = key + '_'
            tagInstanceTemp[key] = tagInstanceFactoryCreate(tag=tagDefinitions[entry], addressStart=parcial_address,
                                                            offset=entry)
            tagInstanceTemp[key].parent = parent
            tagInstanceTemp[key].readIn(f)

    def readTagDefinitionBySelfAddress(self, parent, parcial_address=0, f=None, name_path = '',ref_it={'i': 0, 'f': 0, 'r': 0}):
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

            tagInstanceTemp[key] = tagInstanceFactoryCreate(tag=tagDefinitions[entry], addressStart=parent.addressStart,
                                                            offset=entry)

            tagInstanceTemp[key].parent = parent
            tagInstanceTemp[key].readIn(f, self.full_header)
            if name_path == tagDefinitions[entry].N:
                return tagInstanceTemp[key]
        return None

    def readTagDefinition(self, parent, parcial_address=0, f=None, ref_it={'i': 0, 'f': 0, 'r': 0}):
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

            tagInstanceTemp[key] = tagInstanceFactoryCreate(tag=tagDefinitions[entry], addressStart=parcial_address,
                                                            offset=entry)

            tagInstanceTemp[key].parent = parent
            tagInstanceTemp[key].readIn(f, self.full_header)
            if tagDefinitions[entry].T == 'FUNCTION':
                tagInstanceTemp[key].data_reference = parent.content_entry.l_function[ref_it['f']]
                if tagInstanceTemp[key].data_reference.unknown_property != 0:
                    debug = 0

                assert self.full_header.file_header.data_reference_count != 0
                assert len(parent.content_entry.l_function[ref_it['f']].bin_data) == tagInstanceTemp[
                    key].byteLengthCount

                self.hasFunction += 1
                ref_it['f'] += 1
                self.OnInstanceLoad(tagInstanceTemp[key])
            elif tagDefinitions[entry].T == 'TagRef':
                tagInstanceTemp[key].tag_ref = parent.content_entry.l_tag_ref[ref_it['r']]
                tagInstanceTemp[key].loadPath()
                ref_it['r'] += 1
                self.OnInstanceLoad(tagInstanceTemp[key])
            elif tagDefinitions[entry].T == "TagStructData":
                if tagInstanceTemp[key].__class__ == TagStructData:
                    tagInstanceTemp[key].__class__ = TagStructData
                    if len(parent.content_entry.childs) > ref_it['i']:
                        temp_entry = parent.content_entry.childs[ref_it['i']]
                        assert not (temp_entry.type_id_tg == TagStructType.NoDataStartBlock and len(
                            temp_entry.bin_datas) != 0), \
                            f'Error in {self.filename}'

                        if parent.content_entry.childs[ref_it['i']].type_id_tg == TagStructType.NoDataStartBlock:
                            tagBlocks.append(tagInstanceTemp[key])
                            ref_it['i'] += 1
                        else:
                            self.OnInstanceLoad(tagInstanceTemp[key])
                    """
                    if False and tagInstanceTemp[key].generateEntry:
                        #tagInstanceTemp[key].childrenCount = 1
                        tagBlocks.append(tagInstanceTemp[key])
                        ref_it['i'] += 1
                    """
            elif tagDefinitions[entry].T == "Tagblock":
                tagBlocks.append(tagInstanceTemp[key])
                ref_it['i'] += 1
            elif tagDefinitions[entry].T == "ResourceHandle":
                tagBlocks.append(tagInstanceTemp[key])
                ref_it['i'] += 1
            else:
                tagInstanceTemp[key].parent = parent
                self.OnInstanceLoad(tagInstanceTemp[key])
        return {"parent": tagInstanceTemp, "child_array": tagBlocks}

    def readTagsAndCreateInstancesBySelfAddress(self, instance_parent: TagInstance, name_path, is_only_name= True):
        temp_name = instance_parent.tagDef.N
        return self.readTagDefinitionBySelfAddress(instance_parent, f=self.f, name_path=name_path)

    def readTagsAndCreateInstances(self, instance_parent: TagInstance):
        tagBlocks = []
        instance_parent.content_entry.field_name = instance_parent.tagDef.N

        if instance_parent.content_entry.field_data_block is None:
            # print("Error")
            self.OnInstanceLoad(instance_parent)
            return

        n_items = -1
        read_result = {"parent": {}, "child_array": []}
        ref_count = {'i': 0,
                     'f': 0,
                     'r': 0,
                     }
        for data in instance_parent.content_entry.bin_datas:
            bin_stream = io.BytesIO(data)
            read_result = self.readTagDefinition(instance_parent, f=bin_stream, ref_it=ref_count)
            instance_parent.childs.append(read_result['parent'])
            tagBlocks = tagBlocks + read_result['child_array']
            n_items = read_result['child_array'].__len__()
            # print("debug")

        assert ref_count['f'] == instance_parent.content_entry.l_function.__len__(), f'{self.filename}'
        assert ref_count['r'] == instance_parent.content_entry.l_tag_ref.__len__(), f'{self.filename}'

        if instance_parent.content_entry.type_id == TagStructType.ResourceHandle and read_result['parent'] == {}:
            self.OnInstanceLoad(instance_parent)
            return

        if n_items == -1:
            if instance_parent.content_entry.childs.__len__() != 0:
                debug = 1
        elif n_items == 0:
            if instance_parent.content_entry.childs.__len__() != 0:
                debug = 'error'
                print(f"Error entry childs mayor q tag lay in {self.filename}, {instance_parent.tagDef.N}")
                self.OnInstanceLoad(instance_parent)
                return
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
            # assert len(entry.bin_datas) == tag_child_inst.childrenCount, 'Deberia tener la misma cantidad de data por hijos a leer'
            if tag_child_inst.__class__ == TagStructData:
                # assert entry.unknown_property_bool_0_1 == 1
                assert entry.type_id_tg == TagStructType.NoDataStartBlock, 'Coinciden en tipo NoDataStartBlock'
                assert len(
                    entry.bin_datas) == 0, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
            elif tag_child_inst.__class__ == ResourceHandle:
                assert entry.type_id_tg == TagStructType.ResourceHandle or entry.type_id_tg == TagStructType.ExternalFileDescriptor, f'Coinciden en tipo ResourceHandle in {self.filename},  {instance_parent.tagDef.N}'
                if entry.type_id_tg == TagStructType.ResourceHandle:
                    path_to_hash = os.path.dirname(self.filename)
                    ext = pathlib.Path(self.filename).suffix
                    exter = False
                    for path in pathlib.Path(path_to_hash).rglob(f'*{ext}[0_*'):
                        exter = True
                        break

                    if exter:
                        assert entry.unknown_property_bool_0_1 == 1, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                    else:
                        if self.full_header.file_header.section_3_size == 0:
                            assert entry.unknown_property_bool_0_1 == 0, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                        else:
                            assert entry.unknown_property_bool_0_1 == 1, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                    if len(entry.bin_datas) == 0:
                        assert instance_parent.childs[0][
                                   'bitmap resource handle'].int_value == -1128481604, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                    else:
                        assert len(
                            entry.bin_datas) == 1, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                if entry.type_id_tg == TagStructType.ExternalFileDescriptor:
                    assert entry.unknown_property_bool_0_1 == 0, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                    assert len(
                        entry.bin_datas) == 0, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                if len(entry.bin_datas) != tag_child_inst.childrenCount:
                    assert entry.type_id_tg == TagStructType.ResourceHandle
                else:
                    assert len(
                        entry.bin_datas) == tag_child_inst.childrenCount, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
            else:
                if not len(entry.bin_datas) == tag_child_inst.childrenCount:
                    debug = True
                assert len(
                    entry.bin_datas) == tag_child_inst.childrenCount, f'Error in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                assert entry.type_id_tg == TagStructType.Tagblock, f'Coinciden en tipo Tagblock in {self.filename},  {instance_parent.tagDef.N}, {tag_child_inst.tagDef.N}'
                if entry.unknown_property_bool_0_1 == 1:
                    debug = True
                    assert self.full_header.file_header.section_2_size != 0 or self.full_header.file_header.section_3_size != 0
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
            # print("Error")
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
                # print('algo')

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
