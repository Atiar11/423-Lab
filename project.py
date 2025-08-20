from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math
import sys

# Global variables for rocket animation
x_pos = 370
radius_x = 100
object_width = radius_x
target_x_pos = x_pos
radius_y = 25
points = 0
game_paused = False


def draw_rocket(
    center_x, center_y, body_radius_x, body_radius_y, num_segments, nose_length
):
    # rocket body
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(center_x, center_y)

    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = center_x + body_radius_x * math.cos(angle)
        y = center_y + body_radius_y * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

    # Draw rocket nose
    glBegin(GL_TRIANGLES)
    nose_tip_x = center_x + body_radius_x + nose_length
    nose_tip_y = center_y
    glVertex2f(center_x + body_radius_x, center_y)

    glEnd()

    # Draw rocket fins
    fin_height = 30
    fin_base_width = 15
    fin_top_width = 5

    glBegin(GL_TRIANGLES)
    # Fin 1
    glVertex2f(center_x - body_radius_x, center_y)
    glVertex2f(center_x - body_radius_x - fin_base_width, center_y + fin_height)
    glVertex2f(center_x - body_radius_x - fin_top_width, center_y + fin_height)

    # Fin 2
    glVertex2f(center_x + body_radius_x, center_y)
    glVertex2f(center_x + body_radius_x + fin_base_width, center_y + fin_height)
    glVertex2f(center_x + body_radius_x + fin_top_width, center_y + fin_height)
    glEnd()

    # Draw rocket windows
    window_radius = 5
    num_windows = 4

    glColor3f(0.8, 0.8, 0.8)  # Window color (light gray)

    glBegin(GL_TRIANGLE_FAN)
    for i in range(num_windows):
        angle = 2.0 * math.pi * i / num_windows
        window_x = center_x + (body_radius_x - 20) * math.cos(angle)
        window_y = center_y + (body_radius_y - 20) * math.sin(angle)
        glVertex2f(window_x, window_y)
    glEnd()


def draw():
    glClearColor(0.5, 0.5, 0.5, 1.0)  # Set clear color to grey
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    if points >= 200:
        glColor3f(0.0, 0.0, 0.0)  # Black color

        e(100, 400, 200, 500)
        n(250, 400, 350, 500)
        d(400, 400, 500, 500)
    if points < 0:
        glColor3f(0.0, 0.0, 0.0)  # Black color

        e(100, 400, 200, 500)
        n(250, 400, 350, 500)
        d(400, 400, 500, 500)
    else:
        # Draw Meteorite
        for j in rocks:
            j.draw()

        for k in attacks:
            k.draw()

        # Draw Rocket (UFO)
        glColor3f(0.8, 0.8, 0.8)
        draw_rocket(
            x_pos, 100, radius_x, radius_y, 100, 30
        )  # Adjust nose length as needed

        glColor3f(0.2, 0.2, 0.2)
        # You can draw a smaller rocket body for additional details if needed
        draw_rocket(x_pos, 125, radius_x * 0.6, radius_y * 0.6, 100, 20)

    glColor3f(0.0, 0.0, 0.0)  # Black color
    pointcount(points)
    glutSwapBuffers()


def update_values(value):
    global x_pos, target_x_pos
    if points < 200:
        diff = target_x_pos - x_pos
        x_pos += diff * (0.5)

        glutPostRedisplay()
        glutTimerFunc(16, update_values, value)


attacks = []  # attack global varaible


class attack:
    def __init__(self, x_pos):
        self.x = x_pos
        self.y = 125
        self.speed = 0.5
        self.state = True

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)  # White color
        midpointCircle(5, self.x, self.y) #bullets


def key_input(key, x, y):
    global target_x_pos, attacks, game_paused

    if key == GLUT_KEY_RIGHT and target_x_pos < 800 - 130:
        target_x_pos += 50
    elif key == GLUT_KEY_LEFT and target_x_pos > 0 + 130:
        target_x_pos -= 50
    elif key == GLUT_KEY_UP:
        attacks.append(attack(target_x_pos))
    elif key == b"p" or key == b"P":
        game_paused = not game_paused
        if not game_paused:
            glutTimerFunc(16, update_values, 0)
            glutTimerFunc(1, update, 0)


