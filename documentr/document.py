class Document(object):
    def __init__(self, table_parser):
        self.table_parser = table_parser
        self.document = None

    def create(self, sql):
        try:
            table = self.table_parser.parse_table(sql)
        except Exception, e:
            print "Something wrong with sql {}".format(sql)
            return None

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

        self.document = document

        return self.document

    def write(self, writer):
        if not self.document:
            raise Exception("Document was not generated")

        writer.write(self.document)
