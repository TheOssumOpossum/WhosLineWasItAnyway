########### Python 2.7 #############
import httplib, urllib, base64, json
from bing_key import *
from os import path

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': BING_KEY_SPEAKER,
}

params = urllib.urlencode({
    # Request parameters
    'shortAudio': '{True}',
    'identificationProfileId': '550a4af8-08c6-43a5-aac7-ba2a830e56a8',
})

file_path = path.join(path.dirname(path.realpath(__file__)), "Recording.wav")
print file_path+2

try:
    with open(file_path,'rb') as body:
        print body
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/spid/v1.0/identificationProfiles/{identificationProfileId}/enroll?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
