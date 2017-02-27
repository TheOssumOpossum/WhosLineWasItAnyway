from keys import *
import speech_recognition as sr
from os import path

longer = path.abspath("longer_recording.wav")
shorter = path.abspath("shorter_recording.wav")

def Transcribe(file):
	r = sr.Recognizer()
	with sr.AudioFile(file) as source:
	    audio = r.record(source) # read the entire audio file

	# recognize speech using Microsoft Bing Voice Recognition
	try:
	    print("Microsoft Bing Voice Recognition thinks you said:\n" + r.recognize_bing(audio, key=BING_KEY_TRANSCRIBE))
	except sr.UnknownValueError:
	    print("Microsoft Bing Voice Recognition could not understand audio")
	except sr.RequestError as e:
	    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
