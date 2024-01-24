# Local application/library specific imports
from helpers.llm.visualization import (
    get_dataframe_viz_code,
)
from helpers.utils.visualization import (
    get_image_from_visualization_code,
)

# Third party imports
import numpy as np


def get_visualization_image(llm, query, df) -> (np.ndarray, str, str, Exception):
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

    visualization_code, viz_code_prompt = get_dataframe_viz_code(llm, query, df)

    img, error = get_image_from_visualization_code(visualization_code)

    return img, visualization_code, viz_code_prompt, error
