from win32api import MessageBox  # type: ignore
from win32con import MB_ICONINFORMATION, MB_TOPMOST  # type: ignore
from threading import Thread

def show_message(text: str | bool):
    MessageBox(0, str(text), ' ', MB_TOPMOST | MB_ICONINFORMATION)

def thread_message(text: str | bool):
    proc = Thread(target=lambda: show_message(str(text)))
    proc.start()
