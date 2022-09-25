import subprocess
from ctypes import cdll
from pathlib import Path

from configs.config import Config
from exporters.base_exporter import BaseExporter
from exporters.model.disassemble_byte_code import handleShader
from tag_reader.readers.shader_bytecode import ShaderBytecode



class ShaderBytecodeExporter(BaseExporter):
    def __init__(self, p_shader_bytecode: ShaderBytecode):
        super(ShaderBytecodeExporter, self).__init__()
        self.r_shader_bytecode = p_shader_bytecode
        self.HLSLcc = None

    def export(self):
        super(ShaderBytecodeExporter, self).export()
        if not self.r_shader_bytecode.is_loaded():
            self.r_shader_bytecode.load()

        if not self.r_shader_bytecode.first_child['shaderBytecodeData'].loaded_bin_data:
            with open(self.r_shader_bytecode.full_filepath, 'rb') as f:
                self.r_shader_bytecode.first_child['shaderBytecodeData'].readBinData(f)

        handleShader(self.r_shader_bytecode.full_filepath,self.r_shader_bytecode.first_child['shaderBytecodeData'].bin_data, 'g')


