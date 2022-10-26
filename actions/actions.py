from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionCheckWeather(Action):
    
    def name(self)-> Text:
        return "action_get_weather"
    
    def run(self, dispatcher, tracker, domain):
        loc_dict = {"香港":"HongKong",
                    "上海":"Shanghai",
                    "新加坡":"Singapore",
                    "倫敦":"London",
                    "紐約":"New York"
                    }

        api_key = '95e8fae6528c096528e4f03729940d17'
        print("location:", tracker.get_slot('location') )
        loc_cn = tracker.get_slot('location')   # location in Chinese
        loc = loc_dict[loc_cn]
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main']
        temperature_c = "{:.2f}".format(current['main']['temp'] - 273)
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        response = """It is currently {} in {} at the moment. The temperature is {} celsius degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        dispatcher.utter_message(response)
        return [SlotSet('location', loc)]