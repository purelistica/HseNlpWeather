import json
import requests
import os
from natasha import LocationExtractor
from datetime import datetime


def query_processor(query):
    extractor = LocationExtractor()
    match = extractor(query)
    city = None
    for i in range(len(match)):
        city = match[i].fact.as_json['name']
        break
    return(city)


def get_weather(city, time):
    key = '0f6495f4444469a7bf8dd37c9e562963'
    q = 'http://api.openweathermap.org/data/2.5/forecast?q='\
        +city+'&lang=ru&units=metric&APPID='+key
    res = requests.get(q)
    status = res.status_code
    if status == 200:
        data = res.text
        weather = json.loads(data)['list']
        result = ''
        if time is None:
            result += f"\nСейчас:\n{format_weather(weather[0])}\n"
            result += f"\nВ {get_time(weather[1]['dt'])} часов:\n{format_weather(weather[1])}\n"
            result += f"\nВ {get_time(weather[2]['dt'])} часов:\n{format_weather(weather[2])}"
            return result
    else:
        return None


def get_time(dt):
    time = datetime.utcfromtimestamp(dt).strftime('%H')
    return time


def format_weather(el):
    temp = el['main']['temp']
    feels = el['main']['feels_like']
    state = el['weather'][0]['description']

    template = f"температура {round(temp, 1)},\nощущается как {round(feels, 1)},\n{state}"
    return template


def weather_reply(query):
    city_detected = query_processor(query)
    time_detected = None
    if city_detected is None:
        return 'Укажите город'
    else:
        template = f"Город {city_detected.capitalize()}\n"
        weather = get_weather(city_detected, time_detected)
        if weather is None:
            return f"Я не знаю погоду в городе {city_detected}, попробуйте выбрать другой"
        else:
            template += weather
            return template
