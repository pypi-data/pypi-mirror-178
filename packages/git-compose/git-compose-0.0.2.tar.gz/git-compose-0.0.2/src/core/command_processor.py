import os
import yaml
import shutil
import logging
import src.git.repo as git_repo
import src.git.submodule as git_submodule
from src.model.service import Service
from src.task.task_handler import TaskHandler


class CommandProcessor:
    def __init__(self):
        self.logger = logging.getLogger("git-compose.processor")
        self.task_handler = TaskHandler()

    def init(self):
        if os.path.exists(".git-compose") or os.path.exists(".git"):
            raise Exception(
                "git-compose already initialized. Run git-compose rm first.")
        git_repo.init()
        self.logger.debug("Initialized git repo")
        os.mkdir(".git-compose")
        os.mkdir(".git-compose/repos")
        open(".git-compose/repos/.gitkeep", "w").close()
        self.logger.debug("Created .git-compose/repos/.gitkeep")
        git_repo.add(".git-compose/repos/.gitkeep")
        git_repo.commit("Initialize git-compose")
        self.logger.info("Initialized git-compose")

    def rm(self):
        def on_rmtree_error(func, path, exc_info):
            import stat
            os.chmod(path, stat.S_IWRITE)
            os.unlink(path)

        self.logger.info("Removing git-compose")
        if os.path.exists(".git-compose"):
            shutil.rmtree(".git-compose", onerror=on_rmtree_error)
        self.logger.info("Removing .git")
        if os.path.exists(".git"):
            shutil.rmtree(".git", onerror=on_rmtree_error)
        self.logger.info("Removing .gitmodules")
        if os.path.exists(".gitmodules"):
            os.remove(".gitmodules")

    def clone(
        self,
        compose_file: str = "git-compose.yml",
    ):
        with open(compose_file, "r") as f:
            compose = yaml.safe_load(f)
        services = [Service.from_dict(k, v)
                    for k, v in compose["services"].items()]
        for service in services:
            if not git_submodule.exists(service.url, service.name):
                self.logger.info(f"Adding submodule {service.name}")
                git_submodule.add(
                    service.url, f".git-compose/repos/{service.name}")
        git_repo.commit("Add submodules")

    def apply(
        self,
        task_file: str,
        compose_file: str = "git-compose.yml",
        commit_message: str = "git-compose apply",
        proceed_confirmation: bool = True
    ):
        with open(compose_file, "r") as f:
            compose = yaml.safe_load(f)
        services = [Service.from_dict(k, v)
                    for k, v in compose["services"].items()]
        self.clone(compose_file)
        for service in services:
            for branch in service.branches:
                original_work_dir = os.getcwd()
                shutil.copy(task_file, f".git-compose/repos/{service.name}")
                os.chdir(f".git-compose/repos/{service.name}")
                new_branch = branch.base is not None
                git_repo.checkout(branch.name, create=new_branch)
                if not new_branch:
                    git_repo.pull(branch.name)
                args = [x["value"] for x in branch.args]
                self.task_handler.run(task_file, args)
                os.remove(task_file)
                git_repo.add(".")
                git_repo.commit(f"git-compose apply {task_file}")
                git_repo.push(branch.name)
                os.chdir(original_work_dir)
                while proceed_confirmation:
                    response = input("Continue?[y/N] ")
                    if response.lower() in ["y", "yes"]:
                        break                      
        self.logger.info("Applied git-compose")
