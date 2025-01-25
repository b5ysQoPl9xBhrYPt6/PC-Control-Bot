import json, os

def read(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except Exception as e:
            print(e)
            return False
    
def write(file_path: str, object: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(object, file, indent=4, ensure_ascii=False)
