import os
from wand.api import library
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

import binascii
import ctypes

# Map C-API to Python
# -------------------
# magick-image.h
# WandExport MagickBooleanType MagickImportImagePixels(MagickWand *wand,
#   const ssize_t x,const ssize_t y,const size_t columns,const size_t rows,
#   const char *map,const StorageType storage,const void *pixels)
from configs.config import Config

library.MagickImportImagePixels.argtypes = (ctypes.c_void_p,
                                            ctypes.c_ssize_t,
                                            ctypes.c_ssize_t,
                                            ctypes.c_size_t,
                                            ctypes.c_size_t,
                                            ctypes.c_char_p,
                                            ctypes.c_int,
                                            ctypes.c_void_p)

# Map enum StorageType
StorageType = ('undefined', 'char', 'double', 'float',
               'integer', 'long', 'quantum', 'short')


class MyImage(Image):
    def import_pixels(self, blob, pixel_format='RGBA', pixel_size='char'):
        storage_type = StorageType.index(pixel_size)
        library.MagickImportImagePixels(self.wand,
                                        0,
                                        0,
                                        self.width,
                                        self.height,
                                        pixel_format.encode(),
                                        storage_type,
                                        blob)


class ExportImgWandImpl:
    def __init__(self, p_bitmap_export):
        self.bitmap_export = p_bitmap_export

    def vignette(self, input_image_path, output_path):
        with Image(filename=input_image_path) as img:
            img.vignette(x=10, y=10)
            img.save(filename=output_path)

    def saveToExtToConfig(self, ext='tga'):
        input_path = Config.EXPORTED_TEXTURE_PATH_BASE + 'DDS\\' + self.bitmap_export.bitmap.in_game_path.replace(
            '.bitmap',
            '.dds')
        output_path = Config.EXPORTED_TEXTURE_PATH_BASE + f'{ext.upper()}\\' + self.bitmap_export.bitmap.in_game_path.replace(
            '.bitmap', f'.{ext}')
        path_to_create = os.path.dirname(output_path)
        os.makedirs(f"{path_to_create}", exist_ok=True)
        self.saveToExt(input_path, output_path, ext)

    def saveToExt(self, input_image_path, output_path="", ext='tga'):
        with Image(filename=input_image_path) as img:
            img.compression = "no"

            if output_path == '':
                output_path = os.path.splitext(input_image_path)[0] + f".{ext}"
            img.save(filename=output_path)

    def createImgDrawing(self):
        with Drawing() as ctx:
            colors = ["RED", "GREEN", "BLUE", "WHITE"]
            for index, color_name in enumerate(colors):
                ctx.push()  # Grow context stack
                ctx.fill_color = Color(color_name)  # Allocated color
                ctx.point(index % 2, index / 2)  # Draw pixel
                ctx.pop()  # Reduce context stack
            with Image(width=2, height=2, background=Color("NONE")) as img:
                ctx.draw(img)
                img.sample(100, 100)
                img.save(filename="output.png")

    def createImgRawData(self):
        # Usage
        raw_data_string = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3300005CFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFF9500B158DFFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFB200000003FFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFB100000002FFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFF643040B80FFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF3300002BFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3300002BFFED843913051B59D1FFFFFFFFFFFF03000184FFFF3300002BAB0F00000000000007BBFFFFFFFFFF03000057FFFF330000080100000000000000001DF8FFFFFFFF03000057FFFF330000000042A9D4D08D0D000000ADFFFFFFFF03000057FFFF330000059DFFFFFFFFFFAA00000070FFFFFFFF03000057FFFF3300002BFFFFFFFFFFFFFA05000051FFFFFFFF03000057FFFF3300002BFFFFFFFFFFFFFF18000045FFFFFFFF03000057FFFF3300002BFFFFFFFFFFFFFF1B000043FFFFFFFF03000057FFFF3300002BFFFFFFFFFFFFFF1B000043FFFFFFFF03000057FFFF3300002BFFFFFFFFFFFFFF1B000043FFFFFFFF03000057'
        raw_data_bytes = binascii.unhexlify(raw_data_string)

        with MyImage(width=25, height=25, background=Color('WHITE')) as img:
            img.import_pixels(raw_data_bytes, pixel_format='R', pixel_size='char')
            img.save(filename='output.png')
