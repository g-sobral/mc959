#!/usr/bin/python2.7

import cv2

window = 'MC959 Problem Set 01'
original_img = None
quadrilaterals = []
selected_vert = None
selected_quad = None
registering_quad = 0
new_quad = {'x': [], 'y': []}


class Quadrilateral:
    def __init__(self, x, y, plate):
        self.x = x
        self.y = y
        self.plate = plate

    def contains(self, x, y):
        if x > min(self.x) and x < max(self.x) and y > min(self.y) and y < max(self.y):
            return True
        return False

    def has_vertice(self, x, y):
        for i in range(0, 4):
            if x >= (self.x[i] - 10) and x <= (self.x[i] + 10) and y >= (self.y[i] - 10) and y <= (self.y[i] + 10):
                return i
        return -1

    def get_vertice(self, index):
        return (self.x[index], self.y[index])

    def set_vertice(self, index, x, y):
        self.x[index] = x
        self.y[index] = y

    def move(self, dx, dy):
        for i in range(0, 4):
            self.x[i] += dx
            self.y[i] += dy

    def draw(self, img):
        self.print_points()
        # draw lines
        for i in range(-1, 3):
            cv2.line(img,
                     (self.x[i], self.y[i]),
                     (self.x[i + 1], self.y[i + 1]),
                     (0, 255, 0),
                     3)
        # draw vertices
        for i in range(0, 4):
            cv2.rectangle(img,
                          (self.x[i] - 10, self.y[i] - 10),
                          (self.x[i] + 10, self.y[i] + 10),
                          (255, 0, 255),
                          -1)
        # draw license plate string
        cv2.putText(img, self.plate, (self.x[1], self.y[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,
      (255,0,255), 5)

    def print_points(self):
        print 'x:', self.x
        print 'y:', self.y

    def set_plate(self, plate):
        self.plate = plate

    def print_plate(self):
        print self.plate


def on_mouse_event(event, x, y, flags, param):
    global quadrilaterals
    global selected_vert
    global selected_quad
    global original_img
    global registering_quad
    global new_quad

    if event == cv2.EVENT_LBUTTONDOWN:
        print 'I: left button down:', x, y

        if registering_quad:
            new_quad['x'].append(x)
            new_quad['y'].append(y)
            registering_quad -= 1
            if registering_quad == 0:
                new_quadrilateral(new_quad['x'], new_quad['y'])
            return

        for quad in quadrilaterals:
            i = quad.has_vertice(x, y)
            if i != -1:
                selected_vert = {'quad': quad, 'vert': i}
                print 'I: selected vertice:', i
                break
            elif quad.contains(x, y):
                selected_quad = {'quad': quad, 'x0': x, 'y0': y}
                print 'I: selected quad'
                break
    elif event == cv2.EVENT_LBUTTONUP:
        print 'I: left button up:', x, y
        if selected_vert:
            quad = selected_vert['quad']
            quad.set_vertice(selected_vert['vert'], x, y)
        elif selected_quad:
            quad = selected_quad['quad']
            quad.move(x - selected_quad['x0'], y - selected_quad['y0'])

        selected_vert = None
        selected_quad = None

        img = original_img.copy()
        for quad in quadrilaterals:
            quad.draw(img)
        cv2.imshow(window, img)

def new_quadrilateral(x, y):
    global quadrilaterals

    print 'I: new quadrilateral:', x, y

    q = Quadrilateral(x, y, 'abc1234')
    quadrilaterals.append(q)


cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window, on_mouse_event)

original_img = cv2.imread('../dataset_01/L0.jpg', cv2.IMREAD_UNCHANGED)

q = Quadrilateral([100, 150, 400, 500], [300, 200, 300, 800], 'abc1234')
quadrilaterals.append(q)

img = original_img.copy()
for quad in quadrilaterals:
    quad.draw(img)
cv2.imshow(window, img)

while True:
    k = cv2.waitKey(10)
    if k == ord('n'):
        print 'I: registering new quadrilateral'
        registering_quad = 4
    elif k == 27:         # wait for ESC key to exit
        break

cv2.destroyAllWindows()
