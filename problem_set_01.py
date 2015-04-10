#!/usr/bin/python2.7

import numpy as np
import cv2
import sys


window = 'MC959 Annotation Tool'
quadrilaterals = []
selected_vert = None
moving_quad = None
selected_quad = None
registering_quad = 0
new_quad = {'x': [], 'y': []}
help_str = ''

class Quadrilateral:
    def __init__(self, x, y, plate):
        self.x = x
        self.y = y
        self.plate = plate

    def contains(self, x, y):
        if x > min(self.x) and x < max(self.x) and \
        y > min(self.y) and y < max(self.y):
            return True
        return False

    def has_vertex(self, x, y):
        for i in range(0, 4):
            if x >= (self.x[i] - 10) and x <= (self.x[i] + 10) and \
            y >= (self.y[i] - 10) and y <= (self.y[i] + 10):
                return i
        return -1

    def get_vertex(self, index):
        return (self.x[index], self.y[index])

    def set_vertex(self, index, x, y):
        self.x[index] = x
        self.y[index] = y

    def move(self, dx, dy):
        for i in range(0, 4):
            self.x[i] += dx
            self.y[i] += dy

    def draw(self, img, selected):
        if selected:
            line_color = (0, 0, 255)
            vertex_color = (0, 0, 255)
            plate_color = (0, 0, 255)
        else:
            line_color = (0, 255, 0)
            vertex_color = (255, 0, 255)
            plate_color = (255, 0, 255)

        # draw lines
        for i in range(-1, 3):
            cv2.line(img,
                     (self.x[i], self.y[i]),
                     (self.x[i + 1], self.y[i + 1]),
                     line_color,
                     3)
        # draw vertex
        for i in range(0, 4):
            cv2.rectangle(img,
                          (self.x[i] - 10, self.y[i] - 10),
                          (self.x[i] + 10, self.y[i] + 10),
                          vertex_color,
                          -1)
        # draw license plate string
        cv2.putText(img, self.plate, (self.x[0], self.y[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2,
        plate_color, 5)

    def get_string(self):
        quad_str = ''
        for i in range(0, 4):
            quad_str += str(self.x[i])
            quad_str += ','
            quad_str += str(self.y[i])
            quad_str += ','
        quad_str += self.plate
        return quad_str

    def set_from_string(self, str):
        args = str.split(',')
        if len(args) != 9:
            print 'number of arguments in string is incompatible:', args
            return
        for i in range(0, 4):
            self.x.append(int(args.pop(0)))
            self.y.append(int(args.pop(0)))
        self.plate = args.pop(0)

    def print_points(self):
        print 'x:', self.x
        print 'y:', self.y

    def set_plate(self, plate):
        self.plate = plate

    def print_plate(self):
        print self.plate


def on_mouse_event(event, x, y, flags, param):
    global selected_vert
    global moving_quad
    global selected_quad
    global registering_quad
    global new_quad

    if event == cv2.EVENT_LBUTTONDBLCLK:
        # print 'event: double click:', x, y
        for quad in quadrilaterals:
            if quad.contains(x, y):
                selected_quad = quad
                print 'select quadrilateral:', selected_quad.get_string()

    elif event == cv2.EVENT_LBUTTONDOWN:
        # print 'event: left button down:', x, y
        if registering_quad:
            new_quad['x'].append(x)
            new_quad['y'].append(y)
            registering_quad -= 1
            if registering_quad == 0:
                new_quadrilateral(new_quad['x'][:], new_quad['y'][:])
                del new_quad['x'][:]
                del new_quad['y'][:]
        else:
            for quad in quadrilaterals:
                i = quad.has_vertex(x, y)
                if i >= 0:
                    selected_vert = {'quad': quad, 'vert': i}
                    print 'selected vertex:', i, quad.get_vertex(i)
                    break
                elif quad.contains(x, y):
                    moving_quad = {'quad': quad, 'x0': x, 'y0': y}
                    print 'moving quadrilateral:', quad.get_string()
                    break
    elif event == cv2.EVENT_LBUTTONUP:
        # print 'event: left button up:', x, y
        if selected_vert:
            quad = selected_vert['quad']
            quad.set_vertex(selected_vert['vert'], x, y)
        elif moving_quad:
            quad = moving_quad['quad']
            quad.move(x - moving_quad['x0'], y - moving_quad['y0'])
        selected_vert = None
        moving_quad = None
        update_image()

def new_quadrilateral(x, y):
    global quadrilaterals
    global help_str
    print 'new quadrilateral created:', x, y
    plate_str = ''
    q = Quadrilateral(x, y, plate_str)
    quadrilaterals.append(q)

    help_str = 'type the license plate string and press \'Enter\''
    while True:
        key = cv2.waitKey(10)
        if key != -1:
            if key != 10: # Enter key
                plate_str += chr(key)
            else:
                break
    quadrilaterals[-1].set_plate(plate_str)
    print 'license plate registered:', plate_str
    help_str = ''
    update_image()

def update_image():
    img = original_img.copy()
    for quad in quadrilaterals:
        if quad == selected_quad:
            quad.draw(img, True)
        else:
            quad.draw(img, False)
    cv2.putText(img, help_str, (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 2,
    (255,0,255), 5)
    cv2.imshow(window, img)

def white_file():
    f = open(txt_path, 'w')
    print 'writing annotation file:', txt_path
    if len(quadrilaterals):
        for quad in quadrilaterals:
            f.write(quad.get_string())
            f.write('\n')
    else:
        f.write('None\n')
    f.close()

def read_file():
    global quadrilaterals
    try:
        f = open(txt_path, 'r')
        print 'reading annotation file:', txt_path
        for line in f:
            line = line.rstrip('\n')
            if line != 'None':
                q = Quadrilateral([], [], '')
                q.set_from_string(line)
                quadrilaterals.append(q)
        f.close()
    except IOError:
        print 'annotation file not found'

#
# main
#

try:
    image_path = sys.argv[1]
except IndexError:
    print 'Usage: problem_set_01 IMAGE_PATH'
    exit()

try:
    original_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width, depth = original_img.shape
    print 'reading image:', image_path
except:
    print 'image path isn\'t valid:', image_path
    exit()

cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window, on_mouse_event)

txt_path = image_path.rsplit('.',1)[0] + '.txt'
read_file()
update_image()

while True:
    key = cv2.waitKey(10)
    if key >= 0:
        # 'n' key: create new quadrilateral
        if key == ord('n'):
            print 'pressed \'n\': create new quadrilateral'
            help_str = 'mark the four vertex to define a new quadrilateral'
            update_image()
            registering_quad = 4
        # 's' key: save data file
        elif key == ord('s'):
            print 'pressed \'s\': saving data to file'
            white_file()
        # Delete key: delete quadrilateral
        elif key == 65535:
            if selected_quad:
                print 'pressed \'Delete\': delete quadrilateral', selected_quad.get_string()
                quadrilaterals.remove(selected_quad)
                selected_quad = None
                update_image()
        # Esc key: exit
        elif key == 27:
            print 'pressed \'Esc\': exiting'
            break

cv2.destroyAllWindows()
