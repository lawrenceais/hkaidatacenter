# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:52:09 2020

@author: lawre
"""

import requests

BASE = "http://127.0.0.1:5000/"

#BASE = "http://168.63.239.113:5000/"
#BASE = "http://168.63.239.113/"
response = requests.get(BASE + "helloworld/bill")
print(response.json())