# Standard library imports
import io

# Local application/library specific imports
from helpers.llm.visualization import (
    get_dataframe_viz_code,
)

# Third party imports
import numpy as np
import pandas as pd
from PIL import Image

def exec_code_and_get_figure(code: str):
    """
    Executes a code snippet and returns the figure.

    Args:
        code (str): the code snippet to execute

    Returns:
        matplotlib figure
    """

    try:
        if "fig" not in code:
            raise Exception("Visualization code does not assign plt.gcf() to fig")

        if "```" in code:
            raise Exception("Visualization code contains backticks from get_figure")

        # this is instructed to assign plt.gcf() to fig
        namespace = {}
        exec(code, namespace)

        if namespace['fig'] is None:
            raise Exception("Visualization code did not produce a figure")

        return namespace['fig']

    except Exception as e:
        raise e

def get_visualization_image(llm, query, df) -> (np.ndarray, str, Exception):
    """
    Gets a visualization image from a BigQuery query.

    Args:
        llm (VertexAI): the LLM to use
        query (str): the query to run
        df (pd.DataFrame): the dataframe

    Returns:
        np.ndarray: the visualization image
        str: the visualization code
        Exception: the visualization error
    """

    visualization_code = get_dataframe_viz_code(llm, query, df)
    if visualization_code is None or visualization_code == "":
        return None, "", Exception("Visualization code is empty")

    if "```" in visualization_code:
        return None, visualization_code, Exception("Visualization code contains backticks")

    try:
        # this is instructed to assign plt.gcf() to fig
        fig = exec_code_and_get_figure(visualization_code)

        # Save the figure to a BytesIO object
        buf = io.BytesIO()

        fig.savefig(buf, format='png')

        buf.seek(0)

        # Load the image data from the BytesIO object into a numpy array
        image = Image.open(buf)
        image_array = np.array(image)

        # Print the shape of the image array
        print(image_array.shape)

        # Don't forget to close the BytesIO object
        buf.close()

        return image_array, visualization_code, None

    except Exception as e:
        return None, visualization_code, e
