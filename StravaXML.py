__author__ = 'JuParker'

import datetime
import math
from geopy.distance import vincenty

_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

def printDistAndPace(root):

    prev = (0.0, 0.0)
    prevTime = 0.0
    timeObj, timeStart, totalFeet = 0, 0, 0


    for lap in root.iter(_prefix + "Trackpoint"):
        try:
            timeTag = lap.find(_prefix + "Time")
            timeObj = datetime.datetime.strptime(timeTag.text, _dateFormat)

            posTag = lap.find(_prefix + "Position")
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
        except:
            pass

    td = timeObj - timeStart
    pace = td.seconds/totalFeet.miles/60
    paceMin = math.floor(pace)
    paceSec = round((pace - paceMin) * 60)
    print('Distance:'.ljust(10), round(totalFeet.miles, 2))
    print('Time:'.ljust(10), '%s:%s' % (paceMin, paceSec))