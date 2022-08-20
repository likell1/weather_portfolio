import requests
import json

key = "f0f2de8a8e49d99a77fb762cab177c25"
city_list = ["Seoul", "Tokyo", "New York"]
k2C = lambda k: k - 273.15

for city in city_list:
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    result = requests.get(api)
    data = json.loads(result.text)
    
    temp = round(k2C(data["main"]["temp"]),1)
    print(city,"의 온도는", temp, "°C")