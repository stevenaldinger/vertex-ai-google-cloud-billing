# Local application/library specific imports
import config.config as config

# Third party imports
from langchain_google_vertexai import VertexAI

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
