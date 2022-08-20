from mmap import PROT_READ
import requests
import json

key = "f0f2de8a8e49d99a77fb762cab177c25"
k2C = lambda k: k - 273.15

while True:

    user_city = input("날씨 정보를 원하는 지역을 입력해주세요 : ")

    if user_city == "":
        print("공백은 인식할 수 없습니다.")

    api = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&APPID={key}"
    result = requests.get(api)

    if result.status_code == 200:
        data = json.loads(result.text)
        temp = round(k2C(data["main"]["temp"]),1)
        weather = data["weather"][0]["main"]
        print(data["weather"])
        print(user_city,"의 온도는", temp, "°C")
        print(user_city,"의 날씨는", weather, "입니다.")
        exit()
    else:
        print("다시 입력해주세요")

