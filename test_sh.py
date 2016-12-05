'''
Created on 2016/11/28

@author: metasoft
'''
if __name__ == '__main__':
  #from subprocess import call
  #call(["ls", "-l", "/"])
  import sys
  print '\n'.join(sys.path)
  from six.moves import xrange
  for i in xrange(1,5):
    print(i)