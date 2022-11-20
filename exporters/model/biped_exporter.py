from commons.logs import Log
from configs.config import Config
from exporters.model.base_exporter import BaseExporter
from exporters.model.exporter_factory import ExporterFactory
from tag_reader.readers.biped import Biped
from tag_reader.readers.reader_factory import ReaderFactory


class BipedExporter(BaseExporter):

    def __init__(self, reader: Biped):
        super(BipedExporter, self).__init__()
        self.render_model_exporter = None
        self.reader = reader
        self.model_parse = None
        self.filepath_export = Config.MODEL_EXPORT_PATH

    def export(self):
        pass

    def exportByThemeJson(self, json_path, data):
        Log.Print('export bibet')
        if not self.reader.is_loaded():
            self.reader.load()
        filename = self.reader.first_child['model'].getInGamePath()
        if filename != '':
            self.model_parse = ReaderFactory.create_reader(filename)
            self.model_parse.load()
            exporter = ExporterFactory.create_exporter(self.model_parse)  # ModelExporter(parse_model)
            exporter.exportByJson(json_path, data)