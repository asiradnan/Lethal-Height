import threading
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Shared variables
pressed_keys = set()  # To track keys pressed
lock = threading.Lock()  # To ensure thread-safe access

rotation_angle = [0.0, 0.0]  # X and Y rotation angles

# Thread function to listen for key updates
def key_listener():
    while True:
        with lock:
            # Update rotation based on pressed keys
            if b'w' in pressed_keys:
                rotation_angle[0] += 1.0  # Rotate upward
            if b's' in pressed_keys:
                rotation_angle[0] -= 1.0  # Rotate downward
            if b'a' in pressed_keys:
                rotation_angle[1] -= 1.0  # Rotate left
            if b'd' in pressed_keys:
                rotation_angle[1] += 1.0  # Rotate right

        time.sleep(0.01)  # Avoid high CPU usage

# OpenGL display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Apply rotation
    glRotatef(rotation_angle[0], 1.0, 0.0, 0.0)  # Rotate around X-axis
    glRotatef(rotation_angle[1], 0.0, 1.0, 0.0)  # Rotate around Y-axis

    # Render a simple cube
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glEnd()

    glutSwapBuffers()

# Timer function to update the display
def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # ~60 FPS

# Keyboard press function
def key_pressed(key, x, y):
    with lock:
        pressed_keys.add(key)

# Keyboard release function
def key_released(key, x, y):
    with lock:
        pressed_keys.discard(key)

# OpenGL initialization
def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)

# Main function
def main():
    # Start the key listener thread
    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()

    # Initialize GLUT and create a window
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Threading Test with Key Listener")

    init_opengl()

    # Register GLUT callbacks
    glutDisplayFunc(display)
    glutKeyboardFunc(key_pressed)
    glutKeyboardUpFunc(key_released)
    glutTimerFunc(16, timer, 0)

    # Start the GLUT main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
