from commons.enums_struct_def import TargetPlatform
from halo_infinite_tag_reader.readers.base_template import BaseTemplate


class ShaderBytecode(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'shbc')
        self.json_str_base = '{}'
        self.platform_marker: TargetPlatform = TargetPlatform.pc

    def load(self):
        super().load()
        self.platform_marker = TargetPlatform(self.first_child['platform marker'].value)
