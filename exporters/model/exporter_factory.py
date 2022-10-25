import importlib
import pkgutil

from exporters.model.base_exporter import BaseExporter
from tag_reader.readers.interfaces import IBaseTemplate


class ExporterFactory:
    class_map = {
        'bitm': ('bitmap_exporter', 'BitmapExporter'),
        'hlmt': ('model_exporter', 'ModelExporter'),
        'bipd': ('biped_exporter', 'BipedExporter'),
        'mode': ('render_model_exporter', 'RenderModelExporter')
    }
    path_import = 'tag_reader.readers'
    pluginname = 'swatch'

    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    @staticmethod
    def create_exporter(reader: IBaseTemplate) -> BaseExporter:

        path_import = 'exporters.model'
        pluginname = 'base_exporter'
        if reader is None:
            return BaseExporter()
        tag_group = reader.getTagGroup()
        # relative_path = relative_path.replace('/', '\\')
        if ExporterFactory.class_map.keys().__contains__(tag_group):
            pluginname = ExporterFactory.class_map[tag_group][0]
            plugin = importlib.import_module('{path}.{name}'.format(path=path_import, name=pluginname))
            temp_exporter = eval(f'plugin.{ExporterFactory.class_map[tag_group][1]}(reader)')

        else:
            # generic import Generic
            plugin = importlib.import_module('{path}.{name}'.format(path=path_import, name=pluginname))
            temp_exporter = eval(f'plugin.BaseExporter(reader)')

        return temp_exporter
