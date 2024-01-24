# Local application/library specific imports
from helpers.prompts.bigquery import (
    create_bq_error_resolution_prompt_template,
    create_bq_prompt_template,
)
from helpers.utils.markdown import strip_markdown

# Third party imports
from langchain.prompts import PromptTemplate
from langchain.schema import format_document
from langchain.schema.document import Document

def create_bq_chain(llm, prompt_template):
    """
    Creates a chain for a BigQuery question.
    """

    chain = (
        {
            "content": lambda docs: "\n\n".join(
                format_document(doc, PromptTemplate.from_template("{page_content}"))
                for doc in docs
            )
        }
        | prompt_template
        | llm
    )

    return chain

def get_bigquery_query(llm, bigquery_ddls: Document, query: str, question_class: str) -> str:
    """
    Invokes an LLM chain to generate a BigQuery query.

    """

    prompt_template = create_bq_prompt_template(query, question_class)
    chain = create_bq_chain(llm, prompt_template)

    _result = chain.invoke(bigquery_ddls)
    result = strip_markdown(_result)

    return result, prompt_template.format(content=bigquery_ddls)


def get_bigquery_error_resolution_query(llm, bigquery_ddls: Document, query: str, error: str) -> str:
    """
    Invokes an LLM chain to generate a BigQuery query.

    """

    prompt_template = create_bq_error_resolution_prompt_template(query, error)
    chain = create_bq_chain(llm, prompt_template)

    _result = chain.invoke(bigquery_ddls)
    result = strip_markdown(_result)

    return result
