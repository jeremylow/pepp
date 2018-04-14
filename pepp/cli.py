#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Jeremy Low
from __future__ import absolute_import
import os
from os.path import exists, join
import shlex
import subprocess

import pipfile
import toml
import click

from pepp import core
from pepp import __version__ as pepp_version


@click.group()
@click.version_option(prog_name="pepp", version=pepp_version)
def main():
    pass


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("package")
@click.option("--save", is_flag=True, default=False)
@click.option("--save-dev", is_flag=True, default=False)
@click.argument("pip_args", nargs=-1, type=click.UNPROCESSED)
def install(package, save, save_dev, pip_args):
    packages = core.download_package(package)
    core.install_packages(packages)
    if save:
        core.save_package(packages, dev=False)
    if save_dev:
        core.save_package(packages, dev=True)
    return True


@main.command()
@click.option("--force", is_flag=True, default=False)
def init(force):
    core.init_pipfile(force=force)


@main.command()
def config():
    project_root = click.prompt(
        "Enter the root directory for your project", default=os.path.curdir
    )
    create_pipfile = click.prompt(
        "Would you like to create a default Pipfile now?", default=True
    )

    if create_pipfile:
        if exists(join(project_root, "Pipfile")):
            overwrite = click.prompt(
                "Pipfile found. Would you like to overwrite?", default=False
            )
            if overwrite:
                click.echo("Overwriting and creating Pipfile")
                core.init_pipfile(force=True)
            else:
                click.echo("Aborting creation of Pipfile")

    if exists(join(project_root, "pepp.ini")):
        overwrite = click.prompt("Configuration file exists. Overwrite?", default=False)
        if not overwrite:
            click.echo("Aborting creation of configuration file.")
            return -1

        click.echo("Overwriting configuration file.")

    with open(join(project_root, "pepp.ini"), "w") as f:
        dikt = {"project-root": project_root, "pipfile": join(project_root, "Pipfile")}
        toml.dump(dikt, f)


if __name__ == "__main__":
    main()
