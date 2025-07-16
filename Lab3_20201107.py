from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 80

# Circle class
class GrowingCircle:
    def __init__(self, center_x, center_y, radius, growth_rate, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.growth_rate = growth_rate
        self.color = color  # Add color attribute

    def update(self):
        self.radius += self.growth_rate

    def is_outside_window(self):
        return (
            self.center_x - self.radius < 0
            or self.center_x + self.radius > WINDOW_WIDTH
            or self.center_y - self.radius < 0
            or self.center_y + self.radius > WINDOW_HEIGHT
        )

# Variables
growing_circles = []
is_paused = False
growth_rate = 1

# Initialize GLUT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Lab3_20201107")

# Initialize OpenGL
glClearColor(0, 0, 0, 0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_POINTS)

    for circle in growing_circles:
        draw_growing_circle(circle)

    glEnd()

    glutSwapBuffers()
    
#drawing a colored circle using midpoint circle drawing algorithm
def draw_growing_circle(circle):
    cx, cy, radius, color = circle.center_x, circle.center_y, int(circle.radius), circle.color

    d = 1 - radius
    x, y = 0, radius

    while x < y:
        draw_circle_points(x, y, cx, cy, color)

        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y = y - 1

        x = x + 1
        draw_circle_points(x, y, cx, cy, color)

def draw_circle_points(x, y, cx, cy, color):
    # glVertex2f calls for each of the 8 symmetric points
    glColor3f(*color)  # Set the color
    glVertex2f(cx + x, cy + y)
    glVertex2f(cx + y, cy + x)
    glVertex2f(cx + y, cy - x)
    glVertex2f(cx + x, cy - y)
    glVertex2f(cx - x, cy - y)
    glVertex2f(cx - y, cy - x)
    glVertex2f(cx - y, cy + x)
    glVertex2f(cx - x, cy + y)

def update(value):
    global is_paused, growth_rate, growing_circles

    if not is_paused:
        for circle in growing_circles:
            circle.update()

        growing_circles = [circle for circle in growing_circles if not circle.is_outside_window()]

    glutPostRedisplay()
    glutTimerFunc(int(1000 / FPS), update, 0)


# Keyboard function
def keyboard(key, x, y):
    global is_paused, growth_rate

    if key == b' ':
        is_paused = not is_paused

    elif key == b'q':
        glutLeaveMainLoop()

#handling arrow keys
def arrow_key(key, x, y):
    global growth_rate

    if key == GLUT_KEY_LEFT:
        growth_rate += 1
        for circle in growing_circles:
            circle.growth_rate = growth_rate

    elif key == GLUT_KEY_RIGHT:
        growth_rate = max(1, growth_rate - 1)
        for circle in growing_circles:
            circle.growth_rate = growth_rate

def check_circle_collision(new_circle, existing_circles):
    for circle in existing_circles:
        distance = ((new_circle.center_x - circle.center_x)**2 +
                    (new_circle.center_y - circle.center_y)**2)**0.5
        if distance < new_circle.radius + circle.radius:
            return True  # Collision detected
    return False  # No collision

# Inside the mouse function
def mouse(button, state, x, y):
    global growing_circles, is_paused

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        y = WINDOW_HEIGHT - y
        color = (random.random(), random.random(), random.random())
        new_circle = GrowingCircle(x, y, 5, growth_rate, color)

        # Check for collision with some tolerance before adding the new circle
        if not check_circle_collision(new_circle, growing_circles) and not is_paused:
            growing_circles.append(new_circle)
            glutPostRedisplay()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        glutPostRedisplay()


# Register functions
glutDisplayFunc(display) 
glutTimerFunc(int(1000 / FPS), update, 0)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_key)
glutMouseFunc(mouse)
glutMainLoop()
