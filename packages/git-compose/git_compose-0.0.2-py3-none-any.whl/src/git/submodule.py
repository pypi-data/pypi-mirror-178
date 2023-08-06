import os


def exists(url: str, path: str):
    if not os.path.exists(".gitmodules"):
        return False
    with open(".gitmodules", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)-1):
            if path in lines[i] and url in lines[i + 1]:
                return True
            if url in lines[i] and path in lines[i + 1]:
                return True
    return False


def add(url: str, path: str):
    os.system(f"git submodule add {url} {path}")
