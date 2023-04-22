import sqlite3
#sqlite3 is case-sensitive


#Connect to or create a database
###conn = sqlite3.connect('user.db')

#Creat a cursor (jst do it)
c = conn.cursor()

#Create a table
c.execute(""" CREATE TABLE s_america (
        user_id INTEGER NOT NULL ,
        current_qn INTEGER DEFAULT "0" NOT NULL,
        score INTEGER DEFAULT "0" NOT NULL
    )""") #6 " are used when multiple lines of command are to be written in a single execute function

#actually execute the cursor's command
conn.commit() 


#close the connection
conn.close()