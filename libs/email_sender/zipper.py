# -*- coding: utf-8 -*-

import os
import zipfile


def zip_dir(dir_path, file_path):
    zf = zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED)
    for file_name in os.listdir(dir_path):
        dir_name = dir_path.replace(dir_path, '')
        if file_name.startswith('.'):
            continue
        zf.write(os.path.join(dir_path, file_name), os.path.join(dir_name, file_name))
        print('Compressing ' + file_name)
    zf.close()
    print('Finish')
