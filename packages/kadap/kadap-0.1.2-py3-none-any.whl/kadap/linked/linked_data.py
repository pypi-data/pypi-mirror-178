import requests

class Linked :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/linked-data/"

    def city(self) :
        res = requests.get(self.url + "city-codes")

        return res.text

    def bicycle(self, city, year, key) :
        category = "bicycle"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def child(self, city, year, key) :
        category = "child"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def freezing(self, city, year, key) :
        category = "freezing"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def holiday(self, city, year, key) :
        category = "holiday"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def jaywalking(self, city, year, key) :
        category = "jaywalking"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def local(self, city, year, key) :
        category = "local"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def motorcycle(self, city, year, key) :
        category = "motorcycle"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def oldman(self, city, year, key) :
        category = "oldman"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def schoolzone(self, city, year, key) :
        category = "schoolzone"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

    def violation(self, city, year, key) :
        category = "violation"
        params = {"city": city, "year": year, "key": key}
        res = requests.get(url=self.url+category, params=params)

        return res.text

# linked = Linked()
# print(linked.oldman("11110", "2013098", "PPjO73QvOu67lL5z%2Bfkfmu6ZASEXqi1yn8ZOJXeocdUQcL%2BXyvyfVDWijWSrYbh%2F"))