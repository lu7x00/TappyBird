import pygame, sys, random
from  pygame.locals import *


#########################################################################################################
#                                                                                                       #
#                                    TAPPY BIRD V 1.0                                                   #
#                                                                                                       #
#########################################################################################################


class Game:
    RES = (800, 600)
    WHITE = (255, 255, 255)
    BCG_SCALE = (800, 600)
    GRAVITY = 0.08

    window = None
    background = None
    isStarted = False
    flappy = None
    obstacles = None
    score = 0
    font = None
    text = None
    textRect = None

    def __init__(self, title):
        pygame.display.set_caption(title)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.window = pygame.display.set_mode(self.RES)
        self.background = pygame.image.load("background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.BCG_SCALE)
        self.flappy = Bird()
        self.obstacles = Obstacles()
        self.obstacles.generate_obstacles()

    def input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            if event.type == KEYUP:
                self.flappy.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     self.isStarted = True

    def update(self):
        self.input(pygame.event.get())
        self.window.fill(self.WHITE)
        self.window.blit(self.background, (0, 0))
        if self.isStarted:
            self.flappy.update(self.GRAVITY)
            self.obstacles.update(self.window)
            self.check_collision()
        self.window.blit(self.flappy.image, self.flappy.get_position())
        self.update_score()
        self.check_collision()
        self.window.blit(self.text, self.textRect)

    def update_score(self):
        self.text = self.font.render(str(self.score), True, self.WHITE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (400, 300)

    def check_collision(self):
        for index in range(len(self.obstacles.obstacles)):
            isCollisionTop = pygame.sprite.collide_rect(self.flappy, self.obstacles.obstacles[index][0])
            isCollisionBottom = pygame.sprite.collide_rect(self.flappy, self.obstacles.obstacles[index][1])
            if self.flappy.rect.x == (self.obstacles.obstacles[index][0].get_position())[0] + 100:
                self.obstacles.obstacles.append(self.obstacles.generate_obstacle())
                self.score += 1
            if isCollisionTop or isCollisionBottom:
                sys.exit(0)
            if (self.obstacles.obstacles[index][0].get_position())[0] == 0:
                self.obstacles.obstacles.remove(self.obstacles.obstacles[index])
                break


class Bird(pygame.sprite.Sprite):
    START_POSITION = (200, 300)
    BIRD_SCALE = (50, 45)

    bird = None
    rotateAngle = 0
    speed = 0

    def __init__(self):
        self.set_image()
        self.image = pygame.transform.scale(self.bird, self.BIRD_SCALE)
        self.rect = self.image.get_rect()
        self.set_start_position()

    def set_image(self):
        self.bird = pygame.image.load("bird.png").convert_alpha()

    def set_start_position(self):
        self.rect.x = self.START_POSITION[0]
        self.rect.y = self.START_POSITION[1]

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def jump(self):
        self.speed = -2


    def update(self, GRAVITY):
        if self.rect.y <= 0 or self.rect.y >= 600:
            self.rect.y += GRAVITY * 5
        self.rect.y += self.speed
        self.speed += GRAVITY


class Obstacle(pygame.sprite.Sprite):
    HEIGHT = 500
    OBSTACLE_SCALE = (100, HEIGHT)
    SPEED = 0.1

    obstacle = None

    def __init__(self, angle, position):
        self.obstacle = pygame.image.load("obstacle.png").convert_alpha()
        self.obstacle = pygame.transform.scale(self.obstacle, self.OBSTACLE_SCALE)
        self.obstacle = pygame.transform.rotozoom(self.obstacle, angle, 1)
        self.image = self.obstacle
        self.rect = self.image.get_rect()
        self.set_position(position)

    def move(self):
        self.rect.x -= self.SPEED

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def get_position(self):
        return (self.rect.x, self.rect.y)

class Obstacles:
    START_TOP = (500, -200)
    START_BOTTOM = (500, 400)
    MIN_DISTANCE = 200
    MAX_DISTANCE = 250
    MIN_HEIGHT = 100
    MAX_HEIGHT = 150


    obstacle_top = []
    obstacle_bottom = []
    obstacles = []

    def __init__(self):
        self.create()

    def create(self):
        for index in range(0, 5):
            self.obstacle_top.append(Obstacle(180, self.START_TOP))
            self.obstacle_bottom.append(Obstacle(0, self.START_BOTTOM))
            temp_obstacles = (self.obstacle_top[index], self.obstacle_bottom[index])
            self.obstacles.append(temp_obstacles)

    def update(self, window):
        for index in range(len(self.obstacles)):
            self.obstacles[index][0].move()
            self.obstacles[index][1].move()
            window.blit(self.obstacles[index][0].image, self.obstacles[index][0].get_position())
            window.blit(self.obstacles[index][1].image, self.obstacles[index][1].get_position())

    def generate_obstacle(self):
        distance = random.randrange(self.MIN_DISTANCE, self.MAX_DISTANCE)
        height = random.randrange(-self.MIN_HEIGHT, self.MAX_HEIGHT)
        position_top = self.obstacles[len(self.obstacles) - 1][0].get_position()
        position_bottom = self.obstacles[len(self.obstacles) - 1][1].get_position()
        obstacle_top = Obstacle(180, (position_top[0] + distance, position_top[1] + height))
        obstacle_bottom = Obstacle(0, (position_bottom[0] + distance, position_bottom[1] + height))
        obstacle = (obstacle_top, obstacle_bottom)
        return obstacle

    def generate_obstacles(self):
        for index in range(len(self.obstacles)):
            distance = random.randrange(self.MIN_DISTANCE, self.MAX_DISTANCE)
            height = random.randrange(-self.MIN_HEIGHT, self.MAX_HEIGHT)
            position_top = self.obstacles[index][0].get_position()
            position_bottom = self.obstacles[index][1].get_position()
            ps_top = (position_top[0] + distance * (index + 1), position_top[1] + height)
            ps_bottom = (position_bottom[0] + distance * (index + 1), position_bottom[1] + height)
            self.obstacles[index][0].set_position(ps_top)
            self.obstacles[index][1].set_position(ps_bottom)


pygame.init()

game = Game("Flappy Bird")

while True:
    game.update()
    pygame.display.update()