import sqlite3

class Db(object):
  tb = "log"

  def __init__(self, db): 

    conn = sqlite3.connect(db) 

    #创建一个游标 cursor
    cur = conn.cursor()

    # 建表的sql语句
    sql = '''CREATE TABLE IF NOT EXISTS log
          (ut_type CHAR(50),
            ut_pid CHAR(50),
            ut_id CHAR(50),
            ut_user CHAR(50),
            dev CHAR(50),
            ut_host CHAR(50),
            ut_addr_v6 CHAR(50),
            ut_time CHAR(100),
            ut_timestamp NUMBER
            );'''
    # 执行sql语句
    cur.execute(sql)

    sql = '''CREATE INDEX IF NOT EXISTS i_time on log (ut_timestamp);'''
    cur.execute(sql)
    sql = '''CREATE INDEX IF NOT EXISTS i_host on log (ut_host);'''
    cur.execute(sql)
    sql = '''CREATE INDEX IF NOT EXISTS i_user on log (ut_user);'''
    cur.execute(sql)

    self.conn = conn
    self.cur = cur

  def truncate(self):
    cur = self.cur.execute('DELETE FROM ' +self.tb)
    self.conn.commit() 
    rs = cur.fetchone()
    return rs

  def insert(self, data):
    cur = self.cur.executemany('INSERT INTO ' +self.tb+ ' VALUES (?,?,?,?,?,?,?,?,?)', data)
    # 连接完数据库并不会自动提交，所以需要手动 commit 你的改动conn.commit()
    # 提交改动的方法
    self.conn.commit()
    rs = cur.fetchone()
    return rs

  def total(self):
    sql = "SELECT COUNT(*) FROM " +self.tb
    cur = self.cur.execute(sql)
    rs = cur.fetchone()
    return rs

  def find(self):
    return self.findWith(None, 10,0)

  def findWith(self, fval:list, limit: int, offset: int):
    where = "1"
    params = [limit, offset]
    if fval != None :
      where = fval[0] + "=?"
      params = [fval[1],limit, offset]
    sql = "SELECT * FROM " +self.tb+ " WHERE "+where+" order by ut_timestamp desc limit ? offset ?"
    self.cur.execute(sql, params)
    # 获取查询结果
    list = self.cur.fetchall()
    return list

  def total_by(self, field: str):
    sql = "SELECT "+field+", count(*) FROM " +self.tb+ " group by "+field
    sql = "SELECT COUNT(*) FROM ("+sql+") as sub_query"
    cur = self.cur.execute(sql)
    total = cur.fetchone()
    return total
  def group_by(self, limit: int, offset: int, field: str):
    sql = "SELECT "+field+", count(*) FROM " +self.tb+ " group by "+field+" limit ? offset ?"
    self.cur.execute(sql, [limit, offset])
    list = self.cur.fetchall()
    return list

  def close(self): 
    # 关闭游标
    self.cur.close()
    # 关闭连接
    self.conn.close()