#!/usr/bin/python
import os
import sys
import ssl
import shutil
import urllib.request

# Handy utility function to write a file.
def writeFile(theFilename, theFileData):
	fileDataHandle = open(theFilename, "wb")
	if isinstance(theFileData, str):
		fileDataHandle.write(theFileData.encode())
	else:
		fileDataHandle.write(theFileData)
	fileDataHandle.close()
	
def runCommand(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.readlines()
	commandHandle.close()
	return(result)

userHome = os.path.expanduser("~")

# Set up globals to hold Python details.
pythonHome = ""
pipExe = ""

# Figure out what version of Python we have installed.
pythonVersion = "Unknown"
if os.name == "nt":
	for dirLine in runCommand("dir \"C:\\Program Files\""):
		dirSplit = dirLine.split()
		if len(dirSplit) > 2:
			if dirSplit[3].lower().startswith("python"):
				pythonVersion = dirSplit[3].strip()
else:
	pythonVersion = os.popen("ls /usr/local/lib | grep python3").read().strip()

# Make sure Pip is installed, then check for individual Python modules.
if os.name == "nt":
	pythonHome = sys.executable.rsplit(os.sep, 1)[0]
	pipExe = pythonHome + os.sep + "Scripts" + os.sep + "pip.exe"
	if not os.path.exists(pipExe):
		response = urllib.request.urlopen("https://bootstrap.pypa.io/get-pip.py", context=ssl._create_unverified_context())
		writeFile("get-pip.py", response.read())
		os.system("py get-pip.py")
		os.remove("get-pip.py")

# Set up a couple of globals to hold user options.
userOptions = {}
validValueOptions = []
validBooleanOptions = []

# If the given option name has been set on the command line, simply returns that value as a string.
# Otherwise, asks the user for a value via interactive input and returns that value as a string.
def getUserOption(optionName, theMessage):
	# Parse any options set by the user on the command line.
	if userOptions == {}:
		optionCount = 1
		while optionCount < len(sys.argv):
			if sys.argv[optionCount] in validBooleanOptions:
				userOptions[sys.argv[optionCount]] = True
			elif sys.argv[optionCount] in validValueOptions:
				userOptions[sys.argv[optionCount]] = sys.argv[optionCount+1]
				optionCount = optionCount + 1
			else:
				print("Error - option " + sys.argv[optionCount] + " not valid.")
			optionCount = optionCount + 1
	if not optionName in userOptions.keys():
		userOptions[optionName] = input(theMessage + ": ")
	return(userOptions[optionName])

# Runs the given command only if the given path is missing. Handy for "run this command to install
# X if it isn't installed yet" type commands.
def runIfPathMissing(thePath, theCommand):
	if not os.path.exists(thePath):
		print("Running: " + theCommand)
		os.system(theCommand)

# Utility function to convert Unix-style path strings to Windows ones.
def toWindowsPath(thePath):
	return(thePath.replace("/", "\\"))

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
