"""Minimal PyOpenGL client for the shared traffic model."""

from __future__ import annotations

import math

from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LINES, GL_QUADS, glBegin, glClear, glClearColor, glColor3f, glEnable, glEnd, glLoadIdentity, glPopMatrix, glPushMatrix, glTranslatef, glVertex3f, glViewport
from OpenGL.GLUT import GLUT_DOUBLE, GLUT_DEPTH, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT, GLUT_KEY_UP, GLUT_RGB, GLUT_BITMAP_HELVETICA_18, glutBitmapCharacter, glutCreateWindow, glutDisplayFunc, glutIdleFunc, glutInit, glutInitDisplayMode, glutInitWindowSize, glutKeyboardFunc, glutMainLoop, glutPostRedisplay, glutSolidCube, glutSpecialFunc, glutSwapBuffers
from OpenGL.GLU import gluLookAt, gluPerspective

from .model import TrafficModel


WIDTH, HEIGHT = 1000, 800
model = TrafficModel(seed=27)
camera_angle = 0.0
camera_distance = 900.0
night_mode = False


def text(x: int, y: int, value: str) -> None:
    glColor3f(0.9, 0.95, 1.0)
    for character in value:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))


def draw_scene() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WIDTH, HEIGHT)
    glLoadIdentity()
    gluPerspective(75, WIDTH / HEIGHT, 1, 3000)
    radius = camera_distance
    gluLookAt(radius * math.sin(camera_angle), radius * math.cos(camera_angle), 330,
              0, 0, 0, 0, 0, 1)

    glColor3f(0.08, 0.08, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-300, -1200, 0); glVertex3f(300, -1200, 0)
    glVertex3f(300, 1200, 0); glVertex3f(-300, 1200, 0)
    glEnd()

    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_LINES)
    for lane_marker in (-120, 0, 120):
        glVertex3f(lane_marker, -1200, 1)
        glVertex3f(lane_marker, 1200, 1)
    glEnd()

    for index, car in enumerate(model.cars):
        glPushMatrix()
        glTranslatef(car.lane, car.z, 18)
        glColor3f(1.0, 0.8, 0.1) if index == model.ambulance_index else glColor3f(*car.color)
        glutSolidCube(30)
        glPopMatrix()

    glColor3f(0.2, 1.0, 0.2) if model.signal_green else glColor3f(1.0, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glutSolidCube(24)
    glPopMatrix()
    glSwap = glutSwapBuffers
    glSwap()


def keyboard(key: bytes, _x: int, _y: int) -> None:
    global night_mode
    if key == b"g":
        model.signal_green, model.auto_signal = True, False
    elif key == b"r":
        model.signal_green, model.auto_signal = False, False
    elif key == b"a":
        model.auto_signal = True
    elif key == b"b":
        model.paused = not model.paused
    elif key == b"v":
        model.speed_boost = not model.speed_boost
    elif key == b"n":
        night_mode = not night_mode
    elif key == b"q":
        raise SystemExit


def special(key: int, _x: int, _y: int) -> None:
    global camera_angle, camera_distance
    if key == GLUT_KEY_LEFT:
        camera_angle -= 0.05
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 0.05
    elif key == GLUT_KEY_UP:
        camera_distance = max(300, camera_distance - 80)
    elif key == GLUT_KEY_DOWN:
        camera_distance = min(1800, camera_distance + 80)


def idle() -> None:
    model.tick()
    glutPostRedisplay()


def main() -> None:
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Traffic Flow Simulator")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(draw_scene)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()