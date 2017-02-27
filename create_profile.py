########### Python 2.7 #############
import httplib, urllib, base64, json
from bing_key import *

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': BING_KEY_SPEAKER,
}

params = urllib.urlencode({
})



try:
    body = json.dumps({'locale': 'en-us'})
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################