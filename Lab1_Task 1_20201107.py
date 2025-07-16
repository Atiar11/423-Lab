from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

raindrops = []  # List to store raindrop coordinates and velocities
is_day = True
rain_direction = 0.0  # Initial rain direction

def init():  #initialization
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    init()
    draw()
    updateRain()
    glutSwapBuffers()
    glutPostRedisplay()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(2)
    glLoadIdentity()

    if is_day:
        # Daytime colors
        glClearColor(0.7, 0.9, 1.0, 1.0)  # Light blue background for day
        glColor3f(0.0, 0.6, 0.0)  # Green color for the roof during the day
        glColor3f(0.1, 0.4, 0.6)  # Blue color for windows and door during the day
        raindrop_color = (0.0, 0.0, 1.0)  # White color for raindrops during the day
    else:
        # Nighttime colors
        glClearColor(0.0, 0.0, 0.2, 1.0)  # Dark blue background for night
        glColor3f(0.0, 0.3, 0.0)  # Dark green color for the roof during the night
        glColor3f(0.0, 0.2, 0.4)  # Dark blue color for windows and door during the night
        raindrop_color = (0.5, 0.5, 1.0)  # Light blue color for raindrops during the night

    # Drawing the house
    #color of the roof
    glColor3f(0.0, 0.6, 0.0) 

    # Roof (change the vertices to modify the shape)
    glBegin(GL_TRIANGLES)
    glVertex2f(250, 350)
    glVertex2f(350, 250)
    glVertex2f(150, 250)
    glEnd()

    # House Body
    glColor3f(0.0, 0.5, 0.5)
    
    glBegin(GL_QUADS)
    glVertex2f(150, 50)
    glVertex2f(150, 250)
    glVertex2f(350, 250)
    glVertex2f(350, 50)
    glEnd()

    # color for the windows and door
    glColor3f(0.1, 0.4, 0.6)

    # Windows
    glBegin(GL_QUADS)
    glVertex2f(175, 225)
    glVertex2f(175, 175)
    glVertex2f(225, 175)
    glVertex2f(225, 225)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(275, 225)
    glVertex2f(275, 175)
    glVertex2f(325, 175)
    glVertex2f(325, 225)
    glEnd()

    # Door
    glBegin(GL_QUADS)
    glVertex2f(225, 50)
    glVertex2f(225, 125)
    glVertex2f(275, 125)
    glVertex2f(275, 50)
    glEnd()

    # Doorknob
    glColor3f(1.0, 1.0, 0.0)  # yellow color for the doorknob
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(262.5, 87.5)
    glEnd()

    # raindrops
    glColor3f(*raindrop_color)
    for x, y, vy in raindrops:
        glBegin(GL_LINES)
        glVertex2f(x, y)
        glVertex2f(x + rain_direction, y + 5)  #rain direction #shape of raindrops
        glEnd()

def updateRain():
    for i in range(len(raindrops)):
        x, y, vy = raindrops[i]
        y -= vy
        if y < 0:
            y = random.uniform(450, 500)  #raindrop position
            x = random.uniform(0, 500)
        raindrops[i] = (x, y, vy)

#input handling
def toggle_day_night():
    global is_day
    is_day = not is_day

def control_rain_direction(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 1.0  # Move rain to the left
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 1.0  # Move rain to the right

def keyPressed(key, x, y):
    if key == b'N' or key == b'n':
        toggle_day_night()  # Toggle between day and night
    elif key == b'D' or key == b'd':
        toggle_day_night()  # Toggle between day and night

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Atiar Osman CSE423 LAB1-TASK1")
glutDisplayFunc(showScreen)
glutSpecialFunc(control_rain_direction)
glutKeyboardFunc(keyPressed)

# Initialize raindrops speed
for _ in range(100):
    x = random.uniform(0, 500)
    y = random.uniform(0, 500)
    vy = random.uniform(1, 5)
    raindrops.append((x, y, vy))

init()

glutMainLoop()
