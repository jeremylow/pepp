import os

from pepp import core


def test_parse_stdout_from_pip_download():
    with open("tests/test_data/pip_output.txt", "r") as f:
        text = f.read()
    parsed_text = core.parse_stdout_from_pip_download(text)
    assert isinstance(parsed_text, list)
    for item in parsed_text:
        assert isinstance(item, tuple)
    assert parsed_text[0][0] == "ipython"


def test_create_pipfile():
    pipfile = core.init_pipfile(force=True)
    assert pipfile
    assert os.path.exists(pipfile)
    os.remove(pipfile)


def test_save_package():
    pipfile = core.init_pipfile(force=True)
    assert pipfile
    core.save_package({"test_package": {"package_name": "test_package"}})
    result = core.read_pipfile()
