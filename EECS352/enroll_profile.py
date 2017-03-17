import http.client, urllib.request, urllib.parse, urllib.error, base64, json
from bing_key import *
from os import path


#User Enrollment
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': BING_KEY_SPEAKER,
}

params = urllib.parse.urlencode({
    'shortAudio': 'true',
})

body = open('recording_mono_16.wav','rb')

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/identificationProfiles/{0}/enroll?{1}".format(speaker1, params), body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))