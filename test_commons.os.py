#!/usr/bin/env python2
import itertools
import os,argparse
parser = argparse.ArgumentParser()
parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
args = parser.parse_args()
for directory in args.imgs:
  for subdir, dirs, files in os.walk(directory):
    print(subdir)
    '''for filename in files:
      #if filename.endswith(".asm") or filename.endswith(".py"): 
      print(os.path.join(directory, filename))'''

