import os
from jinja2 import Environment, FileSystemLoader


class Template(object):
    def __init__(self, schema, template="default"):
        self.__base_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../../',
            'resources/templates',
            template
        )

        self.__schema = schema
        self.__template = template

        self.__template = Environment(
            loader=FileSystemLoader(searchpath=self.__base_path)
        )

    def generate(self):
        template = self.__template.get_template("index.jinja")
        print template.render({"schema": self.__schema})
