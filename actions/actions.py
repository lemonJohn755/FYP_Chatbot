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

import json
import os
from typing import Any, Text, Dict, List
from dotenv import dotenv_values

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import requests
from .db import MySQLConnection
class ActionChooseFunction(Action):
    def name(self) -> Text:
        return "utter_say_user_chose"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            template="utter_say_user_chose",
            choice=tracker.get_slot("choice"))
         
        return []


class ActionChooseDistrict(Action):
    
    def name(self) -> Text:
        return "action_district_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        district = tracker.get_slot("selected_district")

        if district is not None:
            dispatcher.utter_message(text=f"幫你搵到'{district}'嘅行山徑")
            query = ActionChooseDistrict.district_db_query(district)

            dispatcher.utter_message(text=query)

        return []

    def district_db_query(district):
        db = MySQLConnection.getInstance().getConnection()
        cursor = db.cursor()
        sql = "SELECT Route, Difficulty, Length, Score, Link FROM sample_data WHERE District='{}'".format(
                district)
        cursor.execute(sql)
        result = cursor.fetchall()

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
        
        cursor.close()
        db.close()
        return result_return
        

class ActionChooseDifficulty(Action):
    def name(self) -> Text:
        return "action_difficulty_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        msg = tracker.get_slot("difficulty")
        difficulty = msg[-1]
        print(difficulty)
        
        if (difficulty is not None) and (int(difficulty) <= 5):
            query = ActionChooseDifficulty.district_db_query(difficulty)
            dispatcher.utter_message(text=f"幫你搵到難度 {difficulty}/5 相關結果\n"
                                     +query)
            return []
        else:
            dispatcher.utter_message(text=f"唔好意思，我手頭上冇難度 {msg} 相關結果。可以問難度（1-5）")

    def district_db_query(difficulty):
        db = MySQLConnection.getInstance().getConnection()
        cursor = db.cursor()

        sql = "SELECT Route, Difficulty, Length, Score, Link FROM sample_data WHERE Difficulty='{}'".format(difficulty)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        heading = "\n第 {}/{} 個結果".format(i, total_num)+ '\n'
        route = '行山徑: '+ x[0] + '\n'
        difficulty = '難度: ' + str(x[1]) + '\n'
        length = '長度: ' + str(x[2]) + 'km\n'
        score = '評分: ' + str(x[3]) + '/5\n'
        detail = '詳情: ' + x[4] + '\n\n'
        result_return = result_return + heading + route + difficulty + length + score + detail
        
        i=0
        total_num = len(result)
        for x in result:
            i=i+1
            print("")
            print("第 {}/{} 個結果".format(i, total_num))
            print('行山徑:',x[0])
            print('難度:',x[1])
            print('長度:',x[2])
            print('評分:',x[3])
            print('詳情:',x[4])
            
            heading = "\n第 {}/{} 個結果".format(i, total_num)+ '\n'
            route = '行山徑: '+ x[0] + '\n'
            difficulty = '難度: ' + str(x[1]) + '\n'
            length = '長度: ' + str(x[2]) + 'km\n'
            score = '評分: ' + str(x[3]) + '/5\n'
            detail = '詳情: ' + x[4] + '\n\n'
            result_return = result_return + heading + route + difficulty + length + score + detail

        cursor.close()
        db.close()
        return result_return
                
    #     weather_entity = next(tracker.get_latest_entity_values("weather"), None)

    #     if not weather_entity:
    #         msg = f"Sorry, 唔係好明你意思"
    #         dispatcher.utter_message(text=msg)
            
    #         return []
        
    #     response = await requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc").json()
    #     dispatcher.utter_message(text=response)

    #     return []
    # """ async def getWeatherData():
    #     response = await requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc").json()

    #     return response """

class ActionAccidentQuery(Action):
    def name(self) -> Text:
        return "action_accident_query"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        accident = tracker.get_slot("accident_name")
        
        result = ActionAccidentQuery.accidt_db_query(accident)
        dispatcher.utter_message(text=result)
        
        return []
    
    def accidt_db_query(accident):
        dotenv_values(".env")
        db = MySQLConnection.getInstance().getConnection()
        cursor = db.cursor()
        
        # execute a query to retrieve data from a table
        query = "SELECT * FROM `hiking_common_accidents` WHERE `Accident`='{}';".format(accident)
        cursor.execute(query)

        # fetch all the rows returned by the query
        rows = cursor.fetchall()

        # print out the data
        accidt = "意外: {}\n".format(rows[0][0])
        des = "描述:\n{}\n".format(rows[0][1])
        caution = "如何避免?\n{}\n".format(rows[0][2])
        measure = "應變措拖:\n{}".format(rows[0][3])
        print(accidt)
        print(des)
        print(caution)
        print(measure)
        result_return = accidt + des + caution + measure
        
        # close the cursor and database connection
        cursor.close()
        db.close()
        
        return result_return
    
class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "action_inquire_weather"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        weather_entity = next(
            tracker.get_latest_entity_values("weather"), None)

        if not weather_entity:
            msg = f"Sorry, 唔係好明你意思"
            dispatcher.utter_message(text=msg)

            return []
        #dispatcher.utter_message(text='ok weather')
        try:
            response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc").json()
            msg = f"{response['forecastPeriod']}\n{response['forecastDesc']}\n{response['outlook']}\n{response['generalSituation']}\n{response['tcInfo']}\n{response['fireDangerWarning']}"
            dispatcher.utter_message(msg)
        except Exception as e:
            print("CheckWeather function error")
            print(e)

        return []

class ActionCheckWeatherForecast(Action):
    def name(self) -> Text:
        return "action_inquire_weather_forecast"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        weather_entity = next(tracker.get_latest_entity_values("weather"), "天氣")
        week_entity = next(tracker.get_latest_entity_values("每週各天"), "每週各天")

        if not weather_entity or week_entity:
            msg = f"Sorry, 唔係好明你意思"
            dispatcher.utter_message(text=msg)

            return []
        #dispatcher.utter_message(text='ok weather')
        try:
            # response = requests.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc").json()
            #print(response)
            # msg = response['weatherForecast'][0]['week']
            # TODO: return full response to frontend
            dispatcher.utter_message(text= 'forecast')
        except Exception as e:
            print("CheckWeather function error")
            print(e)

        return []

class ActionResetAllSlots(Action):
    
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
    