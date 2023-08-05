import cv2
import base64
import requests
import numpy as np

class Benchmarking :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/detecting-model-benchmarking"

    def getResult(self, source, height=640, width=640) :
        params = {"source": source, "height": height, "width": width}
        res = requests.get(url=self.url, params=params)

        return res.text

    def getImg_origin(self, source) :
        category = "origin"
        url = self.url + "/images/" + category
        params = {"source": source}
        res = requests.get(url=url, params=params)
        
        data = base64.b64decode(res.text)
        jpg_arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

        b, g, r = cv2.split(img)
        img_ = cv2.merge([r, g, b])

        return img_

    def getImg_bbox(self, source) :
        category = "bbox"
        url = self.url + "/images/" + category
        params = {"source": source}
        res = requests.get(url=url, params=params)
        
        data = base64.b64decode(res.text)
        jpg_arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

        b, g, r = cv2.split(img)
        img_ = cv2.merge([r, g, b])

        return img_    

benchmarking = Benchmarking()
# result = benchmarking.getResult(source="http://www.prixmotor.es/wp-content/uploads/2022/03/7K1A5572-scaled.jpg")
# print(benchmarking.getImg_origin("7K1A5572-scaled.jpg"))