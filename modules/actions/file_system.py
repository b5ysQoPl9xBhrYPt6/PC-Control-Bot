import os
import shutil
from ..bot_settings import temp_dir_name

temp_path = os.path.join(os.getenv('TEMP'), temp_dir_name)

def create_file(file_path: str):
    with open(file_path, 'w') as file:
        file.write('')

def write_file(file_path: str, data: str):
    with open(file_path, 'w') as file:
        file.write(data)

def rename(file_path: str, new_file_path: str):
    try:
        os.rename(file_path, new_file_path)
        return True
    except Exception as e:
        print(e)
        return False

def remove_file(file_path: str):
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(e)
        return False

def remove_dir(dir: str):
    try:
        shutil.rmtree(dir)
        return True
    except Exception as e:
        print(e)
        return False

def create_dir(dir: str):
    try:
        os.makedirs(dir)
        return True
    except Exception as e:
        print(e)
        return False

def dir_list(path: str):
    try:
        return os.listdir(path)
    except Exception as e:
        print(e)
        return False

def get_file(file_path: str, file_name: str):
    try:
        shutil.copy2(file_path, os.path.join(temp_path, file_name))
        return True
    except Exception as e:
        print(e)
        return False
    