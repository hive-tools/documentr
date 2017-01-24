from loader import Loader
from documentr.generator.template import Template
from documentr.writer import TemplateWriter


class OutputGeneratorFactory(object):
    @staticmethod
    def create_output_generator(name, schema, **kwargs):
        if name == "web":
            template_name = kwargs.get("template")
            output_path = kwargs.get("output_path")
            author_stats = kwargs.get("author_stats")

            template = Template(schema, template_name, author_stats=author_stats)
            content = template.generate()

            template_writer = TemplateWriter(output_path)
            template_writer.write(content)


class OutputGenerator(object):
    def __init__(self, input_path, output_path):
        self.output_path = output_path
        self.input_path = input_path

    def generate(self, engine="web"):
        loader = Loader(self.input_path)
        schema, author_stats = loader.load()

        OutputGeneratorFactory.create_output_generator(
            engine, schema, author_stats=author_stats, template="default",
            output_path=self.output_path
        )
