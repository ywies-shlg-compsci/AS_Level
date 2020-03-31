import os
import pygame
import random

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
        for trackingmonster in trackingmonsters:
            if self.rect.colliderect(trackingmonster.rect):
                self.rect.left = 32
                self.rect.top = 432
                player.status = False

    def drawborder(self, screen):
        left = self.rect.x
        top = self.rect.y
        right = self.rect.x + self.rect.width
        bottom = self.rect.y + self.rect.height
        points = []
        points.append((left, top))
        points.append((right, top))
        points.append((right, bottom))
        points.append((left, bottom))
        points.append((left, top))
        pygame.draw.lines(screen, (0, 255, 255), False, points, 1)


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
    def __init__(self, pos, dx,dy ,behavelist1):
        squaremonsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.dx = dx
        self.dy = dy
        self.state = ''
        self.statelist = behavelist1
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
    def drawborder(self, screen):
        left = self.rect.x
        top = self.rect.y
        right = self.rect.x + self.rect.width
        bottom = self.rect.y + self.rect.height
        points = []
        points.append((left, top))
        points.append((right, top))
        points.append((right, bottom))
        points.append((left, bottom))
        points.append((left, top))
        pygame.draw.lines(screen, (0, 255, 255), False, points, 1)

class Trackingmonster(object):
    def __init__(self, pos, dx, dy):
        trackingmonsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.dx = dx
        self.dy = dy

    def moveright(self,dx,dy):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left

    def moveleft(self,dx,dy):
        self.rect.x -= dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right

    def moveup(self,dx,dy):
        self.rect.y -= dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def movedown(self,dx,dy):
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top

class RandomMonster(object):
    def __init__(self, pos, dx, dy):
        randommonsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.dx = dx
        self.dy = dy
        self.freedirection = []
        self.statelist = [-1,1]
        self.statecounter = 2
        self.counter = 0
        self.direction = -1
    def makebehaviourlist(self):#create new behavior
        xSquare = (self.rect.x//32) -1
        ySquare = (self.rect.y//32) -1
        #print(xSquare,ySquare)
        if level[ySquare - 1][xSquare]!="W":
            self.direction =0 #Moving down
            self.freedirection.append(self.direction)
        if level[ySquare ][xSquare+1]!="W":
            self.direction =1 #Moving right
            self.freedirection.append(self.direction)
        if level[ySquare+1][xSquare]!="W":
            self.direction =2 #Moving up
            self.freedirection.append(self.direction)
        if level[ySquare ][xSquare-1]!="W":
            self.direction =3 #Moving left
            self.freedirection.append(self.direction)
        #print(self.freedirection)
        number = random.randint(0,len(self.freedirection)-1)
        self.statelist.append(self.freedirection[number])
        self.statelist.append(1)
        print(self.statelist)
        self.freedirection = []



    def move(self):
        self.direction = self.statelist[self.statecounter]
        self.counter=self.statelist[self.statecounter + 1]
        print((self.direction))
        if self.direction == 3:
            self.moveleft(self.dx, self.dy)
            self.counter -= 1
            # print("left")
            # print(self.counter)
        if self.direction == 1:
            self.moveright(self.dx, self.dy)
            self.counter -= 1
            # print("right")
            # print(self.counter)
        if self.direction == 2:
            self.moveup(self.dx, self.dy)
            self.counter -= 1
            # print("up")
            # print(self.counter)
        if self.direction == 0:
            self.movedown(self.dx, self.dy)
            self.counter -= 1
            # print("down")
            # print(self.counter)
        if self.counter == 0:
            self.counter = self.statelist[self.statecounter + 1]
            self.statecounter += 2


    def moveright(self,dx,dy):
        self.rect.x += dx

    def moveleft(self,dx,dy):
        self.rect.x -= dx

    def moveup(self,dx,dy):
        self.rect.y -= dy

    def movedown(self,dx,dy):
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
trackingmonsters = []
randommonsters = []

behavelist1 =[]
behavelist2 = []




# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W         WWWWWW   WWW    WWWW  WWWWW  W",
    "W   WWWW       W   W   WWWW       W    W",
    "W T W        WWWW  W  WW    W    WW    W",
    "W WWW  WWWW        WW  W  W WW         W",
    "W   W     W W      W   W  W    WWW   WWW",
    "W   W     W W W WWWW   W  W WW W       W",
    "W   WWW WWW W W W  WWW W WWw W W     W W",
    "W     W   W   W        W     W WWWWWWW W",
    "WWW   W   WW WW WWWWW WWWWW    W       W",
    "W W       M     W   W W   WWWWWW   WWWWW",
    "W W   WWWWWWWWWWW W WWW W   W          W",
    "W  F  WE    S     W     W      R       W",
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
            behavelist1 = ['left',60, 'up',60, 'down',60, 'right',60]
            squaremonsters.append(SquareMonster((x,y+16),3,2,behavelist1))
        if col == "T":
            trackingmonsters.append(Trackingmonster((x,y+16),1,1))
        if col == "R":
            randommonsters.append(RandomMonster((x,y+16),2,2))

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
        pygame.draw.rect(screen, (0, 255, 150), squaremonster.rect)
        squaremonster.drawborder(screen)


    for trackingmonster in trackingmonsters:
        pygame.draw.rect(screen, (150, 150, 255), trackingmonster.rect)
        if player.rect.left < trackingmonster.rect.left:
            trackingmonster.moveleft(trackingmonster.dx,trackingmonster.dy)
        if player.rect.right > trackingmonster.rect.right:

            trackingmonster.moveright(trackingmonster.dx,trackingmonster.dy)
        if player.rect.top > trackingmonster.rect.top:

            trackingmonster.movedown(trackingmonster.dx,trackingmonster.dy)
        if player.rect.bottom < trackingmonster.rect.bottom:

            trackingmonster.moveup(trackingmonster.dx,trackingmonster.dy)

    for randommonster in randommonsters:
        pygame.draw.rect(screen, (150, 150, 150), randommonster.rect)
        randommonster.makebehaviourlist()
        randommonster.move()


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
    player.drawborder(screen)
    #print(player.flashcounter)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)#exit color


    pygame.display.flip()#update the contents of the entire display
    #pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
