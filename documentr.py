from documentr.parser import HiveTableParser
from documentr.document import Document
from documentr.writer import Writer

sql = """
/**
 * @author("Sergio Sola")
 * @description("This table creates some stuff")
 * @version("1.0.0")
 */
CREATE EXTERNAL TABLE IF NOT EXISTS fact_tables.errors_reported (
    mongo_object_id  STRING COMMENT "@reference(database.mongo_object_id)THIS IS A COMMENT an aweful comment",
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
documentr = Document(parser)
table_data = documentr.create(sql)
documentr.write(Writer("/tmp"))
print table_data