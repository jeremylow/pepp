from pepp import core


def test_parse_stdout_from_pip_download():
    with open('tests/test_data/pip_output.txt', 'r') as f:
        text = f.read()
    parsed_text = core.parse_stdout_from_pip_download(text)
    assert isinstance(parsed_text, list)
    for item in parsed_text:
        assert isinstance(item, tuple)
    assert parsed_text[0][0] == 'ipython'


def test_something():
    pass
