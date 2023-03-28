import re
import os
 
# result_list = re.findall(r"\[(.*?)\]", "[6] [01773] [    ] [cox     ] [ssh:notty   ] [177.153.69.93       ] [177.153.69.93  ] [2023-03-02T04:43:25,000000+00:00]")
# for item in result_list:
#   print(item.strip())

file = os.getenv('HOME')+"/Downloads/btmp.log"
with open(file, 'r') as fd:
  i = 0
  for line in iter(fd.readline, ''):
    i+=1
    list = re.findall(r"\[(.*?)\]", line)
    for item in list:
      print(item.strip())
    if i > 10:
      break

