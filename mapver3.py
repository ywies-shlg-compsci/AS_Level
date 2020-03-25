import os
import pygame

class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 432, 16, 16)
        self.status = True
        self.flashcounter = 10

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
                player.status = False
        for flyingspike in flyingspikes:
            if self.rect.colliderect(flyingspike.rect):
                self.rect.left = 32
                self.rect.top = 432
                player.status = False
        for squaremonster in squaremonsters:
            if self.rect.colliderect(squaremonster.rect):
                self.rect.left = 32
                self.rect.top = 432
                player.status = False


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
        self.rect = pygame.Rect(pos[0], pos[1], 10, 20)

    def move(self):
        self.rect.y -= 32

    def trigger(self):
        self.trigger = False


class SquareMonster(object):
    def __init__(self, pos, dx,dy ,behavelist):
        squaremonsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.dx = dx
        self.dy = dy
        self.state = ''
        self.statelist = behavelist
        self.statecounter = 0
        self.counter = self.statelist[self.statecounter + 1]


    def move(self):
        self.state = self.statelist[self.statecounter]
        if self.state == "left":
            self.moveleft(self.dx,self.dy)
            self.counter -= 1
            #print("left")
            #print(self.counter)
        if self.state == "right":
            self.moveright(self.dx,self.dy)
            self.counter -= 1
            #print("right")
            #print(self.counter)
        if self.state == "up":
            self.moveup(self.dx,self.dy)
            self.counter -= 1
            #print("up")
            #print(self.counter)
        if self.state == "down":
            self.movedown(self.dx,self.dy)
            self.counter -= 1
            #print("down")
            #print(self.counter)
        if self. counter == 0:
            self.counter = self.statelist[self.statecounter + 1]
            self.statecounter += 2
            if self.statecounter > 6:
                self. statecounter =0

    def moveright(self,dx,dy):
        if self.counter % 2 == 0:
            self.rect.x += dx

    def moveleft(self,dx,dy):
        if self.counter % 2 == 0:
            self.rect.x -= dx
    def moveup(self,dx,dy):
        if self.counter % 2 == 0:
            self.rect.y -= dy
    def movedown(self,dx,dy):
        if self.counter % 2 == 0:
            self.rect.y += dy



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
squaremonsters = []
behavelist =[]


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
    "W W       M     W   W W   WWWWWW   WWWWW",
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
        if col == "M":
            behavelist = ['left',60, 'up',60, 'down',60, 'right',60]
            squaremonsters.append( SquareMonster((x,y+16),3,2,behavelist))

        x += 32
    y += 32
    x = 0
KEY_PRESSED = False
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
        KEY_PRESSED = True
    if key[pygame.K_RIGHT]:
        player.move(v, 0)
        KEY_PRESSED = True
    if key[pygame.K_UP]:
        player.move(0, -v)
        KEY_PRESSED = True
    if key[pygame.K_DOWN]:
        player.move(0, v)
        KEY_PRESSED = True


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
        if (player.rect.right <= flyingspike.rect.left - 32 or player.rect.left -32 <= flyingspike.rect.right )and KEY_PRESSED == True:
            flyingspike.trigger =True
        if flyingspike.rect.bottom == 0:
            flyingspike.trigger = False

        if flyingspike.trigger == True:
            flyingspike.move()

    for squaremonster in squaremonsters:
        squaremonster.move()
        pygame.draw.rect(screen, (0, 255, 255), squaremonster.rect)

    if player.status == True:
        pygame.draw.rect(screen, (255, 200, 0), player.rect)
    elif player.status == False:
        #print("dead")
        player.flashcounter= player.flashcounter -1
        if player.flashcounter % 2 == 1:
            pygame.draw.rect(screen, (255, 200, 0), player.rect)
        elif player.flashcounter == 0:
            player.status = True
            player.flashcounter = 10

    #print(player.flashcounter)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)#exit color

    pygame.display.flip()#update the contents of the entire display
    #pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
