# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.llm.vertexai import initialize
from helpers.llm.visualization import (
  get_dataframe_viz_code,
)

# Third party imports
from langchain_google_vertexai import VertexAI
import pandas as pd

model_name='gemini-pro@latest'
max_output_tokens = 2048
temperature = 0
top_p = .8
top_k = 40

class VisualizationTestCase(TestCase):
  def test_get_dataframe_viz_code(self):
    """
    This test confirms that the get_dataframe_viz_code function
    returns the expected Python code snippet to visualize a Pandas
    DataFrame.
    """

    initialize()

    llm = VertexAI(
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

    prompt = """How much money have I spent on the top 5 most expensive services?"""

    # Create a dataframe
    df = pd.DataFrame({
        'service_name': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
        'total_cost': [324.631208, 128.644393, 31.970339, 4.732000, 1.587599]
    })

    viz_code = get_dataframe_viz_code(llm, prompt, df)

    self.assertTrue(len(viz_code) > 0)
    self.assertTrue('import matplotlib.pyplot as plt' in viz_code)

    # test that the code snippet can be executed
    exec(viz_code)
