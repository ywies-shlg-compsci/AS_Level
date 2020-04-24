import os
import pygame
import random
import makingmaze_version3 as makingmaze

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STARTX = 32
STARTY = 432

P_SIZE =16
C_SIZE = 8

class Coin(object):

    def __init__(self,x,y):
        coinslist.append(self)
        self.rect = pygame.Rect(x, y,C_SIZE,C_SIZE)
        self.Delete = False

    def draw(self):
        pygame.draw.circle(screen,(255,200,0),(self.rect.x+16,self.rect.y+16),C_SIZE)


class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(STARTX, STARTY, P_SIZE, P_SIZE)
        self.status = True
        self.flashcounter = 10
        self.image = pygame.image.load('mm_04.png')
        self.image_r_1 = pygame.transform.scale(pygame.image.load('mm_01.png'), (P_SIZE, P_SIZE))
        self.image_r_2 = pygame.transform.scale(pygame.image.load('mm_02.png'), (P_SIZE, P_SIZE))
        self.image_r_3 = pygame.transform.scale(pygame.image.load('mm_03.png'), (P_SIZE, P_SIZE))
        self.image_r_4 = pygame.transform.scale(pygame.image.load('mm_04.png'), (P_SIZE, P_SIZE))
        self.image_l_1 = pygame.transform.scale(pygame.image.load('mm_01_l.png'), (P_SIZE, P_SIZE))
        self.image_l_2 = pygame.transform.scale(pygame.image.load('mm_02_l.png'), (P_SIZE, P_SIZE))
        self.image_l_3 = pygame.transform.scale(pygame.image.load('mm_03_l.png'), (P_SIZE, P_SIZE))
        self.image_l_4 = pygame.transform.scale(pygame.image.load('mm_04_l.png'), (P_SIZE, P_SIZE))
        self.animateMoveRight = [self.image_r_1, self.image_r_2, self.image_r_3, self.image_r_4]
        self.animateMoveLeft = [self.image_l_1, self.image_l_2, self.image_l_3, self.image_l_4]
        self.ismove = False
        self.frame = 0

    def drawright(self):

        screen.blit(self.animateMoveRight[3], (self.rect.x, self.rect.y))

    def drawleft(self):

        screen.blit(self.animateMoveLeft[3], (self.rect.x, self.rect.y))


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
        self.trigger = False

    def move(self):
        self.rect.y -= 32

    def triggerActive(self, player, key):
        if (player.rect.right >= self.rect.left - 32 or player.rect.left - 32 >= self.rect.right) and key == True:
            self.trigger = True
            print("trigger")


