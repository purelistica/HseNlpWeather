import json
import requests
import os
from natasha import LocationExtractor


def query_processor(query):
    extractor = LocationExtractor()
    match = extractor(query)
    city = None
    for i in range(len(match)):
        city = match[i].fact.as_json['name']
        break
    return(city)


def get_weather(city):
    key = os.environ['WEATHER_TOKEN']
    q = 'http://api.openweathermap.org/data/2.5/forecast?q=' \
        + city + '&lang=ru&units=metric&APPID=' + key
    res = requests.get(q)
    status = res.status_code
    if status == 200:
        data = res.text
        # print(json.loads(res))

        weather_current = json.loads(data)['list'][0]

        temp = weather_current['main']['temp']
        feels = weather_current['main']['feels_like']
        state = weather_current['weather'][0]['description']

        template = f"Температура {temp},\nощущается как {feels},\n{state}"
        return template
    else:
        return 'Что-то пошло не так'


def weather_reply(query):
    city_detected = query_processor(query)
    if city_detected is None:
        return 'Укажите город'
    else:
        return get_weather(city_detected) + '\n' + city_detected
