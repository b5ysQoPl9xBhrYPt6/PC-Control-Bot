import os
from ..bot_settings import temp_dir_name, processes_object_name
from .. import json
from time import sleep
import psutil
from threading import Thread

temp_path = os.path.join(os.getenv('TEMP'), temp_dir_name)
file_name = 'processes.json'
obj = {str(processes_object_name): []}
path = os.path.join(temp_path, file_name)
IS_TASKS_LOCKED = False

def return_locked_processes():
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if not os.path.exists(path):
        json.write(path, obj)

    if json.read(path) == {}:
        json.write(path, obj)

    return json.read(path)

def change_locked_tasks_data(task_name: str):
    if os.path.exists(path):
        task_list = json.read(path)[str(processes_object_name)]
        try:
            task_list.append(task_name)
            json.write(path, {str(processes_object_name): task_list})
            return True
        except Exception as e:
            print(e)
            return False
    else:
        return False


def lock_tasks():
    global IS_TASKS_LOCKED
    while IS_TASKS_LOCKED:
        try:
            for task in return_locked_processes()[str(processes_object_name)]:
                for proc in psutil.process_iter(['name', 'pid']):
                    if proc.info['name'] == task:
                        proc.terminate()
                        print(f'Terminated: {proc.info['name']}')
                        break
        except psutil.NoSuchProcess:
            print('No such process.')
        except psutil.AccessDenied as access_denied:
            print(f'Access denied to terminate task. Info: {access_denied}')
        sleep(0.7)

def thread_lock_tasks():
    global IS_TASKS_LOCKED
    if IS_TASKS_LOCKED:
        IS_TASKS_LOCKED = False
    else:
        IS_TASKS_LOCKED = True
        proc = Thread(target=lock_tasks, daemon=True)
        proc.start()
    return IS_TASKS_LOCKED
    