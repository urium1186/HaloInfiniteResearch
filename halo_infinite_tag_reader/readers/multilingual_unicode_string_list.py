import os

from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from halo_infinite_tag_reader.tag_instance import TagInstance
from halo_infinite_tag_reader.tag_reader_utils import readStringInPlace


class MultilingualUnicodeStringList(BaseTemplate):
    test_path = 'ui\strings\_olympus\menus\lobbies.multilingual_unicode_string_list'
    def __init__(self, filename):
        super().__init__(filename, 'unic')
        self.json_str_base = '{"root":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        super(MultilingualUnicodeStringList, self).onInstanceLoad(instance)
        variants = {}
        #byteLengthCount
        if instance.tagDef.N == 'string references':
            block_size = self.tag_parse.rootTagInst.childs[0]['string data utf8'].byteLengthCount
            temp_len = os.path.getsize(self.filename)
            offset = temp_len - block_size
            print(offset)

            for lang in instance.childs:
                #continue
                lang_offset = offset + lang['english offset'].value
                temp_s = readStringInPlace(self.tag_parse.f,lang_offset, inplace=True)
                sub_offset = 0
                if temp_s == '':
                    sub_offset = 11
                    temp_s = readStringInPlace(self.tag_parse.f, lang_offset + sub_offset, inplace=True)
                    if temp_s == '':
                        sub_offset = 26
                        temp_s = readStringInPlace(self.tag_parse.f, lang_offset + 26, inplace=True)
                print(temp_s)
                lang['english offset'].extra_data = {"str_":temp_s}
                lang_offset = offset + lang['spanish offset'].value + sub_offset
                temp_s = readStringInPlace(self.tag_parse.f, lang_offset, inplace=True)
                lang['spanish offset'].extra_data = {"str_":temp_s}
                lang_offset = offset + lang['mexican spanish offset'].value + sub_offset
                temp_s = readStringInPlace(self.tag_parse.f, lang_offset, inplace=True)
                lang['mexican spanish offset'].extra_data = {"str_":temp_s}
        elif instance.tagDef.N == 'substitution pairs':
            for lang in instance.childs:
                continue
