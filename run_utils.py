import json
import pathlib
import re

from configs.config import Config
from tag_reader.headers.header import Header
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.var_names import getMmr3HashFrom, Mmr3Hash_str_iu, change_case, getMmr3HashFromInt

dict_str = {}


def createTagNamesInUseFormUnPath():
    path_root = Config.BASE_UNPACKED_PATH
    path_to_hash = Config.ROOT_DIR + '\\tag_reader\\tag_names\\tag_names_iu_generated.txt'
    path_to_hash_e = Config.ROOT_DIR + '\\tag_reader\\tag_names\\tag_names_iu_errors_generated.txt'
    with open(path_to_hash, 'w') as file:
        pass
    with open(path_to_hash_e, 'w') as file:
        pass
    for path in pathlib.Path(path_root).rglob('*{pc}.*'):
        x_s = str(path).replace(Config.BASE_UNPACKED_PATH, '')
        try:
            parse = ReaderFactory.create_reader(x_s)

            tag_inst = parse.readParameterByName('global tag ID')
            hash = getMmr3HashFromInt(tag_inst.value)
            value = x_s.replace("\\", "/")
            hash_str = f'{hash} : {value}'

            if hash_str != '':
                path_to_hash_w = path_to_hash
                if dict_str.keys().__contains__(hash):
                    exist_path = dict_str[hash]
                    path_to_hash_w = path_to_hash_e
                    hash_str=hash_str + f" {exist_path}"
                    pass
                with open(path_to_hash_w, 'a') as f:
                    try:
                        f.write(hash_str + '\n')
                    except UnicodeEncodeError:
                        pass
            dict_str[hash] = x_s
        except:
            pass

def createTempStringHashFormUnPath():
    path_root = Config.BASE_UNPACKED_PATH
    path_to_hash = Config.ROOT_DIR + '\\tag_reader\\hash\\web_generated.txt'
    with open(path_to_hash, 'w') as file:
        pass
    for path in pathlib.Path(path_root).rglob('*.stringlist'):
        x = str(path).replace(Config.BASE_UNPACKED_PATH, '')
        parse = ReaderFactory.create_reader(x)
        parse.load_recursive = True
        parse.load()
        for str_v in parse.first_child['language references'].childs[0]['string list resource'].childs[0][
            'string lookup info'].childs:
            x_1 = str_v['string id'].extra_data['str_'].replace(' ','')
            if x_1 != '':
                addStrValid(x_1)

def createTempStringHashFormStringList():
    path_root = Config.BASE_UNPACKED_PATH
    path_to_hash = Config.ROOT_DIR + '\\tag_reader\\hash\\web_generated.txt'
    with open(path_to_hash, 'w') as file:
        pass
    for path in pathlib.Path(path_root).rglob('*.*'):
        x = str(path).replace(Config.BASE_UNPACKED_PATH, '')
        addStrValid(x)


def createTempStringHashFormWebJson():
    web_json_path = Config.WEB_DOWNLOAD_DATA
    path_to_hash = Config.ROOT_DIR + '\\tag_reader\\hash\\web_generated.txt'
    with open(path_to_hash, 'w') as file:
        pass
    for path in pathlib.Path(web_json_path).rglob('*.json'):
        with open(path, 'rb') as f:
            try:
                data = json.load(f)
                capitalize(data)
            except:
                deb = True


def capitalize(x):
    if isinstance(x, list):
        for v in x:
            capitalize(v)
    elif isinstance(x, dict):
        for k, v in x.items():
            addStrValid(k)
            capitalize(v)
    else:
        addStrValid(x)


def isStrValid(x):
    try:
        float(x)
        return False
    except ValueError:
        x = str(x)
        if not bool(re.search(r'^[a-zA-Z0-9_]*$', x)):
            return False
        elif x.__contains__('\n'):
            return False
        elif x.__len__() > 100:
            return False
        elif x == '':
            return False
        elif x.isdigit():
            return False
        elif dict_str.keys().__contains__(x):
            return False
        elif list(Mmr3Hash_str_iu.values()).__contains__(x):
            return False
        else:
            return True


def canSplit(x: str):
    spliter_l = []
    if x.__contains__(':'):
        spliter_l.append(':')
    if x.__contains__('\\'):
        spliter_l.append('\\')
    if x.__contains__('/'):
        spliter_l.append('/')
    if x.__contains__('-'):
        spliter_l.append('-')
    if x.__contains__('.'):
        spliter_l.append('.')
    if x.__contains__('.json'):
        spliter_l.append('.json')
    return spliter_l


def splitStr(x, p_a):
    str_a = [x.replace('.', '_')]
    for sp in canSplit(x):
        str_a.extend(x.split(sp))
    if len(str_a) == 1:
        result = re.findall(r"{(.+?)}", str_a[0])
        if len(result)!=0:
            debug = True
        str_a_r = [re.sub(r"{(.+?)}", '', str_a[0])]
        return str_a_r
    else:
        temp_a = []
        temp_a.extend(str_a)
        for x_s in temp_a:
            if not p_a.__contains__(x_s):
                p_a.append(x_s)
                splitStr(x_s, p_a)
            """
            else:
                if len(canSplit(x_s))>0:
                    temp_a.extend(splitStr(x_s))
            """
        return p_a


def addStrValid(x):
    x_snake_case = change_case(x)
    temp_a_ini = []
    str_a = splitStr(x_snake_case, temp_a_ini)
    for x_s in str_a:
        if isStrValid(x_s):
            p_hash = getMmr3HashFrom(x_s)
            hash_str = f'{p_hash}:{x_s}'
            path_to_hash = Config.ROOT_DIR + '\\tag_reader\\hash\\web_generated.txt'
            if hash_str != '':
                with open(path_to_hash, 'a') as f:
                    try:
                        f.write(hash_str + '\n')
                    except UnicodeEncodeError:
                        pass
            dict_str[x_s] = ''

def recursiveReadTag(unique_path_dict: list, hast_tag_dict: dict, in_path: str):

    if unique_path_dict.__contains__(in_path):
        return
    else:
        file_header = Header()
        filename = Config.BASE_UNPACKED_PATH + in_path
        with open(filename, 'rb') as f:
            file_header.readHeader(f)
    pass

def searchTagNamesbyTagInPaths():
    pass

if __name__ == "__main__":
    # createTempStringHashFormWebJson()
    #createTempStringHashFormUnPath()
    createTagNamesInUseFormUnPath()
    # createTempStringHashFormUnPath()
    exit()
