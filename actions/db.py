import os
import json
import mysql.connector
from dotenv import dotenv_values

with open('./actions/env.json', 'r') as f:
    env_vars = json.load(f)

class MySQLConnection:
    _client = None
    

    @staticmethod 
    def getInstance():
        if MySQLConnection._client == None:
            MySQLConnection()
        return MySQLConnection._client
    
    def __init__(self):
        if MySQLConnection._client != None:
            raise Exception("MySQL client has been created")
        else:
            MySQLConnection._client = self
            try:
                self.connection = mysql.connector.connect(
                    host=env_vars["DB_HOST"],
                    user=env_vars["DB_USER"],
                    password=env_vars["DB_PASSWORD"],
                    database=env_vars["DB_NAME"],
                )
                # print("connected mysql")
            except mysql.connector.Error as error:
                print("Error while connecting to MySQL:", error)
    
    def getConnection(self):
        return self.connection
