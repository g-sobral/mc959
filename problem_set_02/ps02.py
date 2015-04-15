#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""problem_set_02

"""

import numpy as np
import cv2
import sys

digits = []


def draw_digit(digit, pixel_size):
    image = np.empty((8,8), dtype=np.uint8)
    for i in range(0, 8):
        for j in range(0, 8):
            image[i, j] = digit.pop(0) * 255/16

    cv2.namedWindow('window', cv2.WINDOW_NORMAL)
    cv2.imshow('window', image)
    cv2.waitKey(0)

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

draw_digit(digits[0], 1)
