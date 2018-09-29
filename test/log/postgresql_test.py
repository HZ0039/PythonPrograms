import psycopg2

conn = psycopg2.connect(database="pypost", user="postgres", password="123456", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute("SELECT * FROM info")
rows = cur.fetchall()
conn.commit()
cur.close()
conn.close()

for item in rows:
    print(item)