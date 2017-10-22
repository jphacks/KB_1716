# coding:utf-8
import httplib, urllib, base64, json
import trimming
import choice
import drunkjudge
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
body = open(args[1], 'rb')

img = cv2.imread(args[1])

if True:
    # Execute the REST API call and get the response.
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)

    file_name = args[1]
    if len(parsed) == 2:

        for i in range(2):
            height = parsed[i]['faceRectangle']['height']
            left = parsed[i]['faceRectangle']['left']
            top = parsed[i]['faceRectangle']['top']
            width = parsed[i]['faceRectangle']['width']
            #trimming.trimming(img,top,left,height,width,args[1],i)

        A = {'x':parsed[0][u'faceRectangle'][u'left']}
        #A[u'drunk'] = drunkjudge.drunkjudge(file_name + "0.png")
        A[u'anger'] = parsed[0][u'faceAttributes'][u'emotion'][u'anger']
        A[u'contempt'] = parsed[0][u'faceAttributes'][u'emotion'][u'contempt']
        A[u'disgust'] = parsed[0][u'faceAttributes'][u'emotion'][u'disgust']
        A[u'fear'] = parsed[0][u'faceAttributes'][u'emotion'][u'fear']
        A[u'happiness'] = parsed[0][u'faceAttributes'][u'emotion'][u'happiness']
        A[u'neutral'] = parsed[0][u'faceAttributes'][u'emotion'][u'neutral']
        A[u'sadness'] = parsed[0][u'faceAttributes'][u'emotion'][u'sadness']
        A[u'surprise'] = parsed[0][u'faceAttributes'][u'emotion'][u'surprise']
        A[u'exposure'] = parsed[0][u'faceAttributes'][u'exposure'][u'value']

        B = {'x':parsed[1][u'faceRectangle'][u'left']}
        #B[u'drunk'] = drunkjudge.drunkjudge(file_name + "1.png")
        B[u'contempt'] = parsed[1][u'faceAttributes'][u'emotion'][u'contempt']
        B[u'disgust'] = parsed[1][u'faceAttributes'][u'emotion'][u'disgust']
        B[u'fear'] = parsed[1][u'faceAttributes'][u'emotion'][u'fear']
        B[u'happiness'] = parsed[1][u'faceAttributes'][u'emotion'][u'happiness']
        B[u'neutral'] = parsed[1][u'faceAttributes'][u'emotion'][u'neutral']
        B[u'sadness'] = parsed[1][u'faceAttributes'][u'emotion'][u'sadness']
        B[u'surprise'] = parsed[1][u'faceAttributes'][u'emotion'][u'surprise']
        B[u'exposure'] = parsed[1][u'faceAttributes'][u'exposure'][u'value']

        ret = choice.choice(A, B)

        sys.stdout.write(ret[0])
        sys.stdout.write(' ')
        sys.stdout.write(ret[1])

    else:
        if len(parsed) < 2:
            sys.stdout.write("-1 ツーショットを撮ってください")
        else:
            sys.stdout.write("-1 人数が多すぎます")

    conn.close()

#except Exception as e:
    #print("[Errno {0}] {1}".format(e.errno, e.strerror))
####################################
