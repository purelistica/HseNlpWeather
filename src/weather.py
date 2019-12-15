from deeppavlov import configs, build_model

ner_model = build_model(configs.ner.ner_rus_bert, download=True)

import json
import requests
import pymorphy2
import os


def query_processor(query):
    query_res = ner_model([query])
    # print(query_res)
    city = None
    for i in range(len(query_res[1][0])):
        if 'LOC' in query_res[1][0][i]:
            city = query_res[0][0][i]
            break
    return (city)


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


query = "погода в пскове"

def weather_reply(query):
    city_detected = query_processor(query)
    # print(city_detected)
    morph = pymorphy2.MorphAnalyzer()
    city_normal = morph.parse(city_detected)[0].normal_form
    # print(city_normal)
    return get_weather(city_normal) + '\n' + city_normal
