__author__ = 'JuParker'

import math
import xml.etree.ElementTree as ET
from datetime import datetime
from geopy.distance import vincenty

_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

class StravaXML:

    def __init__(self, inputFile=None):
        if inputFile is not None:
            ET.register_namespace('', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
            ET.register_namespace('TPX', "http://www.garmin.com/xmlschemas/UserProfile/v2")
            tree = ET.parse(inputFile)
            root = tree.getroot()
            self.root = root

    def printDistAndPace(self):
        points = []

        for lap in self.root.iter(_prefix + "Trackpoint"):

            posTag = lap.find(_prefix + "Position")

            if posTag is None:
                continue

            lat = posTag.find(_prefix + "LatitudeDegrees").text
            lon = posTag.find(_prefix + "LongitudeDegrees").text

            time = lap.find(_prefix + "Time").text
            timeObj = datetime.strptime(time, _dateFormat)

            points.append( ((lat, lon), timeObj) )

        td = points[-1][1] - points[0][1]
        totalMiles = self.getMiles(points)
        self.printOutput(td.seconds, totalMiles)

    def getMiles(self, points):
        dist = [vincenty(x[0],y[0]).miles  for (x, y) in zip(points[:-1], points[1:])]
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