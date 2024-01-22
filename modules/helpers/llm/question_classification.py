# Standard library imports
from typing import List

# Local application/library specific imports
from helpers.prompts.question_classification import (
    question_classification,
)

def get_question_classification(llm, question: str) -> str:
    """
    Invokes an LLM to classify a given question as "generic" or
    about a "specific_service".

    Args:
        llm (VertexAI): the LLM to use
        question (str): the question to classify

    Returns:
        str: the classification of the question as "generic" or "specific_service"
    """

    prompt = question_classification(question)

    response = llm.invoke(prompt)

    if response == "yes":
        return "specific_service"
    else:
        return "generic"
