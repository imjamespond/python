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
  
  li = re.findall(r'(?:review: )?(http://url.com/(\d+))\s?','this is the message. review: http://url.com/123 http://url.com/456')
  for g in li:
    print g
    
  m = re.search(r"DSSQLType=\{(.+)\}", "DSSQLType={ACCOUNT_ID=12, ACCOUNT_NAME=12, ACCOUNT_SHORT_NAME=12, CUST_ID=1, CUST_TYPE_CD=1, PRODUCT_ID=12, COMP_PROD_ID=12, PROD_SUBS_ID=12, MEDIUM_TYPE_CDS=1, DEPOSIT_KIND_CD=1, ACCT_ATTR_CD=1, ACCT_STATUS_CD=1, RLOSS_STATUS_CDS=1, AUTH_MODE_CD=1, DRAW_MODE_CDS=1, DRAW_CERT_TYPE_CD=1, DRAW_CERT_NO=12, EXCHANGE_RANGE_CD=1, DEPOSIT_RANGE_CD=1, BELONG_ORG_ID=1, OPEN_DATE=9, OPEN_ORG_ID=1, OPEN_CHK_BOOK_NO=1, OPEN_CERT_TYPE_CD=1, OPEN_CERT_NO=12, CLOSE_DATE=9, CLOSE_ORG_ID=1, LAST_NO_ACCT_DATE=9, ZERO_BAL_ACCT_FLG=1, ETL_JOB=12, ETL_SRC_TABLE=12, ETL_FIRST_DATE=9, ETL_TX_DATE=9},", re.MULTILINE  )
  for g in m.groups():
    print g