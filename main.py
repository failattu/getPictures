import json
import os
import requests
import shutil

token = ""
facebookurl = "graph.facebook.com"
version = "v2.3"
idol = "https://api.idolondemand.com/1/api/sync/detectfaces/v1"
apikey = ""
userid= "me"
def fbtokenize (param):
    params = param+"&access_token=" +token
    return params
def fbget(params, path):
    url = 'https://' + facebookurl +"/"+ version +"/"+ path +"/?"+ params
    r = requests.get(url)
    print(r)
    return json.loads(r.text)

def downloadpic(url, id,folder):
    r = requests.get(url, stream=True)
    with open(folder+'/'+id + ".jpg", 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    del r

def idolondemand (picturename):
    file_path ="picture/"+picturename +".jpg"
    files = [(picturename +".jpg", (file_path, open(file_path, 'rb'), "image/jpeg" ))]
    urls = idol + "?apikey="+apikey+"&file="+picturename
    data = {"apikey":apikey, "file":picturename+".jpg"}
    r = requests.post(urls, data=data,files=files)
    faceinfo =  json.loads(r.text)
    for info in faceinfo["face"]:
        if info["width"]:
            return True
    return False
def fetchpic(data):
    try:
        for photos in data['albums']['data']:
            for picture in photos["photos"]["data"]:
                print(picture["picture"])
                print(picture["id"])
                downloadpic(picture["picture"],picture["id"],"picture")
                face = idolondemand(picture["id"])
                if face:
                    os.rename("picture/"+picture["id"]+".jpg", "face/"+picture["id"]+".jpg")
    except KeyError:
        print("No more pictures add paging")
path = userid
param = "fields=albums{photos{picture}}"

params = fbtokenize(param)
data = fbget(params, path)
fetchpic(data)

