# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:52:09 2020

@author: lawre
"""

import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld/tim")
print(response.json())