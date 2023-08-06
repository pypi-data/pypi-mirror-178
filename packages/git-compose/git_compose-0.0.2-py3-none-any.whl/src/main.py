import typer
import logging
from src.core.command_processor import CommandProcessor

logging.basicConfig(level=logging.NOTSET)

app = typer.Typer()
processor = CommandProcessor()


@app.command()
def init():
    processor.init()


@app.command()
def rm():
    processor.rm()


@app.command()
def clone(
    compose_file: str = "git-compose.yml"
):
    processor.clone()


@app.command()
def apply(
    task_file: str,
    compose_file: str = "git-compose.yml",
    commit_message: str = "git-compose apply",
    proceed_confirmation: bool = True
):
    processor.apply(task_file, compose_file, commit_message, proceed_confirmation)


def main():
    app()


if __name__ == "__main__":
    main()
