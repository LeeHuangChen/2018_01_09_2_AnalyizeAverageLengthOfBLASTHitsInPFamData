import os
import stat
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


#generate all the directories needed for the given path (helper function)
def generateDirectories(path):
	folders=path.split("/")
	curdir=""
	prevFolder=""
	for folder in folders:
		prevFolder=curdir
		curdir=os.path.join(curdir,folder)
		if not os.path.exists(curdir):
			#print curdir
			#os.chmod(prevFolder,stat.S_IWRITE)
			os.mkdir(curdir)

def generateDirectoriesMult(paths):
	for path in paths:
		generateDirectories(path)			

def progressbar(i,length,numberNotification):
	scale=length/numberNotification
	if scale>0:
		if(i%scale==0):
			sys.stdout.write('*')
			if length-i<scale:
				sys.stdout.write('\n')
			sys.stdout.flush()

def progressbarGuide(length):
	sys.stdout.write('|')
	for i in range(0,length-1):
		sys.stdout.write('-')
	sys.stdout.write('|\n')
	sys.stdout.flush()


def histOne(data, numbins, normed=1, facecolor='green', alpha=0.75, label=""):
	print data
	n, bins, patches = plt.hist(data, numbins, normed=normed, facecolor=facecolor, alpha=alpha)

def histographs(datas, numbins, outdir, labels,facecolors, normed=1, alpha=0.75):
	for i, data in enumerate(datas):
		facecolor=facecolors[i]
		label=labels[i]

		n, bins, patches = histOne(data, numbins, normed=normed, facecolor=facecolor, alpha=alpha, label=label)
	plt.legend()
	plt.savefig(outdir)