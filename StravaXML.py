__author__ = 'JuParker'

import datetime
import math
from geopy.distance import vincenty

_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

class StravaXML:

    def __init__(self, root=None):
        self.root = root

    def printDistAndPace(self):

        timeObj, timeStart = None, None
        points = []

        for lap in self.root.iter(_prefix + "Trackpoint"):
            timeTag = lap.find(_prefix + "Time")
            timeObj = datetime.datetime.strptime(timeTag.text, _dateFormat)

            posTag = lap.find(_prefix + "Position")

            if posTag is None:
                continue

            points.append((posTag.find(_prefix + "LatitudeDegrees").text, posTag.find(_prefix + "LongitudeDegrees").text))

            if timeStart is None:
                timeStart = timeObj

        td = timeObj - timeStart
        totalMiles = self.getMiles(points)
        self.printOutput(td.seconds, totalMiles)

    def getMiles(self, points):
        dist = [vincenty(x,y).miles  for (x, y) in zip(points[:-1], points[1:])]
        return sum(dist)
    def convertToMinSec(self, secs):
        min = math.floor(secs/60)
        sec = round(secs % 60)
        return '%s:%s' % (min, sec)

    def getOutput(self, msg, val):
        return '{0: <10}{1: >8}'.format(msg, val)

    def printOutput(self, seconds, miles):

        pace = self.convertToMinSec(seconds/miles)
        total = self.convertToMinSec(seconds)
        dist = round(miles, 2)

        print(self.getOutput('Time:', total))
        print(self.getOutput('Distance:', dist))
        print(self.getOutput('Pace:', pace))