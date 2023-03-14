import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
from copy import deepcopy

import Ball
import Cube

# Setup Fenster 
WIDTH = HEIGHT = DEPTH = 200 

schichtdicke = 4*16
bot_layer = DEPTH/2-schichtdicke/2
top_layer = DEPTH/2+schichtdicke/2
vanishes = 0
layer_time = 0
ent_time = 0
count = 0
in_layer = True

# Tick-Faktor
TIME_STEP = 1
num_steps = 100

# Setup Teilchen
BALL_RADIUS = 0.5 
BALL_AMOUNT = 100
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
    global xlist,ylist,zlist,brown_pos
    xlist = [computed_positions[num,index,0] for index in range(BALL_AMOUNT+1)]
    ylist = [computed_positions[num,index,1] for index in range(BALL_AMOUNT+1)]
    zlist = [computed_positions[num,index,2] for index in range(BALL_AMOUNT+1)]
    graph._offsets3d = (xlist, ylist, zlist)
    line1.set_data(brown_pos[:num,:2].T)
    line1.set_3d_properties(brown_pos[:num, 2])
    title1.set_text('3D-Darstellung, Zeit={}'.format(num))

def update_graph2(num2):
    '''\Ebenenprojektion\:zeichnet die Verschiebung der Position ins Koordinatensystem
    ACHTUNG: funktioniert  nur, wenn vorher auch update_graph1 aufgerufen wurde.'''
    global xlist,ylist,zlist,brown_pos,vanishes, sizes2, colors,plane_graph, in_layer, ent_time, count, layer_time
    layered_xlist = xlist.copy()
    layered_ylist = ylist.copy()
    for index in reversed(range(len(zlist))):
        if index == 0:
            if zlist[index]+ BROWNSCHESTEILCHEN_RADIUS < bot_layer or zlist[index]-BROWNSCHESTEILCHEN_RADIUS > top_layer:
                layered_xlist[index] = None
                layered_ylist[index] = None
                if (in_layer==True):
                    vanishes+=1
                    count=0
                    layer_time=num2-ent_time
                    in_layer=False
            if (zlist[index]- BROWNSCHESTEILCHEN_RADIUS <= top_layer and zlist[index]+BROWNSCHESTEILCHEN_RADIUS >= bot_layer) and count == 0: 
                in_layer = True
                ent_time = num2
                count += 1
        elif zlist[index]+ zlist[index] < bot_layer or zlist[index]- BALL_RADIUS > top_layer:
            layered_xlist[index] = None
            layered_ylist[index] = None
   
    # Für Projektion in die x-y-Ebene:
    line2.set_data(brown_pos[:num2,:2].T)
    plane_graph.set_offsets(np.column_stack([layered_xlist, layered_ylist]))
    #plane_graph = ax2.scatter(layered_xlist,layered_ylist,s= sizes2, c =colors)
    title2.set_text('Top-Down Ansicht, Anzahl Schichtaustritte ={}, Schichtzeit ={}'.format(vanishes, layer_time))

# initialisiert die Teilchen 
brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)

# setzt das brownsche Teilchen in die Mitte und nimmt ihm die Anfangsgeschwindigkeit
brownsches_teilchen.position = np.array([WIDTH/2,HEIGHT/2,DEPTH/2],dtype =float)
brownsches_teilchen.vel_vec = np.array([0,0,0])

# initialisiert die Sektoren
Mothercube = Cube.Cubesector((WIDTH/2,HEIGHT/2,DEPTH/2), WIDTH/2)
subcubes_list = Mothercube.subdivide()

'''erstellt ein dreidimensionales Array [num_steps*(BALL_AMOUNT+1)*3] (+1 wegen des brownschen Teilchens)
  und berechnet alle Positionen der Teilchen vor, indem wiederholt do_everything aufgerufen wird'''                            
computed_positions = np.empty((num_steps, BALL_AMOUNT+1,3))
brown_pos = np.empty((num_steps,3))
print("Starte Berechnung. Anzahl Bälle = {}, Anzahl Schritte = {}".format(BALL_AMOUNT,num_steps))

for i1 in range(num_steps):
    for i2,ball in enumerate(do_everything()):
        computed_positions[i1,i2,0] = ball.position[0]
        computed_positions[i1,i2,1] = ball.position[1]
        computed_positions[i1,i2,2] = ball.position[2]
    if i1%(num_steps/10) == 0:
        print("{}% abgeschlossen".format((i1/num_steps)*100))
    brown_pos[i1,0] = brownsches_teilchen.position[0]
    brown_pos[i1,1] = brownsches_teilchen.position[1]
    brown_pos[i1,2] = brownsches_teilchen.position[2]
    
# Positionen für den Start-Plot, damit später ._offset3D benutzt werden kann
xlist = [ball.position[0] for ball in balls]
ylist = [ball.position[1] for ball in balls]
zlist = [ball.position[2] for ball in balls]

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

# Für XY stattdessen:
fig2 = plt.figure(1,dpi=142)
ax2 = fig2.add_subplot(111)
ax2.set_aspect(1)
title2 = ax2.set_title('Top-Down Ansicht')

sizes2 = np.ones(BALL_AMOUNT+1)*((ax2.get_window_extent().width*(BALL_RADIUS/WIDTH)) ** 2)* 72./fig1.dpi
sizes2[0] = ((ax2.get_window_extent().width*(BROWNSCHESTEILCHEN_RADIUS/WIDTH)) ** 2)* 72./fig1.dpi

line2, = ax2.plot([],[], c="green")
plane_graph = ax2.scatter(xlist, ylist, s= sizes2, c =colors)


# Animiert die berechneten Veränderungen
ani1 = matplotlib.animation.FuncAnimation(fig1, update_graph1, num_steps, interval=50, blit=False)
ani2 = matplotlib.animation.FuncAnimation(fig2, update_graph2, num_steps, interval=50, blit=False)


plt.show()  
