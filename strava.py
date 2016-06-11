__author__ = 'parkerjb22'


from StravaXML import StravaXML
import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()

cwd = os.getcwd()

inputFile = filedialog.askopenfile(parent=root, initialdir=cwd, title='Please select a TCX File', filetypes = [("TCX files","*.tcx")])
if inputFile is None:
    exit('no file selected')

s = StravaXML(inputFile)
s.printDistAndPace()