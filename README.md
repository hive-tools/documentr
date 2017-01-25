# documentr

This package helps you to automate the documentation of your database migrations for creating tables. 

![img](http://i.imgur.com/mrLL6gZ.png)

And now it supports the table graph representation:

![img](http://i.imgur.com/ZbBxidK.png)

## TO-DO

- [ ] Differenciate between a table creation and creating a view
- [x] Create a basic graph representing each table relationships
- [ ] Improve error handling, if something cannot be done, why?
- [x] Improve Documentr default template, right now it's kind of horrible
- [ ] Write tests, and then... more tests
- [ ] Configure Travis CI to run tests after each commit
- [ ] Improve documentation :party:

## Supports
- Hive

## Example
```
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
```

Generates a JSON file like:

```json
{
	"table": "active_customers",
	"metadata": {
		"version": "1.0.0",
		"description": "This table creates a fact table with active customers",
		"author": "Sergio Sola"
	},
	"fields": [{
		"comment": " Reference to customer in time",
		"type": "BIGINT",
		"name": "customer_id",
		"metadata": {
			"reference": "dimensions.customers.customer_sk"
		}
	}, {
		"comment": " Stores the product SKU",
		"type": "STRING",
		"name": "product",
		"metadata": {
			"reference": "other_tables.product.sku"
		}
	}, {
		"comment": "",
		"type": "STRING",
		"name": "country",
		"metadata": null
	}],
	"database": "fact_tables"
}
```

Now with this JSON files we can build a website displaying all these information in a beatiful way.
