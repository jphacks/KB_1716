import httplib, urllib, base64, json
import trimming
import sys
import cv2

args = sys.argv

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'f129ff39951f44389bb7ce898ec23c14'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'

# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})

# The URL of a JPEG image to analyze.
#body = "{'url':'http:q//www.aflo.com/creative/people/img/mainImg.jpg'}"
body = open(args[1],'rb')

img = cv2.imread(args[1] )

try:
    # Execute the REST API call and get the response.
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    for i in range(len(parsed)):
        print('-------------------------')
        height = parsed[i]['faceRectangle']['height']
        left = parsed[i]['faceRectangle']['left']
        top = parsed[i]['faceRectangle']['top']
        width = parsed[i]['faceRectangle']['width']
    	print('height{0}:{1}'.format(i,height))
    	print('left{0}:{1}'.format(i,left))
    	print('top{0}:{1}'.format(i,top))
    	print('width{0}:{1}'.format(i,width))
        trimming.trimming(img,top,left,height,width,args[1],i)
    	print('-------------------------')
    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
####################################