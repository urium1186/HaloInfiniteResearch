from io import BytesIO


from tag_reader.readers.base_template import BaseTemplate
from tag_reader.tag_instance import TagInstance
from tag_reader.tag_reader_utils import readStringInPlace
from tag_reader.tag_parse_control import TagParseControl


class StringList(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'uslg')
        # self.resource = []
        self.json_str_base = '{"root":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        super(StringList, self).onInstanceLoad(instance)
        variants = {}
        if instance.tagDef.N == "language references":
            valid_lang = [0, 3, 2, 4, 5]
            for i, lang in enumerate(instance.childs):
                if not (i in valid_lang):
                    continue
                filename = f'{self.full_filepath}[{i}_string_list_resource]'
                temp = TagParseControl(filename, p_tagLayout=lang['string list resource'].tagDef.B)
                temp.readFile()
                instance_s = temp.rootTagInst.childs[0]['string lookup info']
                if not temp.rootTagInst.childs[0]['string data utf8'].loaded_bin_data:
                    with open(filename, 'rb') as f_temp:
                        temp.rootTagInst.childs[0]['string data utf8'].readBinData(f_temp)
                bin_stream = BytesIO(temp.rootTagInst.childs[0]['string data utf8'].bin_data)
                init_adress = instance_s.content_entry.field_data_block.offset_plus + instance_s.content_entry.field_data_block.size

                for x in instance_s.childs:
                    offset_temp = x['offset'].value  # init_adress +
                    if offset_temp == -1:
                        x['string id'].extra_data = {"str_": ''}
                        continue
                    x['string id'].extra_data = {"str_": readStringInPlace(bin_stream, offset_temp, True)}
                lang['string list resource'].childs = temp.rootTagInst.childs
                # self.resource.append(temp)
