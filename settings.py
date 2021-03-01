import os 

from dotenv import load_dotenv
load_dotenv()

service_url = os.getenv("service_url")
auth = os.getenv('auth')
