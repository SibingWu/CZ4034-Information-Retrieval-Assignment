import json


def save_json(file_path, file_content, ensure_ascii=False, indent=4, sort_keys=False):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(file_content, file, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys)
