# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:03:09 2020

@author: lawre
"""

from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

names = {"tim": {"age":19,"gender":"male"},
         "bill":{"age":20,"gender":"male"}}

class helloWorld(Resource):
    def get(self, name):
        #return {"data":"Hello World!"}
        #return {"name":names, "test": test}
        return names[name]
    
    def post(self):
        return {"data":"Posted"}
    
    
        
#api.add_resource(helloWorld, "/helloworld/<string:name>/<int:test>")
api.add_resource(helloWorld, "/helloworld/<string:name>")


"""
@app.route('/')
def index():
    return "Hello World!"
"""

if __name__ == "__main__":
    app.run(debug=True)