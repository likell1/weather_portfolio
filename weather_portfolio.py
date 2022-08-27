from urllib.parse import urlencode, unquote, quote_plus
import requests
import json
import datetime

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
key = "ZY4X7XsMc45fallLicFTORvp6m52HG6SjGhgBJxq13Nlm0%2BMjdELvxdN1K9opPwSbNg4acNnFRI9%2BdZJ%2FItOUA%3D%3D"
key_Decoded = unquote(key)
now = datetime.datetime.now()
now_year = str(now.year)
now_day = str(now.day)
now_hour = now.hour

if now.month < 10:  #1~9월 까지는 01,02 ~ 09월이 아닌 1,2 ~ 9월로 생성되므로 api요청 시 오휴가 나는 것을 방지
    now_month = "0" + str(now.month)
else:
    now_month = str(now.month)

# user = input("동네이름:") 

#동네 이름 받아오면 위도, 경도 값으로 변환 (excel 데이터 이용)

if now_hour < 2:
    now_day = str(int(now_day)-1)   #00시~ 02시전까지는 전날 23시에 발표한 api를 사용하므로 이를 조정
    basetime = "2300"               #day가 말일에서 다음 달 1일로 바뀌는 경우 상황 고려해야함
elif now_hour < 5:
    basetime = "0200"
elif now_hour < 8:
    basetime = "0500"
elif now_hour < 11:
    basetime = "0800"
elif now_hour < 14:
    basetime = "1100"
elif now_hour < 17:
    basetime = "1400"
elif now_hour < 20:
    basetime = "1700"
elif now_hour < 23:
    basetime = "2000"
else:
    basetime = "2300"

basedate = now_year + now_month + now_day


# def forecast(): #api에서 원하는 data만 뽑아오게 만들어주는 함수

query_params ='?' + urlencode({     #API 항목명과 일치해야함, encode 하는 이유?
                quote_plus('Servicekey') : key_Decoded, 
                quote_plus('numOfRows') : '288',        #1시간에 데이터 12개 나옴. TMN,TMX없음  
                quote_plus('dataType') : 'json',        #한시간에 12 Row datas -> 24시간치 = 288 Rows
                quote_plus('base_date') : basedate, 
                quote_plus('base_time') : basetime, 
                quote_plus('pageNo') : 1, 
                quote_plus('nx') : 55, 
                quote_plus('ny') : 127 })


response = requests.get(url + query_params)
data = json.loads(response.text)

weathers = []
line_number =[]
BASE_ROUTE = data["response"]["body"]["items"]["item"]
baseDate = BASE_ROUTE[0]["baseDate"]     #baseDate, baseTime,
baseTime = BASE_ROUTE[0]["baseTime"]     #x_coordinate, y_coordinate 이것은 input 받은 후 고정값
x_coordinate = BASE_ROUTE[0]["nx"]
y_coordinate = BASE_ROUTE[0]["ny"]
count = 1

for num in range(int(len(BASE_ROUTE)/12) + 1): 
    line_number.append(num * 12)

for i in range(24):
    forecast_Date = BASE_ROUTE[i*12]["fcstDate"]
    forecast_Time = BASE_ROUTE[i*12]["fcstTime"]
    
    categorys = []
        
    for j in range(line_number[count] - 12, line_number[count]):  #기준
        category = BASE_ROUTE[j]["category"]
        fcstValue = BASE_ROUTE[j]["fcstValue"]
        
        categorys_d = {
            "category" : category,
            "fcstValue" : fcstValue
        }

        categorys.append(categorys_d)

    count += 1

    weathers_d = {
            "baseDate": baseDate, 
            "baseTime": baseTime,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
            "forecast_Date": forecast_Date,
            "forecast_Time": forecast_Time,
            "categorys": categorys        
    }

    weathers.append(weathers_d)

    #len(리스트) -> 리스트 요소의 개수 (dict도 하나의 요소임)
    
print(weathers)