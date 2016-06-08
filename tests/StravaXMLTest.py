__author__ = 'juparker'

import unittest
import StravaXML
from io import StringIO

class StravaXMLTest(unittest.TestCase):

    def test_getOutput(self):
        self.assertEqual('longwords 00:12:12\n', StravaXML.getOutput('longwords', '00:12:12'))
        self.assertEqual('words        12:12\n', StravaXML.getOutput('words', '12:12'))

    def test_convertToMinSec(self):
        self.assertEqual('5:40', StravaXML.convertToMinSec(340))
        self.assertEqual('5:40', StravaXML.convertToMinSec(340.5))
        self.assertEqual('5:42', StravaXML.convertToMinSec(341.5))

    def test_printOutput(self):
        expected = \
            "Time:        10:20\n" + \
            "Distance:        2\n" + \
            "Pace:         5:10\n"

        out = StringIO()
        seconds = 620
        miles = 2
        StravaXML.printOutput(seconds, miles, out)

        self.assertEqual(expected, out.getvalue())
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)