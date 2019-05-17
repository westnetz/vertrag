import os
import os.path
import subprocess
import vertrag.settings

from pathlib import Path
from shutil import copy2

base_path = Path(__file__).resolve().parent

FILES = {
    vertrag.settings.ASSETS_DIR: ["contract.css", "logo.png"],
    vertrag.settings.TEMPLATES_DIR: ["contract_template.j2.html", "contract_mail_template.j2"],
}
CONFIG_FILENAME = "vertrag.config.yaml"

class VertragCheckError(Exception):
    pass

def init_dir(directory, without_samples=False):
    """
    Creates directories, copies templates and sample
    configuration to the given directory.
    """

    work_path = Path(directory)
    copy2(
        base_path.joinpath("templates", "sample.config.yaml"),
        work_path.joinpath(CONFIG_FILENAME),
    )

    for d in vertrag.settings.DIRECTORIES:
        full_dir = work_path.resolve().joinpath(d)
        if not full_dir.is_dir():
            full_dir.mkdir()

    for d, fs in FILES.items():
        for f in fs:
            copy2(
                base_path.joinpath(d, f),
                work_path.joinpath(d, f)
            )


def check_dir(directory):
    """
    Check if the tool was initialized properly in the current
    working directory.
    """

    error_messages = []

    for d in vertrag.settings.DIRECTORIES:
        if not Path(directory).joinpath(d).is_dir():
            error_messages.append("Missing directory: {}".format(d))

    if not Path(directory).joinpath(CONFIG_FILENAME).is_file():
        error_messages.append("Missing configuration file: {}".format(CONFIG_FILENAME))

    # Check if directory is tracked with git
    if (
        subprocess.call(
            ["git", "-C", directory, "status"],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, "w"),
        )
        != 0
    ):
        error_messages.append("⚠️ We recommend tracking this directory with git!")

    if len(error_messages):
        raise VertragCheckError("\n".join(error_messages))
    return
