import os
import subprocess

from configs.config import Config


class ExportImgNConvertImpl:
    def __init__(self, p_bitmap_export):
        self.bitmap_export = p_bitmap_export

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
        if output_path == '':
            output_path = os.path.splitext(input_image_path)[0] + f".{ext}"
        path_to_nconvert = os.path.join(Config.ROOT_DIR, 'tools','NConvert', 'nconvert.exe')

        subprocess.call(f'"{path_to_nconvert}"  -o "{output_path}" -out tga "{input_image_path}"',shell=True)
        debug = True

    def call(*popenargs, timeout=None, **kwargs):
        """Run command with arguments.  Wait for command to complete or
        timeout, then return the returncode attribute.

        The arguments are the same as for the Popen constructor.  Example:

        retcode = call(["ls", "-l"])
        """
        with subprocess.Popen(*popenargs, **kwargs) as p:
            try:
                return p.wait(timeout=timeout)
            except:
                p.kill()
                p.wait()
                raise