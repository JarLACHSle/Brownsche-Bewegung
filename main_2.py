import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

import Ball
import Cube

# Setup Fenster 
WIDTH = HEIGHT = DEPTH = 200

# Tick-Faktor
TIME_STEP = 1

# Setup Teilchen
BALL_RADIUS = 2
BALL_AMOUNT = 100
BALL_COLOR = "blue"
BALL_MASSE = 5

BROWNSCHESTEILCHEN_MASSE = 40
BROWNSCHESTEILCHEN_RADIUS = 16
BROWNSCHESTEILCHEN_COLOR = "red"

def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
        balls.append(ball)

    return balls


def do_everything():
    '''ruft alle wichtigen Kollisionsfunktionen an der richtigen Stelle auf'''
    for subcube in subcubes_list:
        subcube.clear()
        for ball in balls:
            index = Mothercube.get_subcube(ball)
            own_subcube = subcubes_list[index]
            own_subcube.balls.append(ball)
        subcube.move_ball()
    return balls

def update_graph(num):
    '''zeichnet die Verschiebung der Position ins Koordinatensystem'''
    global xlist,ylist,zlist
    xlist = [ball.position[0] for ball in do_everything()]
    ylist = [ball.position[1] for ball in do_everything()]
    zlist = [ball.position[2] for ball in do_everything()]
    graph._offsets3d = (xlist, ylist, zlist)
    title.set_text('Brownsche Bewegung, Zeit={}'.format(num))

# initialisiert die Teilchen und Sektoren
brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
Mothercube = Cube.Cubesector((WIDTH/2,HEIGHT/2,DEPTH/2), WIDTH/2)
subcubes_list = Mothercube.subdivide()

#initialisiert das Fenster
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('Brownsche Bewegung')

# Positionen für den Start-Plot
xlist = [ball.position[0] for ball in balls]
ylist = [ball.position[1] for ball in balls]
zlist = [ball.position[2] for ball in balls]

# ordnet den Scatter-Punkten die richtigen Farben und Radien zu
sizes = np.ones(BALL_AMOUNT+1)*BALL_RADIUS**2
sizes[0] = BROWNSCHESTEILCHEN_RADIUS**2
colors = [BALL_COLOR]*(BALL_AMOUNT+1)
colors[0] = BROWNSCHESTEILCHEN_COLOR

# zeichnet den Start-Plot
graph = ax.scatter(xlist, ylist, zlist, s= sizes, c=colors)

# Animiert die berechneten Veränderungen
ani = matplotlib.animation.FuncAnimation(fig, update_graph, 16, interval=50, blit=False)

plt.show()  

