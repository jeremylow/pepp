import optparse
import subprocess
import shlex
import sys
import traceback

import pip
from pip.index import FormatControl


installer = pip.commands.InstallCommand()
install_args = installer.parse_args(['--quiet'])[0]

if __name__ == "__main__":
    try:
        import attr; print(attr.__version__)
    except ImportError:
        print('attr not installed')
    ret = installer.run(install_args, ['python-twitter'])
    try: import ipdb; ipdb.set_trace()
    except ImportError: import pdb; pdb.set_trace()
    import attr
    print(attr.__version__)
