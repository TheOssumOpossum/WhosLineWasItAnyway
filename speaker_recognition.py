import http.client, urllib.request, urllib.parse, urllib.error, base64, json,logging,pickle
from keys import *
import os
from contextlib import closing
import IdentifyFile
from scipy.io import wavfile as wavf


def EnrollProfile(speakerId,file):
	#User Enrollment
	headers = {
	    # Request headers
	    'Content-Type': 'application/octet-stream',
	    'Ocp-Apim-Subscription-Key': BING_KEY_SPEAKER,
	}

	params = urllib.parse.urlencode({
	    'shortAudio': 'true',
	})

	body = open(file,'rb')

	try:
	    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/spid/v1.0/identificationProfiles/{0}/enroll?{1}".format(speakerId, params), body, headers)
	    response = conn.getresponse()
	    data = response.read()
	    print(data)
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

def CreateProfile(name=None):
	if name is None:
		print("Please give a name")
		return
	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': BING_KEY_SPEAKER,
	}

	params = urllib.parse.urlencode({
	})

	body = json.dumps({'locale': 'en-us'})

	try:
	    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, body, headers)
	    response = conn.getresponse()
	    data = response.read()
	    #print(data)
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))
	newid = str(data).split("\"")[3]
	print("Created Profile #: ",newid)
	IdDictionary[newid] = name
	pickle.dump(IdDictionary,open("idDict.p","wb"))
	return newid

def IdentifySpeaker(speakerIds,file):
	return IdentifyFile.identify_file(BING_KEY_SPEAKER, file, 'true', speakerIds)

def generateEnrollAudio(file, start_time, end_time):
	rate, full_file = wavf.read(file)
	start_sample = rate * start_time
	end_sample = rate * end_time
	enrollAudio = full_file[int(start_sample):int(end_sample)]
	wavf.write('enrollment_audio.wav', rate, enrollAudio)
	return enrollAudio

def automatedProfileEnrollment(STarr, file):
	for arr in STarr:
		speaker = arr[0]
		start = arr[1]
		end = arr[2]
		speakerID = CreateProfile(name=speaker)
		eAudio = generateEnrollAudio(file, start, end)
		EnrollProfile(speakerID, 'enrollment_audio.wav')
	



