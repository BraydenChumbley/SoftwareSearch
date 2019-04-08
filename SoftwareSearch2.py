import tkinter as tk
from tkinter import filedialog
import os
import csv

with open("C:\\Users\\bchum\\Documents\\Python Programs\\softwares.txt") as softwares:
	softwareList = softwares.readlines()
	
softwareList = [x.strip() for x in softwareList]

def contains (str, sub):
	if str.lower().find(sub.lower()) != -1:
		return True
	else:
		return False
		
def checkTXT(file):
	with open(file) as groupsFile:
		groupsList = groupsFile.readlines()
		
	groupsList = [x.strip() for x in groupsList]
	
	for group in groupsList:
		for s in softwareList:
			if contains(group, s):
				print(group)
				
	print("")

def checkCSV(file):
	with open(file) as csvFile:
		reader = csv.reader(csvFile)
		
		colHeaders = []
		
		for i, line in enumerate(reader):
			removables = []
			if(i == 0):
				colHeaders = line
				continue
			empGroups = line[colHeaders.index("Groups")].split(",")
			
			for group in empGroups:
				for s in softwareList:
					if contains(group, s):
						removables.append(group)
			
			if(len(removables) > 0):
				empName = line[colHeaders.index("Name")]
				empFacility = line[colHeaders.index("DistinguishedName")].split(",")[3].replace("OU=", "")
				print(empName + " | " + empFacility)
				for s in removables:
					print(s)
				print("")

applicationWindow = tk.Tk()#create application window
applicationWindow.withdraw()#Hide random tkinter window

fileTypes = [("Any Termination", "*.txt;*.csv"),("Text Files", "*.txt"),("CSV Files", "*.csv")]#Only allows these file types to be opened
filePath = filedialog.askopenfilename(parent=applicationWindow, filetypes=fileTypes, title="Select file to open")#Prompt user for file to opena
fileName, fileExt = os.path.splitext(filePath)

if(fileExt == ".txt"):
	checkTXT(filePath)
elif(fileExt == ".csv"):
	checkCSV(filePath)
else:
	print("This aint right")

print("Press Enter to exit")
try:
	input()
except SyntaxError:
	pass