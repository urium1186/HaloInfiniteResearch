import subprocess
from ctypes import cdll
from pathlib import Path

from configs.config import Config

dxc_binary = Config.ROOT_DIR + "\\blender_hi\\libs\\dxc-artifacts\\bin\\dxc.exe"
dxil_spirv = Config.ROOT_DIR + "\\blender_hi\\libs\\dxil-spirv.exe"
multi_output = Config.EXPORT_SHADERS  # "." for current directory, needs to end with '/'
tmp_file = Config.ROOT_DIR + "\\tmp\\shadertmp"
root_path = "/home/ich/haloRIP/HIMU/output/"  # needs to end with '/'
HLSLcc_path = Config.ROOT_DIR + "\\blender_hi\\libs\\hlslcc.dll"
HLSLcc = cdll.LoadLibrary(HLSLcc_path)


def handleShader(filename, bc, mode):
    output_path = filename.split('.')[0:-1][0].replace(Config.BASE_UNPACKED_PATH, "")

    disassembly = disassembleShader(bc)

    shadername = filename.split('\\')[-1].split('{')[0].split('.')[0]

    bytecodename = ""
    if mode == "b":
        bytecodename = output_path + ".dxbc"
    if mode == "d":
        bytecodename = output_path + ".dxil"
    if mode == "g":
        bytecodename = output_path + ".glsl"

    if bytecodename == "":
        print("Error: No valid output format specified!")
        return

    out = Path(multi_output + output_path.replace(output_path.split('\\')[-1], ''))
    out.mkdir(parents=True, exist_ok=True)
    with open(multi_output + bytecodename, "w+b") as result:
        if mode == "d":
            print(f"Writing disassembly to {(multi_output + shadername + '/' + bytecodename)}")
            result.write(disassembly)
        if mode == "b":
            print(f"Writing binary DXBC to {(multi_output + shadername + '/' + bytecodename)}")
            result.write(bc)
        if mode == "g":
            print(f"Writing decompiled GLSL to {(multi_output + shadername + '/' + bytecodename)}")
            result.write(decompileShader(bc))


def disassembleShader(p_bytecode):
    with open(tmp_file, 'w+b') as f:
        f.write(p_bytecode)  # write bytecode into temp file for dxc to disassemble
    try:
        res = subprocess.check_output([dxc_binary, '-dumpbin', tmp_file.replace('\\', '/')])
        return res
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


def decompileShader(p_bytecode):
    with open(tmp_file, 'w+b') as f:
        f.write(p_bytecode)  # write bytecode into temp file for dxc to disassemble
    try:
        res = subprocess.check_output([dxil_spirv, tmp_file, '--glsl'])
        return res
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e
