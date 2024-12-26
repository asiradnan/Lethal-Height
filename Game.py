from OpenGL.GL import *
from OpenGL.GLUT import *

R,G,B = 1,1,1
player1_y, player2_y = 0, 0
def draw_points(x, y, size, flag):
    global R,G,B
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3f(R,G,B)
    glVertex2f(x,y)
    glEnd()

def draw_line(X1, Y1, X2, Y2, size=5):
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
    for _ in range(dx + 1):
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

def draw_circle(x_centre, y_centre, r, size=5):
    x = r
    y = 0
    draw_points(x + x_centre, y + y_centre, size, False)
    if (r > 0):
        draw_points(x + x_centre, -y + y_centre,size, False)
        draw_points(y + x_centre, x + y_centre,size, False)
        draw_points(-y + x_centre, x + y_centre,size, False)
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
        draw_points(x + x_centre, y + y_centre,size, False)
        draw_points(-x + x_centre, y + y_centre,size, False)
        draw_points(x + x_centre, -y + y_centre,size, False)
        draw_points(-x + x_centre, -y + y_centre,size, False)
        if x != y:
            draw_points(y + x_centre, x + y_centre,size, False)
            draw_points(-y + x_centre, x + y_centre,size, False)
            draw_points(y + x_centre, -x + y_centre,size, False)
            draw_points(-y + x_centre, -x + y_centre,size, False)

def draw_player1():
    global player1_y
    #1. LEG
    #Left leg
      # Green color for the rectangle
    draw_line(30,player1_y+40,40,40+player1_y)  # Bottom edge
    draw_line(40,player1_y+40,40,70+player1_y)  # Right edge
    draw_line(30,player1_y+70,40,70+player1_y)  # Top edge
    draw_line(30,player1_y+70,30,40+player1_y)  # Left edge

    #Right leg
    draw_line(40,player1_y+ 40, 50, 40+player1_y)  # Bottom edge
    draw_line(50,player1_y+ 40, 50, 70+player1_y)  # Right edge
    draw_line(50,player1_y+ 70, 40, 70+player1_y)  # Top edge
    draw_line(40,player1_y+ 70, 40, 40+player1_y)  # Left edge

    #2. Shoe
    #Left Shoe
    draw_line(30,player1_y+ 40, 40, 40+player1_y)  # Bottom edge
    draw_line(40,player1_y+ 40, 40, 30+player1_y)  # Right edge
    draw_line(30,player1_y+ 30, 40, 30+player1_y)  # Top edge
    draw_line(30,player1_y+ 30, 30, 40+player1_y)  # Left edge

    # Right Shoe
    draw_line(40,player1_y+ 40, 50, 40+player1_y)  # Bottom edge
    draw_line(50,player1_y+ 40, 50, 30+player1_y)  # Right edge
    draw_line(50,player1_y+ 30, 40, 30+player1_y)  # Top edge
    draw_line(40,player1_y+ 30, 40, 40+player1_y)  # Left edge

    #3. Body
    draw_line(30,player1_y+ 70, 50, 70+player1_y)  # Bottom edge
    draw_line(50,player1_y+ 70, 50, 100+player1_y)  # Right edge
    draw_line(50,player1_y+ 100, 30, 100+player1_y)  # Top edge
    draw_line(30,player1_y+ 100, 30, 70+player1_y)  # Left edge

    #4. Head
    draw_circle(40, 110+player1_y, 10)

    #5.hand
    draw_line(50,player1_y+90,60,90+player1_y)  # Bottom edge
    draw_line(60,player1_y+90,60,100+player1_y)  # Right edge
    draw_line(60,player1_y+100,50,100+player1_y)
    draw_line(50,player1_y+100,50,90+player1_y)

    #6. gun
    draw_line(60,player1_y+100,90,100+player1_y)  # Bottom edge
    draw_line(90,player1_y+100,95,90+player1_y)  # Right edge
    draw_line(95,player1_y+90,65,95+player1_y)  # Top edge
    draw_line(65,player1_y+95,65,80+player1_y)  # Left edge
    draw_line(65,player1_y+80,60,80+player1_y)
    draw_line(60,player1_y+80,60,100+player1_y)
    draw_line(60,player1_y+100,90,100+player1_y)


