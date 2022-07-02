import utils

import os
import copy
import shutil


import json

from halo_infinite_tag_reader.config import Config

coating_data_path = Config.WEB_DOWNLOAD_DATA + 'seasson 2\\economy\\inventory_catalog.json'

root_path = Config.WEB_DOWNLOAD_DATA + 'seasson 2\\'
if __name__ == "__main__":

    f = open(coating_data_path)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    for item in data['Items']:

        file_name = (item['ItemPath'][item['ItemPath'].rfind('/')+1:])
        new_dir_path = root_path+(item['ItemPath'][0:item['ItemPath'].rfind('/')]).replace('/', '\\')
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path, exist_ok=True)
        #print(file_name)
        if not os.path.isfile(root_path+'\\'+'info_'+file_name):
            print(f"No file style {file_name}")
        else:
            if not os.path.isfile(new_dir_path+'\\'+'info_'+file_name):
                print(new_dir_path+'\\'+'info_'+file_name)
                shutil.copyfile(root_path+'\\'+'info_'+file_name, new_dir_path+'\\'+'info_'+file_name)
            else:
                f1 = open(new_dir_path+'\\'+'info_'+file_name)
                data1 = json.load(f1)
                media_path = data1['CommonData']['DisplayPath']['Media']['MediaUrl']['Path']
                media_dir_path = root_path +  media_path[0:media_path.rfind('/')].replace('/', '\\')
                if not os.path.exists(media_dir_path):
                    print(media_dir_path)
                    os.makedirs(media_dir_path, exist_ok=True)

                new_file_path = root_path + media_path.replace('/', '\\')
                old_file_path = root_path + 'Media\\' + media_path[media_path.rfind('/')+1:]
                if not os.path.isfile(old_file_path):
                    print(f'Dont exist {old_file_path}')
                else:
                    if not os.path.isfile(new_file_path):
                        print(f"No new media file  {new_file_path}")
                        shutil.copyfile(old_file_path,
                                        new_file_path)
                #print(media_path)
                f1.close()



    # Iterating through the json
    # list

    # Closing file
    f.close()