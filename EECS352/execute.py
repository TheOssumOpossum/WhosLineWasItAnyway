from keys import *
import audio_transcription as AT
import speaker_recognition as SR
import split_audio as SA
from os import path, listdir
from os.path import isfile, join

testname = 'LatvianSports'

Obama_Interview = path.abspath('Obama_Interview_16.wav')
LatvianSports = path.abspath('testing_data//LatvianSports.wav')
#AT.Transcribe(LatvianSports)
#NumberOfSections = SA.split_audio(Obama_Interview,2,ExportName=testname)
NumberOfSections = SA.split_audio(LatvianSports,3,ExportName=testname,split='start',parameter='log')


filelist = [f for f in listdir(path.abspath('AudioSegments//')) if isfile(join(path.abspath('AudioSegments//'),f))]
relevant_files = []
for file in filelist:
	if testname in file:
		relevant_files += [path.abspath('AudioSegments//' + file)]

i = 0

for file in relevant_files:
	print("-----------------------------------")
	print("File number ",i)
	print("-----------------------------------")
	print("Processing File: " ,file)
	SR.IdentifySpeaker(everybody,file)
	AT.Transcribe(file)
	i+= 1
	if (i >= NumberOfSections):
		break
	print("-----------------------------------")