import shlex
import subprocess

import click

import core


@click.group()
def main():
    pass


@main.command()
@click.argument('package')
@click.option('--upgrade', default=False)
@click.option('--save', is_flag=True, default=False)
@click.option('--save-dev', is_flag=True, default=False)
def install(package, upgrade, save, save_dev):
    packages = core.download_package(package)
    core.install_packages(packages)
    if save:
        core.save_package(packages, dev=False)
    if save_dev:
        core.save_package(packages, dev=True)
    return True


@main.command()
@click.option('--force', is_flag=True, default=False)
def init(force):
    core.init_pipfile(force=force)


if __name__ == "__main__":
    main()
