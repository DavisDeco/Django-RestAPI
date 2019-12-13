import json
import requests
import os

ENDPOINT = "http://127.0.0.1:8000/api/status/"

image_path = os.path.join(os.getcwd(),"Arifu_Logo_Transparent.png")

def do_img(method='get', data={}, is_json=True, img_path=None):
    header = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
        if img_path is not None:
            with open(image_path,'rb') as image:
                file_data = {
                    'image' : image
                }
            r = request.request(method,ENDPOINT,data=data,files=file_data)
        else:
            r = request.request(method,ENDPOINT,data=data,headers=headers)
        print(r.text)
        print(r.status_code)
        return r

do_img(method='post',data={'user':1,"content":""},is_json=False)

def do(method='get', data={}, is_json=True):
    header = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
        r = request.request(method,ENDPOINT,data=data,headers=headers)
        print(r.text)
        print(r.status_code)
        return r