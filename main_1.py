import matplotlib.pyplot as plt
import numpy as np
from vpython import *
import Ball
import Sector
import copy
# (lenght : x; height: y; width: z)
LENGHT = HEIGHT = WIDTH = 20
# Setup Fenster
canvas_2D = canvas(title='Top View', userzoom=False, userspin=False, userpan=False, width=500, height=300,)
wall = box(pos=vector(0, 0, 0), color=color.white, size=vector(LENGHT, HEIGHT, .1))

canvas_3D = canvas(title='3D View',width=500, height=300,)
wall_bottom = box(pos=vector(0, -HEIGHT / 2, 0), color=color.white, size=vector(LENGHT, .1, WIDTH))
wall_back = box(pos=vector(0, 0, -WIDTH / 2), color=color.white, size=vector(LENGHT, HEIGHT, .1))
wall_left = box(pos=vector(-LENGHT / 2, 0, 0), color=color.white, size=vector(.1, HEIGHT, WIDTH))
wall_right = box(pos=vector(LENGHT / 2, 0, 0), color=color.white, size=vector(.1, HEIGHT, WIDTH), opacity=.1)
wall_top = box(pos=vector(0, HEIGHT / 2, 0), color=color.white, size=vector(LENGHT, .1, WIDTH), opacity=.1)
wall_front = box(pos=vector(0, 0, WIDTH/2), color=color.white, size=vector(LENGHT, HEIGHT, .1), opacity=.1)

#setup Schicht
schichtdicke = 6
top_layer = box(pos=vector(0, schichtdicke/2, 0), color=color.green, size=vector(LENGHT, .1, WIDTH), opacity=.1)
bot_layer = box(pos=vector(0, -schichtdicke/2, 0), color=color.green, size=vector(LENGHT, .1, WIDTH), opacity=.2)

DO_VELOCITY_PLOT = True

# Tick-Faktor
TIME_STEP = 0.1
# REPULSE = 0.1

# Setup Teilchen
BALL_RADIUS = .05
BALL_AMOUNT = 300
BALL_COLOR = color.black
BALL_MASSE = 1

BROWNSCHESTEILCHEN_MASSE = 40
BROWNSCHESTEILCHEN_RADIUS = 1
BROWNSCHESTEILCHEN_COLOR = color.red


def generate_balls(amount, can):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, LENGHT, WIDTH, HEIGHT, TIME_STEP, canvas=can)
        balls.append(ball)

    return balls


def generate_sectors(amount_sqr):
    sector_list = []
    sector_1 = Sector.Sector(np.array([0 - 100, 0 - 100]), np.array([WIDTH / 2, HEIGHT / 2]))
    sector_2 = Sector.Sector(np.array([WIDTH / 2, 0 - 100]), np.array([WIDTH + 100, HEIGHT / 2]))
    sector_3 = Sector.Sector(np.array([0 - 100, HEIGHT / 2]), np.array([WIDTH / 2, HEIGHT + 100]))
    sector_4 = Sector.Sector(np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH + 100, HEIGHT + 100]))
    sector_5 = Sector.Sector(np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH + 100, HEIGHT + 100]))
    sector_6 = Sector.Sector(np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH + 100, HEIGHT + 100]))
    sector_7 = Sector.Sector(np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH + 100, HEIGHT + 100]))
    sector_8 = Sector.Sector(np.array([WIDTH / 2, HEIGHT / 2]), np.array([WIDTH + 100, HEIGHT + 100]))
    sector_list.append(sector_1)
    sector_list.append(sector_2)
    sector_list.append(sector_3)
    sector_list.append(sector_4)
    sector_list.append(sector_5)
    sector_list.append(sector_6)
    sector_list.append(sector_7)
    sector_list.append(sector_8)

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


def main():
    run = True
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsches_teilchen_3D = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE,
                                    LENGHT, WIDTH, HEIGHT, TIME_STEP, canvas=canvas_3D)
    balls = [brownsches_teilchen_3D] + generate_balls(BALL_AMOUNT, canvas_3D)
    brownsches_teilchen_2D = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE,
                                    LENGHT, WIDTH, HEIGHT, TIME_STEP, canvas=canvas_2D)
    brownsches_teilchen_2D.pos = vector(brownsches_teilchen_3D.pos.value[0], brownsches_teilchen_3D.pos.value[2], 0)

    # sectors = generate_sectors()
    vel_dict = {}
    # Linie hinter dem Ball
    c_3d = curve(color=color.yellow, pos=brownsches_teilchen_3D.pos, retain=150)
    c_2d = curve(color=color.yellow, pos=brownsches_teilchen_2D.pos, retain=150, canvas=canvas_2D)

    while run:
        rate(60)
        for j, ball in enumerate(balls):
            ''' Bewegung und Kollision aller Teilchen'''
            ball.handle_border_collision()
            for i in range(balls.index(ball) + 1, len(balls)):
                ball.handle_collision(balls[i])
            ball.move()

        if brownsches_teilchen_3D.pos.value[1] - brownsches_teilchen_3D.radius > schichtdicke/2 or brownsches_teilchen_3D.pos.value[1] + brownsches_teilchen_3D.radius < - schichtdicke/2:
            brownsches_teilchen_2D.visible = False
            #c_2d.visible = False
            #c_2d.clear()
        else:
            brownsches_teilchen_2D.visible = True
            #c_2d.visible = True
            brownsches_teilchen_2D.pos = vector(brownsches_teilchen_3D.pos.value[0], brownsches_teilchen_3D.pos.value[2]*-1, 0)
        c_2d.append(pos=vector(brownsches_teilchen_3D.pos.value[0], brownsches_teilchen_3D.pos.value[2]*-1, 0))

        # führt die Linie weiter
        c_3d.append(pos=brownsches_teilchen_3D.pos)

        if DO_VELOCITY_PLOT:
            '''falls True, wird die Geschwindigkeitsverteilung über den gesamten Verlauf der Simulation aufgezeichnet'''
            for ball in balls:
                abselv = mag(ball.vel_vec)
                if abselv in vel_dict:
                    vel_dict[abselv] += 1
                else:
                    vel_dict[abselv] = 1
            # f1 = gcurve(color=color.cyan,)  # a graphics curve
            # for key in vel_dict.keys():
            #    f1.plot(key, vel_dict[key])
            # vel_dict.clear()

    #        for sector in sectors:
    #            sector.clear()
    #            for ball in balls:
    #                sector.append_ball(ball)
    #        for sector in sectors:
    #            sector.move_ball()
    #            if DO_VELOCITY_PLOT:
    #                '''falls True, wird die Geschwindigkeitsverteilung über den gesamten Verlauf der Simulation aufgezeichnet'''
    #                for ball in sector.balls:
    #                    abselv = np.linalg.norm(ball.vel_vec)
    #                    if abselv in vel_dict:
    #                        vel_dict[abselv] += 1
    #                    else:
    #                        vel_dict[abselv] = 1

    if DO_VELOCITY_PLOT:
        '''falls True, wird nach Simulationsende die Geschwindigkeitsverteilung geplottet'''
        keys = list(vel_dict.keys())
        values = list(vel_dict.values())
        plt.bar(keys, values, 0.1, color="blue")
        plt.show()


if __name__ == '__main__':
    main()
