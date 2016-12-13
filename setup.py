from setuptools import setup
from setuptools import find_packages


NAME = "documentr"
VERSION = "1.0.0"

REQUIRES = [
            ]
setup(
    name=NAME,
    version=VERSION,
    description="Documentor",
    author_email="introduccio@gmail.com",
    keywords=["hive", "documentation"],
    install_requires=REQUIRES,
    tests_require=[],
    packages=find_packages()
)