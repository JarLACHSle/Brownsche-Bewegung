class Cubesector:
    def __init__(self, center, length):

        self.center = center
        self.length = length
        self.balls = []

    def subdivide(self):
        '''
        Teilt den Würfel in 8 neue, gleich große Würfel auf und sammelt diese in einer Liste
        '''
        x, y, z = self.center
        l = self.length / 2
        subcubes_list = [
            Cubesector((x - l/2, y - l/2, z - l/2), l),
            Cubesector((x + l/2, y - l/2, z - l/2), l),
            Cubesector((x - l/2, y + l/2, z - l/2), l),
            Cubesector((x + l/2, y + l/2, z - l/2), l),
            Cubesector((x - l/2, y - l/2, z + l/2), l),
            Cubesector((x + l/2, y - l/2, z + l/2), l),
            Cubesector((x - l/2, y + l/2, z + l/2), l),
            Cubesector((x + l/2, y + l/2, z + l/2), l),
        ]
        return subcubes_list
    
    def get_subcube(self, ball):
        '''
        Vergleicht Position eines Punktes und des Mittelpunktes und gibt einen Integer von 0-7 aus,
        der den zugehörigen subcube repräsentiert
        '''
        x,y,z = ball.position[0], ball.position[1], ball.position[2] 
        cx, cy, cz = self.center
    
        # Position des Punktes relativ zum Mittelpunkt des Würfels
        dx, dy, dz = x - cx, y - cy, z - cz
    
        # schwarze Magie (bit-Manipulation) um sich sehr viele if-Abfragen zu sparen
        i = (dx > 0) << 2 | (dy > 0) << 1 | (dz > 0)
    
        return i
    
    def clear(self):
        '''löscht die Zuordnung'''
        for ball in self.balls:
            ball.my_sector = None
        self.balls = []
    
    def move_ball(self):
        ''' Bewegung und Kollision aller Teilchen'''
        for ball in self.balls:
            ball.handle_border_collision()
            for i in range(self.balls.index(ball) + 1, len(self.balls)):
                ball.handle_collision(self.balls[i])
            ball.move()