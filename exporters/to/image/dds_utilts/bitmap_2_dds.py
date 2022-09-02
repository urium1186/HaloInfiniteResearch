import os

from commons.enums_struct_def import TargetPlatform
from exporters.to.image.dds_utilts.dds import DDS_HEADER_FLAGS_LINEARSIZE, DDS_FOURCC, DDS_HEADER_FLAGS_PITCH, DDS_RGB, \
    DDS_HEADER_FLAGS_MIPMAP, DDS_SURFACE_FLAGS_MIPMAP
from exporters.to.image.dds_utilts.dds_file import DdsFile
from exporters.to.image.dds_utilts.dxgiformat import DXGI_FORMAT
from halo_infinite_tag_reader.common_tag_types import TagInstance
from halo_infinite_tag_reader.readers.bitmap import Bitmap

map_select_format = {
    "a8_unorm (000A)": DXGI_FORMAT.DXGI_FORMAT_A8_UNORM,
    "r8_unorm_rrr1 (RRR1)": DXGI_FORMAT.DXGI_FORMAT_R8_UNORM,  # revisar
    "r8_unorm_rrrr (RRRR)": DXGI_FORMAT.DXGI_FORMAT_R8_UNORM,  # revisar
    "r8g8_unorm_rrrg (RRRG)": DXGI_FORMAT.DXGI_FORMAT_R8G8_UNORM,
    "unused1": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "unused2": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "b5g6r5_unorm": DXGI_FORMAT.DXGI_FORMAT_B5G6R5_UNORM,
    "unused3": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "b5g6r5a1_unorm": DXGI_FORMAT.DXGI_FORMAT_B5G6R5_UNORM,
    "b4g4r4a4_unorm": DXGI_FORMAT.DXGI_FORMAT_B4G4R4A4_UNORM,
    "b8g8r8x8_unorm": DXGI_FORMAT.DXGI_FORMAT_B8G8R8X8_UNORM,
    "b8g8r8a8_unorm": DXGI_FORMAT.DXGI_FORMAT_B8G8R8A8_UNORM,
    "unused4": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "DEPRECATED_dxt5_bias_alpha": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "bc1_unorm (dxt1)": DXGI_FORMAT.DXGI_FORMAT_BC1_UNORM,
    "bc2_unorm (dxt3)": DXGI_FORMAT.DXGI_FORMAT_BC2_UNORM,
    "bc3_unorm (dxt5)": DXGI_FORMAT.DXGI_FORMAT_BC3_UNORM,
    "DEPRECATED_a4r4g4b4_font": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "unused7": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "unused8": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "DEPRECATED_SOFTWARE_rgbfp32": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "unused9": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "r8g8_snorm (v8u8)": DXGI_FORMAT.DXGI_FORMAT_R8G8_SNORM,
    "DEPRECATED_g8b8": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "r32g32b32a32_float (abgrfp32)": DXGI_FORMAT.DXGI_FORMAT_R32G32B32A32_FLOAT,
    "r16g16b16a16_float (abgrfp16)": DXGI_FORMAT.DXGI_FORMAT_R16G16B16A16_FLOAT,
    "r16_float_rrr1 (16f_mono)": DXGI_FORMAT.DXGI_FORMAT_R16_FLOAT,
    "r16_float_r000 (16f_red)": DXGI_FORMAT.DXGI_FORMAT_R16_FLOAT,
    "r8g8b8a8_snorm (q8w8v8u8)": DXGI_FORMAT.DXGI_FORMAT_R8G8B8A8_SNORM,
    "r10g10b10a2_unorm (a2r10g10b10)": DXGI_FORMAT.DXGI_FORMAT_R10G10B10A2_UNORM,
    "r16g16b16a16_unorm (a16b16g16r16)": DXGI_FORMAT.DXGI_FORMAT_R16G16B16A16_UNORM,
    "r16g16_snorm (v16u16)": DXGI_FORMAT.DXGI_FORMAT_R16G16_SNORM,
    "r16_unorm_rrr0 (L16)": DXGI_FORMAT.DXGI_FORMAT_R16_UNORM,
    "r16g16_unorm (r16g16)": DXGI_FORMAT.DXGI_FORMAT_R16G16_UNORM,
    "r16g16b16a16_snorm (signedr16g16b16a16)": DXGI_FORMAT.DXGI_FORMAT_R16G16B16A16_SNORM,
    "DEPRECATED_dxt3a": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "bc4_unorm_rrrr (dxt5a)": DXGI_FORMAT.DXGI_FORMAT_BC4_UNORM,
    "bc4_snorm_rrrr": DXGI_FORMAT.DXGI_FORMAT_BC4_SNORM,
    "DEPRECATED_dxt3a_1111": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "bc5_snorm (dxn)": DXGI_FORMAT.DXGI_FORMAT_BC5_SNORM,
    "DEPRECATED_ctx1": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "DEPRECATED_dxt3a_alpha_only": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "DEPRECATED_dxt3a_monochrome_only": DXGI_FORMAT.DXGI_FORMAT_UNKNOWN,
    "bc4_unorm_000r (dxt5a_alpha)": DXGI_FORMAT.DXGI_FORMAT_BC4_UNORM,
    "bc4_unorm_rrr1 (dxt5a_mono)": DXGI_FORMAT.DXGI_FORMAT_BC4_UNORM,
    "bc5_unorm_rrrg (dxn_mono_alpha)": DXGI_FORMAT.DXGI_FORMAT_BC5_UNORM,
    "bc5_snorm_rrrg (dxn_mono_alpha signed)": DXGI_FORMAT.DXGI_FORMAT_BC5_SNORM,
    "bc6h_uf16 ": DXGI_FORMAT.DXGI_FORMAT_BC6H_UF16,
    "bc6h_sf16 ": DXGI_FORMAT.DXGI_FORMAT_BC6H_SF16,
    "bc7_unorm ": DXGI_FORMAT.DXGI_FORMAT_BC7_UNORM,
    "d24_unorm_s8_uint (depth 24)": DXGI_FORMAT.DXGI_FORMAT_D24_UNORM_S8_UINT,
    "r11g11b10_float": DXGI_FORMAT.DXGI_FORMAT_R11G11B10_FLOAT,
    "r16g16_float": DXGI_FORMAT.DXGI_FORMAT_R16G16_FLOAT,

}


