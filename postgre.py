# coding:utf8
import psycopg2

import psycopg2

# Try to connect

try:
    conn = psycopg2.connect("dbname='hellopsql' user='hellopsql' password='hello'")
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()

# try:
#     cur.execute("""
#     CREATE TABLE account(
#  user_id serial PRIMARY KEY,
#  username VARCHAR (50) UNIQUE NOT NULL,
#  password VARCHAR (50) NOT NULL,
#  email VARCHAR (355) UNIQUE NOT NULL,
#  created_on TIMESTAMP NOT NULL,
#  last_login TIMESTAMP
#  );
#      """)
# except:
#     print ( "I can't SELECT from bar")


cur.execute("select count(*) from account")
rows = cur.fetchall()

print("\nRows: \n")
for row in rows:
    print ("   ", row[0])

cur.close()
conn.commit()
if conn is not None:
    conn.close()