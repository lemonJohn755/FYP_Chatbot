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
import aiohttp
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
        db.reconnect()
        # db.close()
        return result_return
        

class ActionChooseDifficulty(Action):
    def name(self) -> Text:
        return "action_difficulty_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        msg = tracker.get_slot("difficulty")
        # difficulty = msg[-1]
        # print(difficulty)
        
        if (msg == "難度一星"):
            difficulty = 1
        elif (msg == "難度二星"):
            difficulty = 2
        elif (msg == "難度三星"):
            difficulty = 3
        elif (msg == "難度四星"):
            difficulty = 4
        elif (msg == "難度五星"):
            difficulty = 5
            
        if (difficulty is not None) and (int(difficulty) <= 5):
            query = ActionChooseDifficulty.district_db_query(difficulty)
            dispatcher.utter_message(text=f"幫你搵到難度 {difficulty}/5 相關結果\n"
                                     +query)
        else:
            dispatcher.utter_message(text=f"唔好意思，我手頭上冇難度 {msg} 相關結果。可以問難度一星至五星")

        return []
        
    def district_db_query(difficulty):
        db = MySQLConnection.getInstance().getConnection()
        cursor = db.cursor()

        sql = "SELECT Route, Difficulty, Length, Score, Link FROM sample_data WHERE Difficulty='{}'".format(difficulty)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        # heading = "\n第 {}/{} 個結果".format(i, total_num)+ '\n'
        # route = '行山徑: '+ x[0] + '\n'
        # difficulty = '難度: ' + str(x[1]) + '\n'
        # length = '長度: ' + str(x[2]) + 'km\n'
        # score = '評分: ' + str(x[3]) + '/5\n'
        # detail = '詳情: ' + x[4] + '\n\n'
        # result_return = result_return + heading + route + difficulty + length + score + detail
        result_return = ''
        
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
        db.reconnect()
        # db.close()
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
        # db.close()
        db.reconnect()
        
        return result_return

class ActionTrailnameQuery(Action):
    def name(self) -> Text:
        return "action_trailname_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        loc = tracker.get_slot("location")

        result = ActionTrailnameQuery.trailname_db_query(loc)
        dispatcher.utter_message(text=result)
        
        return []
        
    def trailname_db_query(location):
        db = MySQLConnection.getInstance().getConnection()
        cursor = db.cursor()

        sql = "SELECT Route, Difficulty, Length, Score, Link FROM sample_data WHERE Route LIKE '%{}%'".format(location)
        cursor.execute(sql)
        result = cursor.fetchall()
        
        result_return = ''
        
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
        db.reconnect()
        # db.close()
        return result_return


class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "action_inquire_weather"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # weather_entity = next(
        #     tracker.get_latest_entity_values("weather"), None)

        # if not weather_entity:
        #     msg = f"Sorry, 唔係好明你意思"
        #     dispatcher.utter_message(text=msg)

        #     return []

        try:
            weather_data = None
            async with aiohttp.ClientSession() as session:
                async with session.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc") as response:
                    weather_data = await response.json()
            
            msg = f"{weather_data['forecastPeriod']}\n{weather_data['forecastDesc']}\n{weather_data['outlook']}\n{weather_data['generalSituation']}\n{weather_data['tcInfo']}\n{weather_data['fireDangerWarning']}"
            dispatcher.utter_message(msg)
        except Exception as e:
            print("CheckWeather function error")
            print(e)

        return []

class ActionCheckWeatherForecast(Action):
    def name(self) -> Text:
        return "action_inquire_weather_forecast"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        weather_entity = next(tracker.get_latest_entity_values("weather"), "天氣")
        duckling_time = tracker.get_slot("time")
        if not weather_entity or not duckling_time:
            msg = f"Sorry, 唔係好明你意思"
            dispatcher.utter_message(text=msg)
            return []
        
        day_of_week = duckling_time[0:10].replace("-","")
  
        try:
            forecast_data = None
            weather_data = None
            async with aiohttp.ClientSession() as session:
                async with session.get("https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc") as response:
                    weather_data = await response.json()
            
            for data in weather_data["weatherForecast"]:
                if data["forecastDate"] == day_of_week:
                    forecast_data = data
                    break

            # TODO: return full response to frontend
            weather_data = f"{forecast_data['week']}{forecast_data['forecastWeather']}{forecast_data['forecastWind']}氣溫介乎{forecast_data['forecastMintemp']['value']}至{forecast_data['forecastMaxtemp']['value']}度。濕度介乎百份之{forecast_data['forecastMinrh']['value']}至{forecast_data['forecastMaxrh']['value']}。"
            dispatcher.utter_message(text=weather_data)
        except Exception as e:
            print(f"CheckWeather function error\n{e}")

        return []

class ActionResetAllSlots(Action):
    
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
