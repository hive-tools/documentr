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

    arg_parser.add_argument('--metadata-destination', dest='metadata_dest',
                            required='True', help='Define where the metadata '
                                                  'and documentation are '
                                                  'going to be stored')

    arg_parser.add_argument('--docs-output', dest="docs_output",
                            required="True", help="Define where to store the "
                                                  "final docs")

    arg_parser.add_argument('--template', dest='template', required='False',
                            default='default', help='Define which template '
                                                    'you want to use to '
                                                    'generate the documentation')

    arg_parser.add_argument('--with-graphs', dest='with_graphs',
                            required='False', default=False, help="If this "
                                                                  "value is "
                                                                  "True it "
                                                                  "will "
                                                                  "generate "
                                                                  "graph image for each table")

    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_input_arguments()

    metadata_generator = MetadataGenerator(
        args.path, args.metadata_dest
    )

    metadata_generator.generate(args.engine)

    # Second step is to generate the HTML documentation from the previous
    # metadata
    output_generator = OutputGenerator(args.metadata_dest, args.docs_output)
    output_generator.generate("web", with_graphs=args.with_graphs)
