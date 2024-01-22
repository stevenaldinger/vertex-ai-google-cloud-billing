from unittest import TestCase
from ..markdown import strip_markdown

class MarkdownTestCase(TestCase):
  def test_strip_markdown(self):
    """
    Tests that markdown code blocks are stripped from strings
    """

    md_string = """
    ```python
    print('hello world')
    ```
    """

    result = strip_markdown(md_string)

    self.assertEqual(result.strip(), "print('hello world')")
