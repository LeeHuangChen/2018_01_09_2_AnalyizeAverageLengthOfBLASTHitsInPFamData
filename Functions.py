import os
import Configurations as conf
import util
from macros import *
import sys
from cPickle import load

total=0
counter=0
protLenFile="00036_Neur_chan_memb_protLen.cPickle"
protLenFilePath=os.path.join(conf.inputFolder,protLenFile)
proteinLengths=load(open(protLenFilePath))

def calculateAverageLenInBLAST(fileInfo,lineInfo):
	global total,counter,proteinLengths
	#format:
	#0    , 1      , 2  , 3       , 4       , 5      , 6  , 7   , 8  , 9   , 10    , 11
	#query, subject, %id, alignlen, mismatch, gapopen, qst, qend, sst, send, Evalue, bitscore
		#query/subject format:
		#1DXZ:sp|P02710.1|ACHA_TETCF
	
	lineIndex=lineInfo[0]
	line=lineInfo[1]
	

	arr=line.split("\t")

	threshold=.10
	doThresholdMethod=True



	qLen=proteinLengths[arr[0]]
	sLen=proteinLengths[arr[1]]
	alignlen=int(arr[3].strip())
	
	#overlap on query is "pretty close" to the entire protein
	qThresh=float(abs(alignlen - qLen)) < (qLen*threshold)

	#overlap on subject is "pretty close" to the entire protein
	sThresh=float(abs(alignlen - sLen)) < (sLen*threshold)

	if doThresholdMethod:
		if not qThresh and not sThresh:
			#sys.stdout.write(arr[3])
			#sys.stdout.write(", ")
			#sys.stdout.flush()
			total+=alignlen
			counter+=1
			with open(os.path.join(conf.resultFolder,fileInfo[2]),"a") as f:
				f.write(str(alignlen)+"\n")
	else:
		total+=alignlen
		counter+=1

def calculateAverageLenInPFam(fileInfo,lineInfo):
	global total,counter
	lineIndex=lineInfo[0]
	line=lineInfo[1]
	#format: first line is header
	#0      1               2               3       4
	#PDB_ID	PdbResNumStart	PdbResNumEnd	eValue	PFAM_ACC
	if lineIndex!=0:
		arr=line.split("\t")
		start=int(arr[1].strip())
		end=int(arr[2].strip())
		difference=end-start
		total+=difference
		counter+=1

		with open(os.path.join(conf.resultFolder,fileInfo[2]),"a") as f:
			f.write(str(difference)+"\n")

def printAllLinesInAllFiles():
	global total,counter

	util.generateDirectories(conf.resultFolder)
	
	print "Blast average hit length:"
	forAllLineInFile((0,conf.inputFolder,"00036_Neur_chan_memb_alltoall.txt"),calculateAverageLenInBLAST)
	print float(total)/counter


	total=0
	counter=0


	print "PFam average domain length:"
	forAllLineInFile((0,conf.inputFolder,"Neur_chan_memb.txt"),calculateAverageLenInPFam)
	print float(total)/counter
	


def test():
	printAllLinesInAllFiles()
	

def main():
	test()

if __name__ == '__main__':
	main()