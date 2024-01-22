# Standard library imports
from typing import List

def question_classification(question: str) -> str:
    """
    Returns a prompt to classify a given question as "generic" or
    about a "specific_service".

    Args:
        question (str): the question to classify

    Returns:
        str: the classification prompt
    """

    prompt = f"""\
Answer the following question with only `yes` or `no`. \
Does the following question ask about a specific service by name?

{question}"""

    return prompt
