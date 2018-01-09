import os
import Configurations as conf
import util
from macros import *
import sys
from cPickle import load, dump

lengthArray=[]

def pfamHitLength(lineIndex,line):
	global lengthArray
	
	
	#format: first line is header
	#0      1               2               3       4
	#PDB_ID	PdbResNumStart	PdbResNumEnd	eValue	PFAM_ACC
	if lineIndex!=0:
		arr=line.split("\t")
		start=int(arr[1].strip())
		end=int(arr[2].strip())
		difference=end-start
		
		lengthArray.append(difference)



def pfamHitLength_File(fileInfo):
	global lengthArray
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	lineIndex=0

	#proteinLenName=inputfile.replace(conf.pfamExt,conf.protLenExt)
	# with open(os.path.join(conf.protLenFolder,proteinLenName)) as f:
	# 	proteinLengths=load(f)

	with open(os.path.join(inputFolder,inputfile),"r") as f:
		for line in iter(f):
			lineInfo=(lineIndex,line)
			pfamHitLength(lineIndex,line)
			lineIndex+=1

	#write the array down and reset the array
	util.generateDirectories(conf.pfamGenFolder)
	outfile=os.path.join(conf.pfamGenFolder,inputfile.replace(conf.pfamExt,".cPickle"))
	with open(outfile,"wb") as f:
		dump(lengthArray, f)
	
	print len(lengthArray)
	
	lengthArray=[]


def analyizeAllLinesInAllFiles():
	forAllFiles(pfamHitLength_File,conf.pfamFolder)

def main():
	analyizeAllLinesInAllFiles()

if __name__ == '__main__':
	main()