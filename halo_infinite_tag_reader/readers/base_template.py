from configs.config import Config
from halo_infinite_tag_reader.tagparsecontrol import TagParseControl
import json


class BaseTemplate:

    def __init__(self, p_in_game_path, tagLayoutExt):
        self.json_str_base = "{}"
        self.json_base = None
        self.in_game_path = p_in_game_path
        self.full_filepath = Config.BASE_UNPACKED_PATH + self.in_game_path
        self.tagLayoutExt = tagLayoutExt
        self.tag_parse = TagParseControl(self.full_filepath, self.tagLayoutExt)
        self.tag_parse.AddSubscribersForOnInstanceLoad(self.onInstanceLoad)
        self._loaded = False

    def load(self):
        self.tag_parse.readFile()
        self._loaded = True

    def is_loaded(self):
        return self._loaded

    def toJson(self):
        self.json_base = json.loads(self.json_str_base)

    def onInstanceLoad(self, instance):
        pass
