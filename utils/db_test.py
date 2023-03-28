from db import Db
import re
import os
import datetime

db = Db("test.db")
db.truncate()
 
file = os.getenv('HOME')+"/Downloads/btmp.log"
with open(file, 'r') as fd:
  i = 0
  rows = []
  for line in iter(fd.readline, ''):
    i+=1
    if i > 10:
      break

    list = re.findall(r"\[(.*?)\]", line) 
    row = []
    for item in list:
      row.append(str(item).strip()) 
    datestr = str(row[7]).strip().split(',', 1 )
    date = datetime.datetime.strptime(datestr[0],"%Y-%m-%dT%H:%M:%S")
    row.append(int(date.timestamp()))
    rows.append(row)

  db.insert(rows)

total = db.total()
list = db.find()
print(list,total)
db.close()