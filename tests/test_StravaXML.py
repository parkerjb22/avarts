__author__ = 'juparker'

from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from lib.StravaXML import StravaXML, _dateFormat, datetime, vincenty, timedelta


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

    def test_newDegrees(self):
        self.assertEqual(90, self.s.newDegrees(90, chance=100))
        self.assertEqual(95, self.s.newDegrees(90, chance=500))
        self.assertEqual(85, self.s.newDegrees(90, chance=750))
        self.assertEqual(-90, self.s.newDegrees(90, chance=1000))

    def test_newPoint(self):
        timeObj = datetime.strptime('2016-03-01T11:39:06.000Z', _dateFormat)
        point = ((33.449885454028845, -86.81012249551713), timeObj)
        mdist = 15
        bearing = 90
        newPoint = self.s.newPoint(point, mdist, bearing)
        v = vincenty(point[0], newPoint[0])
        self.assertAlmostEqual(mdist, v.meters, 5)
        self.assertEqual(timedelta(0, 4), newPoint[1] - timeObj)