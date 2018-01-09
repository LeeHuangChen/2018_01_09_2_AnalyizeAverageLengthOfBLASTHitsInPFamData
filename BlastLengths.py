import os
import Configurations as conf
import util
from macros import *
import sys
from cPickle import load, dump

lengthArray=[]

def BLASTHitLength(line,proteinLengths):
	global lengthArray
	#format:
	#0    , 1      , 2  , 3       , 4       , 5      , 6  , 7   , 8  , 9   , 10    , 11
	#query, subject, %id, alignlen, mismatch, gapopen, qst, qend, sst, send, Evalue, bitscore
		#query/subject format:
		#1DXZ:sp|P02710.1|ACHA_TETCF
	

	arr=line.split("\t")

	threshold=conf.threshold
	doThresholdMethod=conf.doThresholdMethod



	qLen=proteinLengths[arr[0]]
	sLen=proteinLengths[arr[1]]
	alignlen=int(arr[3].strip())
	
	#overlap on query is "pretty close" to the entire protein
	qThresh=float(abs(alignlen - qLen)) < (qLen*threshold)

	#overlap on subject is "pretty close" to the entire protein
	sThresh=float(abs(alignlen - sLen)) < (sLen*threshold)

	if doThresholdMethod:
		if not qThresh and not sThresh:
			lengthArray.append(alignlen)
	else:
		total+=alignlen
		counter+=1


def BLASTHitLength_File(fileInfo):
	global lengthArray
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	lineIndex=0

	proteinLenName=inputfile.replace(conf.blastExt,conf.protLenExt)
	with open(os.path.join(conf.protLenFolder,proteinLenName)) as f:
		proteinLengths=load(f)

	with open(os.path.join(inputFolder,inputfile),"r") as f:
		for line in iter(f):
			lineInfo=(lineIndex,line)
			BLASTHitLength(line,proteinLengths)
			lineIndex+=1

	#write the array down and reset the array
	util.generateDirectories(conf.blastGenFolder)
	outfile=os.path.join(conf.blastGenFolder,inputfile.replace(conf.blastExt,".cPickle"))
	with open(outfile,"wb") as f:
		dump(lengthArray, f)
	#print len(lengthArray)
	lengthArray=[]

def analyizeAllLinesInAllFiles():
	forAllFiles(BLASTHitLength_File,conf.blastFolder)

def main():
	analyizeAllLinesInAllFiles()

if __name__ == '__main__':
	main()