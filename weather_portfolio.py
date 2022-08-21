import googletrans
import requests
import json

translate = googletrans.Translator()
key = "f0f2de8a8e49d99a77fb762cab177c25"
k2C = lambda k: k - 273.15


def total_data():
    user_city = input()
    user_city = translate.translate(user_city, dest="en").text
    print(user_city)
    
    if user_city == "":
        print("공백은 인식할 수 없습니다.")

    api = f"http://api.openweathermap.org/data/2.5/forecast?q={user_city}&APPID={key}"
    result = requests.get(api)

    if result.status_code == 200:
        data = json.loads(result.text)
    
        forecast_data = []
        
        for item in data["list"]:
            
            date = item["dt_txt"]
            temp = round(k2C(item["main"]["temp"]), 1)
            temp_min = round(k2C(item["main"]["temp_min"]), 1)
            temp_max = round(k2C(item["main"]["temp_max"]), 1)
            feels_like = round(k2C(item["main"]["feels_like"]), 1)
            humidity = item["main"]["humidity"]
            weather = item["weather"][0]["main"]
            weather_description = item["weather"][0]["description"]
            
            try:
                rain = item["rain"]
                forecast_data_sub = {
                    "date":date,
                    "temp":temp,
                    "temp_min":temp_min,
                    "temp_max":temp_max,
                    "feels_like":feels_like,
                    "humidity":humidity,
                    "weather":weather,
                    "weather_description":weather_description,
                    "rain": rain
                }
                forecast_data.append(forecast_data_sub) 
            except:
                pass
                    
        return forecast_data

    else:
        print("다시 입력해주세요")

