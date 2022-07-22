#################################################################################
#
#   This script reads Halo Infinite shader bytecode files and saves the disassembly
#
#################################################################################

import sys
import subprocess
from pathlib import Path
from ctypes import cdll

from Header import Header
from DataTable import DataTable
from StringTable import StringTable
from ContentTable import ContentTable


#   Adjust these strings for your system
dxc_binary = "/home/ich/haloRIP/dxc-artifacts/bin/dxc"
dxil_spirv = "/home/ich/haloRIP/dxil-spirv/build/dxil-spirv"
multi_output = "./shaderdis/"  # "." for current directory, needs to end with '/'
tmp_file = "/tmp/shadertmp"
root_path = "/home/ich/haloRIP/HIMU/output/"    # needs to end with '/'
HLSLcc_path = "/home/ich/haloRIP/blender_plugin/libhlslcc.so"

def printUsage():
    print("Usage: python3 disassembleShaders.py <options> <file>")
    print()
    print("Dumps the content Table and Strings of the file")
    print()
    print("Options:")
    print("\t-s\t\tdisassemble a single file")
    print("\t-a\t\tdisassemble all files in the specified folder")
    print("\t-v\t\tdisassemble shader variant file (root path needs to be set in the script)")
    exit()

if len(sys.argv) < 3:
    printUsage()

if not (sys.argv[1] == '-s' or sys.argv[1] == '-a' or sys.argv[1] == '-v'):
    print("Error: Options -s or -a needs to be specified")
    printUsage()

def loadHLSLcc():
    return cdll.LoadLibrary(HLSLcc_path)

def dumpShader(path):
    try:
        with open(path,'rb') as f:
            file_header = Header()
            data_entry_table = DataTable()
            string_table = StringTable()
            content_table = ContentTable()

            if not file_header.checkMagic(f):
                print(f"File has the wrong magic")
                exit()

            file_header.readHeader(f)
            data_entry_table.readTable(f,file_header)
            string_table.readStrings(f,file_header)
            content_table.readTable(f,file_header,data_entry_table)

            bytecodes = []

            for x in range(len(content_table.entries)):
                entry = content_table.entries[x]
                hash = entry.hash
                if entry.data_reference is None:
                    continue
                if hash == b'\xb0&\x83x`E\xff\xd0:\xe9H\xa2\xc2\xf3\x97\xc4':
                    f.seek(entry.data_reference.offset + 0x24)
                    bytecode_size = int.from_bytes(f.read(4),'little')
                    bytecode_offset = entry.data_reference.offset + entry.data_reference.size
                    f.seek(bytecode_offset)
                    bytecode = f.read(bytecode_size)
                    bytecodes.append(bytecode)

            return bytecodes
    except:
        print(f"failed to open bytecode {path}")
        return []

########### notes #############
#
#  Shadervariant:
#  Hash b'l\xc7\xcf\xbb\xb2M\xcb:\xff\xfb\xbb\x8f\xce\x8b\xd5\x17' has 0x48 long entries, one per path to bytecode
#  One Hash b':\r\xd7\x88\xeaJO\xd1\xe3\x17\x00\x8cA\x03\xd7&' per 0x48 block (also set as parent data)
#
#
#
#
#

HLSLcc = loadHLSLcc()

def disassembleShader(bytecode):
    with open(tmp_file,'w+b') as f:
        f.write(bytecode)   # write bytecode into temp file for dxc to disassemble
        res = subprocess.check_output([dxc_binary,'-dumpbin',tmp_file])
        return res

def decompileShader(bytecode):
    with open(tmp_file,'w+b') as f:
        f.write(bytecode)   # write bytecode into temp file for dxc to disassemble
        res = subprocess.check_output([dxil_spirv,tmp_file,'--glsl'])
        return res

if sys.argv[1] == '-v':
    # disassemble shader variant
    with open(sys.argv[2],'rb') as f:
        file_header = Header()
        data_entry_table = DataTable()
        string_table = StringTable()
        content_table = ContentTable()

        if not file_header.checkMagic(f):
            print(f"File has the wrong magic")
            exit()

        file_header.readHeader(f)
        data_entry_table.readTable(f,file_header)
        string_table.readStrings(f,file_header)
        content_table.readTable(f,file_header,data_entry_table)
        for x in range(len(string_table.strings)):
            if 'bytecode' in string_table.strings[x]:
                path = root_path + string_table.strings[x].replace('\\','/') + ".shader_bytecode"
                print(f"Uses bytecode {path}")
                bc = dumpShader(path)
                if bc == []:
                    path = root_path + string_table.strings[x].replace('\\','/') + ".shader_root_signature"
                    print(f"Trying {path}")
                    bc = dumpShader(path)
                for i in range(len(bc)):
                    disassembly = disassembleShader(bc[i])
                    hlslres = b''
                    print(f"HLSLcc: {HLSLcc.TranslateHLSLFromMem(bc[i],0,0,0,0,0,0,hlslres)}")
                    print(hlslres)
                    shadername = sys.argv[2].split('/')[-1].split('{')[0].split('.')[0]
                    #bytecodename = shadername + "." + string_table.strings[x].split('\\')[-1].split('{')[0].split('.')[0] + ".dis"
                    #bytecodename = shadername + "." + string_table.strings[x].split('\\')[-1].split('{')[0].split('.')[0] + ".dxbc"
                    bytecodename = shadername + "." + string_table.strings[x].split('\\')[-1].split('{')[0].split('.')[0] + ".glsl"
                    out = Path(multi_output + shadername + "/")
                    out.mkdir(parents=True,exist_ok=True)
                    with open(multi_output + shadername + "/" + bytecodename,"w+b") as result:
                        #result.write(disassembly)
                        #result.write(bc[i])
                        result.write(decompileShader(bc[i]))
                    

exit()
with open(sys.argv[2],'rb') as f:
    file_header = Header()
    data_entry_table = DataTable()
    string_table = StringTable()
    content_table = ContentTable()

    if not file_header.checkMagic(f):
        print(f"File has the wrong magic")
        exit()

    file_header.readHeader(f)
    data_entry_table.readTable(f,file_header)
    string_table.readStrings(f,file_header)
    content_table.readTable(f,file_header,data_entry_table)

    print(f"\nDumping {len(string_table.strings)} Strings with valid indicies:")
    for x in range(len(string_table.strings)):
        print(f"String {x}: {string_table.strings[x]}")
    
    print(f"\nDumping Content Table:")
    for x in range(len(content_table.entries)):
        entry = content_table.entries[x]
        hash = entry.hash
        print(f"\nContent Entry:")
        print(f"\tHash: {hash}")
        if entry.data_reference is not None:
            print(f"\tReferenced Data:\n\t\tOffset: {hex(entry.data_reference.offset)}\n\t\tSize: {hex(entry.data_reference.size)}")
        if entry.data_parent is not None:
            print(f"\tParent Data:\n\t\tOffset: {hex(entry.data_parent.offset)}\n\t\tSize: {hex(entry.data_parent.size)}")