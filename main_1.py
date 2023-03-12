import pygame
import matplotlib.pyplot as plt
import numpy as np
from vpython import *

import Ball
import Sector


# v python 3d grafik



# Setup Fenster
#(lenght : x; height: y; width: z)
LENGHT, HEIGHT, WIDTH = 20, 20, 20
wall_bottom = box(pos=vector(0, -HEIGHT/2, 0),     color=color.white,  length=LENGHT, height=.1,     width=WIDTH)
wall_back = box(pos=vector(0, 0, -WIDTH/2),       color=color.white,    length=LENGHT, height=HEIGHT, width=.1)
wall_left = box(pos=vector(-LENGHT/2, 0, 0),       color=color.white,   length=.1,     height=HEIGHT, width=WIDTH)
wall_right = box(pos=vector(LENGHT/2, 0, 0),        color=color.white,   length=.1,     height=HEIGHT, width=WIDTH)
wall_top = box(pos=vector(0, HEIGHT/2, 0),         color=color.white,  length=LENGHT, height=.1,     width=WIDTH)

DO_VELOCITY_PLOT = True

# Farbwerte
RED = vector(255, 82, 32)
BLACK = vector(0, 0, 0)
BLUE = vector(23, 2, 255)
WHITE = vector(255, 255, 255)
GREEN = vector(50, 205, 50)
YELLOW = vector(255, 255, 0)

# Tick-Faktor
TIME_STEP = 0.5
# REPULSE = 0.1

# Setup Teilchen
BALL_RADIUS = .1
BALL_AMOUNT = 400
BALL_COLOR = color.black
BALL_MASSE = 5

BROWNSCHESTEILCHEN_MASSE = 40
BROWNSCHESTEILCHEN_RADIUS = 2
BROWNSCHESTEILCHEN_COLOR = color.red


def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, LENGHT, WIDTH, HEIGHT, TIME_STEP)
        balls.append(ball)

    return balls


def generate_sectors(amount_sqr):
    sector_list = []
    sector_1 = Sector.Sector(np.array([0-100, 0-100]), np.array([WIDTH/2, HEIGHT/2]))
    sector_2 = Sector.Sector(np.array([WIDTH/2, 0-100]), np.array([WIDTH+100, HEIGHT/2]))
    sector_3 = Sector.Sector(np.array([0-100, HEIGHT/2]), np.array([WIDTH/2, HEIGHT+100]))
    sector_4 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
    sector_5 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
    sector_6 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
    sector_7 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
    sector_8 = Sector.Sector(np.array([WIDTH/2, HEIGHT/2]), np.array([WIDTH+100, HEIGHT+100]))
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
    run = 1
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, LENGHT, WIDTH, HEIGHT, TIME_STEP)
    balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
    #sectors = generate_sectors()
    vel_dict = {}

    while run:
        for ball in balls:
            ''' Bewegung und Kollision aller Teilchen'''
            ball.handle_border_collision()
            for i in range(balls.index(ball) + 1, len(balls)):
                ball.handle_collision(balls[i])
            ball.move()

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
