from documentr.parser import HiveTableParser
from documentr.document import Document
from documentr.writer import Writer
from documentr.loader import Loader
from documentr.generator.template import Template

# sql = """
# /**
#  * @author("Sergio Sola")
#  * @description("This table creates a fact table with active customers")
#  * @version("1.0.0")
#  */
# CREATE EXTERNAL TABLE IF NOT EXISTS fact_tables.active_customers (
#     customer_id  BIGINT COMMENT "@reference(dimensions.customers.customer_sk) Reference to customer in time",
#     product STRING COMMENT "@reference(other_tables.product.sku) Stores the product SKU"
#  )
#  PARTITIONED BY (country string)
# STORED AS PARQUET
# LOCATION '/YourCompany/fact_tables/active_customers';
# """

sql = """
/**
 * @author("Sergio Sola")
 * @description("Dimension table displays customer data")
 * @version("0.0.1")
 */
CREATE EXTERNAL TABLE IF NOT EXISTS dimensions.customers (
    customer_sk  BIGINT COMMENT "Surrogate key for customer",
    email STRING COMMENT "Customer email"
 )
STORED AS PARQUET
LOCATION '/YourCompany/dimensions/customers';
"""
#
# parser = HiveTableParser()
# documentr = Document(parser)
# table_data = documentr.create(sql)
# documentr.write(Writer("/tmp"))
# print table_data

loader = Loader("/tmp")
schema = loader.load()

template = Template(schema)
template.generate()