from halo_infinite_tag_reader.base_template import BaseTemplate


class Bitmap(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'bitm')

    def toJson(self):
        super().toJson()

    def load(self):
        super().load()
