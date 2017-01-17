'''
Created on 2016/11/28

@author: metasoft
'''
import re
if __name__ == '__main__':
  m = re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match
  for g in m.groups():
    print g
  email = "tony@tiremove_thisger.net"
  m = re.search("remove_this", email)
  print email[:m.start()] + email[m.end():]
  m = re.match(r"(\d+)\.(\d+)", "24.1632")
  for g in m.groups():
    print g
  
  m = re.match(r"(\S+) - (\d+) errors, (\d+) warnings", "/usr/sbin/sendmail - 0 errors, 4 warnings")
  for g in m.groups():
    print g
    
  #non-capturing but the substring matched by the group cannot be retrieved
  li = re.findall(r"\\\[(?:max\\=)?(\d+)\\\]","CUST_ID\\:nullable string\\[max\\=1221\\]\\;\n")
  for g in li:
    print g
  #character except
  li = re.findall(r"[^u](string)","CUST_ID\\:nullable string\\[max\\=1221\\]\\;\n")
  for g in li:
    print g
  print re.sub(r"(?<=[^u])(string)","ustring","CUST_ID\\:nullable string\\[max\\=1221\\]\\;\n")
    
  li = re.findall(r'(?:review: )?(http://url.com/(\d+))\s?','this is the message. review: http://url.com/123 http://url.com/456')
  for g in li:
    print g
    
  m = re.search(r"DSSQLType=\{(.+)\}", "DSSQLType={ACCOUNT_ID=12, ACCOUNT_NAME=12, ACCOUNT_SHORT_NAME=12, CUST_ID=1, CUST_TYPE_CD=1, PRODUCT_ID=12, COMP_PROD_ID=12, PROD_SUBS_ID=12, MEDIUM_TYPE_CDS=1, DEPOSIT_KIND_CD=1, ACCT_ATTR_CD=1, ACCT_STATUS_CD=1, RLOSS_STATUS_CDS=1, AUTH_MODE_CD=1, DRAW_MODE_CDS=1, DRAW_CERT_TYPE_CD=1, DRAW_CERT_NO=12, EXCHANGE_RANGE_CD=1, DEPOSIT_RANGE_CD=1, BELONG_ORG_ID=1, OPEN_DATE=9, OPEN_ORG_ID=1, OPEN_CHK_BOOK_NO=1, OPEN_CERT_TYPE_CD=1, OPEN_CERT_NO=12, CLOSE_DATE=9, CLOSE_ORG_ID=1, LAST_NO_ACCT_DATE=9, ZERO_BAL_ACCT_FLG=1, ETL_JOB=12, ETL_SRC_TABLE=12, ETL_FIRST_DATE=9, ETL_TX_DATE=9},", re.MULTILINE  )
  for g in m.groups():
    print g
    
  w = "TEMPLATES = ( ('index.html', 'home'), ('base.html', 'base'))"
  # find outer parens
  outer = re.compile("\((.+)\)")
  m = outer.search(w)
  inner_str = m.group(1)
  
  # find inner pairs
  innerre = re.compile("\('([^']+)', '([^']+)'\)")
  
  results = innerre.findall(inner_str)
  for x,y in results:
    print "%s <-> %s" % (x,y)
  '''
by default search finds the longest match
  
Explanation:
outer matches the first-starting group of parentheses using \( and \); by default search finds the longest match, giving us the outermost ( ) pair. The match m contains exactly what's between those outer parentheses; its content corresponds to the .+ bit of outer.
innerre matches exactly one of your ('a', 'b') pairs, again using \( and \) to match the content parens in your input string, and using two groups inside the ' ' to match the strings inside of those single quotes.
Then, we use findall (rather than search or match) to get all matches for innerre (rather than just one). At this point results is a list of pairs, as demonstrated by the print loop.
Update: To match the whole thing, you could try something like this:

rx = re.compile("^TEMPLATES = \(.+\)")
rx.match(w)
  '''