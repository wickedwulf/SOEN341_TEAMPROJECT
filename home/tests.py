the following is just a framework


from django.test import TestCase
import unittest
from filename import oldfunctionname
class TestCase(unittest.TestCase):
    def test_file_name(self):
        actual_result =oldfunctionname('')
        self.assertEquals(actual_result,'the right result')
unittest.main()

