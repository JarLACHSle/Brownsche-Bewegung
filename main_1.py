import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

import Ball
import Sector

# Setup Fenster (Es gilt WIDTH~x, HEIGHT~y, DEPTH~z)
WIDTH, HEIGHT, DEPTH = 400, 400, 400

# Tick-Faktor
TIME_STEP = 3

# Setup Teilchen
BALL_RADIUS = 2
BALL_AMOUNT = 200
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


def generate_sectors(amount_sqr):
    '''erstellt 4 Objekte der Sektoren-Klasse für 4 Rechtecke in der x-y-Ebene'''
    sector_list = []
    sector_1 = Sector.Sector(np.array([0-100, 0-100]), np.array([WIDTH/2, HEIGHT/2]))
    sector_2 = Sector.Sector(np.array([WIDTH/2, 0-100]), np.array([WIDTH+100, HEIGHT/2]))
    sector_3 = Sector.Sector(np.array([0-100, HEIGHT/2]), np.array([WIDTH/2, HEIGHT+100]))
    sector_4 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
    sector_list.append(sector_1)
    sector_list.append(sector_2)
    sector_list.append(sector_3)
    sector_list.append(sector_4)

    '''for i in range(amount_sqr):
        for j in range(amount_sqr):
            if i == 0 and j == 0:
                sector = Sector.Sector(np.array([0, 0]), np.array([HEIGHT * (j+1)/amount_sqr, WIDTH * (j+1)/amount_sqr]))
                sector_list.append(sector)
            else:
                sector = Sector.Sector(np.array([HEIGHT * (i+1)/amount_sqr, WIDTH * (i+1)/amount_sqr]), np.array([HEIGHT * (j+1)/amount_sqr, WIDTH * (j+1)/amount_sqr]))
                sector_list.append(sector)
    '''

    return sector_list

def do_everything():
    '''ruft alle wichtigen Kollisionsfunktionen an der richtigen Stelle auf'''
    for sector in sectors:
        sector.clear()
        for ball in balls:
            sector.append_ball(ball)
    for sector in sectors:
        sector.move_ball()
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
sectors = generate_sectors(2)

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
ani = matplotlib.animation.FuncAnimation(fig, update_graph, 100, interval=50, blit=False)

plt.show()  

