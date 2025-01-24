import pyautogui as pyi
from threading import Thread

pyi.PAUSE = 0.01
IS_CURSOR_LOCKED = False

def lock_cursor():
    global IS_CURSOR_LOCKED
    cursor_pos = pyi.position()
    while IS_CURSOR_LOCKED:
        pyi.moveTo(cursor_pos)
        # PAUSE

def thread_lock_cursor():
    global IS_CURSOR_LOCKED
    if IS_CURSOR_LOCKED:
        IS_CURSOR_LOCKED = False
    else:
        IS_CURSOR_LOCKED = True
        proc = Thread(target=lock_cursor, daemon=True)
        proc.start()
    return IS_CURSOR_LOCKED
