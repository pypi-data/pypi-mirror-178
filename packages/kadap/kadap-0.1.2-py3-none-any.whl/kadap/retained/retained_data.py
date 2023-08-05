import requests

class Retained :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/retained-data/retained"
        # self.url = "http://bigdata-car.iptime.org:3455/APIs/retained-data/retained"

    def getData(self, id) :
        params = {"ID": id}
        res = requests.get(url=self.url, params=params)
        # print(res)

        return res.text

retained = Retained()
print(retained.getData(id="maintenance"))