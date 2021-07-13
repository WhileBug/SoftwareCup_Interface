#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
print("Opened database successfully")

cursor = c.execute("SELECT id, name, password  from USER")
for row in cursor:
   print("id = ", row[0])
   print("name = ", row[1])
   print("password = ", row[2],"\n")

print("Operation done successfully")
conn.close()