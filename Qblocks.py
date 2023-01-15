import cv2
import sys, pygame
import numpy as np
import Qstate as Q

def nothing(x):
    pass

#gates = [{0: 'x', 1: 'x'}, {0: 'h'}, {0: 'cnot'}]
#q = Q.state(qubits)

pygame.init()

cap = cv2.VideoCapture(0)
WINDOW_WIDTH = int(cap.get(3))
WINDOW_HEIGHT = int(cap.get(4))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

qubits = 5
block = int(WINDOW_HEIGHT / (qubits))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 48)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    l_h = 114
    l_s = 0
    l_v = 118
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    if int(cv2.__version__[0]) > 3:
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            if len(approx) == 3:
                print("Triangle: " + str(x) + "," + str(y))
                cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
            elif len(approx) == 4:
                print("Rectangle: " + str(x) + "," + str(y))
                cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            elif 6 < len(approx) < 30:
                print("Circle: " + str(x) + "," + str(y))
                cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

    screen.fill(WHITE)
    for x in range(0, WINDOW_WIDTH, block):
        for y in range(0, WINDOW_HEIGHT, block):
            rect = pygame.Rect(x, y, block, block)
            pygame.draw.rect(screen, BLACK, rect, 1)

    for i in range(1, qubits):
        cv2.line(frame, (0, i*block), (WINDOW_WIDTH, i*block), (0, 0, 0), 3)
    for i in range(1, qubits):
        cv2.line(frame, (, 0), (, WINDOW_HEIGHT), (0, 0, 0), 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    pygame.display.update()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()