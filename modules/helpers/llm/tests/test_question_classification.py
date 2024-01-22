# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.llm.vertexai import initialize
from helpers.llm.question_classification import (
  get_question_classification,
)

# Third party imports
from langchain_google_vertexai import VertexAI

model_name='gemini-pro@latest'
max_output_tokens = 2048
temperature = 0
top_p = .8
top_k = 40

class QuestionClassificationTestCase(TestCase):
  def test_question_classification_specific_service(self):
    """
    This test confirms that the get_question_classification function
    returns the expected classification for a question about a
    specific service.
    """

    initialize()

    llm = VertexAI(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

    prompt = """How much money have I spent on Vertex AI this year?"""

    classification = get_question_classification(llm, prompt)

    self.assertEqual(classification, "specific_service")

  def test_question_classification_generic(self):
    """
    This test confirms that the get_question_classification function
    returns the expected classification for a question about general
    billing.
    """

    initialize()

    llm = VertexAI(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

    prompt = """How much money have I spent in total this year?"""

    classification = get_question_classification(llm, prompt)

    self.assertEqual(classification, "generic")
