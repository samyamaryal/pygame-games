import sys
import pygame
import numpy as np
import random

running = True
pygame.init()
index = 1

directions = ['left', 'right']
# SCREEN DIMENSIONS
screen_width = 800
screen_height = 600
screen_size = [screen_width, screen_height]

# RANDOMIZE STARTING POSITION AND ALL
w_number = np.random.randint(0, screen_width)
h_number = np.random.randint(0, screen_height)

# BAT ATTRIBUTES
bat_width = 100.0
bat_height = 10.0
bat_velocity = 1
bat_starting_x = screen_width / 2
bat_starting_y = 500

bat2_starting_x = screen_width/2
bat2_starting_y = 100

# BALL ATTRIBUTES
ball_radius = 10.0
ball_x = w_number
ball_y = h_number
ball_x_velocity = 0.5
ball_y_velocity = 0.5

# GAME ATTRIBUTES
fontsize = 30
rate = 1
score = 0
fontcolor = (255, 255, 255)
pygame.key.set_repeat(rate, rate)

y_direction = 'up'
x_direction = 'right'

# CREATE GAME WINDOW
window = pygame.display.set_mode(screen_size)


# CLASS FOR BAT
class Bat:
    def __init__(self, width, height, velocity, x_pos, y_pos):
        self.width = width
        self.height = height
        self.velocity = velocity
        self.x_pos = x_pos
        self.y_pos = y_pos

    x_pos = screen_width/2

    def create_bat(self):
        pygame.draw.rect(window, (0, 100, 30), (self.x_pos, self.y_pos, self.width, self.height))

    def get_xposition(self):
        # Return the current x-coordinate for the bat (which is the coordinates for its top left corner)
        return self.x_pos

    def get_yposition(self):
        # Return the current y-coordinate for the bat
        return self.y_pos

    def auto_move_bat(self, ball_position):
        self.x_pos = ball_position - self.width/2

    def move_bat(self):
        # Model movement for the bat.
        # Arrow keys move the bat in either direction
        if event.key == pygame.K_LEFT and int(self.x_pos) != 0:
            self.x_pos -= self.velocity
        if event.key == pygame.K_RIGHT and int(self.x_pos + bat_width) != screen_width:
            self.x_pos += self.velocity


class Ball:
    def __init__(self, radius, center_x, center_y, x_velocity, y_velocity):
        self.radius = radius
        self.center_x = center_x
        self.center_y = center_y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def create_ball(self):
        pygame.draw.circle(window, (120, 91, 18), (self.center_x, self.center_y), self.radius)

    def get_xposition(self):
        # Return x coordinate for the center of the ball
        return self.center_x

    def get_yposition(self):
        # Return y coordinate for the center of the ball
        return self.center_y

    def vertical_move(self, dirn, y_velocity):
        # The ball moves automatically, changing direction on collision with the bat or the screen border
        # This function models movement in vertical direction.
        if dirn == 'down':
            self.center_y += y_velocity
        elif dirn == 'up':
            self.center_y -= y_velocity

    def horizontal_move(self, dirn, x_velocity):
        # This function models movement in the horizontal direction.
        if self.center_x - self.radius < 2:
            dirn == 'right'
        if self.center_x + self.radius < screen_width + 2:
            dirn == 'left'
        if dirn == 'right':
            self.center_x += x_velocity
        elif dirn == 'left':
            self.center_x -= x_velocity


# create an object bat with width, height, velocity & starting x position
bat = Bat(bat_width, bat_height, bat_velocity, bat_starting_x, bat_starting_y)

# create another bat
bat2 = Bat(bat_width, bat_height, bat_velocity, bat2_starting_x, bat2_starting_y)

# create an object Ball with radius, x, y, and velocity of movement
ball = Ball(ball_radius, ball_x, ball_y, ball_x_velocity, ball_y_velocity)

# GAME LOOP
pygame.time.wait(10000)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    window.fill((16, 200, 205))

    # Create bat and ball & place them in the game window
    bat.create_bat()
    bat2.create_bat()
    ball.create_ball()

    # if ANY key is being pressed, the move_bat function from 'Bat' class is called
    # The function then checks whether the pressed key is LARROW or RARROW and moves the bat accordingly
    if event.type == pygame.KEYDOWN:
        bat.move_bat()

    # This portion creates a live score box.
    font = pygame.font.SysFont("cambria", fontsize)
    text = font.render(str(score), True, fontcolor)
    textbox = text.get_rect()
    textbox.center = (400, 70)
    window.blit(text, textbox)


    # Reflect if ball makes contact with the AI bat
    if int(ball.get_yposition() - ball_radius) < bat2.get_yposition():
        y_direction = 'down'
        index = random.randint(0, 1)

    # Reflect if the ball makes contact with your bat
    if int(ball.get_yposition()) == int(bat.get_yposition()) \
            and bat.get_xposition() < ball.get_xposition() < bat.get_xposition()+bat_width:
        y_direction = 'up' # MOVE UP

        # The index variable is used to model randomness in the ball's motion
        # Whenever the ball makes contact with the lower bat, the ball can move in either the left or the right direction
        # So the ball can change direction on contact with the lower bat.

        # 0 or 1 is generated at random, and the ball's direction is then determined by that value.
        # 0 = left
        # 1 = right

        index = random.randint(0, 1)
        x_direction = directions[index]
        score += 1

    # Reflect if ball makes contact with top surface
    # Horizontal movement
    if int(ball.get_xposition() - ball_radius) == 0:
        x_direction = 'right'
    elif int(ball.get_xposition() + ball_radius) == screen_width:
        x_direction = 'left'

    random_y_velocity = np.random.random()
    random_x_velocity = np.random.random()

    # Bat2 is the upper bat, and it is controlled by AI. the auto_move_bat moves the bat based on the ball's x coordinate
    # AI stonks go brr

    bat2.auto_move_bat(ball.get_xposition())
    ball.vertical_move(y_direction, random_y_velocity)
    ball.horizontal_move(x_direction, random_x_velocity)

    # Condition for game over
    if ball.get_yposition() > screen_height:
        font2 = pygame.font.SysFont('Arial', 200)
        game_over = "GAME OVER! YOUR SCORE WAS " + str(score) + ". PRESS ENTER TO EXIT!"
        message = font.render(game_over, True, (255, 0, 255))
        msgbox = message.get_bounding_rect(10)
        msgbox.center = (400, 300)
        window.blit(message, msgbox)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            sys.exit()

    pygame.display.flip()
