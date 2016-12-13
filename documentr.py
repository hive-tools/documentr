from documentr.parser import HiveTableParser
from documentr.document import Document
from documentr.writer import Writer

sql = """
/**
 * @author("Sergio Sola")
 * @description("This table creates a fact table with active customers")
 * @version("1.0.0")
 */
CREATE EXTERNAL TABLE IF NOT EXISTS fact_tables.active_customers (
    customer_id  BIGINT COMMENT "@reference(dimensions.customers.customer_sk) Reference to customer in time",
    product STRING COMMENT "@reference(other_tables.product.sku) Stores the product SKU"
 )
 PARTITIONED BY (country string)
STORED AS PARQUET
LOCATION '/YourCompany/fact_tables/active_customers';
"""

parser = HiveTableParser()
documentr = Document(parser)
table_data = documentr.create(sql)
documentr.write(Writer("/tmp"))
print table_data