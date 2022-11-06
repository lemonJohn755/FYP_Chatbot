# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
import requests


class ActionChooseFunction(Action):
    def name(self) -> Text:
        return "action_say_function_chosen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        choice = tracker.get_slot("choice")

        if choice == "1)依照地區推介":
            dispatcher.utter_message(text=f"你選擇了 '{choice}'")
        elif choice == "2)依照難度推介":
            dispatcher.utter_message(text=f"你選擇了 '{choice}'")
        else:
            dispatcher.utter_message(text="唔好意思 唔清楚你嘅選擇 :pray:")

        return []


class ActionChooseDistrict(Action):
    def name(self) -> Text:
        return "action_say_district_chosen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        district = tracker.get_slot("district")

        if district is not None:
            dispatcher.utter_message(text=f"你選擇了 '{district}'，以下係相關結果")
            query = ActionChooseDistrict.district_db_query(district)

            dispatcher.utter_message(text=query)

        return []

    def district_db_query(district):
        mydb = mysql.connector.connect(
            host="0.0.0.0",
            user="root",
            password="root",
            database="FYP_Chatbot"
        )

        mycursor = mydb.cursor()
        sql = "SELECT Route, Difficulty, Length, Score, Link FROM sample_data WHERE District='{}'".format(
            district)
        mycursor.execute(sql)
        result = mycursor.fetchall()

        result_return = ""

        i = 0
        total_num = len(result)
        for x in result:
            i = i+1
            print("")
            print("第 {}/{} 個結果".format(i, total_num))
            print('行山徑:', x[0])
            print('難度:', x[1])
            print('長度:', x[2])
            print('評分:', x[3])
            print('詳情:', x[4])

            heading = "\n第 {}/{} 個結果".format(i, total_num) + '\n'
            route = '行山徑: ' + x[0] + '\n'
            difficulty = '難度: ' + str(x[1]) + '\n'
            length = '長度: ' + str(x[2]) + 'km\n'
            score = '評分: ' + str(x[3]) + '/5\n'
            detail = '詳情: ' + x[4] + '\n\n'
            result_return = result_return + heading + \
                route + difficulty + length + score + detail

        return result_return

    class ActionCheckWeather(Action):
        def name(self) -> Text:
            return "action_inquire_weather"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        weather_entity = next(tracker.get_latest_entity_values("weather"), None)

        if not weather_entity:
            msg = f"Sorry, 唔係好明你意思"
            dispatcher.utter_message(text=msg)
            
            return []
        
        response = await requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc").json()
        dispatcher.utter_message(text=response)

        return []
    """ async def getWeatherData():
        response = await requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc").json()

        return response """