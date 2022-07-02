from halo_infinite_tag_reader.tagparsecontrol import TagParseControl
import json


class BaseTemplate:

    def __init__(self, filename, tagLayoutExt):
        self.json_str_base = "{}"
        self.json_base = None
        self.filename = filename
        self.tagLayoutExt = tagLayoutExt
        self.tag_parse = TagParseControl(filename, self.tagLayoutExt)
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
