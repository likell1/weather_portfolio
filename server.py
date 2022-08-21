from flask import Flask, render_template
from weather_portfolio import total_data

app = Flask(__name__)

@app.route('/home')
def home():
    #API 데이터 가져오기
    data = total_data() #함수 리턴값을 data에 넣겠다
    return render_template("index.html", data = data)
if __name__ == '__main__':
    app.run(debug=True)