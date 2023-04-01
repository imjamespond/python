
from utils.db import Db
import re
import os
import datetime
import geoip2.database 

# logurl =  os.getenv('HOME')+"/Downloads/btmp.log"
# geodb = "/Documents/project/GeoLite2-City.mmdb"
geodb = "/GeoLite2-City.mmdb"
logurl =  "/tmp/btmp.log"

class Service(object):

  def __init__(self):
    self.db = Db("test.db")

    file = os.getenv('HOME')+geodb
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
    field =  query.get('field')
    value =  query.get('value')
    fval = None
    if field != None and value != None:
      fval = field + value
    if limit != None and offset != None:
      rs = self.db.findWith( fval,limit[0],offset[0])
      rows = []
      for tup in rs:
        row = list(tup)
        try:
          ip = row[6]
          rsp = self.reader.city(ip) 
          row.append(rsp.city.name)
        except BaseException as err:
          row.append("error")
          print(err)
        rows.append(row)
      return rows
    
  def total_by_ip(self):
    return self.db.total_by("ut_addr_v6")
  def total_by_user(self):
    return self.db.total_by("ut_user")
  def group_by_ip(self, query:dict[str, list[str]]):
    rs = self.group_by("ut_addr_v6", query)
    if rs != None:
      rows = []
      for tup in rs:
        row = list(tup)
        try:
          ip = row[0]
          rsp = self.reader.city(ip) 
          row.append(rsp.city.name)
        except BaseException as err:
          row.append("error")
          print(err)
        rows.append(row)
      return rows
  def group_by_user(self, query:dict[str, list[str]]):
    return self.group_by("ut_user", query)
  def group_by(self, field:str, query:dict[str, list[str]]):
    limit =  query.get('limit')
    offset =  query.get('offset')
    if limit != None and offset != None:
      return self.db.group_by(limit[0],offset[0],field)
    return None

  def read_result(self):
    file = logurl
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
      self.db.insert(rows)
      print("end insert ", len(rows))
