import os
def forAllLineInFile(fileInfo, doworkwithline):
	#fileInfo=(fileIndex, inputFolder, inputfile)
	inputFolder=fileInfo[1]
	inputfile=fileInfo[2]
	lineIndex=0
	with open(os.path.join(inputFolder,inputfile),"r") as f:
		for line in iter(f):
			lineInfo=(lineIndex,line)
			doworkwithline(fileInfo,lineInfo)
			lineIndex+=1


def forAllInputFiles(doworkwithfile,folder):
	inputfiles=os.listdir(folder)

	for i, inputfile in enumerate(inputfiles):
		fileInfo=(i,folder, inputfile)
		doworkwithfile(fileInfo)