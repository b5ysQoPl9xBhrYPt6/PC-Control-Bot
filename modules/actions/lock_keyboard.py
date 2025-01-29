from keyboard import block_key, unblock_key

IS_KEYBOARD_LOCKED = False

def lock_keyboard():
    global IS_KEYBOARD_LOCKED
    if IS_KEYBOARD_LOCKED:
        for i in range(150):
            unblock_key(i)
        IS_KEYBOARD_LOCKED = False
    else:
        for i in range(150):
            block_key(i)
        IS_KEYBOARD_LOCKED = True
    return IS_KEYBOARD_LOCKED
