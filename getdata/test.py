# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:27:49 2020

@author: lawre
"""

import sqlite3
import os
import datetime

def 

now = datetime.datetime.now()
database_dir = "../database/"
database_name = "st" + str(now.year) + str(now.month).zfill(2) +".db"
database_path = database_dir + database_name


conn = sqlite3.connect(database_path)

