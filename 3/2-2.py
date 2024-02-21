import random

indices = list(range(10))

print(indices)

random.shuffle(indices)

print(indices)

num = len(indices)
for i in range(0, num, 3):
  print(indices[i: min(i+3, num)])

