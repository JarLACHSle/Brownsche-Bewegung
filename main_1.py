import matplotlib.pyplot as plt
import numpy as np
from vpython import *
import Ball
import Cube
import copy
# (lenght : x; height: y; width: z)
LENGHT = HEIGHT = WIDTH = 20

#setup Schicht
schichtdicke = 6

# Tick-Faktor
TIME_STEP = 0.1
# REPULSE = 0.1

# Setup Teilchen
BALL_RADIUS = .005
BALL_AMOUNT = 800
BALL_COLOR = color.black
BALL_MASSE = 0.5

BROWNSCHESTEILCHEN_AMOUNT = 3
BROWNSCHESTEILCHEN_COLOR = [color.red, color.cyan, color.magenta] # Muss die länge von Amount sein
BROWNSCHESTEILCHEN_MASSE = 4
BROWNSCHESTEILCHEN_RADIUS = 1.6
LINE_COLOR = color.blue

# Setup Fenster
canvas_2D = canvas(userzoom=False, userspin=False, userpan=False, width=500, height=500, align="left")
wall = box(pos=vector(0, 0, 0), color=color.white, size=vector(LENGHT, HEIGHT, .1))

canvas_3D = canvas(width=500, height=500, userzoom=True, align="right")
wall_bottom = box(pos=vector(0, -HEIGHT / 2, 0), color=color.white, size=vector(LENGHT, .1, WIDTH))
wall_back = box(pos=vector(0, 0, -WIDTH / 2), color=color.white, size=vector(LENGHT, HEIGHT, .1))
wall_left = box(pos=vector(-LENGHT / 2, 0, 0), color=color.white, size=vector(.1, HEIGHT, WIDTH))
wall_right = box(pos=vector(LENGHT / 2, 0, 0), color=color.white, size=vector(.1, HEIGHT, WIDTH), opacity=.1)
wall_top = box(pos=vector(0, HEIGHT / 2, 0), color=color.white, size=vector(LENGHT, .1, WIDTH), opacity=.1)
wall_front = box(pos=vector(0, 0, WIDTH/2), color=color.white, size=vector(LENGHT, HEIGHT, .1), opacity=.1)

#show schicht
top_layer = box(pos=vector(0, schichtdicke/2, 0), color=color.green, size=vector(LENGHT, .1, WIDTH), opacity=.2)
bot_layer = box(pos=vector(0, -schichtdicke/2, 0), color=color.green, size=vector(LENGHT, .1, WIDTH), opacity=.3)


def generate_balls(amount, radius, color, masse, can):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    if isinstance(color, list) and amount == len(color):
        for i in range(amount):
            ball = Ball.Ball(radius, color[i], masse, LENGHT, WIDTH, HEIGHT, TIME_STEP, canvas=can)
            balls.append(ball)
    else:
        color = [color]
        for i in range(amount):
            ball = Ball.Ball(radius, color[0], masse, LENGHT, WIDTH, HEIGHT, TIME_STEP, canvas=can)
            balls.append(ball)

    return balls


def main():
    run = True
    rate(60)
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsche_teilchen_3D = generate_balls(BROWNSCHESTEILCHEN_AMOUNT, BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, canvas_3D)
    balls = brownsche_teilchen_3D + generate_balls(BALL_AMOUNT, BALL_RADIUS, BALL_COLOR, BALL_MASSE, canvas_3D)
    brownsche_teilchen_2D = generate_balls(BROWNSCHESTEILCHEN_AMOUNT, BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, canvas_2D)

    # Würfel Sektoren
    mothercube = Cube.Cubesector((0, 0, 0), WIDTH/2)
    subcubes_list = mothercube.subdivide()

    # Linie hinter den brownshen Teilchen
    line_3D = []
    line_2D = []
    for i, ball in enumerate(brownsche_teilchen_3D):
        brownsche_teilchen_2D[i].pos = vector(ball.pos.value[0], ball.pos.value[2]*-1, 0)
        line_3D.append(curve(color=LINE_COLOR, pos=ball.pos, retain=300, canvas=canvas_3D))
        line_2D.append(curve(color=LINE_COLOR, pos=vector(ball.pos.value[0], ball.pos.value[2]*-1, 0), retain=300, canvas=canvas_2D))

    while run:
        rate(60)
        for subcube in subcubes_list:
            subcube.clear()
            for ball in balls:
                index = mothercube.get_subcube(ball)
                own_subcube = subcubes_list[index]
                own_subcube.balls.append(ball)
            subcube.move_ball()

        for i, ball in enumerate(brownsche_teilchen_3D):
            if ball.pos.value[1] - ball.radius > schichtdicke/2 or ball.pos.value[1] + ball.radius < - schichtdicke/2:
                brownsche_teilchen_2D[i].visible = False
                #line_2D.visible = False
                #line_2D[i].clear()
            else:
                brownsche_teilchen_2D[i].visible = True
            brownsche_teilchen_2D[i].pos = vector(ball.pos.value[0], ball.pos.value[2]*-1, 0)

            # führt die Linie weiter
            line_2D[i].append(pos=brownsche_teilchen_2D[i].pos)
            line_3D[i].append(pos=ball.pos)


if __name__ == '__main__':
    main()
