__author__ = 'parkerjb22'

import datetime
import xml.etree.ElementTree as ET
import math
from geopy.distance import vincenty


fileLoc = "C:/Users/Juparker/Downloads/activity_1196342431.tcx"
_prefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"

ET.register_namespace('', "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
ET.register_namespace('TPX', "http://www.garmin.com/xmlschemas/UserProfile/v2")
tree = ET.parse(fileLoc)
root = tree.getroot()

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
    print(round(totalFeet.miles, 2), "%s:%s" % (paceMin, paceSec))

printDistAndPace(root)