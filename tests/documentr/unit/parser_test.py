import unittest2

from documentr.parser import ParserFactory
from documentr.items import FieldType


class HiveTableParserTest(unittest2.TestCase):
    def setUp(self):
        self.sql = """
            /**
             * @author('Sergio Sola')
             * @version('v1.0.1')
             * @description('This table is used to store some data')
             */
            CREATE EXTERNAL TABLE IF NOT EXISTS `fact_tables`.some_table (
                country STRING COMMENT "Country",
                fk_date INT COMMENT "Foreing key to Date dimension",
                campaign STRING COMMENT "Campaing ID",
                subchannel STRING COMMENT "Sub channel used for some reason"
             )
            PARTITIONED BY (
              week STRING COMMENT "To which week it belongs"
            )
            STORED AS PARQUET
            LOCATION '/HelloFresh/Databases/fact_tables/some_table';
        """

        self.hive_parser = ParserFactory.create_parser("hive")

    def test_parse_table(self):
        table = self.hive_parser.parse_table(self.sql)

        self.assertEqual("fact_tables", table.database)
        self.assertEqual("some_table", table.table)

    def test_parse_fields(self):
        expected_value = [
            FieldType('country', 'STRING', True, "Country", {}),
            FieldType('fk_date', 'INT', False, "Foreing key to Date dimension", {}),
            FieldType('campaign', 'STRING', False, "Campaing ID", {}),
            FieldType('subchannel', 'STRING', False, "Sub channel used for some reason", {}),
            FieldType('week', 'STRING', False, "To which week it belongs", {}),
        ]

        fields = self.hive_parser.parse_fields(self.sql)

        self.assertEqual(len(expected_value), len(fields))

        for index, item in enumerate(expected_value):
            self.assertEqual(
                expected_value[index], fields[index]
            )
