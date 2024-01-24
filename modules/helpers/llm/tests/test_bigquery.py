# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.llm.vertexai import initialize
from helpers.llm.bigquery import (
  get_bigquery_query,
)

# Third party imports
from langchain_google_vertexai import VertexAI
from langchain.schema.document import Document

model_name='gemini-pro@latest'
max_output_tokens = 2048
temperature = 0
top_p = .8
top_k = 40

class BigQueryTestCase(TestCase):
  def test_get_bigquery_query(self):
    """
    This test confirms that the get_bigquery_query function
    returns the expected query for a generic question.
    """

    initialize()

    llm = VertexAI(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

    question = """Which 5 services do I spend the most money on?"""

    bq_ddls = [
      Document(
        page_content='ddl: CREATE TABLE `steven-aldinger.gdax.gcp_billing_export_v1_0161FF_E1335F_xxx`\n(\n  billing_account_id STRING OPTIONS(description=""),\n  service STRUCT<id STRING OPTIONS(description=""), description STRING OPTIONS(description="")> OPTIONS(description=""),\n  sku STRUCT<id STRING OPTIONS(description=""), description STRING OPTIONS(description="")> OPTIONS(description=""),\n  usage_start_time TIMESTAMP OPTIONS(description=""),\n  usage_end_time TIMESTAMP OPTIONS(description=""),\n  project STRUCT<id STRING OPTIONS(description=""), number STRING OPTIONS(description=""), name STRING OPTIONS(description=""), labels ARRAY<STRUCT<key STRING OPTIONS(description=""), value STRING OPTIONS(description="")>> OPTIONS(description=""), ancestry_numbers STRING OPTIONS(description=""), ancestors ARRAY<STRUCT<resource_name STRING OPTIONS(description=""), display_name STRING OPTIONS(description="")>> OPTIONS(description="")> OPTIONS(description=""),\n  labels ARRAY<STRUCT<key STRING OPTIONS(description=""), value STRING OPTIONS(description="")>> OPTIONS(description=""),\n  system_labels ARRAY<STRUCT<key STRING OPTIONS(description=""), value STRING OPTIONS(description="")>> OPTIONS(description=""),\n  location STRUCT<location STRING OPTIONS(description=""), country STRING OPTIONS(description=""), region STRING OPTIONS(description=""), zone STRING OPTIONS(description="")> OPTIONS(description=""),\n  export_time TIMESTAMP OPTIONS(description=""),\n  cost FLOAT64 OPTIONS(description=""),\n  currency STRING OPTIONS(description=""),\n  currency_conversion_rate FLOAT64 OPTIONS(description=""),\n  usage STRUCT<amount FLOAT64 OPTIONS(description=""), unit STRING OPTIONS(description=""), amount_in_pricing_units FLOAT64 OPTIONS(description=""), pricing_unit STRING OPTIONS(description="")> OPTIONS(description=""),\n  credits ARRAY<STRUCT<name STRING OPTIONS(description=""), amount FLOAT64 OPTIONS(description=""), full_name STRING OPTIONS(description=""), id STRING OPTIONS(description=""), type STRING OPTIONS(description="")>> OPTIONS(description=""),\n  invoice STRUCT<month STRING OPTIONS(description="")> OPTIONS(description=""),\n  cost_type STRING OPTIONS(description=""),\n  adjustment_info STRUCT<id STRING OPTIONS(description=""), description STRING OPTIONS(description=""), mode STRING OPTIONS(description=""), type STRING OPTIONS(description="")> OPTIONS(description=""),\n  tags ARRAY<STRUCT<key STRING OPTIONS(description=""), value STRING OPTIONS(description=""), inherited BOOL OPTIONS(description=""), namespace STRING OPTIONS(description="")>> OPTIONS(description=""),\n  cost_at_list FLOAT64,\n  transaction_type STRING,\n  seller_name STRING\n)\nPARTITION BY DATE(_PARTITIONTIME);',
        metadata={'table_name': 'gcp_billing_export_v1_0161FF_E1335F_xxx'}
      ),
    ]

    query, prompt = get_bigquery_query(llm, bq_ddls, question, "generic")

    # example query output
    #
    # SELECT
    #   service.description AS service_name,
    #   SUM(cost) AS total_cost
    # FROM
    #   `steven-aldinger.gdax.gcp_billing_export_v1_0161FF_E1335F_xxx` AS billing_data
    # WHERE
    #   usage_start_time BETWEEN TIMESTAMP("2023-01-01 00:00:00") AND TIMESTAMP("2024-01-23 23:59:59")
    # GROUP BY
    #   service_name
    # ORDER BY
    #   total_cost DESC
    # LIMIT 5;

    # assert we got a response
    self.assertTrue(query)
    self.assertTrue(prompt)

    # this will never be completely identical but we still need to test important pieces are there
    self.assertIn("SELECT", query)
    self.assertIn("FROM", query)
    self.assertIn("WHERE", query)
    self.assertIn("GROUP BY", query)
    self.assertIn("ORDER BY", query)
    self.assertIn("LIMIT", query)
    self.assertIn("service.description", query)
    self.assertIn("cost", query)
