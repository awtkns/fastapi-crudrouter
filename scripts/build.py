import os
import pathlib

from distutils.core import run_setup

build_dir = pathlib.Path(__file__).parent.parent

if __name__ == '__main__':
    os.chdir(build_dir)
    run_setup('setup.py', script_args=['sdist', 'bdist'])

