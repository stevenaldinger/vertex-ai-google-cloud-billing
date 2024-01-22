import re

def strip_markdown(text):
    """
    Strips markdown code blocks from a string.

    Args:
        text (str): the string to strip

    Returns:
        str: the stripped string
    """

    stripped_results = re.sub(r'```.*\n', '', text)
    stripped_results = re.sub(r'```', '', stripped_results)
    return stripped_results
