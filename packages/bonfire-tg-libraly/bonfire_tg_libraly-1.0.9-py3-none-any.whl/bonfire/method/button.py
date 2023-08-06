from flask import Flask
from flask import request
from flask import Response
import requests

app = Flask(__name__)
from colorama import init
init()
from colorama import Fore, Back, Style
import sys
import os
import signal
from .send import send_message

def button(bot=None,chat_id=None,text=None,message=None):
            url = f'https://api.telegram.org/bot{bot}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': text,
                "reply_markup": {"inline_keyboard": [[{"text":"Visit Unofficed","callback_data":"test"}]]}
                }

            r = requests.post(url,json=payload)
            return r