def keyboard_input(key, x, y):
    global game_paused
    if key == b"p":
        game_paused = not game_paused
        if not game_paused:
            glutTimerFunc(16, update_values, 0)
            glutTimerFunc(1, update, 0)


# Global variables for stars and meteorites
rocks = []


class meteorite:
    def __init__(self):
        self.x = random.randint(130, 800 - 130)
        self.y = 800
        self.size = random.randint(30, 70)
        self.speed = 0.2  # speed of the meteorite
        self.color = (random.uniform(0.15, 0.25), random.uniform(0.08, 0.12), 0.0)
        self.status = True

    def draw(self):
        # meterorites
        glColor3fv(self.color)
        glBegin(GL_POLYGON)
        num_vertices = 6  # Change the number of vertices for a hexagon
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            vertex_x = self.x + self.size * math.cos(angle)
            vertex_y = self.y + self.size * math.sin(angle)
            glVertex2f(vertex_x, vertex_y)
        glEnd()

        # meteorite outline
        glColor3f(0.17, 0.08, 0.02)
        glLineWidth(5.0)
        glBegin(GL_LINE_LOOP)
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            vertex_x = self.x + self.size * math.cos(angle)
            vertex_y = self.y + self.size * math.sin(angle)
            glVertex2f(vertex_x, vertex_y)
        glEnd()


was_points_positive = False  # Initialize the variable


def update(value):
    global rocks
    global attacks
    global points
    global game_paused
    global was_points_positive

    if not game_paused and points < 200:
        # meteorite
        new_rocks = []
        for rock in rocks:
            rock.y = rock.y - rock.speed
            if rock.y > 0 and rock.status:
                new_rocks.append(rock)

            # Check if meteorite reaches the bottom
            if rock.y <= 0 and rock.status:
                rock.status = False
                points -= 10

        rocks = new_rocks

        # attack
        new_attacks = []
        for attack in attacks:
            attack.y += attack.speed
            if attack.y < 800 and attack.state:
                new_attacks.append(attack)

        attacks = new_attacks

        # damage
        for attack in attacks:
            if not attack.state:
                continue
            a, b = 0, 0
            for rock in rocks:
                if not rock.status:
                    continue
                a = rock.x - attack.x
                b = rock.y - attack.y
                if math.sqrt((a**2) + (b**2)) < rock.size + 5 + 5:
                    rock.status = False
                    attack.state = False
                    if rock.size >= 65:
                        points += 15
                    else:
                        points += 10

        was_points_positive = points > 0

    glutPostRedisplay()
    glutTimerFunc(1, update, value)


def create_meteorite(value):
    global rocks
    if points < 200:
        rocks.append(meteorite())
        glutTimerFunc(random.randint(500, 2000), create_meteorite, value)


# Point Generation
def draw_points(x, y):
    glPointSize(2)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def findZone(x0, y0, x1, y1):
    dy = y1 - y0
    dx = x1 - x0
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dy > 0:
            return 1
        else:
            return 5


