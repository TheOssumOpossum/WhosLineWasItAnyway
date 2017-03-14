from keys import *
import audio_transcription as AT
import speaker_recognition as SR
import split_audio as SA
from os import path, listdir
from os.path import isfile, join

def Transcript(fullaudio=None,possibleSpeakers=[],segmentnames='test',numberOfsplits=5,split_type='start',parameter='log',debug=False):
	NumberOfSections = SA.split_audio(fullaudio,numberOfsplits,ExportName=segmentnames,split=split_type,parameter=parameter)
	filelist = [f for f in listdir(path.abspath('AudioSegments//')) if isfile(join(path.abspath('AudioSegments//'),f))]
	relevant_files = []
	for file in filelist:
		if segmentnames in file:
			relevant_files += [path.abspath('AudioSegments//' + file)]

	i = 0

	transcript = ""

	if debug:
		for file in relevant_files:
			print("-----------------------------------")
			print("File number ",i)
			print("-----------------------------------")
			print("Processing File: " ,file)
			SR.IdentifySpeaker(possibleSpeakers,file)
			AT.Transcribe(file)
			i+= 1
			if (i >= NumberOfSections):
				break
			print("-----------------------------------")
	else:
		print(segmentnames + " Transcript:\n")
		for file in relevant_files:
			speaker, confidence = SR.IdentifySpeaker(possibleSpeakers,file)
			text = AT.Transcribe(file)
			printText = "("+confidence[0:]+" confidence)"+IdDictionary[speaker]+": "+text
			print(printText)
			printText += "\n"
			transcript += printText
			i += 1
			if (i >= NumberOfSections):
				break
		transcript += "\n"
	text_file = open(segmentnames+".txt", "w")
	text_file.write(transcript)
	text_file.close()
	return transcript