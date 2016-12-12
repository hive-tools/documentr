import re
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


class Table(object):
    def __init__(self, database, table):
        self.__database = database
        self.__table = table

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
    def __init__(self, name, field_type, has_comment, comment):
        self.__name = name
        self.__field_type = field_type
        self.__has_comment = has_comment
        self.__comment = comment

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
        return self.__comment


class HiveTableParser(Parser):
    FIELDS_REGEX = "([a-zA-Z_]+)\s+(STRING|BIGINT|INT|DOUBLE|string|bigint|int|double)\s?(COMMENT\s)?(\".*\")?"
    TABLE_REGEX = "[EXISTS|TABLE|table|exists][\s]+([a-zA-Z0-9_`?]+\.[" \
                "a-z-A-Z0-9_`?]+)"
    TABLE_METADATA_REGEX = "@(author|description|version)\(\"([\w\s\d,\-\.\'_]+)\"\)"

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
        _fields = re.findall(self.FIELDS_REGEX, sql)

        if not _fields:
            pass

        # Get from regular fields
        for field in _fields:
            if len(field) == 4:
                self.fields.append(
                    FieldType(field[0], field[1], field[2], field[3])
                )

        return self.fields

    def parse_table_metadata(self, sql):
        items = re.findall(self.TABLE_METADATA_REGEX, sql)
        allowed_items = ['author', 'version', 'description']
        stored_items = {}

        for value in items:
            if value[0] in allowed_items:
                stored_items[value[0]] = value[1]

        self.table_metadata = TableMetadata(stored_items)

        return self.table_metadata

sql = """
/**
 * @author("Sergio Sola")
 * @email("ss@hellofresh.com")
 * @version("1.0.0")
 */
CREATE EXTERNAL TABLE IF NOT EXISTS fact_tables.errors_reported (
    mongo_object_id  STRING COMMENT "THIS IS A COMMENT",
    fk_subscription BIGINT,
    fk_customer BIGINT,
    fk_entered_date INT,
    fk_product BIGINT,
    fk_delivery_schedule INT,
    country STRING,
    agent STRING,
    box_id STRING,
    hellofresh_week_where_error_happened STRING,
    channel STRING,
    compensation_type STRING,
    compensation_amount DOUBLE,
    customer_emotion INT,
    description_total STRING,
    reason STRING,
    subreason STRING,
    ingredient STRING,
    error_description STRING,
    has_sorry_gift INT,
    is_pr_box INT,
    inserted_at BIGINT
 )
 PARTITIONED BY (hellofresh_week string, country string)
STORED AS PARQUET
LOCATION '/HelloFresh/Databases/fact_tables/errors_reported';
"""

parser = HiveTableParser()
fields = parser.parse_fields(sql)
table = parser.parse_table(sql)
metadata = parser.parse_table_metadata(sql)

print metadata.author
print metadata.description
print metadata.version
exit()

print "{} {} ".format(table.database, table.table)

for field in fields:
    print "{} {} {}" .format(field.field_name, field.field_type, field.field_has_comment)
exit()