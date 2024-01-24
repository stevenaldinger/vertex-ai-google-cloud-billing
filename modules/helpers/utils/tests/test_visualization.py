# Standard library imports
from unittest import TestCase

# Local application/library specific imports
from ..visualization import get_image_from_visualization_code, exec_code_and_get_figure

# Third party imports
import numpy as np

class VisualizationTestCase(TestCase):
  def test_get_image_from_visualization_code(self):
    visualization_code = """\
import pandas as pd
import matplotlib.pyplot as plt

# Define the dataframe
df = pd.DataFrame({
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [325.275, 128.687, 32.423, 4.739, 1.59191]
})

# Plot the bar chart
df.sort_values(by='TotalCost', ascending=False).head(5).plot.barh(x='ServiceDescription', y='TotalCost')

# Customize the plot
plt.title('Top 5 Most Used Services By Cost')
plt.xlabel('Total Cost')
plt.ylabel('Service Description')
plt.grid(True)
plt.show()

fig = plt.gcf()
"""

    img, error = get_image_from_visualization_code(visualization_code)

    self.assertTrue(error is None)

    # test img is a non-empty numpy array
    self.assertTrue(img is not None)
    self.assertTrue(isinstance(img, np.ndarray))
    self.assertTrue(img.size > 0)

  def test_get_image_from_visualization_code_with_empty_code(self):
    visualization_code = ""

    img, error = get_image_from_visualization_code(visualization_code)

    self.assertTrue(img is None)
    self.assertTrue(error is not None)
    self.assertTrue(isinstance(error, Exception))

  def test_get_image_from_visualization_code_with_backticks(self):
    visualization_code = """\
```py
import pandas as pd
import matplotlib.pyplot as plt

# Define the dataframe
df = pd.DataFrame({
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [325.275, 128.687, 32.423, 4.739, 1.59191]
})

# Plot the bar chart
df.sort_values(by='TotalCost', ascending=False).head(5).plot.barh(x='ServiceDescription', y='TotalCost')

# Customize the plot
plt.title('Top 5 Most Used Services By Cost')
plt.xlabel('Total Cost')
plt.ylabel('Service Description')
plt.grid(True)
plt.show()

fig = plt.gcf()
```
"""
    img, error = get_image_from_visualization_code(visualization_code)

    self.assertTrue(img is None)
    self.assertTrue(error is not None)
    self.assertTrue(isinstance(error, Exception))

  def test_get_image_from_visualization_code_with_no_figure(self):
    visualization_code = """\
import pandas as pd
import matplotlib.pyplot as plt

# Define the dataframe
df = pd.DataFrame({
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [325.275, 128.687, 32.423, 4.739, 1.59191]
})

# Plot the bar chart
df.sort_values(by='TotalCost', ascending=False).head(5).plot.barh(x='ServiceDescription', y='TotalCost')

# Customize the plot
plt.title('Top 5 Most Used Services By Cost')
plt.xlabel('Total Cost')
plt.ylabel('Service Description')
plt.grid(True)
plt.show()
"""

    img, error = get_image_from_visualization_code(visualization_code)

    self.assertTrue(img is None)
    self.assertTrue(error is not None)
    self.assertTrue(isinstance(error, Exception))

  def test_exec_code_and_get_figure_bad_code(self):
    visualization_code = """\
import pandas as p
import matplotlib.pyplot as plt

# Define the dataframe
df = pd.DataFrame({
    'ServiceDescription': ['Compute Engine', 'Vertex AI', 'Cloud Storage', 'Maps API', 'BigQuery'],
    'TotalCost': [325.275, 128.687, 32.423, 4.739, 1.59191]
})
"""

    with self.assertRaises(Exception):
      exec_code_and_get_figure(visualization_code)


  def test_exec_code_and_get_figure_no_figure(self):
    visualization_code = """\
hello = world
"""

    with self.assertRaises(Exception):
      exec_code_and_get_figure(visualization_code)
