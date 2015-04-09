#!/usr/bin/python2.7

import cv2

window = 'MC959 Problem Set 01'
original_img = None
quadrilaterals = []
selected_vert = None
selected_quad = None


class Quadrilateral:
    x = []
    y = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def contains(self, x, y):
        if x > min(self.x) and x < max(self.x) and y > min(self.y) and y < max(self.y):
            return True
        return False

    def has_vertice(self, x, y):
        for i in range(0, 4):
            print i, self.x[i], self.y[i]
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

    def print_points(self):
        print 'x:', self.x
        print 'y:', self.y


def on_mouse_event(event, x, y, flags, param):
    global quadrilaterals
    global selected_vert
    global selected_quad
    global original_img

    if event == cv2.EVENT_LBUTTONDOWN:
        print 'I: left button down:', x, y
        for quad in quadrilaterals:
            i = quad.has_vertice(x, y)
            if i != -1:
                selected_vert = {'quad': quad, 'vert': i}
                print 'I: selected vertice:', selected_vert
                break
            elif quad.contains(x, y):
                selected_quad = {'quad': quad, 'x0': x, 'y0': y}
                print 'I: selected quad:', selected_quad
                break
    elif event == cv2.EVENT_LBUTTONUP:
        print 'I: left button up:', x, y
        if selected_vert:
            quad = selected_vert['quad']
            quad.set_vertice(selected_vert['vert'], x, y)
        elif selected_quad:
            quad = selected_quad['quad']
            quad.move(x - selected_quad['x0'], y - selected_quad['y0'])
        else:
            return

        selected_vert = None
        selected_quad = None

        img = original_img.copy()
        for quad in quadrilaterals:
            quad.draw(img)
        cv2.imshow(window, img)

cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window, on_mouse_event)

original_img = cv2.imread('../dataset_01/L0.jpg', cv2.IMREAD_UNCHANGED)

q = Quadrilateral([100, 150, 400, 500], [300, 200, 300, 800])
quadrilaterals.append(q)

img = original_img.copy()
for quad in quadrilaterals:
    quad.print_points()
    quad.draw(img)
cv2.imshow(window, img)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
