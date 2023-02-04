import io
import struct

import gf
import os
from ctypes import cdll, c_char_p, create_string_buffer

from configs.config import Config

#from tag_group_extension_map import ma_guid_ext

"""
So basically
V51:
if(hd1){
    offset = item.offset + module.dataoffset - module.hd1_delta
} else {
    offset = item.offset + module.dataoffset
}

V52:
if(hd1){
    offset = item.offset + module.hd1_delta
} else {
    offset = item.offset + module.dataoffset
}

(module.dataoffset in this case is the end of the block table aligned)
"""
class OodleDecompressor:
    """
    Oodle decompression implementation.
    Requires Windows and the external Oodle library.
    """

    def __init__(self, library_path: str) -> None:
        """
        Initialize instance and try to load the library.
        """
        if not os.path.exists(library_path):
            print(f'Looking in {library_path}')
            raise Exception("Could not open Oodle DLL, make sure it is configured correctly.")

        try:
            self.handle = cdll.LoadLibrary(library_path)
        except OSError as e:
            raise Exception(
                "Could not load Oodle DLL, requires Windows and 64bit python to run."
            ) from e

    def decompress(self, payload: bytes, output_size) -> bytes:
        """
        Decompress the payload using the given size.
        """
        output = create_string_buffer(output_size)
        try:
            self.handle.OodleLZ_Decompress(
                c_char_p(payload), len(payload), output, output_size,
                0, 0, 0, None, None, None, None, None, None, 3)
        except OSError:
            return False
        return output.raw


def getGUID(hex_string):
    temp_s = hex_string.upper()
    return '{' + temp_s[6:8] + temp_s[4:6] + temp_s[2:4] + temp_s[0:2] + "-" + temp_s[10:12] + temp_s[8:10] + "-" \
           + temp_s[12:16] + "-" + temp_s[16:20] + "-" + temp_s[21:32] + "}"


