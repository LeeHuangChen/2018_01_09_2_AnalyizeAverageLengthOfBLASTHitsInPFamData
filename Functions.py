import os
import Configurations as conf
import util
from macros import *
import sys
from cPickle import load, dump
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy

def BLASTHitLength_File(fileInfo):
	lengthArray=[]
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	lineIndex=0

	proteinLenName=inputfile.replace(conf.blastExt,conf.protLenExt)
	with open(os.path.join(conf.protLenFolder,proteinLenName)) as f:
		proteinLengths=load(f)

	with open(os.path.join(inputFolder,inputfile),"r") as f:
		for lineIndex, line in enumerate(f):
			lineInfo=(lineIndex,line)
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
				lengthArray.append(alignlen)
			

	#write the array down and reset the array
	#util.generateDirectories(conf.blastGenFolder)
	#outfile=os.path.join(conf.blastGenFolder,inputfile.replace(conf.blastExt,".cPickle"))
	# with open(outfile,"wb") as f:
	# 	dump(lengthArray, f)
	
	return lengthArray

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


def generateHistograms(fileInfo):
	util.generateDirectories(conf.histogramFolder)
	pfamArr=pfamHitLength_File(fileInfo)
	

	blastFilename=fileInfo[2].replace(conf.pfamExt, conf.blastExt)
	fileInfoMod=(fileInfo[0],conf.blastFolder, blastFilename)
	blastArr=BLASTHitLength_File(fileInfoMod)

	
	numbins=100
	maxnum=max(numpy.amax(blastArr),numpy.amax(pfamArr))
	bins = numpy.linspace(0, maxnum, numbins)

	plt.hist(pfamArr, bins, normed=1,facecolor="red", alpha=.75, label="pfam")
	plt.hist(blastArr, bins, normed=1,facecolor="blue", alpha=.25, label="blast")
	
	histoutname=fileInfo[2].replace(conf.pfamExt, ".png")
	outdir=os.path.join(conf.histogramFolder,histoutname)

	plt.legend()
	plt.savefig(outdir)
	plt.close()


def analyizeAllLinesInAllFiles():
	forAllFiles(generateHistograms,conf.pfamFolder)

def main():
	analyizeAllLinesInAllFiles()

if __name__ == '__main__':
	main()