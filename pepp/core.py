from collections import namedtuple
import logging
import os
from pip import _internal as pipi
import pipfile as pf
import re
import shlex
import subprocess
import sys
import tempfile

from blindspin import spinner
import toml

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ZipFile = namedtuple("ZipFile", "package_name filename hash")

INSTALLER = pipi.commands.InstallCommand()
INSTALLER_OPTIONS = INSTALLER.parse_args([])[0]

DOWNLOADER = pipi.commands.DownloadCommand()
DOWNLOADER_OPTIONS = DOWNLOADER.parse_args([])[0]

SESSION = pipi.download.PipSession()


def create_configuration_file(force: bool = False):
    if os.path.exists("pepp.ini") and not force:
        raise RuntimeError('Configuration file "pepp.ini" already exists')


def init_pipfile(force: bool = False):
    if os.path.exists("Pipfile") and not force:
        raise RuntimeError("Pipfile already exists")

    python_version = "{0}.{1}".format(sys.version_info.major, sys.version_info.minor)

    default = {
        "source": [
            {
                "url": "https://pypi.python.org/simple",
                "verify_ssl": True,
                "name": "pypi",
            }
        ],
        "requires": {"python_version": python_version},
        "packages": {},
        "dev-packages": {},
    }

    try:
        with open(os.path.join(os.path.curdir, "Pipfile"), "w") as f:
            toml.dump(default, f)
    except Exception as e:
        print(e)
        print("could not create pipfile")
    return f.name


def read_pipfile(pipfile: str = None):
    if not pipfile:
        pipfile = pf.Pipfile.find()
    with open(pipfile, "r") as f:
        return toml.load(f)


def save_package(package_dict: dict, dev: bool = False):
    """Saves a package to packages or dev-packages."""
    pip_toml = read_pipfile()
    if dev:
        section = "dev-packages"
    else:
        section = "packages"

    try:
        deps = pip_toml.get(section)
    except KeyError:
        deps = {section: {}}

    for package in package_dict:
        deps.update({package_dict[package]["package_name"]: "*"})
    pip_toml[section].update(deps)

    with open(pf.Pipfile.find(), "w") as f:
        toml.dump(pip_toml, f)


def parse_stdout_from_pip_download(output: str):
    collecting_regex = re.compile(r"Collecting (?P<package_name>[a-zA-Z0-9-_]+)")
    package_names = re.findall(collecting_regex, output)
    saved_reg = re.compile(r"(?:Saved )[\.]{0,}([\//*]+.*)")
    package_filenames = re.findall(saved_reg, output)
    return list(zip(package_names, package_filenames))


def hash_package(package: str):
    package_hash = subprocess.run(
        shlex.split("pip hash {0}".format(package)),
        stdout=subprocess.PIPE,
        encoding="utf8",
    )

    # find the hash in stdout
    regex = re.compile(r"(--hash=.*)")
    return re.search(regex, package_hash.stdout).groups(0)[0]


def _pip_download(package_name: str = None, temp_dir: str = None):
    temp_dir = tempfile.mkdtemp()
    return DOWNLOADER.run(DOWNLOADER_OPTIONS, package_name)


def download_package(package_name: str, option: dict = None):
    # create a temp dir to hold files
    package_dict = {}  # gonna hold our info to write to pipfile
    package = INSTALLER.run(INSTALLER_OPTIONS, [package_name])

    package_reqs = package.requirements.keys()

    try:
        import ipdb

        ipdb.set_trace()
    except ImportError:
        import pdb

        pdb.set_trace()

    for (package_name, package_path) in package_reqs:
        try:
            w = pipi.wheel.Wheel(package_path)
            w.hash = hash_package(w.filename)
            w.package_name = package_name
        except pipi.wheel.InvalidWheelFilename:
            w = ZipFile(package_name, package_path, hash_package(package_path))

        package_dict.update(
            {
                package_name: {
                    "package_name": package_name, "filename": w.filename, "hash": w.hash
                }
            }
        )
    return package_dict


def install_packages(packages: list):
    for package in packages:
        fname = packages[package]["filename"]
        fhash = packages[package]["hash"]
        cmd = "pip install {0}".format(fname)


if __name__ == "__main__":
    download_package("attrs")
