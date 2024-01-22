# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.prompts.question_classification import (
  question_classification,
)

class QuestionClassificationTestCase(TestCase):
  def test_question_classification(self):
    """
    This test confirms that the question_classification function
    returns the expected prompt.
    """

    prompt = """How much money have I spent on Vertex AI this year?"""

    classification_prompt = question_classification(prompt)

    prompt_expected = """Answer the following question with only `yes` or `no`. Does the following question ask about a specific service by name?

How much money have I spent on Vertex AI this year?"""

    self.assertEqual(classification_prompt, prompt_expected)