class MipmapIndexException(Exception):
    pass


class BitmapToDds:
    def __init__(self, p_bitmap: Bitmap, p_mipmap_index=0):
        if p_bitmap is None:
            raise Exception("Bitmap is None")
        self.bitmap_ti: TagInstance = p_bitmap.tag_parse.rootTagInst.childs[0]
        self.bitmap: Bitmap = p_bitmap
        self.bitmaps_0 = self.bitmap_ti['bitmaps'].childs[0]
        self.dds_file: DdsFile = None
        self.mipmap_index = p_mipmap_index
        if self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childrenCount != 0:
            if not (p_mipmap_index < self.bitmaps_0['bitmap resource handle'].childs[0][
                'mipmaps'].childrenCount):
                raise MipmapIndexException('mipmap_index es mayor q lo permitido')
        self._fillDdsFile()

    def isCompresed(self):
        dds_format_str = map_select_format[self.bitmaps_0['format'].selected].name.split('_')[2]
        return dds_format_str[0:2] == 'BC'

    def computePitch(self, dds_format: DXGI_FORMAT):
        width = self.dds_file.header.width
        block_compressed = ['BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7']
        block_uncompressed = [DXGI_FORMAT.DXGI_FORMAT_R8G8_B8G8_UNORM, DXGI_FORMAT.DXGI_FORMAT_G8R8_G8B8_UNORM,
                              DXGI_FORMAT.DXGI_FORMAT_YUY2]
        pitch = -1
        dds_format_str = dds_format.name.split('_')[2]
        if dds_format_str in block_compressed:
            block_size = 16
            temp_f = ['BC1', 'BC4']
            if dds_format_str in temp_f:
                block_size = 8
            pitch = max(1, ((width + 3) / 4)) * block_size
        elif dds_format in block_uncompressed:
            pitch = ((width + 1) >> 1) * 4
        else:
            bits_per_pixel = 3
            pitch = (width * bits_per_pixel + 7) / 8
        return int(pitch)

    def computeMipmapSize(self, dds_format: DXGI_FORMAT):
        width = self.dds_file.header.width
        height = self.dds_file.header.height
        block_compressed = ['BC1', 'BC2', 'BC3', 'BC4', 'BC5', 'BC6', 'BC7']
        dds_format_str = dds_format.name.split('_')[2]
        if dds_format_str in block_compressed:
            min_bytes = 16  # or 16(DXT2 - 5)
            if dds_format_str[2] == '1':
                min_bytes = 8  # 8(DXT1)
            size = max(1, ((width + 3) / 4)) * max(1, ((height + 3) / 4)) * min_bytes
            return size
        assert False, 'no es un formato comprimido'

    def _fillDdsFile(self):
        self.dds_file = DdsFile()
        if self.bitmap_ti['target platform'].value != TargetPlatform.pc:
            raise Exception("Need to be pc")
        if self.bitmaps_0['type'].selected_index == Bitmap.BitmapType.TEXTURE2D:
            self.load2DTexture()
        elif self.bitmaps_0['type'].selected_index == Bitmap.BitmapType.TEXTURE3D:
            print(f'Bitmap.BitmapType.TEXTURE3D {self.bitmap.in_game_path}')
            debug = True
            self.load3DTexture()
        elif self.bitmaps_0['type'].selected_index == Bitmap.BitmapType.CUBEMAP:
            print(f'Bitmap.BitmapType.CUBEMAP {self.bitmap.in_game_path}')
            debug = True
            self.loadCubeMapTexture()
        elif self.bitmaps_0['type'].selected_index == Bitmap.BitmapType.ARRAY:
            print(f'Bitmap.BitmapType.ARRAY {self.bitmap.in_game_path}')
            debug = True
            self.loadArrayTexture()
            # assert False, 'Sin Implementar Bitmap.BitmapType.ARRAY'
        else:
            assert False, 'Error desconocido tipo'

    def _getAllChunkData(self):
        bitmap_handle = self.bitmap.full_filepath
        if "{pc}" not in bitmap_handle:
            raise Exception("Need to be pc")
        # form = bitmap_handle.split("{pc}")[0].split("_")[-:]
        # print(form)
        # Finding largest
        q = bitmap_handle.split('\\')[-1]
        folder = os.path.dirname(bitmap_handle)
        d = {x.split('_bitmap_resource_handle')[-1][-2]: x for x in os.listdir(folder) if ".chunk" in x and q in x}
        if len(d.keys()) == 0:
            print(f"{bitmap_handle} has no texture files to use, skipping...")
            return b''
        data = b''
        for pa in d:
            with open(folder + '\\' + d[pa], "rb") as f:
                data += f.read()

        return data

    def _getChunkData(self, mitmap_size):
        bitmap_handle = self.bitmap.full_filepath
        if "{pc}" not in bitmap_handle:
            raise Exception("Need to be pc")
        # form = bitmap_handle.split("{pc}")[0].split("_")[-:]
        # print(form)
        # Finding largest
        q = bitmap_handle.split('\\')[-1]
        folder = os.path.dirname(bitmap_handle)
        d = {x.split('_bitmap_resource_handle')[-1][-2]: x for x in os.listdir(folder) if ".chunk" in x and q in x}
        if len(d.keys()) == 0:
            print(f"{bitmap_handle} has no texture files to use, skipping...")
            return b''
        chunk_to_use = d[min(d.keys())]
        for pa in d:
            temp_len = os.path.getsize(folder + '\\' + d[pa])
            if temp_len == mitmap_size:
                chunk_to_use = d[pa]
                break

        # chunk_to_use = d[str(bitmap_index)]
        fb = open(folder + '\\' + chunk_to_use, "rb").read()
        return fb

    def load2DTexture(self):

        if self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childrenCount == 0:
            # assert bitmaps_0['mipmap count'].value == 0, f'El numero de mimap deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value != 0, f'debe tener la data embebida'
            assert self.bitmaps_0['bitmap resource handle'].childs[0]['embed_data_len'].value == \
                   len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data), f'la data deberia estar en sect 3 '

            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])

            self.dds_file.header.width = self.bitmaps_0['width'].value
            self.dds_file.header.height = self.bitmaps_0['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header10 = None
            # self.dds_file.header10 = None
            self.dds_file.bdata = self.bitmap.tag_parse.full_header.file_header.section_3_bin_data
        else:
            assert self.bitmaps_0['mipmap count'].value != 0, f'El numero de mimap no deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value == 0, f'No debe tener la data embebida'
            assert len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data) == 0 \
                , f'la data deberia estar en sect 3 por tanto 0'
            selected = self.mipmap_index  # len(bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs)-1
            minmap = self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs[selected]
            f_name = self.bitmap.in_game_path.split('\\')[-1]
            print(f"======== {f_name} ===========")
            print(f"======== {self.bitmap_ti['Usage'].value} ===========")
            print(f"======== {self.bitmap_ti['UsageId'].value} ===========")
            print(f"======== {self.bitmap_ti['texture group'].str_value} ===========")
            for x in self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs:
                if x['mipmap index'].value == selected:
                    minmap = x
                print(f"desconocido short 0 - {x['desconocido short 0'].value}")
                print(f"desconocido short 1 - {x['desconocido short 1'].value}")
                print(f"data_size - {x['data_size'].value}")
                print(f"desconocido short 3 - {x['desconocido short 3'].value}")
                print(f"mipmap index - {x['mipmap index'].value}")
                print(f"desconocido byte    - {x['desconocido byte'].value}")
                print(f"width - {x['width'].value}")
                print(f"height - {x['height'].value}")
                print(f"===========================================================")

            assert self.bitmaps_0['bitmap resource handle'].childs[0]['format'].value == \
                   map_select_format[self.bitmaps_0['format'].selected], 'deberian ser el mismo tipo de formato'

            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = minmap['width'].value
            self.dds_file.header.height = minmap['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header.ddspf.flags = minmap['desconocido short 1'].value
            t_type = self.bitmaps_0['type'].selected_index
            t_type_str = self.bitmaps_0['type'].selected
            mipmap_count = self.bitmaps_0['mipmap count'].value
            # self.dds_file.header.mipMapCount = mipmap_count
            self.dds_file.bdata = self._getChunkData(minmap['data_size'].value)
            size = self.computeMipmapSize(map_select_format[self.bitmaps_0['format'].selected])

            DEBUG = True

        if self.isCompresed():
            self.dds_file.header.flags = DDS_HEADER_FLAGS_LINEARSIZE | DDS_FOURCC
        else:
            self.dds_file.header.flags = DDS_HEADER_FLAGS_PITCH | DDS_RGB

    def load3DTexture(self):

        if self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childrenCount == 0:
            # assert bitmaps_0['mipmap count'].value == 0, f'El numero de mimap deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value != 0, f'debe tener la data embebida'
            assert self.bitmaps_0['bitmap resource handle'].childs[0]['embed_data_len'].value == \
                   len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data), f'la data deberia estar en sect 3 '

            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = self.bitmaps_0['width'].value
            self.dds_file.header.height = self.bitmaps_0['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header10 = None
            # self.dds_file.header10 = None
            self.dds_file.bdata = self.bitmap.tag_parse.full_header.file_header.section_3_bin_data
        else:
            assert self.bitmaps_0['mipmap count'].value != 0, f'El numero de mimap no deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value == 0, f'No debe tener la data embebida'
            assert len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data) == 0 \
                , f'la data deberia estar en sect 3 por tanto 0'
            selected = 0  # len(bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs)-1
            minmap = self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs[selected]
            f_name = self.bitmap.in_game_path.split('\\')[-1]
            print(f"======== {f_name} ===========")
            print(f"======== {self.bitmap_ti['Usage'].value} ===========")
            print(f"======== {self.bitmap_ti['UsageId'].value} ===========")
            print(f"======== {self.bitmap_ti['texture group'].str_value} ===========")
            for x in self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs:
                if x['mipmap index'].value == selected:
                    minmap = x
                print(f"desconocido short 0 - {x['desconocido short 0'].value}")
                print(f"desconocido short 1 - {x['desconocido short 1'].value}")
                print(f"data_size - {x['data_size'].value}")
                print(f"desconocido short 3 - {x['desconocido short 3'].value}")
                print(f"mipmap index - {x['mipmap index'].value}")
                print(f"desconocido byte    - {x['desconocido byte'].value}")
                print(f"width - {x['width'].value}")
                print(f"height - {x['height'].value}")
                print(f"===========================================================")

            if self.bitmaps_0['bitmap resource handle'].childs[0]['format'].value != \
                    map_select_format[self.bitmaps_0['format'].selected]:
                debug = True
            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = minmap['width'].value
            self.dds_file.header.height = minmap['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header.ddspf.flags = minmap['desconocido short 1'].value
            t_type = self.bitmaps_0['type'].selected_index
            t_type_str = self.bitmaps_0['type'].selected
            mipmap_count = self.bitmaps_0['mipmap count'].value
            # self.dds_file.header.mipMapCount = mipmap_count
            self.dds_file.bdata = self._getChunkData(minmap['data_size'].value)
            size = self.computeMipmapSize(map_select_format[self.bitmaps_0['format'].selected])

            DEBUG = True

    def loadCubeMapTexture(self):

        if self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childrenCount == 0:
            # assert bitmaps_0['mipmap count'].value == 0, f'El numero de mimap deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value != 0, f'debe tener la data embebida'
            assert self.bitmaps_0['bitmap resource handle'].childs[0]['embed_data_len'].value == \
                   len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data), f'la data deberia estar en sect 3 '

            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = self.bitmaps_0['width'].value
            self.dds_file.header.height = self.bitmaps_0['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header10 = None
            # self.dds_file.header10 = None
            self.dds_file.bdata = self.bitmap.tag_parse.full_header.file_header.section_3_bin_data
        else:
            assert self.bitmaps_0['mipmap count'].value != 0, f'El numero de mimap no deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value == 0, f'No debe tener la data embebida'
            assert len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data) == 0 \
                , f'la data deberia estar en sect 3 por tanto 0'
            selected = 0  # len(bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs)-1
            minmap = self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs[selected]
            f_name = self.bitmap.in_game_path.split('\\')[-1]
            print(f"======== {f_name} ===========")
            print(f"======== {self.bitmap_ti['Usage'].value} ===========")
            print(f"======== {self.bitmap_ti['UsageId'].value} ===========")
            print(f"======== {self.bitmap_ti['texture group'].str_value} ===========")
            for x in self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs:
                if x['mipmap index'].value == selected:
                    minmap = x
                print(f"desconocido short 0 - {x['desconocido short 0'].value}")
                print(f"desconocido short 1 - {x['desconocido short 1'].value}")
                print(f"data_size - {x['data_size'].value}")
                print(f"desconocido short 3 - {x['desconocido short 3'].value}")
                print(f"mipmap index - {x['mipmap index'].value}")
                print(f"desconocido byte    - {x['desconocido byte'].value}")
                print(f"width - {x['width'].value}")
                print(f"height - {x['height'].value}")
                print(f"===========================================================")

            if self.bitmaps_0['bitmap resource handle'].childs[0]['format'].value != \
                    map_select_format[self.bitmaps_0['format'].selected]:
                debug = True
            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = minmap['width'].value
            self.dds_file.header.height = minmap['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header.ddspf.flags = minmap['desconocido short 1'].value
            t_type = self.bitmaps_0['type'].selected_index
            t_type_str = self.bitmaps_0['type'].selected
            mipmap_count = self.bitmaps_0['mipmap count'].value
            # self.dds_file.header.mipMapCount = mipmap_count
            self.dds_file.bdata = self._getChunkData(minmap['data_size'].value)
            size = self.computeMipmapSize(map_select_format[self.bitmaps_0['format'].selected])

            DEBUG = True

    def loadArrayTexture(self):

        if self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childrenCount == 0:
            # assert bitmaps_0['mipmap count'].value == 0, f'El numero de mimap deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value != 0, f'debe tener la data embebida'
            assert self.bitmaps_0['bitmap resource handle'].childs[0]['embed_data_len'].value == \
                   len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data), f'la data deberia estar en sect 3 '

            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = self.bitmaps_0['width'].value
            self.dds_file.header.height = self.bitmaps_0['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header10 = None
            # self.dds_file.header10 = None
            self.dds_file.bdata = self.bitmap.tag_parse.full_header.file_header.section_3_bin_data
        else:
            assert self.bitmaps_0['mipmap count'].value != 0, f'El numero de mimap no deberia ser 0'
            assert self.bitmaps_0['bitmap resource handle'].childs[0][
                       'embed_data_len'].value == 0, f'No debe tener la data embebida'
            assert len(self.bitmap.tag_parse.full_header.file_header.section_3_bin_data) == 0 \
                , f'la data deberia estar en sect 3 por tanto 0'
            selected = 0  # len(bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs)-1
            minmap = self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs[selected]
            f_name = self.bitmap.in_game_path.split('\\')[-1]
            print(f"======== {f_name} ===========")
            print(f"======== {self.bitmap_ti['Usage'].value} ===========")
            print(f"======== {self.bitmap_ti['UsageId'].value} ===========")
            print(f"======== {self.bitmap_ti['texture group'].str_value} ===========")
            for x in self.bitmaps_0['bitmap resource handle'].childs[0]['mipmaps'].childs:
                if x['mipmap index'].value == selected:
                    minmap = x
                print(f"desconocido short 0 - {x['desconocido short 0'].value}")
                print(f"desconocido short 1 - {x['desconocido short 1'].value}")
                print(f"data_size - {x['data_size'].value}")
                print(f"desconocido short 3 - {x['desconocido short 3'].value}")
                print(f"mipmap index - {x['mipmap index'].value}")
                print(f"desconocido byte    - {x['desconocido byte'].value}")
                print(f"width - {x['width'].value}")
                print(f"height - {x['height'].value}")
                print(f"===========================================================")

            if self.bitmaps_0['bitmap resource handle'].childs[0]['format'].value != \
                    map_select_format[self.bitmaps_0['format'].selected]:
                debug = True
            self.dds_file.loadDefaultValues(map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.width = minmap['width'].value
            self.dds_file.header.height = minmap['height'].value
            self.dds_file.header.pitchOrLinearSize = self.computePitch(
                map_select_format[self.bitmaps_0['format'].selected])
            self.dds_file.header.depth = self.bitmaps_0['depth'].value
            # self.dds_file.header.ddspf.flags = minmap['desconocido short 1'].value
            t_type = self.bitmaps_0['type'].selected_index
            t_type_str = self.bitmaps_0['type'].selected
            mipmap_count = self.bitmaps_0['mipmap count'].value
            # self.dds_file.header.mipMapCount = mipmap_count
            self.dds_file.bdata = self._getChunkData(minmap['data_size'].value)
            size = self.computeMipmapSize(map_select_format[self.bitmaps_0['format'].selected])

            DEBUG = True
