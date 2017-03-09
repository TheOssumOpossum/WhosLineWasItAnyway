from keys import *
import audio_transcription as AT
import speaker_recognition as SR
import split_audio as SA
from os import path, listdir
from os.path import isfile, join

testname = 'ObamaTest'

Obama_Interview = path.abspath('Obama_Interview_16.wav')
AT.Transcribe(Obama_Interview)
SA.split_audio(Obama_Interview,2,testname)


filelist = [f for f in listdir(path.abspath('AudioSegments//')) if isfile(join(path.abspath('AudioSegments//'),f))]
relevant_files = []
for file in filelist:
	if testname in file:
		relevant_files += [path.abspath('AudioSegments//' + file)]

for file in relevant_files:
	print("Can't currently identify or transcribe due to format:" ,file)
	#SR.IdentifySpeaker(vin_and_obama,file)