def zeroconvert(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def originalconvert(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y


def midpointline(x1, y1, x2, y2, z):
    dx = x2 - x1
    dy = y2 - y1
    x = x1
    y = y1
    d = (2 * dy) - dx
    east = 2 * dy
    northeast = 2 * (dy - dx)
    if dx == 0:
        while y <= y2:
            t1, t2 = originalconvert(x, y, z)
            draw_points(t1, t2)
            y += 1
    else:
        while x <= x2:
            t1, t2 = originalconvert(x, y, z)
            draw_points(t1, t2)
            x += 1
            if d > 0:
                d += northeast
                y += 1
            else:
                d += east


# score number generation
def eightSem(x0, y0, x1, y1):
    z = findZone(x0, y0, x1, y1)
    x0_0, y0_0 = zeroconvert(x0, y0, z)
    x1_0, y1_0 = zeroconvert(x1, y1, z)
    midpointline(x0_0, y0_0, x1_0, y1_0, z)


def zero(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y1, x1, y2)


def one(x1, y1, x2, y2):
    eightSem(x2, y1, x2, y2)


def two(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x2, y2)
    eightSem(x1, y1, x1, (y1 + y2) // 2)
    eightSem(x2, (y1 + y2) // 2, x2, y2)


def three(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, y2, x2, y2)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x2, y1, x2, y2)


def four(x1, y1, x2, y2):
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x1, (y1 + y2) // 2)
    eightSem(x2, y1, x2, y2)


def five(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, (y1 + y2) // 2)
    eightSem(x1, (y1 + y2) // 2, x1, y2)


def six(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, (y1 + y2) // 2)
    eightSem(x1, y1, x1, y2)


def seven(x1, y1, x2, y2):
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)


def eight(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y1, x1, y2)


def nine(x1, y1, x2, y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, (y1 + y2) // 2, x2, (y1 + y2) // 2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y2, x1, (y1 + y2) // 2)


def e(x1, y1, x2, y2):
    eightSem(x1, y1, x1, y2)
    eightSem(x1, y1, x2, y1)
    eightSem(x1, y2, x2, y2)
    eightSem(x1, (y1 + y2) / 2, x2, (y1 + y2) / 2)


def n(x1, y1, x2, y2):
    eightSem(x1, y1, x1, y2)
    eightSem((x1 + x2) / 2, y1 + 49, (x1 + x2) / 2, y2 - 49)
    eightSem(x1, y2, (x1 + x2) / 2, y2 - 49)
    eightSem((x1 + x2) / 2, y1 + 49, x2, y1)
    eightSem(x2, y1, x2, y2)


def d(x1, y1, x2, y2):
    eightSem(x2, y1 + 20, x2, y2 - 20)
    eightSem(x1, y1, x2, y1 + 20)
    eightSem(x1, y2, x2, y2 - 20)
    eightSem(x1, y1, x1, y2)


# score drawing
def pointcount(p):
    bleep = str(p)
    x1, y1 = 10, 760
    x2, y2 = 20, 790
    for i in bleep:
        if i == "0":
            zero(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == "1":
            one(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == "2":
            two(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == "3":
            three(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == "4":
            four(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == "5":
            five(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == "6":
            six(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == "7":
            seven(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == "8":
            eight(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == "9":
            nine(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)


def increase(x1, x2):
    a = x2 + 10
    b = x2 + 10 + (x2 - x1)
    return a, b


def circlePoints(x, y, x1, y1):
    draw_points(x + x1, y + y1)  # 0
    draw_points(y + x1, x + y1)  # 1
    draw_points(-y + x1, x + y1)  # 2
    draw_points(-x + x1, y + y1)  # 3
    draw_points(-x + x1, -y + y1)  # 4
    draw_points(-y + x1, -x + y1)  # 5
    draw_points(y + x1, -x + y1)  # 6
    draw_points(x + x1, -y + y1)  # 7


def midpointCircle(r, a, b):
    d = 1 - r
    x, y = 0, r
    circlePoints(x, y, a, b)
    while y > x:
        if d < 0:
            d = d + x * 2 + 3
            x += 1
        else:
            d = d + (x - y) * 2 + 5
            x += 1
            y -= 1
        circlePoints(x, y, a, b)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"UFO Attack Game")

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 0, 800, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw)
    glutSpecialFunc(key_input)
    glutKeyboardFunc(keyboard_input)
    glutTimerFunc(16, update_values, 0)  # chatgpt ask
    glutTimerFunc(0, update, 0)
    glutTimerFunc(0, create_meteorite, 0)
    if points >= 20:
        sys.end()
    glutMainLoop()


if __name__ == "__main__":
    main()
