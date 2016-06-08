__author__ = 'JuParker'

import datetime
import math
import sys
from geopy.distance import vincenty

_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

def printDistAndPace(root):

    prev = (0.0, 0.0)
    prevTime = 0.0
    timeObj, timeStart, totalFeet = 0, 0, 0

    for lap in root.iter(_prefix + "Trackpoint"):
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

    printOutput(td.seconds, totalFeet.miles)

def convertToMinSec(secs):
    min = math.floor(secs/60)
    sec = round(secs % 60)
    return '%s:%s' % (min, sec)

def getOutput(msg, val):
    return '{0: <10}{1: >8}\n'.format(msg, val)

def printOutput(seconds, miles, out=sys.stdout):
    pace = convertToMinSec(seconds/miles)
    total = convertToMinSec(seconds)
    dist = round(miles, 2)

    out.write(getOutput('Time:', total))
    out.write(getOutput('Distance:', dist))
    out.write(getOutput('Pace:', pace))