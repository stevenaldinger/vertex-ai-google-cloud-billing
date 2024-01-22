# Local application/library specific imports
import config.config as config

# Third party imports
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain.schema import format_document

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

def initialize_llm():
    llm = VertexAI(
        model_name=config.model_name,
        max_output_tokens=config.max_output_tokens,
        temperature=config.temperature,
        top_p=config.top_p,
        top_k=config.top_k,
        verbose=config.verbose,
    )

    return llm
