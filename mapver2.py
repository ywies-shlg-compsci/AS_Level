import os
import pygame

class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 432, 16, 16)

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.rect.left = 32
                self.rect.top = 432
        for flyingspike in flyingspikes:
            if self.rect.colliderect(flyingspike.rect):
                self.rect.left = 32
                self.rect.top = 432

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Spike(object):
    def __init__(self, pos):
        spikes.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)

class FlyingSpike(object):
    def __init__(self, pos):
        flyingspikes.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
    def move(self):
        self.rect.y -= 20


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!" )#the headline
screen = pygame.display.set_mode((1280, 480))#the size of the screen
clock = pygame.time.Clock()
walls = []  # List to hold the walls
player = Player()
spikes = []
flyingspikes = []


# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W         WWWWWW   WWW    WWWW  WWWWW  W",
    "W   WWWW       W   W   WWWW       W    W",
    "W   W        WWWW  W  WW    W    WW    W",
    "W WWW  WWWW        WW  W  W WW         W",
    "W   W     W W      W   W  W    WWW   WWW",
    "W   W     W W W WWWW   W  W WW W       W",
    "W   WWW WWW W W W  WWW W WWw W W     W W",
    "W     W   W   W        W     W WWWWWWW W",
    "WWW   W   WW WW WWWWW WWWWW    W       W",
    "W W             W   W W   WWWWWW   WWWWW",
    "W W   WWWWWWWWWWW W WWW W   W          W",
    "W  F  WE    S     W     W              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))#thw wall block
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)#the exit block
        if col == "F":
            FlyingSpike((x, 650))
        if col == "S":
            Spike((x,y+22))
        x += 32
    y += 32
    x = 0

running = True
while running:
    v = 8
    clock.tick(120)

    for e in pygame.event.get():#quit function
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-v, 0)
    if key[pygame.K_RIGHT]:
        player.move(v, 0)
    if key[pygame.K_UP]:
        player.move(0, -v)
    if key[pygame.K_DOWN]:
        player.move(0, v)


    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        print("You win!")
        break
    # Draw the scene
    screen.fill((0, 0, 0))#background color
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)#wall color
    for spike in spikes:
        pygame.draw.rect(screen,(0,255,0),spike.rect)
    for flyingspike in flyingspikes:
        pygame.draw.rect(screen, (0, 255, 0), flyingspike.rect)
        if player.rect.right <= flyingspike.rect.left - 32 or player.rect.left -32 <= flyingspike.rect.right:
            flyingspike.move()
    pygame.draw.rect(screen, (255, 0, 0), end_rect)#exit color
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()#update the contents of the entire display
    #pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
