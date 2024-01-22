# Local application/library specific imports
from helpers.utils.markdown import strip_markdown
from helpers.prompts.visualization import (
    dataframe_visualization_code_prompt
)

def get_dataframe_viz_code(llm, query, df) -> str:
    """
    Returns a Python code snippet that will visualize a Pandas DataFrame.

    Args:
        llm (VertexAI): the LLM to use
        query (str): the query that generated the DataFrame
        df (pd.DataFrame): the DataFrame to visualize

    Returns:
        str: the Python code snippet
    """

    visualization_code_query = dataframe_visualization_code_prompt(query, df)

    visualization_code = llm.invoke(visualization_code_query)

    return strip_markdown(visualization_code).strip()
