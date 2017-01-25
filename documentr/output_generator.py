import os

from loader import Loader
from documentr.generator.template import Template
from documentr.generator.graphs import GraphGenerator
from documentr.writer import TemplateWriter


class OutputGeneratorFactory(object):
    @staticmethod
    def create_output_generator(name, schema, **kwargs):
        template_name = kwargs.get("template")
        output_path = kwargs.get("output_path")

        if name == "web":
            author_stats = kwargs.get("author_stats")
            template = Template(schema, template_name, author_stats=author_stats)
            content = template.generate()

            template_writer = TemplateWriter(output_path)
            template_writer.write(content)
        elif name == "graphs":
            generator = GraphGenerator(schema, output_path)
            generator.generate()


class OutputGenerator(object):
    def __init__(self, input_path, output_path):
        self.output_path = output_path
        self.input_path = input_path

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def generate(self, engine="web", **kwargs):
        with_graphs = kwargs.get("with_graphs")

        loader = Loader(self.input_path)
        schema, author_stats = loader.load()

        OutputGeneratorFactory.create_output_generator(
            engine, schema, author_stats=author_stats, template="default",
            output_path=self.output_path
        )

        if with_graphs:
            OutputGeneratorFactory.create_output_generator(
                "graphs", schema, output_path=self.output_path
            )
