import os
import subprocess

def create_git(work_dir):
    subprocess.call(
        ["git", "init"],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, "w"),
        cwd=work_dir
    )

