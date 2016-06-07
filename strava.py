__author__ = 'parkerjb22'


import xml.etree.ElementTree as ET
import StravaXML
import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()

cwd = os.getcwd()

inputFile = filedialog.askopenfile(parent=root, initialdir=cwd, title='Please select a TCX File', filetypes = [("TCX files","*.tcx")])
if inputFile is None:
    exit('no file selected')


ET.register_namespace('', "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
ET.register_namespace('TPX', "http://www.garmin.com/xmlschemas/UserProfile/v2")
tree = ET.parse(inputFile)
root = tree.getroot()

StravaXML.printDistAndPace(root)