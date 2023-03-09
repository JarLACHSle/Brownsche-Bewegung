import random
import numpy as np


class Ball:
    '''Klasse für alle stoßenden Teilchen'''

    def __init__(self, radius, color, masse, WIDTH, HEIGHT, DEPTH, zeitschritt):
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_depth = DEPTH

        self.my_sector = None

        # Startwert und aktuelle Position
        self.x = self.original_x = random.randint(0 + radius, self.window_width - radius)
        self.y = self.original_y = random.randint(0 + radius, self.window_height - radius)
        self.z = self.original_z = random.randint(0 + radius, self.window_depth - radius)
        self.position = np.array([self.x, self.y, self.z], dtype=float)
        self.zeitschritt = zeitschritt

        # zufälliger, normierter Start-Geschwindigkeitsvektor
        self.x_vel = random.uniform(-1, 1)
        self.y_vel = random.uniform(-1, 1)
        self.z_vel = random.uniform(-1, 1)
        self.vel_vec = np.array([self.x_vel, self.y_vel, self.z_vel])
        norm = np.linalg.norm(self.vel_vec)
        self.vel_vec = self.vel_vec/norm
                
        self.radius = radius

        self.masse = masse
        self.acceleration = np.array([0, 0, 0])
        self.color = color
        self.last_collision = None  # Teilchen mit dem self als letztes kollidiert ist

    def move(self):
        '''bewegt das Teilchen um die Geschwindigkeit'''
        self.position += self.vel_vec * self.zeitschritt

    def move_debug(self, moving):
        '''bewegt das Teilchen um einen festen Wert'''
        self.position += moving

    def handle_border_collision(self):
        '''überprüft Kollision mit der Wand, invertiert Geschwindigkeitskomponente
        und setzt das Teilchen zurück ins Fenster'''
        if self.position[2] + self.radius >= self.window_depth:
            self.vel_vec[2] *= -1
            self.move_debug(np.array([0, 0, -((self.position[2] + self.radius) - self.window_depth)]))
            self.last_collision = None
        elif self.position[2] - self.radius <= 0:
            self.vel_vec[2] *= -1
            self.move_debug(np.array([0, 0, - self.position[2] + self.radius]))
            self.last_collision = None
        if self.position[1] + self.radius >= self.window_height:
            self.vel_vec[1] *= -1
            self.move_debug(np.array([0, -(self.position[1] + self.radius - self.window_height), 0]))
            self.last_collision = None
        elif self.position[1] - self.radius <= 0:
            self.vel_vec[1] *= -1
            self.move_debug(np.array([0, - self.position[1] + self.radius, 0]))
            self.last_collision = None
        if self.position[0] + self.radius >= self.window_width:
            self.vel_vec[0] *= -1
            self.move_debug(np.array([-(self.position[0] + self.radius - self.window_width), 0, 0]))
            self.last_collision = None
        elif self.position[0] - self.radius <= 0:
            self.vel_vec[0] *= -1
            self.move_debug(np.array([-self.position[0] + self.radius, 0, 0]))
            self.last_collision = None

    def handle_collision(self, b2):
        """überprüft Kollision mit anderen Teilchen und berechnet neue Geschwindigkeit"""
        abstand = np.linalg.norm(b2.position - self.position)
        if abstand <= self.radius + b2.radius and not (self.last_collision == b2 and b2.last_collision == self):
            # Zwischenspeicher für Geschwindigkeiten
            b1_vel_vec = self.vel_vec
            b2_vel_vec = b2.vel_vec

            # Berechnung elastischer Stoß
            self.vel_vec = (self.masse * b1_vel_vec + b2.masse * (2 * b2_vel_vec - b1_vel_vec)) / (self.masse + b2.masse)
            b2.vel_vec = (b2.masse * b2_vel_vec + self.masse * (2 * b1_vel_vec - b2.vel_vec)) / (self.masse + b2.masse)

            self.last_collision = b2
            b2.last_collision = self
            if b2.color == "red":
                print("Stoß mit brownschem Teilchen!")
