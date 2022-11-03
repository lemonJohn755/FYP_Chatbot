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
            dispatcher.utter_message(text=f"你選擇了 '{district}'")
            
        return []
