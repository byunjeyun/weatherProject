import sys
import threading
import time
import requests
from bs4 import BeautifulSoup
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread

form_class = uic.loadUiType("D:/python_workspace/weatherProject/ui/weather.ui")[0]

class WeatherInfoThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def weatherInfoOutput(self, weather_area):
        weather_info = []

        weather_html = requests.get(f"https://search.naver.com/search.naver?&query={weather_area}날씨")

        weather_soup = BeautifulSoup(weather_html.text,'html.parser')

        try:
            area_text = weather_soup.find('h2', {'class':'title'}).text
            print(area_text)
            today_temper = weather_soup.find('div',{'class':'temperature_text'}).text
            today_temper = today_temper[6:11]
            print(today_temper)
            yesterday_weather = weather_soup.find('p',{'class':'summary'}).text
            yesterday_weather = yesterday_weather[0:13].strip()
            print(yesterday_weather)
            today_weather = weather_soup.find('span', {'class':'weather before_slash'}).text
            print(today_weather)
            sense_temper = weather_soup.select('dl.summary_list>dd')
            sense_temper_text = sense_temper[0].text
            print(sense_temper_text)
            dust_info = weather_soup.select('ul.today_chart_list>li')
            dust1_info = dust_info[0].find('span', {'class':'txt'}).text
            dust2_info = dust_info[1].find('span', {'class':'txt'}).text
            print(dust1_info)
            print(dust2_info)

            weather_info.append([area_text] + [today_temper] + [yesterday_weather] + [today_weather] + [sense_temper_text] + [
                    dust1_info] + [dust2_info])
            return weather_info

        except:
            try:
                area_text = weather_soup.find('span', {'class': 'btn_select'}).text
                area_text = area_text.strip()  # 공백제거
                today_temper = weather_soup.find('span', {'class': 'todaytemp'}).text  # 현재온도
                today_weather = weather_soup.find('p', {'class': 'cast_txt'}).text  # 오늘날씨
                today_weather = today_weather[0:2]
                today_weather = today_weather.strip()
                print(today_weather)
                # 해외 지역에 없는 날씨 값
                yesterday_weather = "-"
                sense_temper_text = "-"
                dust1_info = "-"
                dust2_info = "-"

                weather_info.append([area_text] + [today_temper] + [yesterday_weather] + [today_weather] + [sense_temper_text] + [
                        dust1_info] + [dust2_info])
                return weather_info

            except:
                return 0

class WeatherAppWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨정보")
        self.setWindowIcon(QIcon("D:/python_workspace/weatherProject/icons/temp.png"))
        self.statusBar().showMessage("Weather App Ver 1.1 by.uragil")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.weather_info = WeatherInfoThread(self)

        self.weather_btn.clicked.connect(self.crawling_weather)

    def crawling_weather(self):
        weather_area = self.input_area.text()
        weather_result = self.weather_info.weatherInfoOutput(weather_area)

        if weather_result == 0:
            self.area_label.setText(f"{weather_area}의 날씨정보는 없어요")
        else:
            self.area_label.setText(weather_result[0][0])
            self.setWeatherImg(weather_result[0][3])
            self.compare_label.setText(weather_result[0][2])
            self.s_temp_label.setText(weather_result[0][4])
            self.dust1_label.setText(weather_result[0][5])
            self.dust2_label.setText(weather_result[0][6])
            self.temp_label.setText(weather_result[0][1])

    def setWeatherImg(self, today_weather):
        if today_weather == "흐림":
            print(today_weather)
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "맑음":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/sun.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "구름":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "비":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/rain.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "눈":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/rain.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "구름 조금":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/cloud.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))
        elif today_weather == "소낙":
            weatherImg = QPixmap("D:/python_workspace/weatherProject/img/windrain.png")
            self.weather_label.setPixmap(QPixmap(weatherImg))

    def reflashTimer(self):
        self.crawling_weather()
        threading.Timer(60, self.reflashTimer).start()

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = WeatherAppWindow()
    ex.show()
    sys.exit(app.exec_())