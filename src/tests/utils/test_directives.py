from unittest import TestCase

from ...utils.directives import half

class HalfTestCases(TestCase):
    def test_with_integer(self):
        self.assertEqual(half(4), 2)

    def test_with_double(self):
        self.assertEqual(half(5.0), 2.5)
