__author__ = 'juparker'

from unittest import TestCase
from unittest.mock import patch
from StravaXML import StravaXML
from io import StringIO

class StravaXMLTest(TestCase):

    s = StravaXML()

    def test_getOutput(self):
        self.assertEqual('longwords 00:12:12', self.s.getOutput('longwords', '00:12:12'))
        self.assertEqual('words        12:12', self.s.getOutput('words', '12:12'))

    def test_convertToMinSec(self):
        self.assertEqual('5:40', self.s.convertToMinSec(340))
        self.assertEqual('5:40', self.s.convertToMinSec(340.5))
        self.assertEqual('5:42', self.s.convertToMinSec(341.5))

    @patch('sys.stdout', new_callable=StringIO)
    def test_printOutput(self, mock_stdout):
        expected = \
            "Time:        10:20\n" + \
            "Distance:        2\n" + \
            "Pace:         5:10\n"

        seconds = 620
        miles = 2
        self.s.printOutput(seconds, miles)

        self.assertEqual(expected, mock_stdout.getvalue())

    def test_getMiles(self):
        myList = [
            ((33.449885454028845, -86.81012249551713), ''),
            ((33.44981093890965, -86.81014596484601), ''),
            ((33.449710523709655, -86.81016624905169), '')
        ]
        self.assertEqual(0.01233031270241276, self.s.getMiles(myList))

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)