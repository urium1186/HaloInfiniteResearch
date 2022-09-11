import importlib
import os
import pkgutil

from commons.share_mem import parse_dict
from commons.tag_group_extension_map import map_ext
from halo_infinite_tag_reader.readers.interfaces import IBaseTemplate

class ReaderFactory:
    """
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
        'shbc': ShaderBytecode
    }
    """
    class_map = {
        'bitm': ('bitmap','Bitmap'),
        'mat ': ('material','Material'),
        'mwpl': ('materialpalette','MaterialPalette'),
        'mwsy': ('materialstyles','MaterialStyles'),
        'hlmt': ('model','Model'),
        'unic': ('multilingual_unicode_string_list','MultilingualUnicodeStringList'),
        'mode': ('render_model','RenderModel'),
        'uslg': ('stringlist','StringList'),
        'mwsw': ('swatch','Swatch'),
        'shbc': ('shader_bytecode','ShaderBytecode')
    }
    path_import = 'halo_infinite_tag_reader.readers'
    pluginname = 'swatch'

    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    @staticmethod
    def create_reader(relative_path: str) -> IBaseTemplate:
        file_ext = os.path.splitext(relative_path)[1].replace('.', '')
        tag_group = ''
        for key in map_ext.keys():
            if map_ext[key] == file_ext:
                tag_group = str(key)
                break
        path_import = 'halo_infinite_tag_reader.readers'
        pluginname = 'generic'
        relative_path = relative_path.replace('\\','/')
        if parse_dict.keys().__contains__(relative_path):
            return parse_dict[relative_path]
        if ReaderFactory.class_map.keys().__contains__(tag_group):
            pluginname = ReaderFactory.class_map[tag_group][0]
            plugin = importlib.import_module('{path}.{name}'.format(path=path_import, name=pluginname))
            temp_parse = eval(f'plugin.{ReaderFactory.class_map[tag_group][1]}("{relative_path}")')

        else:
            # generic import Generic
            plugin = importlib.import_module('{path}.{name}'.format(path=path_import, name=pluginname))
            temp_parse = eval(f'plugin.Generic("{relative_path}")')

        parse_dict[relative_path] = temp_parse
        return temp_parse
