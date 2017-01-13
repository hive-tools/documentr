import json
import os


class Writer(object):
    def __init__(self, path):
        self.__path = path

        if not os.path.exists(self.__path):
            raise ValueError("Path {} does not exists".format(self.__path))

    def write(self, document):
        json_output = json.dumps(document)

        file_name = "{}.{}.json".format(
            document["database"],
            document["table"]
        )

        full_path = os.path.join(
            self.__path, file_name
        )

        with open(full_path, 'w+') as _file:
            _file.write(json_output)