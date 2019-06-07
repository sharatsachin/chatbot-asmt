import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"

import dialogflow_v2 as dialogflow
from weather import Weather, Unit

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "sharat-fyisbx"

from gnewsclient import gnewsclient
client = gnewsclient.NewsClient(max_results=3)

def get_news(parameters):
	# print(parameters)
	client.topic = parameters.get('news_type')[0]
	client.language = parameters.get('language')
	client.location = parameters.get('geo-country')
	return client.get_news()

import json
import requests
def get_weather(parameters):
	city = parameters.get('geo-city')
	url1 = 'https://www.metaweather.com/api/location/search/?query='+city
	response = requests.get(url1)
	data = json.loads(response.content.decode('utf-8'))
	url2 = 'https://www.metaweather.com/api/location/{}/'.format(data[0]['woeid'])
	response = requests.get(url2)
	data = json.loads(response.content.decode('utf-8'))
	wea = data['consolidated_weather'][0]
	str = "Here is your weather report.\n\nThe weather is '{}'. The current temperature is {}°C, with the minimum being {}°C and the maximum being {}°C. \n\nThe air pressure is {} mbar, with the humidity being {}% and the visibility being {} miles.".format(wea['weather_state_name'], round(wea['the_temp'],1), round(wea['min_temp'],1), round(wea['max_temp'],1), round(wea['air_pressure'],1), round(wea['humidity'],1), round(wea['visibility'],1))
	img_url = "https://www.metaweather.com/static/img/weather/png/64/{}.png".format(wea['weather_state_abbr'])
	return (str,img_url)

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	# print(response)
	if response.intent.display_name == 'get_news':
		return get_news(dict(response.parameters))
	elif response.intent.display_name == 'get_weather':
		return get_weather(dict(response.parameters))
	else:
		return response.fulfillment_text, "text"