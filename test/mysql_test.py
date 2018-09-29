import pymysql

db = pymysql.connect("localhost","root","","pymysql")

cursor = db.cursor()
cursor.execute("select * from test")
data=cursor.fetchall()

print(data*3)

db.close()