import pygame
import matplotlib.pyplot as plt
import Ball
import numpy as np

import Sector

pygame.init()

# v python 3d grafik

# Setup Fenster
WIDTH, HEIGHT = 700, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brownsche Bewegung")

DO_VELOCITY_PLOT = False

# Farbwerte
RED = (255, 82, 32)
BLACK = (0, 0, 0)
BLUE = (23, 2, 255)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)

# Tick-Faktor
TIME_STEP = 3
# REPULSE = 0.1

# Setup Teilchen
BALL_RADIUS = 2
BALL_AMOUNT = 200
BALL_COLOR = BLUE
BALL_MASSE = 5

BROWNSCHESTEILCHEN_MASSE = 40
BROWNSCHESTEILCHEN_RADIUS = 16
BROWNSCHESTEILCHEN_COLOR = RED


def draw_ball(win, ball):
    '''zeichnet das Teilchen ins Fenster'''
    pygame.draw.circle(win, ball.color, (ball.position[0], ball.position[1]), ball.radius)


def draw(win, balls):
    '''animiert Teilchen'''
    win.fill(WHITE)
    #draw_ball(win,balls[0])
    for ball in balls:
        draw_ball(win, ball)
    pygame.display.update()


def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, WIDTH, HEIGHT, TIME_STEP)
        balls.append(ball)

    return balls


def generate_sectors(amount_sqr):
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

def main():
    run = 1
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, TIME_STEP)
    balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
    sectors = generate_sectors(2)
    vel_dict = {}

    while run:
        draw(WIN, balls)
        pygame.time.Clock().tick(60)

        # prüft, ob das Fenster geschlosen wurde und beendet das Programm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
                break

        for sector in sectors:
            sector.clear()
            for ball in balls:
                sector.append_ball(ball)
        for sector in sectors:
            sector.move_ball()

        #for ball in balls:
        #    ''' Bewegung und Kollision aller Teilchen'''
        #    ball.handle_border_collision()
        #    for i in range(balls.index(ball) + 1, len(balls)):
        #        ball.handle_collision(balls[i])
        #        # ball.repulse(balls[i])
        #    ball.move()
        #    if DO_VELOCITY_PLOT:
        #        '''falls True, wird die Geschwindigkeitsverteilung über
        #        den gesamten Verlauf der Simulation aufgezeichnet'''
        #        abselv = math.sqrt(ball.x_vel ** 2 + ball.y_vel ** 2)
        #        if abselv in vel_dict:
        #            vel_dict[abselv] += 1
        #       else:
        #            vel_dict[abselv] = 1

    if DO_VELOCITY_PLOT:
        '''falls True, wird nach Simulationsende die Geschwindigkeitsverteilung geplottet'''
        for key in vel_dict:
            plt.bar(key, vel_dict[key], 0.1, color="blue")
            plt.show()

    pygame.quit()


if __name__ == '__main__':
    main()
