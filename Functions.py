import os
import Configurations as conf
import util
from macros import *

def printName(fileInfo):
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	print inputfile

def printLine(fileInfo,lineInfo):
	lineIndex=lineInfo[0]
	line=lineInfo[1]
	print line

def printAllLinesInFile(fileInfo):
	forAllLineInFile(fileInfo,printLine)

def printAllLinesInAllFiles():
	forAllInputFiles(printAllLinesInFile,conf.inputFolder)


def printAllNames():
	forAllInputFiles(printName,conf.inputFolder)

def test():
	#printAllNames()
	printAllLinesInAllFiles()
	

def main():
	test()

if __name__ == '__main__':
	main()