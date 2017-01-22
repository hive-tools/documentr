import re


class Cleaner(object):
    @staticmethod
    def clean_str(str):
        return str.replace('`', '')


class Table(object):
    def __init__(self, database, table):
        self.__database = Cleaner.clean_str(database)
        self.__table = Cleaner.clean_str(table)

    @property
    def database(self):
        return self.__database

    @property
    def table(self):
        return self.__table


class TableMetadata(object):
    def __init__(self, metadata):
        self.__author = metadata['author'] if 'author' in metadata else None
        self.__version = metadata['version'] if 'version' in metadata else None
        self.__description = metadata['description'] if 'description' in metadata else None

    @property
    def author(self):
        return self.__author

    @property
    def version(self):
        return self.__version

    @property
    def description(self):
        return self.__description


class FieldType(object):
    def __init__(self, name, field_type, has_comment, comment, field_metadata):
        self.__name = name
        self.__field_type = field_type
        self.__has_comment = has_comment
        self.__comment = comment
        self.__metadata = field_metadata

    @property
    def field_name(self):
        return self.__name.lower()

    @property
    def field_type(self):
        return self.__field_type.upper()

    @property
    def field_has_comment(self):
        if self.__has_comment.lower() == "comment":
            return True

        return False

    @property
    def field_comment(self):
        comment = re.sub(
            "@(reference|default)\(([\w\s\d,\-\.\'_]+)\)", "", self.__comment
        )

        comment = re.sub("\"", "", comment).strip()

        return comment

    @property
    def field_metadata(self):
        return self.__metadata

    def __eq__(self, other):
        _NOTFOUND = object()

        for attr in ['field_name', 'field_type', 'field_comment',
                     'field_metadata']:
            v1, v2 = [getattr(obj, attr, _NOTFOUND) for obj in [self, other]]
            if v1 is _NOTFOUND or v2 is _NOTFOUND:
                return False
            elif v1 != v2:
                return False

        return True
