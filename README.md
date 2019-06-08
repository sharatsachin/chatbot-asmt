# chatbot-asmt

Chatbot made using Twilio, Dialogflow, and Flask.

The chatbot has two Dialogflow intents : the `get_weather` and `get_news` intents.

The `get_news` intent has two entities, `news_type` and `geo-country`. Some sample queries are 'Tell me sports news from India', 'Show me sports news from Australia', and 'un news from Chile', etc. The news stories come in seperate messages and the links are shortened using tinyurl.com. 

The `get_weather` intent has a single entity, `geo-city`. Some sample queries are 'Weather in New York', or 'temperature in Chennai'.

MongoDB has been integrated to ensure that parameters passed to the functions persist between queries.
For example, first asking 'Weather in Melbourne' and then asking 'Weather' leads to the weather in Melbourne being shown. 
Similarly, First asking 'Sports news from India' and then asking 'Technology news' leads to technology news from India being shown.

### Hosted on : https://evening-plains-91335.herokuapp.com/

### To interact with the bot 

Send a WhatsApp message to +14155238886 with code join wrote-softly.
