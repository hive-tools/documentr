import os
import pydot


class GraphGenerator(object):
    def __init__(self, schema, output_path):
        self.__output_path = output_path
        self.__schema = schema

    def generate(self):
        if not self.__schema:
            return None

        for database in self.__schema:
            for table in self.__schema[database]:
                graph = pydot.Dot(graph_type='digraph')
                main_node_name = "{}.{}".format(database, table['table'])
                graph.add_node(
                    pydot.Node(main_node_name, style="filled",
                               fillcolor="#CCCCCC")
                )

                for field in table['fields']:
                    if not field['metadata']:
                        continue

                    if 'reference' not in field['metadata']:
                        continue

                    related_table = "{}.{}".format(
                        field['metadata']['reference']['database'],
                        field['metadata']['reference']['table']
                    )

                    graph.add_node(
                        pydot.Node(related_table, style="filled",
                                   fillcolor="#FFFFFF")
                    )

                    # add relationship
                    relationship = "{} -> {}".format(
                        field['name'],
                        field['metadata']['reference']['field']
                    )

                    graph.add_edge(
                        pydot.Edge(
                            main_node_name, related_table, label=relationship
                        )
                    )

                    full_path = os.path.join(
                        self.__output_path, 'graph_img'
                    )

                    if not os.path.exists(full_path):
                        os.makedirs(full_path)

                    final_path = os.path.join(
                        full_path, '{}.png'.format(main_node_name)
                    )

                    graph.write_png(final_path)

                graph = None
