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

DO_VELOCITY_PLOT = True

# Farbwerte
RED = (255, 82, 32)
BLACK = (0, 0, 0)
BLUE = (23, 2, 255)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)

# Tick-Faktor
TIME_STEP = 3

# Setup Teilchen
BALL_RADIUS = 2
BALL_AMOUNT = 200
BALL_COLOR = BLUE
BALL_MASSE = 5

BROWNSCHESTEILCHEN_MASSE =  40
BROWNSCHESTEILCHEN_RADIUS = 16
BROWNSCHESTEILCHEN_COLOR = RED


class Ball:
    '''Klasse für alle stoßenden Teilchen'''

    def __init__(self, radius, color, masse):
        # Startwert und aktuelle Position
        self.x = self.original_x = random.randint(0 + radius, WIDTH - radius)
        self.y = self.original_y = random.randint(0 + radius, HEIGHT - radius)
        self.position = np.array([self.x, self.y], dtype=float)
        self.zeitschritt = TIME_STEP

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
        self.last_collision = None  # Teilchen mit dem self als letztes kollidert ist

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
    
class Sector:
    '''Aufteilung von Teilchen in Listen(Sektoren), die je einem Abschnitt des Fensters zugeordnet sind'''
    def __init__(self):
        self.sec1 = []
        self.sec2 = []
        self.sec3 = []
        self.sec4 = []
    def sectorize(self,ball, height=HEIGHT, width=WIDTH):
        '''ordnet den Ball einem Sektor im Koordinatensystem zu'''
        if ball.position[0] >= width/2 and ball.position[1] >= height/2:
            self.sec1.append(ball)
            return(self.sec1)
        elif ball.position[0] < width/2 and ball.position[1] >= height/2:
            self.sec2.append(ball)
            return(self.sec2)
        elif ball.position[0] < width/2 and ball.position[1] < height/2:
            self.sec3.append(ball)
            return(self.sec3)
        else:
            self.sec4.append(ball)
            return(self.sec4)
    def flush(self):
        '''leert die Sektoren'''
        self.sec1 = []
        self.sec2 = []
        self.sec3 = []
        self.sec4 = []
    
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
    # dictionary für die Auswertung der Geschwindigkeitsverteilung
    vel_dict = {}  
    sector = Sector()

    while run:
        draw(WIN, balls)
        pygame.time.Clock().tick(60)

        # prüft, ob das Fenster geschlosen wurde und beendet das Programm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
                break
        sector.flush()
        for ball in balls:
            own_sector = sector.sectorize(ball)
            ''' Bewegung und Kollision aller Teilchen'''
            ball.handle_border_collision()
            for i in range(len(own_sector)-1):
                ball.handle_collision(own_sector[i])
            ball.move()
            if DO_VELOCITY_PLOT:
                '''falls True, wird die Geschwindigkeitsverteilung über 
                den gesamten Verlauf der Simulation aufgezeichnet'''
                abselv = math.sqrt(ball.vel_vec[0] ** 2 + ball.vel_vec[1] ** 2)
                if abselv in vel_dict:
                    vel_dict[abselv] += 1
                else:
                    vel_dict[abselv] = 1

    if DO_VELOCITY_PLOT:
        '''falls True, wird nach Simulationsende die Geschwindigkeitsverteilung geplottet'''
        keys = list(vel_dict.keys())
        values = list(vel_dict.values())
        plt.bar(keys, values, 0.1, color="blue")
        plt.show()

    pygame.quit()


if __name__ == '__main__':
    main()
