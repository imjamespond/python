# -*- coding: utf-8 -*- 
'''
Created on 2016/11/28

@author: metasoft
'''
import xml.etree.ElementTree as ET
import re
import math
from os import listdir
from sets import Set

gDir="data/"

def do_job(file):
  tree = ET.parse(gDir+file)
  root = tree.getroot()
  print(root.tag)
  for child in root:
    print child.tag, child.attrib
  
  job = root.find('Job')
  recs = job.findall('Record')
  for rec in recs:
    #OrchestrateCode
    for prop in rec.findall('Property'):
      if(prop.get('Name')=='OrchestrateCode'):
        _set = getDSSQLTypeEQ1FromRecord(prop)
        getDSDisplayWidthFromRecord(prop, _set)
        getDSSQLPrecisionFromRecord(prop, _set)
        getDSSchemaFromRecord(prop, _set)
    
    for collection in rec.findall('Collection'):
      for subrec in collection.findall('SubRecord'):
        SqlType = -1
        for prop in subrec.findall('Property'): 
          if(prop.get('Name')=='Name'):
            field = prop.text
            
            if(prop.text == 'supportedTransactionModel'):
              collection.remove(subrec)
          elif(prop.get('Name')=='SqlType'):
            SqlType = int(prop.text)
            if(SqlType == 1):
              #print field,":",prop.text
              prop.text = '12'
          elif(prop.get('Name')=='Precision'):
            if(SqlType == 1 or SqlType == 12):
              prec = scaleby1_5(prop.text)
              prop.text = str(prec)
          elif(prop.get('Name')=='ExtendedPrecision'):
            if(SqlType == 1 or SqlType == 12):
              prop.text = '1'
            
  
  #tree.write('db2_vertica.xml')
  text = ET.tostring(root).replace("'", "&apos;")
  xmlfile = open(gDir+"output/"+file, 'wb+')
  #tree.write(xmlfile, xml_declaration=True, encoding='UTF-8')
  xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  xmlfile.write(text)
  xmlfile.close()

  
def getDSSQLTypeEQ1FromRecord(prop):
  _set = Set([])
  #print(prop.text)
  m = re.search(r"(-target|-file)(.+?)((?<=DSSQLType=\{).+?(?=\}))", prop.text, re.DOTALL)
  if(m):
    mstr = m.group(3)
    print("DSSQLType:",mstr)
    for t in mstr.split(","):
      #print(t.strip())
      t = t.strip()
      t_ = t.split("=")
      if(t_[1]=="1" or t_[1]=="12"):
        _set.add( t_[0])
    gg = re.sub(r"=1,", "=12,", mstr)
    #print(gg)
    prop.text = prop.text[:m.regs[3][0]] + gg + prop.text[m.regs[3][1]:]
  print(_set)
  return _set

def getDSDisplayWidthFromRecord(prop,_set):
  m = re.search(r"(-target|-file)(.+?)(DSDisplayWidth=\{.+?\})", prop.text, re.DOTALL)
  if(m):
    mstr = m.group(3)
    print("DSDisplayWidth:",m.string[m.regs[3][0] : m.regs[3][1]])
    for field in _set:
      mstr = re.sub(r"(?<="+field+"=)\d+", repl1, mstr)
    prop.text = prop.text[:m.regs[3][0]] + mstr + prop.text[m.regs[3][1]:]
def getDSSQLPrecisionFromRecord(prop,_set):
  m = re.search(r"(-target|-file)(.+?)(DSSQLPrecision=\{.+?\})", prop.text, re.DOTALL)
  if(m):
    mstr = m.group(3)
    print("DSSQLPrecision:",mstr)
    for field in _set:
      mstr = re.sub(r"(?<="+field+"=)\d+", repl1, mstr)
    prop.text = prop.text[:m.regs[3][0]] + mstr + prop.text[m.regs[3][1]:]
def getDSSchemaFromRecord(prop,_set):
  m = re.search(r"(-target|-file)(.+?)(DSSchema=[^(]+?\([^)]+?\))", prop.text, re.DOTALL)
  if(m):
    mstr = m.group(3)
    #print(m.start(), m.end())
    print("DSSchema:",mstr)
    for field in _set:
      #gg = re.sub(r""+field+".*\[[max\\=]?\d+\\\]", repl, gg)#[max\\=]? wrong regex!!!
      mstr = re.sub(r""+field+".*\[", repl2, mstr)
    prop.text = prop.text[:m.regs[3][0]] + mstr + prop.text[m.regs[3][1]:]
def repl(m):
  li = re.findall(r"\\\[(?:max\\=)?(\d+)\\\]",m.string)
  _len = math.ceil(int(li[0])*1.5)
  _str = m.string[m.regs[0][0] : m.regs[0][1]]
  return re.sub(r'\d+\\\]', str(_len)+'\\\]', _str)
def repl1(m):
  _str = m.string[m.regs[0][0] : m.regs[0][1]]
  return str(scaleby1_5(_str))
def repl2(m):
  _str = m.string[m.regs[0][0] : m.regs[0][1]]
  return re.sub(r'(?<=[^u])(string)', 'ustring', _str)

def scaleby1_5(s):
  num = int(s)
  if(num<120 and num>6):
    return int(math.ceil(int(s)*1.5))
  else:
    return num

if __name__ == '__main__':
  for f in listdir(gDir):
    if f.endswith('.xml'):
      do_job(f)