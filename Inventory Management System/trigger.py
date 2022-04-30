import sqlite3
def Trigger(): 
    try:
        sqliteConnection = sqlite3.connect('ims.db') 
        cursor = sqliteConnection.cursor()   
        print("Connected to SQLite")           
        sql_trigger_query = """ CREATE TRIGGER insert_trigger AFTER INSERT ON employee
                                BEGIN
                                     INSERT INTO register (eid,name,utype)
                                     VALUES (NEW.eid,NEW.name,NEW.utype);
                                END;"""                             
        cursor.execute(sql_trigger_query)     
        sqliteConnection.commit()         
        cursor.close() 
    except sqlite3.Error as error: 
        print("Failed to delete record from sqlite table", error) 
    finally:
        if sqliteConnection: 
            sqliteConnection.close() 
            print("the sqlite connection is closed") 
Trigger()