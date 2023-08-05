import requests

class VIN :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/vin-decoder"
    
    def decoded(self, vin) :
        params = {"VIN": vin}
        res = requests.get(url=self.url, params=params)

        return res.text

# vin = VIN()
# print(vin.decoded("KMHEM44CPLU123456"))