import re
from items import TableMetadata, Table, FieldType
from abc import ABCMeta, abstractmethod


class Parser:
    def __init__(self):
        pass

    __metaclass__ = ABCMeta

    @abstractmethod
    def parse_fields(self, sql):
        raise Exception("Method not implemented")

    @abstractmethod
    def parse_table(self, sql):
        raise Exception("Method not implemented")

    @abstractmethod
    def parse_table_metadata(self, sql):
        raise Exception("Method not implemented")


class HiveTableParser(Parser):
    NAME = "hive"
    FIELDS_REGEX = "([a-zA-Z_]+)\s+(" \
                   "STRING|BIGINT|INT|DOUBLE|BOOLEAN|TINYINT|tinyint|boolean" \
                   "|string|bigint" \
                   "|int|double)\s?(COMMENT\s)?(\".*\")?"
    TABLE_REGEX = "[EXISTS|TABLE|table|exists][\s]+([a-zA-Z0-9_`?]+\.[" \
                "a-z-A-Z0-9_`?]+)"
    TABLE_METADATA_REGEX = "@(author|description|version)\(\"([\w\s\d,\-\.\'_]+)\"\)"
    FIELD_METADATA = "@(reference|default|example)\(([\w\s\d,\-\.\'_]+)\)"

    def __init__(self):
        super(HiveTableParser, self).__init__()

        self.table = None
        self.fields = []
        self.table_metadata = None

    def parse_table(self, sql):
        items = re.findall(self.TABLE_REGEX, sql)
        if len(items) == 0:
            raise ValueError("No table or database found")

        items = items[0].split('.')

        self.table = Table(items[0], items[1])

        return self.table

    def parse_fields(self, sql):
        self.fields = []
        _fields = re.findall(self.FIELDS_REGEX, sql, re.MULTILINE)

        if not _fields:
            pass

        # Get from regular fields
        for field in _fields:
            if len(field) == 4:
                _metadata = None
                if field[3]:
                    _metadata = self.parse_field_metadata(field[3])
                self.fields.append(
                    FieldType(field[0], field[1], field[2], field[3], _metadata)
                )

        return self.fields

    def parse_table_metadata(self, sql):
        self.table_metadata = None

        items = re.findall(self.TABLE_METADATA_REGEX, sql)
        allowed_items = ['author', 'version', 'description']
        stored_items = {}

        for value in items:
            if value[0] in allowed_items:
                stored_items[value[0]] = value[1]

        self.table_metadata = TableMetadata(stored_items)

        return self.table_metadata

    def parse_field_metadata(self, comment):
        items = re.findall(self.FIELD_METADATA, comment)
        allowed_items = ['reference', 'default', 'example']
        stored_items = {}

        for value in items:
            if value[0] in allowed_items:
                data = value[1]
                if value[0] == 'reference':
                    reference_data = value[1].split('.')
                    data = {
                        "database": reference_data[0],
                        "table": reference_data[1],
                        "field": reference_data[2]
                    }
                stored_items[value[0]] = data

        return stored_items


class ParserFactory(object):
    @staticmethod
    def create_parser(engine=HiveTableParser.NAME):
        if engine == HiveTableParser.NAME:
            return HiveTableParser()
