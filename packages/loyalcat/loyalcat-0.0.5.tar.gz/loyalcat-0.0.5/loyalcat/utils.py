from typing import Any


path = []
temp_path = ''


def parse_params(url: str) -> list[str]:
    params = []
    temp_path = ''
    for i in url:
        if (i == '/' and len(temp_path) > 0):
            path.append(temp_path)
            temp_path = ''
            
        if (i == ':') or len(temp_path) > 0:
            temp_path += i
    else:
        path.append(temp_path) if temp_path else None
    return params

def insert_params(path: str, params: dict[str, Any]) -> str:
    for k, v in params.items():
        path = path.replace(k, v)
    return path