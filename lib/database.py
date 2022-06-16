#To make importing databases easier & simpler
import lib.color as c, json, mysql.connector

class db: 
    def connect(db: str):
        if db == "db1": 
            with open('./json/database-conf.json') as f: db = json.load(f)
        elif db == "db2": 
            with open('./json/database-conf2.json') as f: db = json.load(f)    
        elif db == "db3": 
            with open('./json/database-conf3.json') as f: db = json.load(f)
        elif db == "db4": 
            with open('./json/database-conf4.json') as f: db = json.load(f)
        elif db == "db5": 
            with open('./json/database-conf5.json') as f: db = json.load(f)

        try:
            connect = mysql.connector.connect(**db)
            cursor = connect.cursor(buffered=True)
        except mysql.connector.Error as err: 
            print(c.color.FAIL + "[ERROR] " + c.color.END + str(err))
            
        return [connect, cursor]