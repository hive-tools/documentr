import json
import fnmatch
import os

from collections import defaultdict


class Loader(object):
    def __init__(self, base_path):
        self.__base_path = base_path

        if not os.path.exists(self.__base_path):
            raise ValueError(
                "Base path {} do not exists".format(self.__base_path)
            )

    def load(self):
        files = self._list_files()

        if not files:
            return []

        schema = {}
        authors_stats = defaultdict(int)

        for _file in files:
            with open(_file, 'r') as _f:
                json_payload = json.loads(_f.read())
                if json_payload['database'] not in schema:
                    schema[json_payload['database']] = []

                json_payload['metadata']['has_docs'] = self._has_docs(json_payload)
                schema[json_payload['database']] += [json_payload]

                # register some author stats
                author = json_payload['metadata']['author']

                if author:
                    authors_stats[author] += 1

        return schema, authors_stats

    def _has_docs(self, table_schema):
        if not table_schema['metadata']['author'] and \
                not table_schema['metadata']['description']:
            return False

        return True

    def _list_files(self):
        file_list = []

        for root, dirnames, filenames in os.walk(self.__base_path):
            for filename in fnmatch.filter(filenames, '*.json'):
                file_list.append(os.path.join(root, filename))

        return file_list
