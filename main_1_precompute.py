import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

import Ball
import Cube

# Setup Fenster 
WIDTH = HEIGHT = DEPTH = 100 # in z.B. [m]*10^-4 -> gesamt 1 cm

# Tick-Faktor
TIME_STEP = 1
num_steps = 100

# Setup Teilchen
BALL_RADIUS = 2 # 0.2mm
BALL_AMOUNT = 200
BALL_COLOR = "blue"
BALL_MASSE = 0.5 # 0.05g

BROWNSCHESTEILCHEN_MASSE = 4 # 0.4 g 
BROWNSCHESTEILCHEN_RADIUS = 16 # 4mm
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

def update_graph(num):
    '''zeichnet die Verschiebung der Position ins Koordinatensystem'''
    global xlist,ylist,zlist,brown_pos,count
    xlist = [computed_positions[num,index,0] for index in range(BALL_AMOUNT+1)]
    ylist = [computed_positions[num,index,1] for index in range(BALL_AMOUNT+1)]
    zlist = [computed_positions[num,index,2] for index in range(BALL_AMOUNT+1)]
    graph._offsets3d = (xlist, ylist, zlist)
    line.set_data(brown_pos[:num, :2].T)
    line.set_3d_properties(brown_pos[:num, 2])
    # Für Projektion in die x-y-Ebene: plane_graph.set_offsets(np.column_stack([xlist, ylist]))
    title.set_text('Brownsche Bewegung, Zeit={}'.format(num))

# initialisiert die Teilchen und Sektoren
brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, DEPTH, TIME_STEP)
balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
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
    
#initialisiert das Fenster
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)
# Für XY stattdessen : ax = fig.add_subplot(111)
title = ax.set_title('Brownsche Bewegung')

#Anfangswerte für die Positionen, damit später ._offset3d genutzt werden kann
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
line, = ax.plot([],[],[], c="green")
# Für XY stattdessen plane_graph = ax.scatter(xlist, ylist, s= sizes, c =colors)

# Animiert die berechneten Veränderungen
ani = matplotlib.animation.FuncAnimation(fig, update_graph, num_steps, interval=50, blit=False)

#speichert die Animation als Video
ani.save('Brownsche_Bewegung_Render.mp4', fps=30, )
print("saved!")

plt.show()  
