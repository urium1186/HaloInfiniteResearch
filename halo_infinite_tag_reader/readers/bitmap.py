from enum import IntFlag

from commons.common_utils import getGUID
from commons.debug_utils import fillDebugDict, bitmap_id_usage
from halo_infinite_tag_reader.common_tag_types import TagInstance
from halo_infinite_tag_reader.readers.base_template import BaseTemplate
import re


class Bitmap(BaseTemplate):
    class BitmapType(IntFlag):
        TEXTURE2D = 0
        TEXTURE3D = 1
        CUBEMAP = 2
        ARRAY = 3

    def __init__(self, filename):
        super().__init__(filename, 'bitm')

    def toJson(self):
        super().toJson()

    def load(self):
        super().load()

    def isNormalMapUsage(self):
        return self.tag_parse.rootTagInst.childs[0]['UsageId'].value == '70370440'

    def onInstanceLoad(self, instance: TagInstance):
        if not (instance.content_entry is None):
            hash_0 = getGUID(b'R\xab5#hBJ\xc2}\x8fr\x94#\x19m\xd3'.hex())
            hash_1 = getGUID(b'*\x80\xeb\x8akA\n\xf6\x9cp\x0c\x97MU6#'.hex())
            hash_2 = getGUID(b'jQ\xb0\xde\x98D\x1c\x02\xcd\xc6A\x99i\xaa\x94\xc2'.hex())
            hash_3 = getGUID(b'9, \xd1\xdcH\xfc\xbdI\xde+\x81\x93\xaf\xe8\xb0'.hex())

            if instance.content_entry.GUID == hash_0:
                debug = True
            elif instance.content_entry.GUID == hash_1:
                debug = True
            elif instance.content_entry.GUID == hash_2:
                debug = True
            elif instance.content_entry.GUID == hash_3:
                debug = True
        if instance.tagDef.N == 'Root':
            regex = re.compile(r"([_]{1}\d{3}[_]{1}|[_s]{1}\d{3}[_]{1})", re.IGNORECASE)
            main_key = f"{instance.childs[0]['Usage'].value}-{instance.childs[0]['UsageId'].str_value}-{instance.childs[0]['Package'].str_value}-{instance.childs[0]['texture group'].str_value}"
            main_key = f"{instance.childs[0]['UsageId'].str_value}"

            name_key = self.in_game_path.split('\\')[-1]
            f_s = re.findall(regex, name_key)
            if f_s.__len__() > 0:
                name_key = name_key.split(f_s[-1])[-1]
            fillDebugDict(main_key, name_key, bitmap_id_usage)
            debug = True
