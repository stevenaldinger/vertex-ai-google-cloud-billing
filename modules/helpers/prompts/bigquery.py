# Local application/library specific imports
from helpers.utils.date import get_todays_date

# Third party imports
from langchain.prompts import PromptTemplate

def create_bq_error_resolution_prompt_template(failed_query: str, error_message: str) -> PromptTemplate:
    """
    Creates a prompt template for a BigQuery error resolution question.

    Args:
        failed_query (str): the query that failed
        error_message (str): the error message

    Returns:
        PromptTemplate: the prompt template
    """

    template = f"""\
Fix the following BigQuery Google Standard SQL code to resolve the error. \
Only respond with code, no explanation.

BigQuery Google Standard SQL code:
```sql
{failed_query}
```

Error message:
```
{error_message}
```

Schema context:
{{content}}"""

    return PromptTemplate.from_template(template)

def create_bq_prompt_template(question: str, question_class: str) -> PromptTemplate:
    """
    Creates a prompt template for a BigQuery question.

    If question_class is about a specifci service, the prompt template will
    include instructions to use the service description column instead of
    the service ID column for better results.

    Args:
        question (str): the question to answer
        question_class (str): the class of the question, either "generic" or "specific_service"

    Returns:
        PromptTemplate: the prompt template
    """

    # deals with the LLM's lack of date awareness
    todays_date = get_todays_date()
    date_context = f"Today's date is {todays_date}."

    # deals with the LLM's tendency to assume the service ID column is human-readable
    svc_description_instructions = (
        "\nFor any service names mentioned, use the service description column."
        if question_class == "specific_service"
        else ""
    )

    # deals with the LLM's tendency to generate invalid GoogleSQL code
    date_range_instructions = """\
If a date/time range is necessary, use `BETWEEN` and the format `TIMESTAMP("2005-01-03 12:34:56+00")` when appropriate.
If using DATE_SUB or TIMESTAMP_SUB, you cannot use the MONTH date part when the argument is TIMESTAMP type.
"""

    template = f"""\
Write a BigQuery Google Standard SQL query that answers the following question.{svc_description_instructions}
{date_context}
{date_range_instructions}
Question: {question}

{{content}}"""

    return PromptTemplate.from_template(template)
