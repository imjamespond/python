# -*- coding: utf-8 -*- 
'''
Created on 2016/11/28

@author: metasoft
'''
import xml.etree.ElementTree as ET
import re
import math
from sets import Set

def do_job(xml):
  tree = ET.parse(xml)
  root = tree.getroot()
  print(root.tag)
  for child in root:
    print child.tag, child.attrib
  
  job = root.find('Job')
  recs = job.findall('Record')
  for rec in recs:
    _set = getDSSQLTypeEQ1FromRecord(rec)
    getDSSchemaFromRecord(rec, _set)
    
    for collection in rec.findall('Collection'):
      for subrec in collection.findall('SubRecord'):
        SqlType = -1
        for prop in subrec.findall('Property'): 
          if(prop.get('Name')=='Name'):
            field = prop.text
          elif(prop.get('Name')=='SqlType'):
            SqlType = int(prop.text)
            if(SqlType == 1):
              #print field,":",prop.text
              prop.text = '12'
          elif(prop.get('Name')=='Precision'):
            prec = int(math.ceil(int(prop.text)*1.5))
            prop.text = str(prec)
          elif(prop.get('Name')=='ExtendedPrecision'):
            if(SqlType == 1 or SqlType == 12):
              prop.text = '1'
  
  tree.write('db2_vertica.xml')
  
def getDSSQLTypeEQ1FromRecord(rec):
  _set = Set([])
  #OrchestrateCode
  for prop in rec.findall('Property'):
    if(prop.get('Name')=='OrchestrateCode'):
      #print(prop.text)
      m = re.search(r"(DSSQLType=\{.+\})", prop.text,re.MULTILINE)
      if(m):
        print(m.start(), m.end())
        for g in m.groups(): 
          #print("DSSQLType:",g)
          
          for t in g.split(","):
            #print(t.strip())
            t = t.strip()
            t_ = t.split("=")
            if(t_[1]=="1"):
              _set.add( t_[0])
          gg = re.sub(r"=1,", "=12,", g)
          #print(gg)
          prop.text = prop.text[:m.start()] +gg + prop.text[m.end():]
  print(_set)
  return _set
            
def getDSSchemaFromRecord(rec,_set):
  #OrchestrateCode
  for prop in rec.findall('Property'):
    if(prop.get('Name')=='OrchestrateCode'):
      m = re.search(r"(DSSchema=.*\(.+\))", prop.text,re.MULTILINE|re.DOTALL)
      if(m):
        #print(m.start(), m.end())
        for g in m.groups(): 
          print("DSSchema:",g)
          gg = g
          for field in _set:
            gg = re.sub(r""+field+".*\[[max\\=]?\d+\\\]", repl, gg)
          prop.text = prop.text[:m.start()] +gg + prop.text[m.end():]
def repl(m):
  str = m.string[m.regs[0][0] : m.regs[0][1]]
  return re.sub(r'd+\\\]', '999\\\]', str)
if __name__ == '__main__':
  do_job('data/db2_vertica_无unicode.xml')