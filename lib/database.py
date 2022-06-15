#To make importing databases easier & simpler
import lib.color as c, json, mysql.connector

class db: 
    def connect(db: str):
        if db == "db1": 
            with open('./json/database-conf.json') as f: db1 = json.load(f)
            db = db1
        elif db == "db2": 
            with open('./json/database-conf2.json') as f: db2 = json.load(f)    
            db = db2
        elif db == "db3": 
            with open('./json/database-conf3.json') as f: db3 = json.load(f)
            db = db3
        elif db == "db4": 
            with open('./json/database-conf4.json') as f: db4 = json.load(f)
            db = db4
        elif db == "db5": 
            with open('./json/database-conf5.json') as f: db5 = json.load(f)
            db = db5

        try:
            connect = mysql.connector.connect(**db)
            cursor = connect.cursor(buffered=True)
        except mysql.connector.Error as err: 
            print(c.color.FAIL + "[ERROR] " + c.color.END + str(err))
            
        return [connect, cursor]