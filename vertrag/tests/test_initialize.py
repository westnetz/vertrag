import os
import pytest
import subprocess

from vertrag.initialize import init_dir, check_dir, FILES, VertragCheckError
from vertrag.settings import DIRECTORIES
from vertrag.tests import create_git
from pathlib import Path


def test_init_dir(tmp_path):
    """
    Tests if the init command, creates all required directories, and copies all the files
    """
    init_dir(tmp_path)
    for d in DIRECTORIES:
        d_path = tmp_path / d
        assert d_path.is_dir()
    for d, fs in FILES.items():
        for f in fs:
            f_path = tmp_path / d / f
            assert f_path.is_file()

def test_check_dir_in_empty(tmp_path):
    with pytest.raises(VertragCheckError):
        check_dir(tmp_path)

def test_check_dir_after_init(tmp_path):
    init_dir(tmp_path)
    with pytest.raises(VertragCheckError):
        check_dir(tmp_path)

def test_check_dir_after_init_with_git(tmp_path):
    init_dir(tmp_path)
    create_git(tmp_path)
    assert check_dir(tmp_path) == None
