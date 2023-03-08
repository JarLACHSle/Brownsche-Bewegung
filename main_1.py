import random
import math
import pygame
import matplotlib.pyplot as plt
import Ball
import numpy as np

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
SPEEDING = 2
# REPULSE = 0.1

# Setup Teilchen
BALL_RADIUS = 10
BALL_AMOUNT = 20
BALL_COLOR = BLUE
BALL_MASSE = 5

BROWNSCHESTEILCHEN_MASSE = 10
BROWNSCHESTEILCHEN_RADIUS = 10
BROWNSCHESTEILCHEN_COLOR = RED


def draw_ball(win, ball):
    '''zeichnet das Teilchen ins Fenster'''
    pygame.draw.circle(win, ball.color, (ball.position[0], ball.position[1]), ball.radius)


def draw(win, balls):
    '''animiert Teilchen'''
    win.fill(WHITE)
    for ball in balls:
        draw_ball(win, ball)
    pygame.display.update()


def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball.Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE, WIDTH, HEIGHT, SPEEDING)
        balls.append(ball)

    return balls


def main():
    run = 1
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsches_teilchen = Ball.Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE, WIDTH, HEIGHT, SPEEDING)
    balls = [brownsches_teilchen] + generate_balls(BALL_AMOUNT)
    vel_dict = {}

    while run:
        draw(WIN, balls)
        pygame.time.Clock().tick(60)

        # prüft, ob das Fenster geschlosen wurde und beendet das Programm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
                break
        for ball in balls:
            ''' Bewegung und Kollision aller Teilchen'''
            ball.handle_border_collision()
            for i in range(balls.index(ball) + 1, len(balls)):
                ball.handle_collision(balls[i])
                # ball.repulse(balls[i])
            ball.move()
            if DO_VELOCITY_PLOT:
                '''falls True, wird die Geschwindigkeitsverteilung über 
                den gesamten Verlauf der Simulation aufgezeichnet'''
                abselv = math.sqrt(ball.x_vel ** 2 + ball.y_vel ** 2)
                if abselv in vel_dict:
                    vel_dict[abselv] += 1
                else:
                    vel_dict[abselv] = 1

    if DO_VELOCITY_PLOT:
        '''falls True, wird nach Simulationsende die Geschwindigkeitsverteilung geplottet'''
        for key in vel_dict:
            plt.bar(key, vel_dict[key], 0.1, color="blue")
            plt.show()

    pygame.quit()


if __name__ == '__main__':
    main()
