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
BALL_RADIUS = 0.5 
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
    for subcube in subcubes_list:
        subcube.clear()
        for ball in balls:
            index = Mothercube.get_subcube(ball)
            own_subcube = subcubes_list[index]
            own_subcube.balls.append(ball)
        subcube.move_ball(G=GRAVITATION)           
    return balls

def update_graph1(num):
    '''\3D-Darstellung\:zeichnet die Verschiebung der Position ins Koordinatensystem'''
    global xlist,ylist,zlist,brown_pos,count
    newballs = do_everything()
    count += 1
    xlist = [ball.position[0] for ball in newballs]
    ylist = [ball.position[1] for ball in newballs]
    zlist = [ball.position[2] for ball in newballs]
    brown_pos[count-1] = brownsches_teilchen.position
    graph._offsets3d = (xlist, ylist, zlist)
    line1.set_data(brown_pos[:num,:2].T)
    line1.set_3d_properties(brown_pos[:num, 2])
    title1.set_text('3D-Darstellung, Zeit={}'.format(num))

def update_graph2(num2):
    '''\Ebenenprojektion\:zeichnet die Verschiebung der Position ins Koordinatensystem
    ACHTUNG: funktioniert  nur, wenn vorher auch update_graph1 aufgerufen wurde.'''
    global xlist,ylist,zlist,brown_pos,count,vanishes
    if brownsches_teilchen.position[2]+BROWNSCHESTEILCHEN_RADIUS < bot_layer or brownsches_teilchen.position[2]-BROWNSCHESTEILCHEN_RADIUS > top_layer:
        vanishes +=1
    brown_pos[count-1] = brownsches_teilchen.position
    # Für Projektion in die x-z-Ebene:
    line2.set_data(brown_pos[:num2,0],brown_pos[:num2,2])
    plane_graph.set_offsets(np.column_stack([xlist, zlist]))
    title2.set_text('Seitenansicht, Zeit={}, Anzahl Schichtaustritte ={}'.format(num2,vanishes))

# initialisiert die Teilchen und Sektoren
brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
brownsches_teilchen.position = np.array([WIDTH/2,HEIGHT/2,DEPTH/2],dtype =float)
brownsches_teilchen.vel_vec = np.array([0,0,0])

balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
Mothercube = Cube.Cubesector((WIDTH/2,HEIGHT/2,DEPTH/2), WIDTH/2)
subcubes_list = Mothercube.subdivide()

# Positionen für den Start-Plot, damit später ._offset3D benutzt werden kann
xlist = [ball.position[0] for ball in balls]
ylist = [ball.position[1] for ball in balls]
zlist = [ball.position[2] for ball in balls]
brown_pos = np.empty((num_steps,3))
count = 0

#initialisiert das Fenster
fig1 = plt.figure(0,dpi=142)
ax1 = fig1.add_subplot(111, projection='3d')
ax1.grid(False)
title1 = ax1.set_title('3 Dimensionen')

# ordnet den Scatter-Punkten die richtigen Farben und Radien zu 
# Radien sind nicht vollständig repräsentativ, die Methode aus sizes2 (unten) funktioniert in 3D leider nicht.
sizes1 = np.ones(BALL_AMOUNT+1)*BALL_RADIUS**2
sizes1[0] = BROWNSCHESTEILCHEN_RADIUS**2
colors = [BALL_COLOR]*(BALL_AMOUNT+1)
colors[0] = BROWNSCHESTEILCHEN_COLOR

# zeichnet den Start-Plot (3D)
line1, = ax1.plot([],[],[], c="green")
graph = ax1.scatter(xlist, ylist, zlist, s= sizes1, c=colors)

# Für XZ stattdessen:
fig2 = plt.figure(1,dpi=142)
ax2 = fig2.add_subplot(111)
ax2.set_aspect(1)
title2 = ax2.set_title('Seitenansicht')

sizes2 = np.ones(BALL_AMOUNT+1)*((ax2.get_window_extent().width*(BALL_RADIUS/WIDTH)) ** 2)* 72./fig2.dpi
sizes2[0] = ((ax2.get_window_extent().width*(BROWNSCHESTEILCHEN_RADIUS/WIDTH)) ** 2)* 72./fig2.dpi

line2, = ax2.plot([],[], c="green")
plane_graph = ax2.scatter(xlist, zlist, s= sizes2, c =colors)

# zeichnet die Schichtgrenzen
plt.plot([0,WIDTH],[bot_layer,bot_layer], c= "black")
plt.plot([0,WIDTH],[top_layer,top_layer], c= "black")

# Animiert die berechneten Veränderungen
ani1 = matplotlib.animation.FuncAnimation(fig1, update_graph1, num_steps, interval=50, blit=False)
ani2 = matplotlib.animation.FuncAnimation(fig2, update_graph2, num_steps, interval=50, blit=False)


plt.show()  
