import os
import Configurations as conf
import util
from macros import *
import sys
from cPickle import load, dump



def pfamHitLength_File(fileInfo):
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	
	lengthArray=[]
	#proteinLenName=inputfile.replace(conf.pfamExt,conf.protLenExt)
	# with open(os.path.join(conf.protLenFolder,proteinLenName)) as f:
	# 	proteinLengths=load(f)

	with open(os.path.join(inputFolder,inputfile),"r") as f:
		for lineIndex, line in enumerate(f):
			lineInfo=(lineIndex,line)
			#format: first line is header
			#0      1               2               3       4
			#PDB_ID	PdbResNumStart	PdbResNumEnd	eValue	PFAM_ACC
			if lineIndex!=0:
				arr=line.split("\t")
				start=int(arr[1].strip())
				end=int(arr[2].strip())
				difference=end-start
				
				lengthArray.append(difference)
			

	#write the array down and reset the array
	util.generateDirectories(conf.pfamGenFolder)
	outfile=os.path.join(conf.pfamGenFolder,inputfile.replace(conf.pfamExt,".cPickle"))
	with open(outfile,"wb") as f:
		dump(lengthArray, f)
	
	return lengthArray


def analyizeAllLinesInAllFiles():
	forAllFiles(pfamHitLength_File,conf.pfamFolder)

def main():
	analyizeAllLinesInAllFiles()

if __name__ == '__main__':
	main()