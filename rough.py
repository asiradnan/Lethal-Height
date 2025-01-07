# Task - 1
from math import cos, sin, radians

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w, h = 800, 800
player1_y, player2_y = 0, 0
num_drops = 200
raindrops = []
control = 0
controlLight = 0
R, G, B = 0,0,0
player1_y, player2_y = 0, 0
player1_up = False
player1_down = False
player2_up = False
player2_down = False
player_speed = 5

player1_health = 10
player2_health = 10

player1_score = 0
player2_score = 0

wall_height = 220
wall_decrease_rate = 0.05  # Pixels per second

game_over = False
paused = False
show_menu = True

last_shot_time = {"player1": 0, "player2": 0}
cooldown = 0.5
bullets = []
bullet_speed = 10

night_mode_presses = 0  # Track number of night mode presses
circle_y = 650          # Starting Y position of the circle
circle_move_step = 5    # Step size for moving the circle
min_circle_y = 430
def draw_points(x, y, size, flag):
    global R, G, B
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3f(R, G, B)
    glVertex2f(x, y)
    glEnd()
def draw_line(X1, Y1, X2, Y2, size=2):
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    sx = 1 if X2 > X1 else -1  # Step for x
    sy = 1 if Y2 > Y1 else -1  # Step for y
    if dy > dx:
        dx, dy = dy, dx
        steep = True
    else:
        steep = False
    d = 2 * dy - dx
    x, y = X1, Y1
    for _ in range(int(dx + 1)):
        draw_points(x, y, size, True)
        if d > 0:
            if steep:
                x += sx
            else:
                y += sy
            d -= 2 * dx
        if steep:
            y += sy
        else:
            x += sx
        d += 2 * dy

def draw_circle(x_centre, y_centre, r, size=2):
    x = r
    y = 0
    draw_points(x + x_centre, y + y_centre, size, False)
    if (r > 0):
        draw_points(x + x_centre, -y + y_centre, size, False)
        draw_points(y + x_centre, x + y_centre, size, False)
        draw_points(-y + x_centre, x + y_centre, size, False)
    P = 1 - r
    while x > y:
        y += 1
        if P <= 0:
            P = P + 2 * y + 1
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1
        if (x < y):
            break
        draw_points(x + x_centre, y + y_centre, size, False)
        draw_points(-x + x_centre, y + y_centre, size, False)
        draw_points(x + x_centre, -y + y_centre, size, False)
        draw_points(-x + x_centre, -y + y_centre, size, False)
        if x != y:
            draw_points(y + x_centre, x + y_centre, size, False)
            draw_points(-y + x_centre, x + y_centre, size, False)
            draw_points(y + x_centre, -x + y_centre, size, False)
            draw_points(-y + x_centre, -x + y_centre, size, False)


def try1():
    # Draw the filled circle (inner part) with red color
    radius = 50
    center_x, center_y = 600, circle_y

    glColor3f(1.0, 0.0, 0.0)
    draw_circle(center_x, center_y, radius)


def specialKeyListener(key, x, y):
    global control
    if key==GLUT_KEY_RIGHT:
        print("Directiong to Right")
        control+=1
        if control >= 12:
            control = 12
            print("In maximum Right!!!!!")
    if key==GLUT_KEY_LEFT:
        print("Directiong to Left")
        control-=1
        if control <= -12:
            control = -12
            print("In maximum Left!!!!!")

def keyboardListener(key, x, y):
    global controlLight, circle_y, night_mode_presses
    if key == b'n':
        print("Night++")
        if controlLight >= 1:
            controlLight = 1
        else:
            controlLight += 0.06
    if key == b'm':
        print("Day++")
        if controlLight <= 0:
            controlLight = 0
        else:
            controlLight -= 0.06

def iterate():
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def getBackgroundColor(controlLight):
    colors = [
        (0.9, 0.4, 0.1),  # Dark Orange
        (1.0, 0.8, 0.2),  # Yellow
        (0.9, 0.9, 0.7),  # Yellowish White
        (0.6, 0.8, 1.0),  # Light Sky Blue
        (0.1, 0.1, 0.5),  # Dark Blue
        (0.0, 0.0, 0.0),  # Black
    ]
    num_stages = len(colors) - 1
    stage = min(int(controlLight * num_stages), num_stages - 1)  # Clamp stage to valid range
    stage_progress = (controlLight * num_stages) - stage  # Progress within the stage

    if stage < num_stages:
        r = colors[stage][0] + (colors[stage + 1][0] - colors[stage][0]) * stage_progress
        g = colors[stage][1] + (colors[stage + 1][1] - colors[stage][1]) * stage_progress
        b = colors[stage][2] + (colors[stage + 1][2] - colors[stage][2]) * stage_progress
    else:
        r, g, b = colors[-1]

    return r, g, b


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    try1()
    r, g, b = getBackgroundColor(controlLight)
    glClearColor(r, g, b, 1.0)
    glutSwapBuffers()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(20, update, 0)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Task1_21201543")
glutDisplayFunc(showScreen)
glutTimerFunc(0, update, 0)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()