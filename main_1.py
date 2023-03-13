import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

import Ball
import Cube

# Setup Fenster 
WIDTH = HEIGHT = DEPTH = 200 

schichtdicke = 4*16
bot_layer = DEPTH/2-schichtdicke/2
top_layer = DEPTH/2+schichtdicke/2
vanishes = 0

# Tick-Faktor
TIME_STEP = 1
num_steps = 1000

# Setup Teilchen
BALL_RADIUS = 2 
BALL_AMOUNT = 200
BALL_COLOR = "blue"
BALL_MASSE = 0.5 

BROWNSCHESTEILCHEN_MASSE = 4  
BROWNSCHESTEILCHEN_RADIUS = 16 
BROWNSCHESTEILCHEN_COLOR = "red"

GRAVITATION = 0.098

def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
        balls.append(ball)

    return balls


def do_everything():
    '''ruft alle wichtigen Kollisionsfunktionen an der richtigen Stelle auf'''
    global vanishes
    for subcube in subcubes_list:
        subcube.clear()
        for ball in balls:
            index = Mothercube.get_subcube(ball)
            own_subcube = subcubes_list[index]
            own_subcube.balls.append(ball)
        subcube.move_ball(G=GRAVITATION)
        if brownsches_teilchen.position[2]+BROWNSCHESTEILCHEN_RADIUS < bot_layer or brownsches_teilchen.position[2]-BROWNSCHESTEILCHEN_RADIUS > top_layer:
            vanishes +=1
            
    return balls

def update_graph(num):
    '''zeichnet die Verschiebung der Position ins Koordinatensystem'''
    global xlist,ylist,zlist,brown_pos,count
    count += 1
    xlist = [ball.position[0] for ball in do_everything()]
    ylist = [ball.position[1] for ball in do_everything()]
    zlist = [ball.position[2] for ball in do_everything()]
    brown_pos[count-1] = brownsches_teilchen.position
    #brown_pos = np.append(brown_pos, brownsches_teilchen.position, axis = 0)
    #graph._offsets3d = (xlist, ylist, zlist)
    line.set_data(brown_pos[:num,0],brown_pos[:num,2])
    #line.set_3d_properties(brown_pos[:num, 2])
    # Für Projektion in die x-z-Ebene: 
    plane_graph.set_offsets(np.column_stack([xlist, zlist]))
    title.set_text('Seitenansicht, Zeit={}, Anzahl Schichtaustritte ={}'.format(num,vanishes))

# initialisiert die Teilchen und Sektoren
brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
brownsches_teilchen.position = np.array([WIDTH/2,HEIGHT/2,DEPTH/2],dtype =float)
brownsches_teilchen.vel_vec = np.array([0,0,0])

balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
Mothercube = Cube.Cubesector((WIDTH/2,HEIGHT/2,DEPTH/2), WIDTH/2)
subcubes_list = Mothercube.subdivide()

#initialisiert das Fenster
fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.grid(False)
# Für XZ stattdessen : 
ax = fig.add_subplot(111)
title = ax.set_title('Seitenansicht')

# Positionen für den Start-Plot
xlist = [ball.position[0] for ball in balls]
ylist = [ball.position[1] for ball in balls]
zlist = [ball.position[2] for ball in balls]
brown_pos = np.empty((num_steps,3))
count = 0

# ordnet den Scatter-Punkten die richtigen Farben und Radien zu
sizes = np.ones(BALL_AMOUNT+1)*math.pi*BALL_RADIUS**2
sizes[0] = math.pi*BROWNSCHESTEILCHEN_RADIUS**2
colors = [BALL_COLOR]*(BALL_AMOUNT+1)
colors[0] = BROWNSCHESTEILCHEN_COLOR

# zeichnet den Start-Plot
#graph = ax.scatter(xlist, ylist, zlist, s= sizes, c=colors)
line, = ax.plot([],[], c="green")
#Für XZ stattdessen 
plane_graph = ax.scatter(xlist, zlist, s= sizes, c =colors)
plt.plot([0,WIDTH],[bot_layer,bot_layer], c= "black")
plt.plot([0,WIDTH],[top_layer,top_layer], c= "black")

# Animiert die berechneten Veränderungen
ani = matplotlib.animation.FuncAnimation(fig, update_graph, num_steps, interval=50, blit=False)

plt.show()  
