import os

from documentr.generator.template import Template
from argparse import ArgumentParser
from documentr.parser import HiveTableParser
from documentr.document import Document
from documentr.writer import Writer
from documentr.loader import Loader


def parse_input_arguments():
    arg_parser = ArgumentParser()

    arg_parser.add_argument('--path', dest='path',
                            required=True, help='Define where the SQL files '
                                                'are located')

    arg_parser.add_argument('--engine', dest='engine', default='hive',
                            required=False, help='Define which database '
                                                 'engine you are using in '
                                                 'those queries')

    arg_parser.add_argument('--doc-destination', dest='docs_dest',
                            required='True', help='Define where the metadata '
                                                  'and documentation are '
                                                  'going to be stored')

    arg_parser.add_argument('--template', dest='template', required='False',
                            default='default', help='Define which template '
                                                    'you want to use to '
                                                    'generate the documentation')

    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_input_arguments()

    engine_parser = None
    if args.engine.lower() == 'hive':
        engine_parser = HiveTableParser()

    # Get all files in the --path directory?
    file_list = []

    # First step is to create the metadata for a given directory
    documentr = Document(engine_parser)
    for _file in file_list:
        with open(_file) as sql_content:
            table_data = documentr.create(sql_content)
            documentr.write(Writer(args.docs_dest))

    # Second step is to generate the HTML documentation from the previous
    # metadata
    loader = Loader(args.docs_dest)
    schema = loader.load()

    template = Template(schema)
    template.generate()
