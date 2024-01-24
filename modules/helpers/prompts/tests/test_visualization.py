# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from helpers.prompts.visualization import (
  dataframe_visualization_code_prompt,
)

# Third party imports
import pandas as pd

class VisualizationTestCase(TestCase):
  def test_dataframe_visualization_code_prompt(self):
    """
    This test confirms that the dataframe_visualization_code_prompt function
    returns the expected prompt.
    """

    prompt = """How much money have I spent on the top 5 most expensive services?"""

    # Create a dataframe
    df = pd.DataFrame({
        'service_name': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
        'total_cost': [324.631208, 128.644393, 31.970339, 4.732000, 1.587599]
    })

    viz_code_prompt = dataframe_visualization_code_prompt(prompt, df)

    prompt_expected = """\
Write python code to visualize the following pandas dataframe using matplotlib. Only respond with code, no explanation.
Be sure to define the dataframe as `df` before plotting.
Assign the figure to a variable named `fig`.

[START_EXAMPLE]
The question asked was "What are the top 5 most expensive services used?"
The corresponding dataframe is:
|    | service_name   |   total_cost |
|---:|:---------------|-------------:|
|  0 | Compute Engine |     324.631  |
|  1 | Vertex AI      |     128.644  |
|  2 | Cloud Storage  |      31.9703 |
|  3 | Maps API       |       4.732  |
|  4 | BigQuery       |       1.5876 |

Visualization code:
```py
import pandas as pd
import matplotlib.pyplot as plt

# Define the dataframe
df = pd.DataFrame({
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [324.631, 128.644, 31.9703, 4.732, 1.5876]
})

# Plot the bar chart
df.sort_values(by='TotalCost', ascending=False).head(5).plot.barh(x='ServiceDescription', y='TotalCost')

# Customize the plot
plt.title('Top 5 Most Expensive Services Used')
plt.xlabel('Total Cost')
plt.ylabel('Service Description')
plt.grid(True)
plt.show()

fig = plt.gcf()
```
[END_EXAMPLE]


Prompt:
The question asked was "How much money have I spent on the top 5 most expensive services?"
The corresponding dataframe is:
|    | service_name   |   total_cost |
|---:|:---------------|-------------:|
|  0 | Compute Engine |     324.631  |
|  1 | Vertex AI      |     128.644  |
|  2 | Cloud Storage  |      31.9703 |
|  3 | Maps API       |       4.732  |
|  4 | BigQuery       |       1.5876 |

Visualization code:
"""

    self.assertEqual(viz_code_prompt, prompt_expected)
