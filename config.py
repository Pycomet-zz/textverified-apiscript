import os
import requests
import sys
from telethon import TelegramClient, events, connection
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
import json
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


cwd = os.getcwd()

data_file = open(f'{cwd}/data.json')
data = json.load(data_file)