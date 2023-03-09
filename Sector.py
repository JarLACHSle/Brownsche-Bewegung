import numpy as np

class Sector:

    def __init__(self, edge_left, edge_right):
        self.balls = []
        self.sektor_edge_left = edge_left
        self.sektor_edge_right = edge_right

    def append_ball(self, ball):
        '''ordnet Bälle in Sektoren nach ihrer Projektion auf die X-Y-Ebene ein'''
        position_in_plane = np.array([ball.position[0],ball.position[1]]) 
        ball_is_in_right = position_in_plane <= self.sektor_edge_right
        ball_is_in_left = position_in_plane >= self.sektor_edge_left

        if True in ball_is_in_right and not False in ball_is_in_right and True in ball_is_in_left and not False in ball_is_in_left:
            self.balls.append(ball)
            ball.my_sector = self

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
