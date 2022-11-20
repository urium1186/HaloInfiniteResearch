import os
import pathlib

from commons.tag_group_extension_map import map_ext
from tag_reader.readers.base_template import BaseTemplate


class Generic(BaseTemplate):

    def __init__(self, filename):
        file_ext = os.path.splitext(filename)[1].replace('.','')
        tag_group = ''
        for key in map_ext.keys():
            if map_ext[key] == file_ext:
                tag_group = str(key)
                break

        if tag_group != '':
            super().__init__(filename, tag_group)
        else:
            raise Exception(f'No tag group for {file_ext} in {filename}')

    def toJson(self, from_first_child=False):
        super().toJson(True)