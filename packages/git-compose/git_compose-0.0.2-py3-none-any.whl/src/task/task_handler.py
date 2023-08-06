import logging
import os
import shutil


class TaskHandler:
    def __init__(self):
        self.logger = logging.getLogger("git-compose.task")

    def run(self, task_file: str, arguments: list):
        task_file_name = os.path.basename(task_file)
        os.system(f"python {task_file_name} {' '.join(arguments)}")
