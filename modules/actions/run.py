import subprocess
import os

def is_exe(file_path: str):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in {'.exe'}

def run_file(file_path: str):
    try:
        if is_exe(file_path):
            subprocess.Popen([file_path], cwd=os.path.join(file_path, os.pardir))
            print('exe')
        else:
            os.startfile(file_path, cwd=os.path.join(file_path, os.pardir))
            print('other')
        return (True, None)
    except Exception as e:
        print(e)
        return (False, e)
