#written python 2.7
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS

def PreProcess(file):
	#returns numberofsegments in textfile
	[Fs, x] = aIO.readAudioFile(file)
	segments = aS.silenceRemoval(x, Fs, 0.020, 0.020, smoothWindow = 1.0, Weight = 0.3, plot = False)
	f = open('numberofsegments.txt', 'w')
	f.write(str(len(segments)))	
	f.truncate()
	f.close()
	print(str(len(segments)))
