import os

from commons.tag_group_extension_map import map_ext
from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from halo_infinite_tag_reader.readers.bitmap import Bitmap
from halo_infinite_tag_reader.readers.generic import Generic
from halo_infinite_tag_reader.readers.material import Material
from halo_infinite_tag_reader.readers.materialpalette import MaterialPalette
from halo_infinite_tag_reader.readers.materialstyles import MaterialStyles
from halo_infinite_tag_reader.readers.model import Model
from halo_infinite_tag_reader.readers.multilingual_unicode_string_list import MultilingualUnicodeStringList
from halo_infinite_tag_reader.readers.render_model import RenderModel
from halo_infinite_tag_reader.readers.stringlist import StringList
from halo_infinite_tag_reader.readers.swatch import Swatch


class ReaderFactory:
    class_map = {
        'bitm': Bitmap,
        'mat ': Material,
        'mwpl': MaterialPalette,
        'mwsy': MaterialStyles,
        'hlmt': Model,
        'unic': MultilingualUnicodeStringList,
        'mode': RenderModel,
        'uslg': StringList,
        'mwsw': Swatch,
    }

    @staticmethod
    def create_reader(relative_path: str) -> BaseTemplate:
        file_ext = os.path.splitext(relative_path)[1].replace('.', '')
        tag_group = ''
        for key in map_ext.keys():
            if map_ext[key] == file_ext:
                tag_group = str(key)
                break

        if ReaderFactory.class_map.keys().__contains__(tag_group):
            return ReaderFactory.class_map[tag_group](relative_path)
        else:
            return Generic(relative_path)
