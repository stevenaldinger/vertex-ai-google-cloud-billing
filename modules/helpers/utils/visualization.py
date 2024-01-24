# Standard library imports
import io

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
        # this is instructed to assign plt.gcf() to fig
        namespace = {}
        exec(code, namespace)

        if namespace['fig'] is None:
            raise Exception("Visualization code did not produce a figure")

        return namespace['fig']

    except Exception as e:
        raise e

def get_image_from_visualization_code(visualization_code: str) -> (np.ndarray, Exception):
    """
    Gets a visualization image from a BigQuery query.

    Args:
        visualization_code (str): the visualization code to run

    Returns:
        np.ndarray: the visualization image
        Exception: the visualization error
    """

    if visualization_code is None or visualization_code == "":
        return None, Exception("Visualization code is empty")

    if "```" in visualization_code:
        return None, Exception("Visualization code contains backticks")


    if "fig" not in visualization_code:
        return None, Exception("Visualization code does not assign plt.gcf() to fig")


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

        return image_array, None

    except Exception as e:
        return None, e
