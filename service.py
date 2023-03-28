
from utils.db import Db
import re
import os
import datetime
import geoip2.database 

class Service(object):

  def __init__(self):
    self.db = Db("test.db")

    file = os.getenv('HOME')+"/GeoLite2-City.mmdb"
    self.reader = geoip2.database.Reader(file)

  def close(self):
    self.reader.close()

  def clear_result(self):
    return self.db.truncate()
  def total(self):
    return self.db.total()

  def get_result(self, query:dict[str, list[str]]):
    limit =  query.get('limit')
    offset =  query.get('offset')
    if limit != None and offset != None:
      rs = self.db.findWith(limit[0],offset[0])
      rows = []
      for tup in rs:
        row = list(tup)
        try:
          ip = row[6]
          rsp = self.reader.city(ip) 
          row.append(rsp.city.name)
        except BaseException as err:
          row.append(err)
        rows.append(row)
      return rows

  def read_result(self):
    file = "/tmp/btmp.log"
    with open(file, 'r') as fd:
      i = 0
      rows = []
      for line in iter(fd.readline, ''):
        i+=1
        if i % 1000 == 0:
          print("insert ", i)
          self.db.insert(rows)
          rows = []
          # break

        # 读取括号
        list = re.findall(r"\[(.*?)\]", line) 
        # 各列放入数组
        row = []
        for item in list:
          row.append(str(item).strip())
        # 最后一列转成timestamp
        datestr = str(row[7]).strip().split(',', 1 )
        date = datetime.datetime.strptime(datestr[0],"%Y-%m-%dT%H:%M:%S")
        row.append(int(date.timestamp()))
        # 加入行队列
        rows.append(row)

      print("end insert ", len(rows))