def extract_module(module, filter = '', save_to_files = True, unpack_path = '', deploy_path = '', out_memo_files = []):
    fb = open(f"{deploy_path}/{module}.module", "rb")
    #fb = open("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo Infinite\\deploy\\any\\globals\\globals-rtx-new.module", "rb")
    file_size = fb.seek(0, 2)
    fb.seek(0)
    # Parsing header
    magic = gf.read_uint32(fb)
    assert magic == gf.get_uint32(b"mohd", 0), "Incorrect file given. Must be a module file."
    version = gf.read_uint32(fb)
    # version 48: first flight
    # version 51: second flight
    # assert version == 51, "Unsupported file version"
    assert version == 52, "Unsupported file version"
    unk0x08 = gf.read_uint32(fb)
    unk0x0C = gf.read_uint32(fb)
    files_count = gf.read_uint32(fb)
    unk0x14 = gf.read_int32(fb)
    # assert unk0x14 == gf.get_uint32(b"\xFF\xFF\xFF\xFF", 0), "Header has non-FFFFFFFF 0x14"
    unk0x18 = gf.read_int32(fb)
    # assert unk0x18 == gf.get_uint32(b"\x00\x00\x00\x00", 0), "Header has non-0 0x18"
    unk0x1C = gf.read_int32(fb)
    # assert unk0x1C == gf.get_uint32(b"\xFF\xFF\xFF\xFF", 0), "Header has non-FFFFFFFF 0x1C"
    table3_first_value = gf.read_uint32(fb)
    string_table_length = gf.read_uint32(fb)
    table3_count = gf.read_uint32(fb)
    blocks_count = gf.read_uint32(fb)
    unk0x30 = gf.read_uint32(fb)
    unk0x34 = gf.read_uint32(fb)
    unk0x38 = gf.read_uint32(fb)
    unk0x3C = gf.read_uint32(fb)
    unk0x40 = gf.read_uint32(fb)
    unk0x44 = gf.read_uint32(fb)
    hd1_delta = file_size

    # Check if we need to use an hd1 file (no hd2 files just yet...)
    fb_hd1 = None
    if os.path.isfile(f"{deploy_path}/{module}.module_hd1"):
        fb_hd1 = open(f"{deploy_path}/{module}.module_hd1", "rb")

    # Table1
    class FileEntry:
        def __init__(self):
            pass

    files = []
    for i in range(files_count):
        t1e = FileEntry()
        t1e.resource_count = gf.read_uint32(fb)  # 0x00
        t1e.parent_file_index = gf.read_int32(fb)  # 0x04
        t1e.unk0x08 = gf.read_uint16(fb)  # 0x08
        t1e.block_count = gf.read_uint16(fb)  # 0x0A
        t1e.first_block_index = gf.read_uint32(fb)  # 0x0C
        t1e.first_resource_index = gf.read_uint32(fb)  # 0x10
        t1e.tag = fb.read(4)  # 0x14
        t1e.local_data_offset = int.from_bytes(fb.read(6), byteorder='little')  # 0x18
        t1e.unk0x1F = fb.read(2)  # 0x1F
        if t1e.local_data_offset > 100000000000:
            q = fb.tell()
            a = 0
        t1e.comp_size = gf.read_uint32(fb)  # 0x20
        t1e.decomp_size = gf.read_uint32(fb)  # 0x24
        t1e.unk0x28 = gf.read_uint32(fb)  # 0x28
        t1e.unk0x2C = gf.read_uint32(fb)  # 0x2C
        t1e.unk0x30 = gf.read_uint32(fb)  # 0x30
        t1e.unk0x34 = gf.read_uint32(fb)  # 0x34
        t1e.unk0x38 = gf.read_uint32(fb)  # 0x38
        t1e.header_size = gf.read_uint32(fb)  # 0x3C
        t1e.string_offset = gf.read_uint32(fb)  # 0x40
        t1e.unk0x44 = gf.read_int32(fb)  # 0x44, -1 int for one type, not for another
        t1e.hash = fb.read(0x10).hex().upper()  # 0x48 -> 0x58

        files.append(t1e)
    pos = fb.tell()
    fb.seek(8, 1)
    string_table_offset = fb.tell()
    for t1e in files:
        t1e.string = gf.offset_to_string(fb, string_table_offset + t1e.string_offset)
    pos2 = fb.tell()
    # Table 3
    t3es = []
    for i in range(table3_count):
        t3es.append(gf.read_uint32(fb))

    # Table 4
    class BlockEntry:
        def __init__(self):
            pass

    blocks = []
    for i in range(blocks_count):
        t4e = BlockEntry()
        t4e.comp_offset = gf.read_uint32(fb)  # 0x00
        t4e.comp_size = gf.read_uint32(fb)  # 0x04
        t4e.decomp_offset = gf.read_uint32(fb)  # 0x08
        t4e.decomp_size = gf.read_uint32(fb)  # 0x0C
        t4e.b_compressed = gf.read_uint32(fb)  # 0x10
        blocks.append(t4e)

    # Get data

    # To skip zeros
    while fb.read(1) == b"\x00":
        continue

    data_offset = fb.seek(-1, 1)
    #return
    oodleDllPath = Config.ROOT_DIR + "\\unpacker\\oo2core_8_win64.dll"
    decompressor = OodleDecompressor(oodleDllPath)

    #print(f"File count: {len(files)}")
    for i, t1e in enumerate(files):
        # Cleaning string to be savable

        if ":" in t1e.string:
            t1e.string = t1e.string.replace(" ", "_")
            t1e.string = t1e.string.replace(":", "_")

        t1e.save_path = f"{unpack_path}{t1e.string}"

        # if "[5_bitmap_resource_handle.chunk5]" in t1e.string:
        #     continue

        temp = ('/'.join(t1e.save_path.split('/')[:-1]))
        #if not (temp.__contains__('spartan_armor') or temp.__contains__('gear')):
        #if not (temp.__contains__('pc__/objects/characters/spartan_armor/bitmaps/')):
        #if not (temp.__contains__('materials/generic/')):
        # if not (temp.__contains__('__chore/pc__/shaders/')):
        #if not (temp.__contains__('coatings')):
        #if not (temp.__contains__('materialswatch')):
        # if not (temp.__contains__('objects')) or (temp.__contains__('pc__')):
        # if not (temp.__contains__('objects/characters')):
        # if not (temp.__contains__('spartan_armor/gear')):
        # if not (t1e.save_path.__contains__('.')):
        # if not (temp.__contains__('brute_atriox')):
        #if not (temp.__contains__('hum_base_fabric_oriental_pattern_01_normal{pc}')):
        #if not (t1e.save_path.__contains__('hum_base_fabric_oriental_pattern_02_normal{pc}')):
        #if not (t1e.save_path.__contains__('_normal{pc}') and t1e.save_path.__contains__('__chore/pc__/materials/generic/')):
        if not (temp.__contains__(filter)):
            continue
        # print(t1e.save_path)
        # os.makedirs('/'.join(t1e.save_path.split('/')[:-1]), exist_ok=True)

        in_file_offset = data_offset + t1e.local_data_offset

        if in_file_offset >= file_size:
            if not fb_hd1:
                if len(files) - i > 1000:
                    raise Exception(f"Files could not be found with debug value {in_file_offset}")
                else:
                    continue
            # if not fb_hd1:
            #     raise Exception(f"Local data offset fail, trying to get offset {in_file_offset} with file size {file_size} for file index {i}, string {t1e.string}. Rest of files offsets are {[x.local_data_offset for x in files[i:]]}")
            tmp = fb_hd1
            file_data_offset = in_file_offset - hd1_delta
        else:
            tmp = fb
            file_data_offset = in_file_offset
        decomp_save_data = b""
        if t1e.decomp_size == 0:
            with open(t1e.save_path, "wb"):
                continue
        if t1e.block_count:  # Leer el GUID
            for block in blocks[t1e.first_block_index:t1e.first_block_index + t1e.block_count]:
                if block.b_compressed:
                    tmp.seek(file_data_offset + block.comp_offset)
                    data = tmp.read(block.comp_size)
                    decomp = decompressor.decompress(data, block.decomp_size)
                    if len(decomp_save_data) != block.decomp_offset:
                        raise Exception("Skipped data fix")
                    if decomp == False:
                        decomp_save_data += b"\0" * block.decomp_size
                        raise Exception("Warning: failed to decompress block in file: " + t1e.string)
                    else:
                        decomp_save_data += decomp
                else:
                    tmp.seek(file_data_offset + block.comp_offset)
                    decomp = tmp.read(block.comp_size)
                    if len(decomp_save_data) != block.decomp_offset:
                        raise Exception("Skipped data fix")
                    decomp_save_data += decomp
        else:
            tmp.seek(file_data_offset)
            if t1e.comp_size == t1e.decomp_size:
                decomp_save_data = tmp.read(t1e.comp_size)
                #print(t1e.save_path)
            else:
                decomp_save_data = decompressor.decompress(tmp.read(t1e.comp_size), t1e.decomp_size)

        if save_to_files:
            new_dir_path = os.path.dirname(t1e.save_path)
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path, exist_ok=True)
            with open(t1e.save_path, "wb") as f:
                f.write(decomp_save_data)
                print(t1e.save_path)
        else:
            out_memo_files.append(decomp_save_data)


