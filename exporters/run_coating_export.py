import codecs
import json
import pathlib

from configs.config import Config

from halo_infinite_tag_reader.readers.reader_factory import ReaderFactory
from halo_infinite_tag_reader.varnames import map_alt_name_id

if __name__ == "__main__":
    print('comienzo')
    dict_core = {
        'iron_eagle_spartan_style{ct}': "eag",
        'lone_wolves_spartan_style{ct}': "wlv",
        'mc117_spartan_style{ct}': "mc117",
        'olympus_spartan_style{ct}': "olympus",
        'reach_spartan_style{ct}': "reach",
        'samurai_spartan_style{ct}': "samurai"

    }
    for path in pathlib.Path(Config.SPARTAN_STYLE_PATH).rglob('*spartan_style{ct}.materialstyles'):
        # continue
        with open(path, 'rb') as f:
            filename = str(path).replace(Config.BASE_UNPACKED_PATH, '')

            parse_mwsy = ReaderFactory.create_reader(filename)
            parse_mwsy.load()
            ##print("------------------------" + dict_core[path.stem] + "------------------------")

            for i in range(parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childrenCount):
                temp_palette = parse_mwsy.tag_parse.rootTagInst.childs[0]['style'].childs[i]

                # #print(temp_palette['palette'].path)

                parse_mwsy.default_style = i
                parse_mwsy.toJson()
                coat_file_name = dict_core[path.stem] + '____' + parse_mwsy.json_base['name']
                #print('00000000:' + parse_mwsy.json_base['name'])
                if map_alt_name_id.keys().__contains__(coat_file_name):
                    coat_file_name = map_alt_name_id[coat_file_name]
                else:
                    depo = 1
                saveTo = Config.EXPORT_JSON + 'coating\\' + coat_file_name + '.json'
                with open(saveTo, 'wb') as fw:
                    json.dump(parse_mwsy.json_base, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
                    fw.close()

            f.close()
    # print("parse_mwsy")
    print("fin")
