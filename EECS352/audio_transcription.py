from keys import *
import speech_recognition as recog
from os import path

longer = path.abspath("longer_recording.wav")
shorter = path.abspath("shorter_recording.wav")

def Transcribe(file):
	r = recog.Recognizer()
	with recog.AudioFile(file) as source:
	    audio = r.record(source) # read the entire audio file

	transcription = ""
	# recognize speech using Microsoft Bing Voice Recognition
	try:
		transcription = r.recognize_bing(audio, key=BING_KEY_TRANSCRIBE)
		#print("Microsoft Bing Voice Recognition thinks you said:\n" + transcription)
	except recog.UnknownValueError:
	    print("Microsoft Bing Voice Recognition could not understand audio")
	except recog.RequestError as e:
	    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
	return transcription
