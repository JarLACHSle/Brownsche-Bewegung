from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

import Ball
import Sector
import main_1
from main_1 import do_everything

def update_graph(num):
    global xlist,ylist,zlist
    xlist = [ball.position[0] for ball in do_everything()]
    ylist = [ball.position[1] for ball in do_everything()]
    zlist = [ball.position[2] for ball in do_everything()]
    graph._offsets3d = (xlist, ylist, zlist)
    title.set_text('3D Test, time={}'.format(num))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('3D Test')

graph = ax.scatter(xlist, ylist, zlist)

ani = matplotlib.animation.FuncAnimation(fig, update_graph, 100, 
                               interval=500, blit=False)

plt.show()
