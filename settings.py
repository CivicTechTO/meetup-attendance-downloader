from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

MEETUP_API_KEY = os.getenv('MEETUP_API_KEY')
PORT = os.getenv('PORT', 5000)
