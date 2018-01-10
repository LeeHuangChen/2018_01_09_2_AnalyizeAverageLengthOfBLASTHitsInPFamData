import Configurations as conf 
import BlastLengths
import pfamLengths


def main():
	print "running BlastLengths"
	BlastLengths.main()
	
	print "running pfamLengths"
	pfamLengths.main()

if __name__ == '__main__':
	main()