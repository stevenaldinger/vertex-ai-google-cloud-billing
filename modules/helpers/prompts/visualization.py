# Third party imports
import pandas as pd

def dataframe_visualization_code_prompt(query: str, df: pd.DataFrame) -> str:
    """
    Returns a Python code snippet that will visualize a Pandas DataFrame.

    Args:
        query (str): the query that generated the DataFrame
        df (pd.DataFrame): the DataFrame to visualize

    Returns:
        str: the prompt asking for a visualization code snippet
    """

    visualization_code_query = f"""\
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
df = pd.DataFrame({{
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [324.631, 128.644, 31.9703, 4.732, 1.5876]
}})

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
The question asked was "{query}"
The corresponding dataframe is:
{df.to_markdown()}
Visualization code:
"""

    return visualization_code_query