def draw_player2():
    global player2_y
    #1. LEG
    #Left leg
    draw_line(760,+player2_y+40,770,40+player2_y)  # Bottom edge  (X: x1=800-40,x2=800-30+player2_y)
    draw_line(770,+player2_y+40,770,70+player2_y)  # Right edge
    draw_line(760,+player2_y+70,770,70+player2_y)  # Top edge
    draw_line(760,+player2_y+70,760,40+player2_y)  # Left edge

    #Right leg
    draw_line(750,+player2_y+ 40, 760, 40+player2_y)  # Bottom edge  (X: x1=800-50,x2=800-40+player2_y)
    draw_line(760,+player2_y+ 40, 760, 70+player2_y)  # Right edge
    draw_line(760,+player2_y+ 70, 750, 70+player2_y)  # Top edge
    draw_line(750,+player2_y+ 70, 750, 40+player2_y)  # Left edge

    #2. Shoe
    #Left Shoe
    draw_line(760,+player2_y+ 40, 770, 40+player2_y)  # Bottom edge
    draw_line(770,+player2_y+ 40, 770, 30+player2_y)  # Right edge
    draw_line(760,+player2_y+ 30, 770, 30+player2_y)  # Top edge
    draw_line(760,+player2_y+ 30, 760, 40+player2_y)  # Left edge

    # Right Shoe
    draw_line(750,+player2_y+ 40, 760, 40+player2_y)  # Bottom edge
    draw_line(760,+player2_y+ 40, 760, 30+player2_y)  # Right edge
    draw_line(760,+player2_y+ 30, 750, 30+player2_y)  # Top edge
    draw_line(750,+player2_y+ 30, 750, 40+player2_y)  # Left edge

    #3. Body
    draw_line(750,+player2_y+ 70, 770, 70+player2_y)  # Bottom edge  (x1=800-50,x2=800-30+player2_y)
    draw_line(770,+player2_y+ 70, 770, 100+player2_y)  # Right edge
    draw_line(770,+player2_y+ 100, 750, 100+player2_y)  # Top edge
    draw_line(750,+player2_y+ 100, 750, 70+player2_y)  # Left edge


    #4. Head
    draw_circle(760, 110+player2_y, 10) #x=800-40

    #5.hand
    draw_line(740,+player2_y+90,750,90+player2_y)  # Bottom edge  #x1=800-60, x2=800-50
    draw_line(750,+player2_y+90,750,100+player2_y)  # Right edge
    draw_line(750,+player2_y+100,740,100+player2_y)
    draw_line(740,+player2_y+100,740,90+player2_y)

    #6. gun
    draw_line(710,+player2_y+100,740,100+player2_y)
    draw_line(710,+player2_y+100,710,90+player2_y)
    draw_line(735,+player2_y+95,710,90+player2_y)
    draw_line(735,+player2_y+95,735,80+player2_y)
    draw_line(740,+player2_y+80,735,80+player2_y)
    draw_line(740,+player2_y+80,740,100+player2_y)
    draw_line(710,+player2_y+100,740,100+player2_y)

def draw_walls():
    draw_line(120,0,120,220)
    draw_line(680,0,680,220)



def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    draw_player1()
    draw_player2()
    draw_walls()


    glutSwapBuffers()

def redraw():
    
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global player1_y
    if key == b'w':
        player1_y += 10
    elif key == b's':
        player1_y -= 10

def specialKeyListener(key, x, y):
    global  player2_y
    if key == GLUT_KEY_UP:
        player2_y += 10
    elif key == GLUT_KEY_DOWN:
        player2_y -= 10
        


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600)  #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Game!")  #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)
glutIdleFunc(redraw)
make_game_over = False
glutMainLoop()