from OpenGL.GL import *
from OpenGL.GLUT import *
import threading
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

R,G,B = 1,1,1
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



def decrease_walls():
    global wall_height
    while True:
        if not paused and wall_height > 0:
            wall_height -= wall_decrease_rate
        time.sleep(0.01)


def shoot_bullet(player, x, y, direction):
    global last_shot_time
    current_time = time.time()
    if current_time - last_shot_time[player] >= cooldown:
        bullets.append((x, y, direction))
        last_shot_time[player] = current_time

def check_bullet_collision():
    global bullets, player1_health, player2_health, player1_score, player2_score, game_over
    new_bullets = []
    for x, y, direction in bullets:
        if direction == 1:  # Player 1's bullet
            if 740 <= x <= 770 and player2_y + 30 <= y <= player2_y + 120:  # Check collision with Player 2's body
                player2_health -= 1
                player1_score += 1
                if player2_health <= 0:
                    game_over = True
                    print("Player 1 wins!")
                continue  # Skip adding this bullet
        elif direction == -1:  # Player 2's bullet
            if 30 <= x <= 60 and player1_y + 30 <= y <= player1_y + 120:
                player1_health -= 1
                player2_score += 1
                if player1_health <= 0:
                    game_over = True
                    print("Player 2 wins!")
                continue  # Skip adding this bullet
        new_bullets.append((x, y, direction))
    bullets = new_bullets

def move_bullets():
    global bullets
    new_bullets = []
    for x, y, direction in bullets:
        new_x = x + (bullet_speed * direction)
        if direction==-1 and y<=wall_height and x<=680: continue
        elif direction == 1 and y<=wall_height and x>=120: continue
        if 0 <= new_x <= 800: 
            new_bullets.append((new_x, y, direction))
    bullets = new_bullets
def manage_bullets():
    while True:
        move_bullets()
        check_bullet_collision()
        time.sleep(0.01)

def draw_bullets():
    for x, y, _ in bullets:
        draw_circle(x, y, 5, size=3)

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
    draw_line(120, 0, 120, wall_height)
    draw_line(680, 0, 680, wall_height)



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
    draw_bullets() 

    draw_text(10, SCREEN_HEIGHT - 65, f"Player 1 Score: {player1_score}", 0.2)
    draw_text(535, SCREEN_HEIGHT - 65, f"Player 2 Score: {player2_score}", 0.2)
    draw_text(10, SCREEN_HEIGHT - 105, f"Player 1 Health: {player1_health}/10", 0.2)
    draw_text(495, SCREEN_HEIGHT - 105, f"Player 2 Health: {player2_health}/10", 0.2)

    draw_pause_button(20, SCREEN_HEIGHT-40)
    draw_cross_button(SCREEN_WIDTH-40, SCREEN_HEIGHT-40)
    draw_restart_button(SCREEN_WIDTH/2-10, SCREEN_HEIGHT-40)

    # if game_over:
    #     if player1_score > player2_score:
    #         print(f"Player 1 wins with the score: {player1_score}")
    #     else:
    #         print(f"Player 2 wins with the score: {player2_score}")

    #     draw_text(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, "GAME OVER", 0.3)

    glutSwapBuffers()

def redraw():
    if game_over or  paused:
        return
    move_bullets()
    check_bullet_collision() 
    glutPostRedisplay()

def move_player1():
    global player1_y, player1_up, player1_down
    while True:
        if player1_up:
            player1_y = min(480, player1_y+player_speed)
        if player1_down:
            player1_y = max(0,player1_y-player_speed)
        time.sleep(0.01)

def move_player2():
    global player2_y, player2_up, player2_down
    while True:
        if player2_up:
            player2_y = min(480, player2_y+player_speed)
        if player2_down:
            player2_y = max(0,player2_y-player_speed)
        time.sleep(0.01)

# Update keyboard listeners
def keyboardListener(key, x, y):
    global player1_up, player1_down
    if key == b'w':
        player1_up = True
    elif key == b's':
        player1_down = True

def keyboardUpListener(key, x, y):
    global player1_up, player1_down
    if key == b'w':
        player1_up = False
    elif key == b's':
        player1_down = False
    elif key == b'd':  
        shoot_bullet("player1", 90, 100 + player1_y, 1)

def specialKeyListener(key, x, y):
    global player2_up, player2_down
    if key == GLUT_KEY_UP:
        player2_up = True
    elif key == GLUT_KEY_DOWN:
        player2_down = True
    elif key == GLUT_KEY_LEFT: 
        shoot_bullet("player2", 710, 100 + player2_y, -1)

def specialKeyUpListener(key, x, y):
    global player2_up, player2_down
    if key == GLUT_KEY_UP:
        player2_up = False
    elif key == GLUT_KEY_DOWN:
        player2_down = False

def draw_pause_button(x, y, size=20):
    if paused:
        # Draw play triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(x, y)
        glVertex2f(x, y + size)
        glVertex2f(x + size, y + size/2)
        glEnd()
    else:
        # Draw pause bars
        draw_line(x, y, x, y + size)
        draw_line(x + size/2, y, x + size/2, y + size)

def draw_cross_button(x, y, size=20):
    draw_line(x, y, x + size, y + size)
    draw_line(x, y + size, x + size, y)

def draw_restart_button(x, y, size=20):
    draw_circle(x + size/2, y + size/2, size/2)
    # Draw arrow
    draw_line(x + size/2, y + size, x + size, y + size/2)
    draw_line(x + size, y + size/2, x + size/2, y)

def draw_text(x, y, text, scale=1.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, scale)
    glColor3f(1.0, 1.0, 1.0)
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()

def mouseListener(button, state, x, y):
    global paused, show_menu, player1_health, player2_health, player1_score, player2_score, game_over
    if state == GLUT_DOWN:
        # Convert window coordinates to OpenGL coordinates
        y = SCREEN_HEIGHT - y
        
        # Check pause button (top left)
        if 20 <= x <= 40 and SCREEN_HEIGHT-40 <= y <= SCREEN_HEIGHT-20:
            paused = not paused
            
        # Check cross button (top right)
        if SCREEN_WIDTH-40 <= x <= SCREEN_WIDTH-20 and SCREEN_HEIGHT-40 <= y <= SCREEN_HEIGHT-20:
            glutLeaveMainLoop()
            
        # Check restart button (top middle)
        if SCREEN_WIDTH/2-10 <= x <= SCREEN_WIDTH/2+10 and SCREEN_HEIGHT-40 <= y <= SCREEN_HEIGHT-20:
            # Reset game state
            player1_health = 10
            player2_health = 10
            player1_score = 0
            player2_score = 0
            paused = False
            game_over = False

# Start threads
threading.Thread(target=move_player1, daemon=True).start()
threading.Thread(target=move_player2, daemon=True).start()
threading.Thread(target=manage_bullets, daemon=True).start()
threading.Thread(target=decrease_walls, daemon=True).start()

        


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)  #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Game!")  #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardUpFunc(keyboardUpListener)
glutSpecialUpFunc(specialKeyUpListener)
glutMouseFunc(mouseListener)
glutIdleFunc(redraw)
make_game_over = False
glutMainLoop()