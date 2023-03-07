import random
import math
import pygame
import matplotlib.pyplot as plt
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


class Ball:
    '''Klasse für alle stoßenden Teilchen'''

    def __init__(self, radius, color, masse):
        # Startwert und aktuelle Position
        self.x = self.original_x = random.randint(0 + radius, WIDTH - radius)
        self.y = self.original_y = random.randint(0 + radius, HEIGHT - radius)
        self.position = np.array([self.x, self.y], dtype=float)
        self.zeitschritt = SPEEDING

        # zufälliger, normierter Start-Geschwindigkeitsvektor
        self.x_vel = random.uniform(-1, 1)
        self.y_vel = random.uniform(-1, 1)
        norm = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        self.x_vel = self.x_vel / norm
        self.y_vel = self.y_vel / norm
        self.vel_vec = np.array([self.x_vel, self.y_vel])

        self.radius = radius

        self.masse = masse
        self.acceleration = np.array([0, 0])
        self.color = color
        self.last_collision = None  # Teilchen mit dem self als letztes kollidert sind

    def draw(self, win):
        '''zeichnet das Teilchen ins Fenster'''
        pygame.draw.circle(win, self.color, (self.position[0], self.position[1]), self.radius)

    def move(self):
        '''bewegt das Teilchen um die Geschwindigkeit'''
        self.position += self.vel_vec * self.zeitschritt

    def move_debug(self, moving):
        '''bewegt das Teilche um einen festen Wert'''
        self.position += moving

    def handle_border_collision(self):
        '''überprüft Kollision mit der Wand, invertiert Geschwindigkeitskomponente
        und setzt das Teilchen zurück ins Fenster'''
        if self.position[1] + self.radius >= HEIGHT:
            self.vel_vec[1] *= -1
            self.move_debug(np.array([0, -((self.position[1] + self.radius) - HEIGHT)]))
            self.last_collision = None
        elif self.position[1] - self.radius <= 0:
            self.vel_vec[1] *= -1
            self.move_debug(np.array([0, - self.position[1] + self.radius]))
            self.last_collision = None
        if self.position[0] + self.radius >= WIDTH:
            self.vel_vec[0] *= -1
            self.move_debug(np.array([-((self.position[0] + self.radius) - WIDTH), 0]))
            self.last_collision = None
        elif self.position[0] - self.radius <= 0:
            self.vel_vec[0] *= -1
            self.move_debug(np.array([-self.position[0] + self.radius, 0]))
            self.last_collision = None

    def handle_collision(self, b2):
        """überprüft Kollision mit anderen Teilchen und berechnet neue Geschwindigkeit"""
        count = 0
        abstand = np.linalg.norm(b2.position - self.position)
        if abstand <= self.radius + b2.radius and not (self.last_collision == b2 and b2.last_collision == self):
            # Zwischenspeicher für Geschwindigkeiten
            b1_vel_vec = self.vel_vec
            b2_vel_vec = b2.vel_vec

            # Berechnung elastischer Stoß
            self.vel_vec = (self.masse * b1_vel_vec + b2.masse * (2 * b2_vel_vec - b1_vel_vec)) / (
                        self.masse + b2.masse)
            b2.vel_vec = (b2.masse * b2_vel_vec + self.masse * (2 * b1_vel_vec - b2.vel_vec)) / (self.masse + b2.masse)

            self.last_collision = b2
            b2.last_collision = self
            count += 1
        abstand2 = np.linalg.norm(b2.position - self.position)
        if abstand2 > self.radius + b2.radius and count > 0:
            self.last_collision = None

    # idee: problem ist dass die teilchen nicht weit genug zurückgehen und dann wieder in die andere richtung fliegen
    # -> count einführen?
    '''def repulse(self,b2):
        ab_x = b2.x - self.x
        ab_y = b2.y - self.y
        distance = math.sqrt(ab_x ** 2 + ab_y ** 2)
        if distance <= (self.radius + b2.radius):
            repulse_force = -REPULSE/((distance**5)*self.masse)
            self.x_vel += (ab_x/distance)*repulse_force
            self.y_vel += (ab_y/distance)*repulse_force'''


def draw(win, balls):
    '''animiert Teilchen'''
    win.fill(WHITE)
    for ball in balls:
        ball.draw(win)
    pygame.display.update()


def generate_balls(amount):
    '''initialisert eine Liste aller (nicht-brownschen) Teilchen'''
    balls = []
    for i in range(amount):
        ball = Ball(BALL_RADIUS, BALL_COLOR, BALL_MASSE)
        balls.append(ball)

    return balls


def main():
    run = 1
    # generiert das brownsche Teilchen als ersten Eintrag einer Liste aller Teilchen
    brownsches_teilchen = Ball(BROWNSCHESTEILCHEN_RADIUS, BROWNSCHESTEILCHEN_COLOR, BROWNSCHESTEILCHEN_MASSE)
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
