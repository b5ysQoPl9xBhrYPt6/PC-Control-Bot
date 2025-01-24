import mss
import mss.tools
import os
from ..bot_settings import temp_dir_name

temp_path = os.path.join(os.getenv('TEMP'), temp_dir_name)
file_name = 'screenshot.jpg'

def get_screenshot():
    try:
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        with mss.mss() as sct:
            sct.shot(mon=-1, output=os.path.join(temp_path, file_name))
        return os.path.join(temp_path, file_name)
    except Exception as e:
        print(e)

def get_screenshot_path():
    path = os.path.join(temp_path, file_name)
    return path if os.path.exists(path) else False
