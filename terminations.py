# My CS teacher preaches adding a header to every file so this now exists
# Author:	Brayden Chumbley
# Description:	A program that searches for software to be removed in event of a termination
#				Yeah, I have no idea what is actually going on in this file. It really is just
#				a bunch of solutions on stackoverflow stitched together with only the most spaghetti
#				of code and commented with the most vaguest of comments. Have fun maintaining this.

import tkinter as tk #tkinter import for GUI
from tkinter import filedialog #filedialog input for GUI
import os
import csv #Love how there is a dedicated library for csv reading because python

#Set to directory that contains this python file. "\\" at the end are mandatory
ROOT_DIR = "D:\\Users\\bchumbley\\Documents\\"

#Groups that require additional action by technician
softwareDict = {"EmpCenter" : "-> !!!CHECK EMPCENTER ACCOUNT LIST!!!", "InfoHR" : "-> !!!CHECK NURSE!!!"}

#Open the list of removable software. MAKE SURE "softwares.txt" IS IN THE SAME DIRECTORY OF THIS PYTHON FILE
with open(ROOT_DIR + "softwares.txt") as softwares:
	softwareList = softwares.readlines()
	
softwareList = [x.strip() for x in softwareList]

def contains (str, sub):
	if str.lower().find(sub.lower()) != -1: #Match found
		return True
	else: #Match not found
		return False
		
def getFacility(arr):
	for OU in arr:
		if(OU == "OU=Users"):
			return arr[arr.index(OU) + 1]
		
def checkTXT(file):
	with open(file) as groupsFile:
		groupsList = groupsFile.readlines()
		
	groupsList = [x.strip() for x in groupsList]
	
	#Loops through all groups and prints out possible removable groups
	for group in groupsList:
		for s in softwareList:
			if contains(group, s):
				additionalAction = ""
				try: #Check if there is an addtional action required to check this software
					additionalAction = softwareDict[s]
				except KeyError: #No additional action for this software; We just pass
					pass
				print(group + " " + additionalAction)
				
	print("")

def checkCSV(file):
	with open(file) as csvFile:
		reader = csv.reader(csvFile)
		
		colHeaders = []
		empNoGroup = []
		
		for i, line in enumerate(reader):
			#if on line 0 then csv values are stored as column headers
			if(i == 0):
				colHeaders = line
				continue
			
			removables = []
			empGroups = line[colHeaders.index("Groups")].split(",") #get all groups employee belongs to
			
			#Loop through all groups and append removables if a group that is removable is found
			for group in empGroups:
				for s in softwareList:
					if contains(group, s):
						additionalAction = ""
						try: #Check if there is an addtional action required to check this software
							additionalAction = softwareDict[s]
						except KeyError: #No additional action for this software; We just pass
							pass
						removables.append(group + " " + additionalAction)
			
			empName = line[colHeaders.index("Name")]
			empFacility = getFacility(line[colHeaders.index("DistinguishedName")].split(",")).replace("OU=", "")
			
			if(len(removables) > 0):
				print("===== " + empName + " | " + empFacility + " =====")
				for s in removables:
					print(s)
				print("")
			else:
				#Add employee to empNoGroup if no removable groups are found
				empNoGroup.append([empName, empFacility, line[colHeaders.index("SamAccountName")].upper()])
		
		#Print out all employees that have no groups
		if(len(empNoGroup) > 0):
			print("==========CHECK IFS==========")
			for empName, empFacility, empSAM in empNoGroup:
				print(empName + " | " + empFacility + " | " + empSAM)
			print("")

applicationWindow = tk.Tk()#create application window context
applicationWindow.withdraw()#Hide random tkinter window

fileTypes = [("Any Termination", "*.txt;*.csv"),("Text Files", "*.txt"),("CSV Files", "*.csv")]#Only allows these file types to be opened
filePath = filedialog.askopenfilename(parent=applicationWindow, filetypes=fileTypes, title="Select file to open")#Prompt user for file to open
fileName, fileExt = os.path.splitext(filePath)#get the file extension of the file being opened

if(fileExt == ".txt"): #TXT files exported from GetGroupMembership
	print("Opening " + filePath + "...\n")
	checkTXT(filePath)
elif(fileExt == ".csv"): #CSV files exported by AD AUDIT ADMIN
	print("Opening " + filePath + "...\n")
	checkCSV(filePath)
else: #An unsupported file type was selected
	print("This aint right")

#Prompt user for input before exiting script execution, SyntaxError is caught if input() if left blank
print("Press Enter to exit...")
try:
	input()
except SyntaxError:
	pass
