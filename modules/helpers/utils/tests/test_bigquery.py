from unittest import TestCase
from ..bigquery import get_bigquery_schema_query

class BigQueryTestCase(TestCase):
  def test_get_bigquery_schema_query(self):
    schema_sql_query = get_bigquery_schema_query("test")

    expected = """
SELECT table_name, ddl
FROM `test.INFORMATION_SCHEMA.TABLES`
WHERE table_type = 'BASE TABLE'
ORDER BY table_name;
"""

    self.assertTrue(schema_sql_query == expected)
