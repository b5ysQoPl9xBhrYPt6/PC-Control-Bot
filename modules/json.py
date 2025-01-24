import json, os

def read(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def write(file_path: str, object: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(object, file, indent=4, ensure_ascii=False)
