import os
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements

NAME = "documentr"
VERSION = "1.0.0"

try:
    requirements = []
    if os.path.exists('requirements.txt'):
        install_reqs = parse_requirements('requirements.txt', session=False)
        requirements = [str(ir.req) for ir in install_reqs]
except OSError:
    requirements = []

test_requirements = [
    'pytest',
    'unittest2'
]

setup(
    name=NAME,
    version=VERSION,
    description="Documentor",
    author_email="introduccio@gmail.com",
    keywords=["hive", "documentation"],
    install_requires=requirements,
    tests_require=test_requirements,
    packages=find_packages(),
    tests_suite='tests',
)
