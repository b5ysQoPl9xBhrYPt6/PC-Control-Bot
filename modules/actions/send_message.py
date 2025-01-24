from win32api import MessageBox  # type: ignore
from win32con import MB_ICONINFORMATION, MB_TOPMOST  # type: ignore
from threading import Thread

def show_message(text):
    MessageBox(0, text, ' ', MB_TOPMOST | MB_ICONINFORMATION)

def thread_message(text):
    proc = Thread(target=lambda: show_message(text))
    proc.start()
