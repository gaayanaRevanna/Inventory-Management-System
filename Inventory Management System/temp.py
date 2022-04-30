import sqlite3
con=sqlite3.connect(database=r'ims.db')
cur=con.cursor()
cur.execute("select * from employee")
print(cur.fetchall())

     