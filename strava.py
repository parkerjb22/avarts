__author__ = 'parkerjb22'


from StravaXML import StravaXML, _dateFormat, datetime, timedelta
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()

dirName = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
if dirName is None:
    exit('no directory selected')

s = StravaXML()
timeObj = datetime.strptime('2016-03-01T11:39:06.000Z', _dateFormat)
for x in range(0, 25):
    s.createRoute(5.0, timeObj, dirName)
    timeObj += timedelta(days=1)