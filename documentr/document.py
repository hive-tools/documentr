class Document(object):
    def __init__(self, table_parser):
        self.table_parser = table_parser

    def create(self, sql):
        table = self.table_parser.parse_table(sql)
        table_metadata = self.table_parser.parse_table_metadata(sql)
        fields = self.table_parser.parse_fields(sql)

        document = {
            "database": table.database,
            "table": table.table,
            "metadata": {
                "author": table_metadata.author,
                "version": table_metadata.version,
                "description": table_metadata.description
            },
            "fields": []
        }

        for field in fields:
            document["fields"].append(
                {
                    "name": field.field_name,
                    "type": field.field_type,
                    "comment": field.field_comment,
                    "metadata": field.field_metadata
                }
            )

        return document
