#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""Problem Set 02 - Clustering (GRP, IS)

Python, OpenCV and K-Means

In this assignment, use python and OpenCV. Grab the dataset (file digits.raw)
from the assignment page on the course Moodle. Each line of the file is a data
element – 64 integers ([0-16] range) separated by commas that represents an
8x8 matrix, or image snippet, of a manuscript digit.

Author: Gabriel Sobral <gasan.sobral@gmail.com>

"""

import numpy as np
import cv2


#
# Q1: Using python and OpenCV, learn how to read the data.
#

digits = []
try:
    filepath = 'digits.raw'
    f = open(filepath, 'r')
    print 'reading file:', filepath
    for line in f:
        line = line.rstrip('\n')
        line = line.split(',')
        line = [int(x) for x in line]
        digits.append(line)
    f.close()
except IOError:
    print 'file not found:', filepath
    exit()

digits = np.array(digits, dtype=np.uint8)

print 'number of digits:', len(digits)
print 'elements per digit:', len(digits[0])

#
# Q2: Write a function that receives to parameters, a data element and a
#     size k, which returns an image with resolution kxk that represent
#     the grayscale digit.
#


def draw_digit(digit, k, lines=False, save=False, image_name='digit.png'):
    pixel_size = k/8
    image = np.empty((k, k), dtype=np.uint8)
    for i in range(0, k, pixel_size):
        for j in range(0, k, pixel_size):
            pixel_value = digit.pop(0) * 255/16
            for x in range(0, pixel_size):
                for y in range(0, pixel_size):
                    if lines and (x == 0 or y == 0):
                        image[i+x, j+y] = 0
                    else:
                        image[i+x, j+y] = pixel_value
    if save:
        cv2.imwrite(image_name, image)
        print 'saving:', image_name
    else:
        cv2.namedWindow('digit', cv2.WINDOW_NORMAL)
        cv2.imshow('digit', image)
        cv2.waitKey(0)

# draw_digit(list(digits[0]), 344, True)

#
# Q3: Use OpenCV’s KMeans implementation to explore and cluster the dataset
#     in 10 groups.
#

data = np.float32(digits)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness, labels, centroids = cv2.kmeans(data, 10, criteria, 10, flags)

#
# Q3a: Use the function of Question 2 to draw the centroid of every cluster.
#

for index, centroid in enumerate(centroids):
    image_name = 'centroid' + str(index) + '.png'
    draw_digit(centroid.tolist(), 200, True, True, image_name)

#
# Q3b: Analyze the algorithm’s sensitivity according to changes in the
#      initial seeds.
#


#
# Q4: Calculate the Covariance Matrix of each of the groups.
#

flags = cv2.COVAR_NORMAL | cv2.COVAR_ROWS

grouped_data = []
icovariance = []
for c in range(0, 10):
    grouped_data.append([])
    for i in range(0, len(digits)):
        if labels[i] == c:
            grouped_data[c].append(digits[i])
    print 'group:', c, len(grouped_data[c])
    x = np.array(grouped_data[c])
    covar, mean = cv2.calcCovarMatrix(x, flags)
    icovar = np.empty(covar.shape, covar.dtype)
    cv2.invert(covar, icovar, cv2.DECOMP_SVD)
    icovariance.append(icovar)


#
# Q5: For each group, calculate the Mahalanobis distance of every element
#     to the centroid, then draw the centroid followed by the three farthest
#     elements (showing their Mahalanobis distance).
#

for index, centroid in enumerate(centroids):
    points = np.float32(grouped_data[index])
    icovar = np.float32(icovariance[index])

    mdistance = []
    for point in points:
        mdistance.append(cv2.Mahalanobis(centroid, point, icovar))

    farthest = sorted(mdistance, reverse=True)[:3]
    for far in farthest:
        print mdistance.index(far), far
        image_name = 'g' + str(index) + '_dist' + str(far) +  '.png'
        draw_digit(points[mdistance.index(far)].tolist(), 200, True, True, image_name)
