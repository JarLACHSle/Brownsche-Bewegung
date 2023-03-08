import Ball


class Sector:

    def __init__(self, edge_left, edge_right):
        self.balls = []
        self.sektor_edge_left = edge_left
        self.sektor_edge_right = edge_right

    def append_ball(self, ball):
        ball_is_in_right = ball.position <= self.sektor_edge_right
        ball_is_in_left = ball.position >= self.sektor_edge_left

        if True in ball_is_in_right and not False in ball_is_in_right and True in ball_is_in_left and not False in ball_is_in_left:
            self.balls.append(ball)
            ball.my_sector = self

    def clear(self):
        for ball in self.balls:
            ball.my_sector = None
        self.balls = []

    def move_ball(self):
        for ball in self.balls:
            ''' Bewegung und Kollision aller Teilchen'''
            ball.handle_border_collision()
            for i in range(self.balls.index(ball) + 1, len(self.balls)):
                ball.handle_collision(self.balls[i])
                # ball.repulse(balls[i])
            ball.move()
