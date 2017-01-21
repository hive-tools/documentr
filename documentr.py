from argparse import ArgumentParser
from documentr.metadata_generator import MetadataGenerator
from documentr.output_generator import OutputGenerator


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

    metadata_generator = MetadataGenerator(
        args.path, args.docs_dest
    )

    metadata_generator.generate(args.engine)

    # Second step is to generate the HTML documentation from the previous
    # metadata
    output_generator = OutputGenerator(args.docs_dest, args.docs_dest)
    output_generator.generate("web")
