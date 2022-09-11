from commons.common_utils import resolvePathFile
from configs.config import Config

from halo_infinite_tag_reader.readers.interfaces import IBaseTemplate
from halo_infinite_tag_reader.readers.reader_factory import ReaderFactory

from halo_infinite_tag_reader.tagparsecontrol import TagParseControl
import json


class BaseTemplate(IBaseTemplate):

    def __init__(self, p_in_game_path, tagLayoutExt):
        self.json_str_base = "{}"
        self.json_base = None
        self.in_game_path = p_in_game_path
        self.full_filepath = Config.BASE_UNPACKED_PATH + self.in_game_path
        self.tagLayoutExt = tagLayoutExt
        self.tag_parse = TagParseControl(self.full_filepath, self.tagLayoutExt)
        self.tag_parse.AddSubscribersForOnInstanceLoad(self.onInstanceLoad)
        self._loaded = False
        self.loading = False
        self.first_child = None
        self.load_recursive = False

    def load(self, force = False):
        self.loading = True
        if not self._loaded:
            self.tag_parse.readFile()
        else:
            if force:
                self.tag_parse.reset()
                self.tag_parse.readFile()

        self._loaded = True
        self.loading = False
        self.first_child = self.tag_parse.rootTagInst.childs[0]

    def is_loaded(self):
        return self._loaded

    def toJson(self):
        self.json_base = json.loads(self.json_str_base)

    def onInstanceLoad(self, instance):
        if self.load_recursive and instance.tagDef.T == 'TagRef':
            if instance.ref_id_int != -1 and instance.path == '':
                debug = True
            if instance.path != '' and instance.path is not None:
                path_full = resolvePathFile(instance.path, instance.tagGroupRev).replace(Config.BASE_UNPACKED_PATH,'')
                if path_full != '':
                    print(path_full)
                    instance.parse = ReaderFactory.create_reader(path_full)
                    if not instance.parse.is_loaded() and not instance.parse.loading:
                        instance.parse.load_recursive = self.load_recursive
                        instance.parse.load()
                else:
                    debug = True
                    print(f'Error missing file {instance.path }')
        pass
