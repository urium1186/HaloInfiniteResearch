import os

from commons.common_utils import resolvePathFile
from configs.config import Config

from tag_reader.readers.interfaces import IBaseTemplate
from tag_reader.readers.reader_factory import ReaderFactory

from tag_reader.tag_parse_control import TagParseControl
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

        if self.tag_parse.rootTagInst is not None :
            if len(self.tag_parse.rootTagInst.childs) != 0:
                self.first_child = self.tag_parse.rootTagInst.childs[0]
            else:
                if Config.VERBOSE:
                    print(f'len(self.tag_parse.rootTagInst.childs) == 0 in {self.full_filepath}')

    def getTagGroup(self):
        super(BaseTemplate, self).getTagGroup()
        return self.tagLayoutExt
        
    def readParameterByName(self, str_name):
        return self.tag_parse.readTagDefinitionByNamePathSelfAddress(str_name)

    def is_loaded(self):
        return self._loaded

    def toJson(self):
        self.json_base = json.loads(self.json_str_base)

    def onInstanceLoad(self, instance):
        if self.load_recursive and instance.tagDef.T == 'TagRef':
            if instance.ref_id_int != -1 and instance.path == '':
                debug = True
            if instance.path != '' and instance.path is not None:
                path_full = instance.getInGamePath()
                if path_full == '' or not os.path.exists(Config.BASE_UNPACKED_PATH+path_full):
                    path_full = resolvePathFile(instance.path, instance.tagGroupRev).replace(Config.BASE_UNPACKED_PATH,'')
                    if path_full!= '' and not (path_full.__contains__('{') and path_full.__contains__('}')):
                        #print(f'No mapped but exist {path_full} ')
                        pass
                if path_full != '':
                    #print(path_full)
                    instance.parse = ReaderFactory.create_reader(path_full)
                    if not instance.parse.is_loaded() and not instance.parse.loading:
                        instance.parse.load_recursive = self.load_recursive
                        instance.parse.load()
                else:
                    debug = True
                    #print(f'Error missing file {instance.path }')
        pass
