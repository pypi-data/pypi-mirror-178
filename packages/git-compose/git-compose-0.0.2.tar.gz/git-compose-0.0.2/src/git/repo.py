import os


def init():
    os.system("git init")


def add(*files: str):
    files = [f'"{x}"' for x in files]
    files = ' '.join(files)
    os.system(f"git add {files}")


def commit(message: str):
    os.system(f'git commit -m "{message}"')


def checkout(branch: str, create: bool = False):
    options = "-b" if create else ""
    os.system(f"git checkout {options} {branch}")


def pull(branch: str):
    os.system(f"git pull origin {branch}")


def push(branch: str = "", new_branch: bool = False):
    options = "-u" if new_branch else ""
    os.system(f"git push {options} origin {branch}")
