from halo_infinite_tag_reader.base_template import BaseTemplate


class Material(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mat ')
        self.json_str_base = '{"swatches":[]}'

    def load(self):
        super().load()