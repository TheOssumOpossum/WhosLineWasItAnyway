from keys import *
import audio_transcription as AT
import speaker_recognition as SR
import split_audio as SA
from os import path, listdir
from os.path import isfile, join
from scipy.io import wavfile as wavf

def Project(STarr,file,name='test'):
	speakerDictionary = automatedProfileEnrollment(STarr,file)
	f = open('numberofsegments.txt','t')
	splits = 2#int(f.read())
	transcript = Create_Transcript(file,speakerDictionary,name,2)
	#look for the file called name.txt
	return transcript

def generateEnrollAudio(file, start_time, end_time):
	#segments an audio file
	#returns array of audio
	rate, full_file = wavf.read(file)
	start_sample = rate * start_time
	end_sample = rate * end_time
	enrollAudio = full_file[int(start_sample):int(end_sample)]
	wavf.write('enrollment_audio.wav', rate, enrollAudio)
	return enrollAudio

def automatedProfileEnrollment(STarr, file):
	#takes an array of arrays
	#every row is a (speaker,start_time,end_time) for a given audio file
	#returns dictionary of speaker ids key:speakerId, value:name
	speakerDictionary = {}
	for arr in STarr:
		speaker = arr[0]
		start = arr[1]
		end = arr[2]
		if not speaker in speakerDictionary.values():#if enrolling new speaker
			speakerID = SR.CreateProfile(name=speaker)
			speakerDictionary[speakerID] = speaker#add entry to dictionary
		else:
			for key in speakerDictionary.keys():#look for exisiting entry in dictionary
				if speakerDictionary[key] == speaker:
					speakerID = key
		eAudio = generateEnrollAudio(file, start, end)
		SR.EnrollProfile(speakerID, 'enrollment_audio.wav')
	return speakerDictionary

def Create_Transcript(fullaudio=None,possibleSpeakers={},segmentnames='test',numberOfsplits=5,split_type='start',parameter='log',debug=False):
	#fullaudio-Audio file to transcribe
	#possibleSpeakers-Dictionary, names are keys, ids are values
	#segmentnames-segments will be saved as xxxx_segment_n.wav
	#numberOfsplits - estimated number of changes in speakers
	#split_type- 'start' or 'neighbor' affects how the similarity matrix is processed
	#parameter - 'log' 'mfcc' 'chroma' similarity matrix
	#debug - if true doesn't print out the transcript
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
			SR.IdentifySpeaker(possibleSpeakers.keys(),file)
			AT.Transcribe(file)
			i+= 1
			if (i >= NumberOfSections):
				break
			print("-----------------------------------")
	else:
		print(segmentnames + " Transcript:\n")
		transcript += segmentnames + " Transcript:\n"
		for file in relevant_files:
			speaker, confidence = SR.IdentifySpeaker(possibleSpeakers.keys(),file)
			text = AT.Transcribe(file)
			printText = "("+confidence[0:]+" confidence)"+possibleSpeakers[speaker]+": "+text
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
