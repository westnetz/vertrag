import click
import os
import subprocess
import vertrag.cli

from vertrag.tests import create_git
from click.testing import CliRunner
from vertrag.cli import cli


def test_command_initialize(tmp_path):
    vertrag.cli.cwd = tmp_path
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["init"])
        assert result.exit_code == 0

def test_command_check(tmp_path):
    vertrag.cli.cwd = tmp_path
    runner = CliRunner()
    r_check_fail = runner.invoke(cli, ["check"])
    assert r_check_fail.exit_code == 1
    r_init = runner.invoke(cli, ["init"])
    assert r_init.exit_code == 0
    r_check_no_git = runner.invoke(cli, ["check"])
    assert r_check_no_git.exit_code == 1
    create_git(tmp_path)
    r_check_with_git = runner.invoke(cli, ["check"])
    assert r_check_with_git.exit_code == 0

