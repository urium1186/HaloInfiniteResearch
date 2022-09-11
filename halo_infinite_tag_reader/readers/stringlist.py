from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from halo_infinite_tag_reader.tag_instance import TagInstance
from halo_infinite_tag_reader.tag_reader_utils import readStringInPlace
from halo_infinite_tag_reader.tagparsecontrol import TagParseControl



class StringList(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'uslg')
        #self.resource = []
        self.json_str_base = '{"root":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        super(StringList, self).onInstanceLoad(instance)
        variants = {}
        if instance.tagDef.N == "language references":
            valid_lang = [0,3,2,4,5]
            for i, lang in enumerate(instance.childs):
                if not (i in valid_lang):
                    continue
                filename = f'{self.full_filepath}[{i}_string_list_resource]'
                temp = TagParseControl(filename,p_tagLayout=lang['string list resource'].tagDef.B)
                temp.readFile()
                instance_s = temp.rootTagInst.childs[0]['string lookup info']
                init_adress = instance_s.content_entry.field_data_block.offset_plus + instance_s.content_entry.field_data_block.size
                with open(filename, 'rb') as f_temp:
                    for x in instance_s.childs:
                        offset_temp = init_adress + x['offset'].value
                        x['string id'].extra_data = {"str_": readStringInPlace(f_temp, offset_temp, True)}
                lang['string list resource'].childs = temp.rootTagInst.childs
                # self.resource.append(temp)