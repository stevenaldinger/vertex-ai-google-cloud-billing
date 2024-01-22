from unittest import TestCase
from ..date import get_todays_date

class DateTestCase(TestCase):
  def test_read_file_that_does_not_exist(self):
    today = get_todays_date()

    self.assertTrue(today is not None)
    self.assertTrue(today.count('/') == 2)
