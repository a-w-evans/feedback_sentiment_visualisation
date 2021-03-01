# feedback_sentiment_visualisation
Uses AI to convert written customer feedback into sentiment based on locations and keywords. Stores this in a database, which can be dynamically accessed to create bar-graphs.


WHAT IT DOES: 

1. Takes customer feedback in a text box. 
2. Makes an API call to Watson NLU, and processes the returning JSON into sentiment based on specific keywords. 
3. Stores this information in an SQLite3 database. 
4. Using Pandas and Matplotlib, processes relevant data in the database every time the admin clicks a button. It displays sentiment ratings based on location overall, specific keywords overall, and also provides the option to search for a specific location and see ratings for different service areas. 

I created this project as part of a tech accelerator course. It was one of my first exposures to using professional cloud AI services (aside from creating a simple chatbot). 
API keys are not included, so for functionality, you will want to create an IBM account and generate your own Watson NLU API keys. 
To include these, simple create a .env file in your root directory and store your URL in a variable called service_url and your authentication key in a variable called auth. You should then be good to go. 

To initialise a new database: Simply delete the .db file. When you do this, the next time you run the Flask App, a new database will be generated. 


For some weird reason, my main App is called practice.py (I must fix this), so running this python file (provided you have your API keys linked in) will create a wee local server and let you play with the data visualisation. 
