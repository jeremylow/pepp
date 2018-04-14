import os
import click

from pepp import cli

import toml
from click.testing import CliRunner


def test_cli_config():
    """test with a clean slate (no existing files)"""
    runner = CliRunner()
    if os.path.exists("pepp.ini"):
        os.remove("pepp.ini")
    result = runner.invoke(cli.config)
    assert result.output
    assert os.path.exists("pepp.ini")
    with open("pepp.ini") as f:
        pepp_toml = toml.load(f)
    assert pepp_toml["project-root"] == "."
    assert pepp_toml["pipfile"] == "./Pipfile"
    os.remove("pepp.ini")


def test_cli_init():
    """tests with a clean slate: no existing pipfile"""
    runner = CliRunner()
    if os.path.exists("Pipfile"):
        os.remove("Pipfile")
    result = runner.invoke(cli.init)
    assert os.path.exists("Pipfile")


def test_cli_init_existing_file():
    """test creation with existing pipfile"""
    runner = CliRunner()
    runner.invoke(cli.init)
    if not os.path.exists("Pipfile"):
        assert 0
    runner.invoke(cli.init, input="")
