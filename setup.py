import re
import sys
from pathlib import Path

from setuptools import find_packages, setup

here = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


def read_reqs( reqs_path: Path):
    return re.findall(r'(^[^#-][\w]+[-~>=<.\w]+)', reqs_path.read_text(), re.MULTILINE)


#-----------------------------------------------------------------
install_requirements = read_reqs( here / "requirements.txt" )
test_requirements = []

setup(
    name='photo-scripts',
    version="0.1.0",
    packages=find_packages(where='src'),
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    package_data={
        '': [
            ]
    },
    entry_points={
        #'console_scripts': [
        #    'photo-scripts=photo_scripts.__main__:main', ]
        },
    python_requires='>=3.6',
    install_requires=install_requirements,
    tests_require=test_requirements
)
