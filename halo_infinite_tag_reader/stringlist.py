from halo_infinite_tag_reader.base_template import BaseTemplate
from halo_infinite_tag_reader.common_tag_types import TagInstance
from configs.config import Config
from halo_infinite_tag_reader.stringlist_resource import StringListResource


class StringList(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'uslg')
        self.resource = []
        self.json_str_base = '{"root":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        variants = {}
        if instance.tagDef.N == "language references":
            valid_lang = [0,3,2,4,5]
            for i, lang in enumerate(instance.childs):
                if not (i in valid_lang):
                    continue
                filename = Config.BASE_UNPACKED_PATH + f'ui\\strings\\_olympus\\menus\\inspect_player_armor.stringlist[{i}_string_list_resource]'
                parse_string_list_r = StringListResource(filename)
                parse_string_list_r.load()
                self.resource.append(parse_string_list_r)