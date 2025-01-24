# import pyautogui as pyi
import mss
import mss.tools
import os

def get_screenshot():
    try:
        temp_path = os.path.join(os.getenv('TEMP'), f'temp_direction')
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        with mss.mss() as sct:
            sct.shot(mon=-1, output=os.path.join(temp_path, 'screenshot.jpg'))
        return os.path.join(temp_path, 'screenshot.jpg')
    except Exception as e:
        print(e)

# print(get_screenshot())