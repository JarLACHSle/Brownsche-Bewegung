import random
import vpython

GRAVITATION = vpython.vector(0, .098, 0)

class Ball(vpython.sphere):
    '''Klasse für alle stoßenden Teilchen'''

    def __init__(self, radius, color, masse, length, width, height, zeitschritt, **args):
        super().__init__(**args)

        self.window_length = length
        self.window_width = width
        self.window_height = height

        # Startwert und aktuelle Position
        self.x = random.uniform(-self.window_length/2 + radius, self.window_length/2 - radius)
        self.y = random.uniform(-self.window_width/2 + radius, self.window_width/2 - radius)
        self.z = random.uniform(-self.window_width/2 + radius, self.window_height/2 - radius)
        self.pos = vpython.vector(self.x, self.y, self.z)
        self.zeitschritt = zeitschritt

        # zufälliger, normierter Start-Geschwindigkeitsvektor
        self.vel_vec = vpython.norm(vpython.vector.random())
        #self.vel_vec = vpython.vector(0, -1, 0)
        self.radius = radius

        self.masse = masse
        self.acceleration = ([0, 0])
        self.color = color
        self.last_collision = None  # Teilchen mit dem self als letztes kollidiert ist

    def move(self):
        '''bewegt das Teilchen um die Geschwindigkeit'''
        self.vel_vec -= GRAVITATION * self.zeitschritt
        self.pos += self.vel_vec * self.zeitschritt

    def move_debug(self, moving):
        '''bewegt das Teilche um einen festen Wert'''
        self.pos += moving

    def handle_border_collision(self):
        '''überprüft Kollision mit der Wand, invertiert Geschwindigkeitskomponente
        und setzt das Teilchen zurück ins Fenster'''
        if self.pos.z + self.radius > self.window_width/2:
            self.vel_vec = vpython.vector(self.vel_vec.x, self.y, self.vel_vec.z * -1)
            self.move_debug(vpython.vector(0, 0, -(self.pos.z + self.radius - self.window_width/2)))
            self.last_collision = None
        elif self.pos.z - self.radius < -self.window_width/2:
            self.vel_vec = vpython.vector(self.vel_vec.x, self.vel_vec.y, self.vel_vec.z * -1)
            self.move_debug(vpython.vector(0, 0, -(self.pos.z - self.radius) - self.window_width/2))
            self.last_collision = None
        if self.pos.y + self.radius > self.window_height/2:
            self.vel_vec = vpython.vector(self.vel_vec.x, self.vel_vec.y * -1, self.vel_vec.z)
            self.move_debug(vpython.vector(0, -(self.pos.y + self.radius - self.window_height/2), 0))
            self.last_collision = None
        elif self.pos.y - self.radius < -self.window_height/2:
            self.vel_vec = vpython.vector(self.vel_vec.x, self.vel_vec.y * -1, self.vel_vec.z)
            self.move_debug(vpython.vector(0, -(self.pos.y - self.radius)-self.window_height/2, 0))
            self.last_collision = None
        if self.pos.x + self.radius > self.window_length/2:
            self.vel_vec = vpython.vector(self.vel_vec.x * -1, self.vel_vec.y, self.vel_vec.z)
            self.move_debug(vpython.vector(-(self.pos.x + self.radius - self.window_length/2), 0, 0))
            self.last_collision = None
        elif self.pos.x - self.radius < -self.window_length/2:
            self.vel_vec = vpython.vector(self.vel_vec.x * -1, self.vel_vec.y, self.vel_vec.z)
            self.move_debug(vpython.vector(-(self.pos.x - self.radius)-self.window_length/2, 0, 0))
            self.last_collision = None

    def handle_collision(self, b2):
        """überprüft Kollision mit anderen Teilchen und berechnet neue Geschwindigkeit"""
        abstand = vpython.mag(b2.pos - self.pos)
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
