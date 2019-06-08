import os
import dialogflow_v2 as dialogflow
import json
import requests
from gnewsclient import gnewsclient
from pymongo import MongoClient

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"
PROJECT_ID = "sharat-fyisbx" # for DialogFlow
dialogflow_session_client = dialogflow.SessionsClient()

client = gnewsclient.NewsClient(max_results=3)
mongocl = MongoClient("mongodb+srv://test777:test777@cluster0-y84qa.mongodb.net/test?retryWrites=true&w=majority")

db = mongocl.get_database('nagarro')
records = db.people

def update_records(session_id, top, loc, cit):
	if top:
		db.people.update_one({'from': session_id}, {'$set': {'news_type': top }}, upsert=True)
	if loc:
		db.people.update_one({'from': session_id}, {'$set': {'geo-country': loc }}, upsert=True)
	if cit:
		db.people.update_one({'from': session_id}, {'$set': {'geo-city': cit }}, upsert=True)
	a = records.find({'from': session_id})[0]
	return a['news_type'], a['geo-country'], a['geo-city']

def get_news(parameters,session_id):
	top = parameters.get('news_type')
	loc = parameters.get('geo-country')
	client.topic, client.location, temp = update_records(session_id, top, loc, '')
	return client.get_news()

def get_weather(parameters,session_id):
	city = parameters.get('geo-city')
	t1, t2, city = update_records(session_id, '', '', city)
	url1 = 'https://www.metaweather.com/api/location/search/?query='+city
	response = requests.get(url1)
	data = json.loads(response.content.decode('utf-8'))
	url2 = 'https://www.metaweather.com/api/location/{}/'.format(data[0]['woeid'])
	response = requests.get(url2)
	data = json.loads(response.content.decode('utf-8'))
	wea = data['consolidated_weather'][0]
	str = "Here is your weather report for {}.".format(city)
	str += "\nThe weather is '{}'. \nCurrent temp : {}°C\nMinimum temp : {}°C\nMaximum temp : {}°C. \n\nThe air pressure is {} mbar, with the humidity being {}% and the visibility being {} miles.".format(wea['weather_state_name'], round(wea['the_temp'],1), round(wea['min_temp'],1), round(wea['max_temp'],1), round(wea['air_pressure'],1), round(wea['humidity'],1), round(wea['visibility'],1))
	img_url = "https://www.metaweather.com/static/img/weather/png/{}.png".format(wea['weather_state_abbr'])
	return (str,img_url)

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	print(dict(response.parameters))
	if response.intent.display_name == 'get_news':
		return get_news(dict(response.parameters),session_id)
	elif response.intent.display_name == 'get_weather':
		return get_weather(dict(response.parameters),session_id)
	else:
		return response.fulfillment_text, "text"