import os

def read_file(path, as_array = False, strip = False):
    """
    Reads the contents of a file and returns it as a string, or an array of strings.

    Parameters
    ----------
    path : str
        The path to the file to read.
    as_array : bool, optional
        Whether to return the file contents as an array of lines (default is False).
    strip : bool, optional
        Whether to strip whitespace and newlines from text (default is False). This
        can be useful if you're reading in a file that has empty lines between
        paragraphs and you want to remove them. Only applies if as_array is True.

    Returns
    -------
    str
        The contents of the file.

    Raises
    ------
    Exception
        If the file doesn't exist.
    """

    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')

    with open(path, 'r') as file:
        if as_array:
            text = file.readlines() if not strip else [line.strip() for line in file.readlines()]
        else:
            text = file.read()

    return text
