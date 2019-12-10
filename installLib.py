#!/usr/bin/python
import os
import sys
import shutil

# A library for building install scripts.

# Find where this .py file is running from.
rootPath = sys.argv[0][0:sys.argv[0].rfind(os.sep)]

# Utility function to convert Unix-style path strings to Windows ones.
def toWindowsPath(thePath):
	return(thePath.replace("/", "\\"))

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
    
def writeFile(theFilename, theFileData):
	fileDataHandle = open(theFilename, "wb")
	fileDataHandle.write(theFileData)
	fileDataHandle.close()

def replaceVariables(theFile, theKeyValues):
	fileData = readFile(theFile)
	for keyValue in theKeyValues.keys():
		fileData = fileData.replace("<<" + keyValue + ">>", theKeyValues[keyValue])
	writeFile(theFile, fileData)
