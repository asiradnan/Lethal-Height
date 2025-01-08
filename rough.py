from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

controlLight = 0.5  # Controls background interpolation between day and night

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def getBackgroundColor(control):
    # Interpolates background color between blue (night) and white (day)
    dayColor = [1.0, 1.0, 1.0]
    nightColor = [0.0, 0.0, 0.5]
    r = nightColor[0] + control * (dayColor[0] - nightColor[0])
    g = nightColor[1] + control * (dayColor[1] - nightColor[1])
    b = nightColor[2] + control * (dayColor[2] - nightColor[2])
    return r, g, b

def getSunColor(control):
    # Interpolates the sun's color from yellow (day) to black (night)
    black = [1.0, 1.0, 0.0]  # Sun's color during the day
    yellow = [0.0, 0.0, 0.0]   # Sun's color during the night
    r = yellow[0] * (1 - control) + black[0] * control
    g = yellow[1] * (1 - control) + black[1] * control
    b = yellow[2] * (1 - control) + black[2] * control
    return r, g, b

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
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()
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
    P = 1 - r
    draw_line(x_centre + x, y_centre, x_centre - x, y_centre, size)  # Horizontal line for the center
    draw_line(x_centre, y_centre + x, x_centre, y_centre - x, size)  # Vertical line for the center
    while x > y:
        y += 1
        if P <= 0:
            P = P + 2 * y + 1
        else:
            x -= 1
            P = P + 2 * y - 2 * x + 1
        if x < y:
            break
        # Drawing octants
        draw_line(x_centre + x, y_centre + y, x_centre - x, y_centre + y, size)
        draw_line(x_centre + x, y_centre - y, x_centre - x, y_centre - y, size)
        draw_line(x_centre + y, y_centre + x, x_centre - y, y_centre + x, size)
        draw_line(x_centre + y, y_centre - x, x_centre - y, y_centre - x, size)

def draw_sun():
    # Get sun color based on the current day-night control
    r, g, b = getSunColor(controlLight)
    glColor3f(r, g, b)  # Set the sun color
    draw_circle(600, 600, 30)  # Draw filled circle for the sun

    # Draw sun rays using Midpoint Line Algorithm
    for angle in range(0, 360, 15):  # 15-degree step for rays
        rad = angle * math.pi / 180.0
        x1 = 600 + 30 * math.cos(rad)  # Start point of the ray
        y1 = 600 + 30 * math.sin(rad)
        x2 = 600 + 60 * math.cos(rad)  # End point of the ray
        y2 = 600 + 60 * math.sin(rad)
        draw_line(x1, y1, x2, y2)  # Draw each ray

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the buffer
    glLoadIdentity()
    iterate()

    # Get interpolated background color
    r, g, b = getBackgroundColor(controlLight)
    glClearColor(r, g, b, 1.0)  # Set background color

    # Draw the sun AFTER setting the background
    draw_sun()

    glutSwapBuffers()

def keyboardListener(key, x, y):
    global controlLight
    if key == b'n':  # Night (day to night)
        print("Night++")
        if controlLight >= 1:
            controlLight = 1
        else:
            controlLight += 0.06
    elif key == b'm':  # Day (night to day)
        print("Day++")
        if controlLight <= 0:
            controlLight = 0
        else:
            controlLight -= 0.06
    glutPostRedisplay()  # Ensure the screen updates

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Sun with Background")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutMainLoop()

main()
