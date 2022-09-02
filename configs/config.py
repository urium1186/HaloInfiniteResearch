import os


class Config:
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

    BASE_UNPACKED_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\"
    BASE_UNPACKED_PATH_CAMPAIGN = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\campaign\\"
    #BASE_UNPACKED_PATH = BASE_UNPACKED_PATH_CAMPAIGN
    MODEL_EXPORT_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\Converted\\RE_OtherGames\\HI\\models\\"
    INFOS_PATH = 'C:\\Users\\Jorge\\Downloads\\Mover\\infos\\'
    EXPORT_JSON = 'J:\\Games\\Halo Infinite Stuf\\Extracted\\HI\\json\\'
    SPARTAN_STYLE_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\"
    WEB_DOWNLOAD_DATA = "J:\\Games\\Halo Infinite Stuf\\Web-Json\\"
    UE5_PROJECT_IMPORTED_PC_PATH = "H:\\UE4\\Unreal_Projects\\HaloInfinities " \
                                   "5.0\\Content\\__chore\\gen__\\pc__\\"

    EXPORTED_TEXTURE_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\Converted\\Textures\\TGA\\pc__\\"
    EXPORTED_TEXTURE_PATH_BASE = "J:\\Games\\Halo Infinite Stuf\\Extracted\\Converted\\Textures\\"
