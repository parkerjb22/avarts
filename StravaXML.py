__author__ = 'JuParker'

import datetime
import math
import sys
from geopy.distance import vincenty

_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

class StravaXML:

    def __init__(self, root=None):
        self.root = root

    def printDistAndPace(self):

        prev = (0.0, 0.0)
        prevTime = 0.0
        timeObj, timeStart, totalFeet = 0, 0, 0

        for lap in self.root.iter(_prefix + "Trackpoint"):
            timeTag = lap.find(_prefix + "Time")
            timeObj = datetime.datetime.strptime(timeTag.text, _dateFormat)

            posTag = lap.find(_prefix + "Position")

            if posTag is None:
                continue

            latLon = (posTag.find(_prefix + "LatitudeDegrees").text, posTag.find(_prefix + "LongitudeDegrees").text)

            if prevTime is not 0.0:
                v = vincenty(prev, latLon)
                if totalFeet == 0:
                    totalFeet = v
                else:
                    totalFeet += v
            else:
                timeStart = timeObj

            prevTime = timeObj
            prev = latLon

        td = timeObj - timeStart

        self.printOutput(td.seconds, totalFeet.miles)

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