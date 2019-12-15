#!/usr/bin/env bash

rm -rf ~/.venv/HseNlpWeather
python3 -m venv ~/.venv/HseNlpWeather
source ~/.venv/HseNlpWeather/bin/activate && pip3 install -r requirements.txt