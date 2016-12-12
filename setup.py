from setuptools import setup
from setuptools import find_packages


NAME = "hive-docu"
VERSION = "1.0.0"

REQUIRES = [
            'pyparsing',
            ]
setup(
    name=NAME,
    version=VERSION,
    description="Hive Documentor",
    author_email="introduccio@gmail.com",
    keywords=["hive", "documentation"],
    install_requires=REQUIRES,
    tests_require=[],
    packages=find_packages()
)