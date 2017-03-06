from keys import *
import http.client, urllib.request, urllib.parse, urllib.error, base64, json,logging
from keys import *
from os import path
from contextlib import closing
import IdentifyFile


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

def CreateProfile():
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
	    print(data)
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

def IdentifySpeaker(speakerIds,file):
	IdentifyFile.identify_file(BING_KEY_SPEAKER, file, 'true', speakerIds)