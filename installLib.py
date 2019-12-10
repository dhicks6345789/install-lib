#!/usr/bin/python
import os
import sys
import ssl
import shutil
import urllib.request

# Handy utility function to write a file.
def writeFile(theFilename, theFileData):
	fileDataHandle = open(theFilename, "wb")
	fileDataHandle.write(theFileData)
	fileDataHandle.close()
	
# Make sure Pip is installed.
if os.name == "nt":
	pythonHome = sys.executable.rsplit(os.sep, 1)[0]
	pipExe = pythonHome + os.sep + "Scripts" + os.sep + "pip.exe"
	if not os.path.exists(pipExe):
		response = urllib.request.urlopen("https://bootstrap.pypa.io/get-pip.py", context=ssl._create_unverified_context())
		writeFile("get-pip.py", response.read())
		os.system("py get-pip.py")
		os.remove("get-pip.py")
	os.system(pipExe)
#import pexpect

# Set up a couple of globals to hold user options.
validValueOptions = []
userOptions = {}

# If the given option name has been set on the command line, simply returns that value as a string.
# Otherwise, asks the user for a value via interactive input and returns that value as a string.
def getUserOption(optionName, theMessage):
	# Parse any options set by the user on the command line.
	if userOptions == {}:
		validBooleanOptions = []
		optionCount = 1
		while optionCount < len(sys.argv):
			if sys.argv[optionCount] in validBooleanOptions:
				userOptions[sys.argv[optionCount]] = True
			elif sys.argv[optionCount] in validValueOptions:
				userOptions[sys.argv[optionCount]] = sys.argv[optionCount+1]
				optionCount = optionCount + 1
			optionCount = optionCount + 1
	if not optionName in userOptions.keys():
		userOptions[optionName] = input(theMessage + ": ")
	return(userOptions[optionName])

# Utility function to convert Unix-style path strings to Windows ones.
def toWindowsPath(thePath):
	return(thePath.replace("/", "\\"))

# Runs the given command only if the given path is missing. Handy for "run this command to install
# X if it isn't installed yet" type commands.
def runIfPathMissing(thePath, theCommand):
	if not os.path.exists(thePath):
		print("Running: " + theCommand)
		os.system(theCommand)

def mkdir(theDir):
	if not os.path.exists(theDir):
		print("Creating " + theDir)
		os.makedirs(theDir)

def copyfile(src, dest, mode=None):
	srcStat = os.stat(src)
	if (not os.path.exists(dest)) or (not str(srcStat.st_mtime) == str(os.stat(dest).st_mtime)):
		print("Copying file " + src + " to " + dest)
		shutil.copyfile(src, dest)
		os.utime(dest, (srcStat.st_atime, srcStat.st_mtime))
		if not mode == None:
			os.chmod(dest, mode)
		return(1)
	return(0)

def copyfolder(srcFolder, destFolder):
	print("Copying folder " + srcFolder + " to " + destFolder)
	if not os.path.isdir(destFolder):
		mkdir(destFolder)
	for item in os.listdir(srcFolder):
		if os.path.isfile(srcFolder + os.sep + item):
			copyfile(srcFolder + os.sep + item, destFolder + os.sep + item)
		else:
			copyfolder(srcFolder + os.sep + item, destFolder + os.sep + item)

def runCommand(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.readlines()
	commandHandle.close()
	return(result)

def readFile(theFilename):
	fileDataHandle = open(theFilename, "rb")
	fileData = fileDataHandle.read()
	fileDataHandle.close()
	return(fileData)

def replaceVariables(theFile, theKeyValues):
	fileData = readFile(theFile)
	for keyValue in theKeyValues.keys():
		fileData = fileData.replace("<<" + keyValue + ">>", theKeyValues[keyValue])
	writeFile(theFile, fileData)
	
def runExpect(inputArray):
	writeFile("temp.expect", inputArray)
	os.system("expect temp.expect")
	os.system("rm temp.expect")
