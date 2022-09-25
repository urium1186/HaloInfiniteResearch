import os

from configs.config import Config
from exporters.base_exporter import BaseExporter
from exporters.to.image.dds_utilts.bitmap_2_dds import BitmapToDds, MipmapIndexException
from exporters.to.image.export_to_img_nconvert import ExportImgNConvertImpl
from exporters.to.image.export_to_img_pillow import ExportImgPillowImpl
from exporters.to.image.export_to_img_wand import ExportImgWandImpl
from tag_reader.readers.bitmap import Bitmap


class BitmapExporter(BaseExporter):
    def __init__(self, p_bitmap: Bitmap, type: str = 'tga'):
        super(BitmapExporter, self).__init__()
        self.dds_to_export = None
        self.bitmap = p_bitmap

    def loadRawDataFRomChunk(self, index):
        pass

    def saveDdsFile(self, to_config=True, mipmap_index = 0):
        self.dds_to_export = BitmapToDds(self.bitmap, mipmap_index)
        full_save_path = self.bitmap.full_filepath
        if to_config:
            full_save_path = Config.EXPORTED_TEXTURE_PATH_BASE +'DDS\\'+ self.bitmap.in_game_path

        full_save_path = os.path.splitext(full_save_path)[0] + f".dds"
        path_to_create = os.path.dirname(full_save_path)
        os.makedirs(f"{path_to_create}", exist_ok=True)
        with open(full_save_path, 'wb') as b:
            b.write(self.dds_to_export.dds_file.getBinaryData())



    def export(self):
        super(BitmapExporter, self).export()
        self.saveDdsFile()
        img_exporter_pill = ExportImgPillowImpl(self)
        img_exporter_wand = ExportImgWandImpl(self)

        img_path = 'J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_01\\hum_base_fabric_oriental_pattern_01_normal{pc}.dds'
        #img_path = full_save_path
        # img_exporter.vignette('C:\\Users\\Jorge\\Pictures\\Core-mix-2022-04-23_220744.png', 'C:\\Users\\Jorge\\Pictures\\Core-mix.png')
        try:
            if self.bitmap.isNormalMapUsage():
                try:
                    ka = 0
                    img_exporter_pill.saveToExtToConfig(ext='tga', is_normal_map=True)
                    try:
                        w = self.dds_to_export.dds_file.header.width
                        h = self.dds_to_export.dds_file.header.height
                        while img_exporter_pill.hasArtifact:
                            ka += 1
                            self.saveDdsFile(mipmap_index=ka)
                            img_exporter_pill.saveToExtToConfig(ext='tga', is_normal_map=True, up_scale=True,w=w,h=h)
                    except MipmapIndexException:
                        self.saveDdsFile(mipmap_index=ka-1)
                        w = self.dds_to_export.dds_file.header.width
                        h = self.dds_to_export.dds_file.header.height
                        img_exporter_pill.saveToExtToConfig(ext='tga', is_normal_map=True, up_scale=True, w=w, h=h, flatten_normal=True)
                        pass
                except Exception as error1:
                    debug = True
                    img_exporter_wand.saveToExtToConfig(ext='tga')
            else:
                try:
                    img_exporter_wand.saveToExtToConfig(ext='tga')
                except Exception as error1:
                    debug = True
                    img_exporter_pill.saveToExtToConfig(ext='tga')

        except Exception as error:
            debug = True
            img_exporter_nconvert = ExportImgNConvertImpl(self)
            img_exporter_nconvert.saveToExtToConfig(ext='tga')
