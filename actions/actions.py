from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionFetchWeather(Action):

    def name(self) -> Text:
        return "action_fetch_weather"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=d8113207638a71e6323a77beb4ee5d0d"
        response = requests.get(url).json()

        if response.get("cod") == 200:
            temp_kelvin = response["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            description = response["weather"][0]["description"]
            message = f"The current temperature in {location} is {temp_celsius:.2f}°C and the weather is {description}."
        else:
            message = f"I couldn't fetch the weather information for {location}. Please try another location."

        dispatcher.utter_message(text=message)

        return []
