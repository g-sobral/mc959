#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""problem_set_02

"""

import numpy as np
import cv2
import sys

digits = []

try:
    file_path = sys.argv[1]
except IndexError:
    print 'Usage: ps02 FILE_PATH'
    exit()

try:
    f = open(file_path, 'r')
    print 'reading file:', file_path
    for line in f:
        line = line.rstrip('\n')
        line = line.split(',')
        line = [int(x) for x in line]
        digits.append(line)
    f.close()
except IOError:
    print 'annotation file not found'
    exit()

print 'number of digits:', len(digits)
print 'elements per digit:', len(digits[0])
