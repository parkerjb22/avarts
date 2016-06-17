__author__ = 'JuParker'

import math
import random
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
from geopy.distance import vincenty, VincentyDistance, Point
from xml.dom import minidom

_defaultPrefix = "{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}"
_dateFormat = "%Y-%m-%dT%H:%M:%S.000Z"
_fileNameFormat = "%Y-%m-%dT%H_%M_%S"

class StravaXML:

    def createRoute(self, distance, startTime, path):
        root = ET.Element("TrainingCenterDatabase")
        timeObj = startTime
        track = self.setupTrack(root, timeObj.strftime(_dateFormat))

        distance = distance * 1610
        totalDist = 0.0
        distInc = 15
        point = ((33.45618202351034, -86.80428626015782), timeObj)
        degrees = 45

        while True:
            self.createPoint(track, point, totalDist)
            if totalDist >= distance:
                break
            totalDist += distInc
            degrees = self.newDegrees(degrees)
            point = self.newPoint(point, distInc, degrees)

        root = self.prettify(root)
        outputFile = path + '\\ouput_' + startTime.strftime(_fileNameFormat) + '.tcx'
        with open(outputFile, "w") as text_file:
            print(root, file=text_file)

    def printDistAndPace(self, inputFile, prefix=_defaultPrefix):
        ET.register_namespace('', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
        ET.register_namespace('TPX', "http://www.garmin.com/xmlschemas/UserProfile/v2")
        tree = ET.parse(inputFile)
        root = tree.getroot()

        points = []

        for lap in root.iter(prefix + "Trackpoint"):

            posTag = lap.find(prefix + "Position")

            if posTag is None:
                continue

            lat = posTag.find(prefix + "LatitudeDegrees").text
            lon = posTag.find(prefix + "LongitudeDegrees").text

            time = lap.find(prefix + "Time").text
            timeObj = datetime.strptime(time, _dateFormat)

            points.append( ((lat, lon), timeObj) )

        td = points[-1][1] - points[0][1]
        totalMiles = self.getMiles(points)
        self.printOutput(td.seconds, totalMiles)

    def createPoint(self, root, point, dist):
        trackPoint = ET.SubElement(root, "Trackpoint")
        ET.SubElement(trackPoint, "Time").text = point[1].strftime(_dateFormat)
        pos = ET.SubElement(trackPoint, "Position")
        ET.SubElement(pos, "LatitudeDegrees").text = '%.14f' % point[0][0]
        ET.SubElement(pos, "LongitudeDegrees").text = '%.14f' % point[0][1]
        ET.SubElement(trackPoint, "DistanceMeters").text = '%.5f' % dist

    def setupTrack(self, root, startTime):
        activities = ET.SubElement(root, "Activities")
        activity = ET.SubElement(activities, "Activity", Sport="Running")
        ET.SubElement(activity, "Id").text = startTime
        lap = ET.SubElement(activity, "Lap", StartTime=startTime)
        ET.SubElement(lap, "TotalTimeSeconds", ).text = "515.26"
        ET.SubElement(lap, "DistanceMeters", ).text = "1610.719970703125"
        track = ET.SubElement(lap, "Track")
        return track

    def prettify(self, elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reParsed = minidom.parseString(rough_string)
        return reParsed.toprettyxml(indent="  ")

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

    def newPoint(self, point, mDist, bearing):
        kmDist = mDist/1000
        origin = Point(point[0][0], point[0][1])
        destination = VincentyDistance(kilometers=kmDist).destination(origin, bearing)
        return ((destination.latitude, destination.longitude), point[1] + timedelta(0,4))

    def newDegrees(self, degrees, chance=None):
        cap=1000
        stability = .5 * cap

        if chance is None:
            chance = random.randrange(1,cap)

        if chance < stability:
            return degrees
        if chance < (cap - stability/2):
            return degrees + 5
        if chance < cap:
            return degrees - 5

        return -degrees