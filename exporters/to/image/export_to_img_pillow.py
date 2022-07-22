import os
from io import BytesIO

from PIL import Image
from PIL.DdsImagePlugin import DdsImageFile
from sympy import re

from commons.debug_utils import normal_artifact_files, fillDebugDict
from configs.config import Config


def getBatNormal(sorted_pixels, total_pixel, tolerance):
    count = 0
    if len(sorted_pixels) > 10:
        for i in range(5):
            if sorted_pixels[i][1] < 20:
                count += sorted_pixels[i][0]
            if sorted_pixels[-i][1] > 235:
                count += sorted_pixels[-i][0]

    if total_pixel == 0:
        return True
    count_porcet = count / total_pixel * 100
    if count_porcet > tolerance:
        return True
    else:
        return False

    # list1 to demonstrate the use of sorting


class ExportImgPillowImpl:
    def __init__(self, p_bitmap_export):
        self.hasArtifact = False
        self.bitmap_export = p_bitmap_export

    def loadDds(self):
        # newDds = DdsImageFile()
        pass

    def dds_to_png(data, box=None, rotate=0):
        with BytesIO(data) as io_dds:
            map_image = DdsImageFile(io_dds)
            if box is not None:
                map_image = map_image.crop(box)

            if rotate == 1:
                map_image = map_image.transpose(Image.ROTATE_90)

            with BytesIO() as io_png:
                map_image.save(io_png, 'png')
                # data_png = IOHelper.read_range(io_png)

    def putBTo1(self, img):
        img = img.convert("RGBA")
        R, G, B, A = img.split()
        B.paste(255, [0, 0, B.size[0], B.size[1]])
        self.hasArtifact = False
        if self.detectArtifactInNormalMap(G):
            print(f'Normal Artifact {self.bitmap_export.bitmap.in_game_path}')
            self.hasArtifact = True
            fillDebugDict(self.bitmap_export.bitmap.in_game_path, self.bitmap_export.bitmap.full_filepath,
                          normal_artifact_files)
        newImg = Image.merge("RGBA", [R, G, B, A])
        return newImg

    def generateFlatNormal(self, img):
        img = img.convert("RGBA")
        R, G, B, A = img.split()
        B.paste(255, [0, 0, B.size[0], B.size[1]])
        G.paste(127, [0, 0, B.size[0], B.size[1]])
        R.paste(127, [0, 0, B.size[0], B.size[1]])
        newImg = Image.merge("RGBA", [R, G, B, A])
        return newImg

    def upScale(self, img, w, h):
        # PIL.Image.Resampling.NEAREST,
        newImgUp = img.resize((w, h), resample=Image.NEAREST)
        return newImgUp

    def sortSecond(self, val):
        return val[1]

    def detectArtifactInNormalMap(self, chanel):
        debug = True
        colors = chanel.getcolors()
        s_colors = sorted(colors, reverse=True)
        pixel_x = chanel.getpixel((15, 15))
        colors.sort(key=self.sortSecond)
        return getBatNormal(colors, chanel.width * chanel.height, 6)

        """
        print(colors)

        # sorts the array in descending according to
        # second element
        colors.sort(key=self.sortSecond, reverse=True)

        print(colors)
        """
        debug = True

    def saveToExtToConfig(self, ext='tga', is_normal_map=False, up_scale=False, w=-1, h=-1, flatten_normal=False):
        input_path = Config.EXPORTED_TEXTURE_PATH_BASE + 'DDS\\' + self.bitmap_export.bitmap.in_game_path.replace(
            '.bitmap',
            '.dds')
        output_path = Config.EXPORTED_TEXTURE_PATH_BASE + f'{ext.upper()}\\' + self.bitmap_export.bitmap.in_game_path.replace(
            '.bitmap', f'.{ext}')
        path_to_create = os.path.dirname(output_path)
        os.makedirs(f"{path_to_create}", exist_ok=True)
        self.saveToExt(input_path, output_path, ext, is_normal_map, up_scale, w, h, flatten_normal)

    def saveToExt(self, input_image_path, output_path="", ext='tga', is_normal_map=False, up_scale=False, w=-1, h=-1, flatten_normal=False):
        try:
            img = Image.open(input_image_path)
            if output_path == '':
                output_path = os.path.splitext(input_image_path)[0] + f".{ext}"
            if is_normal_map:
                img = self.putBTo1(img)
            if up_scale:
                img = self.upScale(img, w, h)
            if flatten_normal:
                img = self.generateFlatNormal(img)
            img.save(output_path)

        except Exception as error:
            raise error
            pass