class SquareMonster(object):
    def __init__(self, pos, dx, dy, behavelist1):
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
            self.moveleft(self.dx, self.dy)
            self.counter -= 1
            # print("left")
            # print(self.counter)
        if self.state == "right":
            self.moveright(self.dx, self.dy)
            self.counter -= 1
            # print("right")
            # print(self.counter)
        if self.state == "up":
            self.moveup(self.dx, self.dy)
            self.counter -= 1
            # print("up")
            # print(self.counter)
        if self.state == "down":
            self.movedown(self.dx, self.dy)
            self.counter -= 1
            # print("down")
            # print(self.counter)
        if self.counter == 0:
            self.counter = self.statelist[self.statecounter + 1]
            self.statecounter += 2
            if self.statecounter > 6:
                self.statecounter = 0

    def moveright(self, dx, dy):
        if self.counter % 2 == 0:
            self.rect.x += dx

    def moveleft(self, dx, dy):
        if self.counter % 2 == 0:
            self.rect.x -= dx

    def moveup(self, dx, dy):
        if self.counter % 2 == 0:
            self.rect.y -= dy

    def movedown(self, dx, dy):
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
        # print(pos[0],pos[1])
        self.dx = dx
        self.dy = dy
        self.freedirection = []
        self.statelist = []
        self.counter = 0
        self.direction = -1
        self.num = 1
        self.prePosx = self.rect.x
        self.prePosy = self.rect.y

    def makebehaviourlist(self):  # create new behavior
        self.statelist = []
        self.xSquare = (self.rect.x // 32)
        self.ySquare = (self.rect.y // 32)
        # print(self.xSquare,self.ySquare)
        if level[self.ySquare + 1][self.xSquare] != "W":
            self.direction = DOWN  # Moving down
            self.freedirection.append(self.direction)
        if level[self.ySquare][self.xSquare + 1] != "W":
            self.direction = RIGHT  # Moving right
            self.freedirection.append(self.direction)
        if level[self.ySquare - 1][self.xSquare] != "W":
            self.direction = UP  # Moving up
            self.freedirection.append(self.direction)
        if level[self.ySquare][self.xSquare - 1] != "W":
            self.direction = LEFT  # Moving left
            self.freedirection.append(self.direction)
        # print(self.freedirection)
        number = random.randint(0, len(self.freedirection) - 1)
        self.statelist.append(self.freedirection[number])
        self.direction = self.statelist[0]
        dir = self.direction
        self.calculatedistance()
        self.num = random.randint(1, self.num)
        # print("previous",self.num)
        # print(self.rect.x,self.rect.y)
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 16:  # block bottom left
            if dir == RIGHT or dir == UP:
                self.num = self.num + 0.5
            if dir == LEFT or dir == DOWN:
                self.num = self.num
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:  # block top left
            if dir == RIGHT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == LEFT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 0:  # block top right
            if dir == LEFT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 16:  # block bottom right
            if dir == LEFT or dir == UP:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == DOWN:
                self.num = self.num
        # print("after", self.num)
        self.statelist.append(16 * self.num)
        # print(self.statelist)
        self.freedirection = []
        self.num = 1
        self.counter = self.statelist[1]
        # print((self.direction))

    def makebehaviourlistkeyboard(self, dir):  # create new behavior
        self.statelist = []
        self.xSquare = (self.rect.x // 32)
        self.ySquare = (self.rect.y // 32)

        # print(self.xSquare,self.ySquare)

        self.direction = dir

        # print(self.freedirection)
        # number = random.randint(0,len(self.freedirection)-1)
        self.statelist.append(self.direction)
        # print("Here",self.rect.topleft)
        # self.direction = self.statelist[0]
        self.calculatedistance()
        print("previous:", self.num)
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 16:  # block bottom left
            if dir == RIGHT or dir == UP:
                self.num = self.num + 0.5
            if dir == LEFT or dir == DOWN:
                self.num = self.num
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:  # block top left
            if dir == RIGHT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == LEFT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 0:  # block top right
            if dir == LEFT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 16:  # block bottom right
            if dir == LEFT or dir == UP:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == DOWN:
                self.num = self.num

        # if self.rect.x % 32 == 16:
        # self.num = self.num * 2
        # if self.rect.y % 32 == 0:
        # self.num = self.num * 2 + 1
        # if self.rect.y % 32 == 16:
        # self.num = self.num * 2

        print(self.num)

        self.statelist.append(16 * self.num)
        self.prePosx = self.rect.x
        self.prePosy = self.rect.y

        # print("statelist",self.statelist)

        self.freedirection = []
        self.num = 1  # must be 1
        self.counter = self.statelist[1]

    def calculatedistance(self):
        # print("pos",self.ySquare,self.xSquare)
        if self.direction == DOWN:
            while level[self.ySquare + self.num][self.xSquare] != "W":
                self.num += 1

        if self.direction == RIGHT:
            while level[self.ySquare][self.xSquare + self.num] != "W":
                self.num += 1

        if self.direction == UP:
            while level[self.ySquare - self.num][self.xSquare] != "W":
                self.num += 1

        if self.direction == LEFT:
            while level[self.ySquare][self.xSquare - self.num] != "W":
                self.num += 1

        self.num -= 1
    def move(self):

        #if self.counter != 0:
            if self.direction == LEFT:
                self.moveleft(self.dx, self.dy)
                #self.counter -= 1
                # print("left")
                # print(self.counter)
            if self.direction == RIGHT:
                self.moveright(self.dx, self.dy)
                #self.counter -= 1
                # print("right")
                # print(self.counter)
            if self.direction == UP:
                self.moveup(self.dx, self.dy)
                #self.counter -= 1
                # print("up")
                # print(self.counter)
            if self.direction == DOWN:
                self.movedown(self.dx, self.dy)
                #self.counter -= 1
                # print("down")
                # print(self.counter)
            #if self.counter == 0:
                # print(self.statelist)
                self.makebehaviourlist()
                #self.counter = self.statelist[1]

    def moveright(self, dx, dy):
        self.rect.x += dx

    def moveleft(self, dx, dy):
        self.rect.x -= dx

    def moveup(self, dx, dy):
        self.rect.y -= dy

    def movedown(self, dx, dy):
        self.rect.y += dy


class RandomMonster(object):
    def __init__(self, pos, dx, dy):
        randommonsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        # print(pos[0],pos[1])
        self.dx = dx
        self.dy = dy
        self.freedirection = []
        self.statelist = []
        self.counter = 0
        self.direction = -1
        self.num = 1
        self.prePosx = self.rect.x
        self.prePosy = self.rect.y

    def makebehaviourlist(self):  # create new behavior
        self.statelist = []
        self.xSquare = (self.rect.x // 32)
        self.ySquare = (self.rect.y // 32)
        # print(self.xSquare,self.ySquare)
        if level[self.ySquare + 1][self.xSquare] != "W":
            self.direction = DOWN  # Moving down
            self.freedirection.append(self.direction)
        if level[self.ySquare][self.xSquare + 1] != "W":
            self.direction = RIGHT  # Moving right
            self.freedirection.append(self.direction)
        if level[self.ySquare - 1][self.xSquare] != "W":
            self.direction = UP  # Moving up
            self.freedirection.append(self.direction)
        if level[self.ySquare][self.xSquare - 1] != "W":
            self.direction = LEFT  # Moving left
            self.freedirection.append(self.direction)
        # print(self.freedirection)
        number = random.randint(0, len(self.freedirection) - 1)
        self.statelist.append(self.freedirection[number])
        self.direction = self.statelist[0]
        dir = self.direction
        self.calculatedistance()
        self.num = random.randint(1, self.num)
        # print("previous",self.num)
        # print(self.rect.x,self.rect.y)
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 16:  # block bottom left
            if dir == RIGHT or dir == UP:
                self.num = self.num + 0.5
            if dir == LEFT or dir == DOWN:
                self.num = self.num
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:  # block top left
            if dir == RIGHT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == LEFT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 0:  # block top right
            if dir == LEFT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 16:  # block bottom right
            if dir == LEFT or dir == UP:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == DOWN:
                self.num = self.num
        # print("after", self.num)
        self.statelist.append(16 * self.num)
        # print(self.statelist)
        self.freedirection = []
        self.num = 1
        self.counter = self.statelist[1]
        # print((self.direction))

    def makebehaviourlistkeyboard(self, dir):  # create new behavior
        self.statelist = []
        self.xSquare = (self.rect.x // 32)
        self.ySquare = (self.rect.y // 32)

        # print(self.xSquare,self.ySquare)

        self.direction = dir

        # print(self.freedirection)
        # number = random.randint(0,len(self.freedirection)-1)
        self.statelist.append(self.direction)
        # print("Here",self.rect.topleft)
        # self.direction = self.statelist[0]
        self.calculatedistance()
        print("previous:", self.num)
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 16:  # block bottom left
            if dir == RIGHT or dir == UP:
                self.num = self.num + 0.5
            if dir == LEFT or dir == DOWN:
                self.num = self.num
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:  # block top left
            if dir == RIGHT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == LEFT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 0:  # block top right
            if dir == LEFT or dir == DOWN:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == UP:
                self.num = self.num
        if self.rect.x % 32 == 16 and self.rect.y % 32 == 16:  # block bottom right
            if dir == LEFT or dir == UP:
                self.num = self.num + 0.5
            if dir == RIGHT or dir == DOWN:
                self.num = self.num

        # if self.rect.x % 32 == 16:
        # self.num = self.num * 2
        # if self.rect.y % 32 == 0:
        # self.num = self.num * 2 + 1
        # if self.rect.y % 32 == 16:
        # self.num = self.num * 2

        print(self.num)

        self.statelist.append(16 * self.num)
        self.prePosx = self.rect.x
        self.prePosy = self.rect.y

        # print("statelist",self.statelist)

        self.freedirection = []
        self.num = 1  # must be 1
        self.counter = self.statelist[1]

    def calculatedistance(self):
        # print("pos",self.ySquare,self.xSquare)
        if self.direction == DOWN:
            while level[self.ySquare + self.num][self.xSquare] != "W":
                self.num += 1

        if self.direction == RIGHT:
            while level[self.ySquare][self.xSquare + self.num] != "W":
                self.num += 1

        if self.direction == UP:
            while level[self.ySquare - self.num][self.xSquare] != "W":
                self.num += 1

        if self.direction == LEFT:
            while level[self.ySquare][self.xSquare - self.num] != "W":
                self.num += 1

        self.num -= 1

    def drawpath(self):
        point = []
        # print("previous X: :", self.prePosx)
        # print("previous Y: :", self.prePosy)
        if len(self.statelist) >= 2:
            for i in range(0, 1):
                if self.direction == 0:  # down
                    point.append((self.prePosx, self.prePosy))
                    point.append((self.prePosx + 16, self.prePosy))
                    point.append((self.prePosx + 16, self.prePosy + self.statelist[1]))
                    point.append((self.prePosx, self.prePosy + self.statelist[1]))
                if self.direction == 1:  # right
                    point.append((self.prePosx, self.prePosy))
                    point.append((self.prePosx + self.statelist[1], self.prePosy))
                    point.append((self.prePosx + self.statelist[1], self.prePosy + 16))
                    point.append((self.prePosx, self.prePosy + 16))
                if self.direction == 2:  # 2 up
                    point.append((self.prePosx, self.prePosy))
                    point.append((self.prePosx + 16, self.prePosy))
                    point.append((self.prePosx + 16, self.prePosy - self.statelist[1]))
                    point.append((self.prePosx, self.prePosy - self.statelist[1]))
                if self.direction == 3:  # left
                    point.append((self.prePosx, self.prePosy))
                    point.append((self.prePosx - self.statelist[1], self.prePosy))
                    point.append((self.prePosx - self.statelist[1], self.prePosy + 16))
                    point.append((self.prePosx, self.prePosy + 16))
                point.append((self.prePosx, self.prePosy))
            pygame.draw.lines(screen, (0, 125, 255), False, point, 1)

    def move(self):

        if self.counter != 0:
            if self.direction == LEFT:
                self.moveleft(self.dx, self.dy)
                self.counter -= 1
                # print("left")
                # print(self.counter)
            if self.direction == RIGHT:
                self.moveright(self.dx, self.dy)
                self.counter -= 1
                # print("right")
                # print(self.counter)
            if self.direction == UP:
                self.moveup(self.dx, self.dy)
                self.counter -= 1
                # print("up")
                # print(self.counter)
            if self.direction == DOWN:
                self.movedown(self.dx, self.dy)
                self.counter -= 1
                # print("down")
                # print(self.counter)
            if self.counter == 0:
                # print(self.statelist)
                self.makebehaviourlist()
                self.counter = self.statelist[1]

    def moveright(self, dx, dy):
        self.rect.x += dx

    def moveleft(self, dx, dy):
        self.rect.x -= dx

    def moveup(self, dx, dy):
        self.rect.y -= dy

    def movedown(self, dx, dy):
        self.rect.y += dy


def drawGrid():
    points = []
    x = 0
    y = 0

    for i in range(15 * 2):
        points.append((0, y))
        points.append((40 * 32, y))
        y = y + 16
        points.append((40 * 32, y))

    pygame.draw.lines(screen, (0, 255, 255), False, points, 1)
    points = []
    for i in range(40 * 2):
        points.append((x, 0))
        points.append((x, 15 * 32))
        x = x + 16
        points.append((x, 15 * 32))

    pygame.draw.lines(screen, (0, 255, 255), False, points, 1)

    points = []
    x = 0
    y = 0

    for i in range(15):
        points.append((0, y))
        points.append((40 * 32, y))
        y = y + 32
        points.append((40 * 32, y))

    pygame.draw.lines(screen, (255, 0, 0), False, points, 1)
    points = []
    for i in range(40):
        points.append((x, 0))
        points.append((x, 15 * 32))
        x = x + 32
        points.append((x, 15 * 32))

    pygame.draw.lines(screen, (255, 0, 0), False, points, 1)

def replace_C(s, index, character):
    #newLevel[0] = newLevel[0][:2] + "E" + newLevel[0][2+1:]
    s = s[:index] + character + s[index+1:]
    return s


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")  # the headline
screen = pygame.display.set_mode((1280, 480))  # the size of the screen
clock = pygame.time.Clock()
walls = []  # List to hold the walls
player = Player()
spikes = []
flyingspikes = []
squaremonsters = []
trackingmonsters = []
randommonsters = []
coinslist = []
behavelist1 = []
behavelist2 = []
CoinNum = 6

# Holds the level layout in a list of strings.
#level = [
    #"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    #"W                          T           W",
    #"W         WWWWWW   WWW    WWWW  WWWWW  W",
    #"W   WWWW       W   W   WWWW       W    W",
    #"W   W        WWWW  W  WW    W    WW    W",
    #"W WWW  WWWW        WW  W  W WW         W",
    #"W   W     W W      W   W  W    WWW   WWW",
    #"W   W     W W W WWWW   W  W WW W       W",
    #"W   WWW WWW W W W  WWW W WWw W W     W W",
    #"W     W   W   W        W     W WWWWWWW W",
    #"WWW   W   WW WW WWWWW WWWWW    W       W",
    #"W W    F  M     W   W W   WWWWWW   WWWWW",
    #"W W   WWWWWWWWWWW W WWW W   W          W",
    #"W  F  WE    S     W     W         F    W",
    #"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",

level = makingmaze.createNewMazeWithRooms()
level[2] = replace_C (level[2], 2 , "R")
level[7] = replace_C (level[7], 28 , "R")
for i in range(0,CoinNum):
    RanX = random.randint(1,13)
    RanY = random.randint(1,38)
    level[RanX] = replace_C(level[RanX],RanY,"C")


# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))  # thw wall block
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)  # the exit block
        if col == "F":
            FlyingSpike((x, 650))
        if col == "S":
            Spike((x, y + 22))
        if col == "M":
            behavelist1 = ['left', 60, 'up', 60, 'down', 60, 'right', 60]
            squaremonsters.append(SquareMonster((x, y + 16), 3, 2, behavelist1))
        #if col == "T":
            #temp2 = Trackingmonster([x, y + 16], 2, 2)
            #temp2.makebehaviourlist()
            #trackingmonsters.append(temp2)
        if col == "R":
            temp1 = RandomMonster([x, y + 16], 2, 2)
            temp1.makebehaviourlist()
            randommonsters.append(temp1)
        if col == "C":
            Coin(x,y)

        x += 32
    y += 32
    x = 0

KEY_PRESSED = False
running = True
Playerdraw = False
Flag = 0
yPos = (STARTY - 16)//32
xPos = STARTX//32
CollectedCoin = 0
newcoinlist = []
while level[yPos][xPos] == "W":
    STARTY = STARTY - 32
    yPos = (STARTY - 16)//32

player.rect.x = STARTX
player.rect.y = STARTY


while running:
    v = 8
    clock.tick(120)



    for e in pygame.event.get():  # quit function

        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

        #if e.type == pygame.KEYUP:
            #monster = trackingmonsters[0]
            #if e.key == pygame.K_a:
                #monster.makebehaviourlistkeyboard(LEFT)
            #if e.key == pygame.K_d:
                #monster.makebehaviourlistkeyboard(RIGHT)
            #if e.key == pygame.K_w:
                #monster.makebehaviourlistkeyboard(UP)
            #if e.key == pygame.K_s:
                #monster.makebehaviourlistkeyboard(DOWN)

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
    screen.fill((0, 0, 0))  # background color
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)  # wall color
    # create all the coins (before the game loop)
    # make sure the coins ARE NOT in the wall
    # put them in the map
    # Loop through all the coins
    # check to see if coins are touching the player see line 769 for example
    # coin then is eatten by player (erase it somehow) - AFTER the loop

    # that means coin class needs 'state' = 'eatten'
    # change state of coin to 'eatten'
    # player maybe has coin score... and if you are touched by enemy
    # you only lose coins unless you don't have enough...

    # Loop through all the coins
    # if the coin is NOT eatten
    # add that coin to a NEWcoinList
    # coinList = NEWcoinList (all coins that haven't been eatten)
    for coin in coinslist:
        coin.draw()




    for spike in spikes:
        pygame.draw.rect(screen, (0, 255, 0), spike.rect)
    for flyingspike in flyingspikes:
        pygame.draw.rect(screen, (0, 255, 0), flyingspike.rect)
        flyingspike.triggerActive(player, KEY_PRESSED)
        if flyingspike.trigger == True:
            flyingspike.move()

    for squaremonster in squaremonsters:
        squaremonster.move()
        pygame.draw.rect(screen, (0, 255, 150), squaremonster.rect)
        squaremonster.drawborder(screen)

    for trackingmonster in trackingmonsters:
        pygame.draw.rect(screen, (150, 150, 255), trackingmonster.rect)
        trackingmonster.move()

    for randommonster in randommonsters:
        pygame.draw.rect(screen, (150, 150, 150), randommonster.rect)
        randommonster.move()
        # randommonster.drawpath()
    for coin in coinslist:
        if player.rect.collidepoint(coin.rect.x+16, coin.rect.y+16) == True:
            coin.Delete =True
            CollectedCoin = CollectedCoin + 1
        if coin.Delete == False:
            newcoinlist.append(coin)
            coinslist = newcoinlist

    print(CollectedCoin)


    for spike in spikes:
        if player.rect.colliderect(spike.rect):
            player.status = False
    for flyingspike in flyingspikes:
        if player.rect.colliderect(flyingspike.rect):
            player.status = False
    for squaremonster in squaremonsters:
        if player.rect.colliderect(squaremonster.rect):
            player.status = False
    for trackingmonster in trackingmonsters:
        if player.rect.colliderect(trackingmonster.rect):
            player.status = False
    for randommonster in randommonsters:
        if player.rect.colliderect(randommonster.rect):
            player.status = False

    if player.status == True:
        #pygame.draw.rect(screen, (255, 200, 0), player.rect)
        if Flag == 0:
            if key[pygame.K_LEFT]:
                player.drawleft()
                Flag = 1
            else:
                player.drawright()
        if Flag == 1:
            if key[pygame.K_RIGHT]:
                player.drawright()
                Flag = 0
            else:
                player.drawleft()



    elif player.status == False:
        player.rect.left = STARTX
        player.rect.top = STARTY
        # print("dead")
        player.flashcounter = player.flashcounter - 1
        if player.flashcounter % 2 == 1:
            #pygame.draw.rect(screen, (255, 200, 0), player.rect)
            player.drawright()
        elif player.flashcounter == 0:
            player.status = True
            player.flashcounter = 10
    #player.drawborder(screen)
    #print("HERE", STARTX, STARTY)
    #print(level[(STARTY + 16) // 32][STARTX // 32])
    # print(player.flashcounter)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)  # exit color
    # drawGrid()

    pygame.display.flip()  # update the contents of the entire display
    # pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