def extract_all_modules(filter = '', save_to_files = True, unpack_path = '', deploy_path = '',  out_memo_files = []):
    # Ignoring module hd files
    p = [os.path.join(dp, f)[len(deploy_path):].replace("\\", "/") for dp, dn, fn in
         os.walk(os.path.expanduser(deploy_path)) for f in fn if ".module" in f and ".module_" not in f]
    for file in p:
        # print(file)
        extract_module(file.replace(".module", ""), filter, save_to_files, unpack_path, deploy_path)




if __name__ == "__main__":
    unpack_directory = "J:/Games/Halo Infinite Stuf/Extracted/HI/models/beta 1/"
    directory = f"{unpack_directory}/__chore\pc__\objects\weapons/"
    directory = f"{unpack_directory}/__chore\pc__\materials\generic/"
    directory = f"{unpack_directory}/__chore\pc__\objects\characters\spartan_armor/"
    directory = f"{unpack_directory}/__chore\pc__\shaders/"
    directory = directory.replace("\\", "/")
    path_to_create = [
        f"{unpack_directory}/__chore\pc__\objects\characters".replace("\\", "/"),
    ]

    # unpack_path = "C:/Users/Jorge/Downloads/Compressed/deploy1/HIU1/"
    # unpack_path = "J:/Games/Halo Infinite Stuf/Extracted/HI/models/beta 1/"
    # unpack_path = "J:/Games/Halo Infinite Stuf/Extracted/UnPaked/season2/models/"
    unpack_path = "J:/Games/Halo Infinite Stuf/Extracted/UnPacked/season2/"  # multiplayer
    #unpack_path = "J:/Games/Halo Infinite Stuf/Extracted/UnPacked/campaign/"  # campaign
    # deploy_path = "J:/Games/Halo Infinite Stuf/Extracted/Paked/deploy"
    # deploy_path = "H:/SteamLibrary/steamapps/common/Halo Infinite/deploy/"
    deploy_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo Infinite\\deploy\\"  # multiplayer
    #deploy_path = "J:\\Games\\Instalados\\Halo Infinite\\deploy\\"  # campaign
    # deploy_path = "H:/HI/temp/globals"
    # module_path = "pc/globals/forge/forge_objects-rtx-new"
    # module_name = "any/globals/forge/"
    # extract_module(module_path)
    out_memo_files = []
    save_to_files = False
    filter = ''
    extract_all_modules(filter, save_to_files, unpack_path, deploy_path, out_memo_files)
    #print(ma_guid_ext)
    print('end extract')

    ## pc/globals/forge/forge_objects-rtx-new.module is broken
