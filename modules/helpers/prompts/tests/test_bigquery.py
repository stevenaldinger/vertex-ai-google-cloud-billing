# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.prompts.bigquery import (
  create_bq_error_resolution_prompt_template,
  create_bq_prompt_template,
)
from helpers.utils.date import get_todays_date

class BigQueryClassificationTestCase(TestCase):
  def test_create_bq_prompt_template(self):
    """
    This test confirms that the create_bq_prompt_template function
    returns the expected prompt.
    """

    prompt = """How much money have I spent on Vertex AI this year?"""

    bq_prompt_template = create_bq_prompt_template(prompt, "specific_service")

    todays_date = get_todays_date()

    prompt_expected = f"""\
Write a BigQuery Google Standard SQL query that answers the following question.
For any service names mentioned, use the service description column.
Today's date is {todays_date}.
If a date/time range is necessary, use `BETWEEN` and the format `TIMESTAMP("2005-01-03 12:34:56+00")` when appropriate.
If using DATE_SUB or TIMESTAMP_SUB, you cannot use the MONTH date part when the argument is TIMESTAMP type.

Question: How much money have I spent on Vertex AI this year?

{{content}}"""

    self.assertEqual(bq_prompt_template.template, prompt_expected)

  def test_create_bq_error_resolution_prompt_template(self):
    """
    This test confirms that the create_bq_error_resolution_prompt_template function
    returns the expected prompt.
    """

    failed_query = """SELECT * FROM `bigquery.fake_dataset.fake_table`"""
    error_message = """Not found: Table bigquery.fake_dataset.fake_table was not found in location US"""

    bq_error_resolution_prompt_template = create_bq_error_resolution_prompt_template(failed_query, error_message)

    prompt_expected = """\
Fix the following BigQuery Google Standard SQL code to resolve the error. Only respond with code, no explanation.

BigQuery Google Standard SQL code:
```sql
SELECT * FROM `bigquery.fake_dataset.fake_table`
```

Error message:
```
Not found: Table bigquery.fake_dataset.fake_table was not found in location US
```

Schema context:
{content}"""

    self.assertEqual(bq_error_resolution_prompt_template.template, prompt_expected)
