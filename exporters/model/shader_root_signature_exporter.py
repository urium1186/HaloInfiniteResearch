import subprocess
from ctypes import cdll
from pathlib import Path

from configs.config import Config
from exporters.base_exporter import BaseExporter
from exporters.model.disassemble_byte_code import handleShader
from tag_reader.readers.shader_bytecode import ShaderBytecode
tmp_file = Config.ROOT_DIR + "\\tmp\\shadertmp"
fxc_binary = "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.19041.0\\x64\\fxc.exe"
dxil_spirv = Config.ROOT_DIR + "\\blender_hi\\libs\\dxil-spirv.exe"

class ShaderRootSignatureExporter(BaseExporter):
    def __init__(self, p_shader_bytecode: ShaderBytecode):
        super(ShaderRootSignatureExporter, self).__init__()
        self.r_shader_bytecode = p_shader_bytecode
        self.HLSLcc = None

    def export(self):
        super(ShaderRootSignatureExporter, self).export()
        if not self.r_shader_bytecode.is_loaded():
            self.r_shader_bytecode.load()

        if not self.r_shader_bytecode.first_child['rootSignatureData'].loaded_bin_data:
            with open(self.r_shader_bytecode.full_filepath, 'rb') as f:
                self.r_shader_bytecode.first_child['rootSignatureData'].readBinData(f)
        """
        tmp_file_1 = Config.ROOT_DIR + "\\tmp\\rs1.rs.fxo"

        try:
            res = subprocess.check_output([dxil_spirv, tmp_file_1, '--glsl'])
            return res
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise e
        
        self.extractsRootSignatur()
        """

    def extractsRootSignatur(self):
        p_bytecode = self.r_shader_bytecode.first_child['rootSignatureData'].bin_data
        with open(tmp_file, 'w+b') as f:
            f.write(p_bytecode)  # write bytecode into temp file for dxc to disassemble
        try:
            res = subprocess.check_output([fxc_binary, '-dumpbin', tmp_file.replace('\\', '/')])
            return res
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise e
