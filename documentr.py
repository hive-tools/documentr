import os
import fnmatch
import hashlib

from documentr.generator.template import Template
from argparse import ArgumentParser
from documentr.parser import HiveTableParser
from documentr.document import Document
from documentr.writer import Writer, TemplateWriter
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

    for root, dirnames, filenames in os.walk(args.path):
        for filename in fnmatch.filter(filenames, '*.sql'):
            file_list.append(os.path.join(root, filename))

    # First step is to create the metadata for a given directory
    for file_ in file_list:
        documentr = Document(engine_parser)

        with open(file_) as buffer_:
            sql_content = buffer_.read()
            table_data = documentr.create(sql_content)

            if table_data:
                documentr.write(Writer(args.docs_dest))
                print "File [{}] {} parsed".format(
                    hashlib.md5(sql_content).hexdigest(), file_
                )

        buffer_.close()

    # Second step is to generate the HTML documentation from the previous
    # metadata
    loader = Loader(args.docs_dest)
    schema = loader.load()

    template = Template(schema)
    content = template.generate()

    template_writer = TemplateWriter(args.docs_dest)
    template_writer.write(content)
