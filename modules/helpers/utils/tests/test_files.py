from unittest import TestCase
from tempfile import NamedTemporaryFile
from ..files import read_file

class FilesTestCase(TestCase):
  def test_read_file_that_does_not_exist(self):
    with self.assertRaises(Exception) as context:
        read_file('definitely-does-not-exist.txt')

    self.assertTrue('does not exist' in str(context.exception))

  def test_read_file_that_exists(self):
      with NamedTemporaryFile() as tf:
        result = read_file(tf.name)

  def test_read_file_that_exists_as_array(self):
      with NamedTemporaryFile() as tf:
        result = read_file(tf.name, as_array=True)
