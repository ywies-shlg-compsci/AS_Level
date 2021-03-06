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

color = (0,0,0)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

P_SIZE = 16
C_SIZE = 16
S_SIZE = 7

xPosition = 0
yPosition = 0
class Coin(object):

    def __init__(self,x,y):
        coinslist.append(self)
        self.rect = pygame.Rect(x, y,C_SIZE,C_SIZE)
        self.Delete = False

        self.image_coin = pygame.transform.scale(pygame.image.load('coin.png'), (C_SIZE, C_SIZE))

    def draw(self):
        #pygame.draw.circle(screen,(255,200,0),(self.rect.x+16,self.rect.y+16),C_SIZE)
        screen.blit(self.image_coin, (self.rect.x, self.rect.y))

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
        screen.blit(self.animateMoveRight[animationindex], (self.rect.x, self.rect.y))

    def drawleft(self):
        screen.blit(self.animateMoveLeft[animationindex], (self.rect.x, self.rect.y))


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
        self.image_wall = pygame.transform.scale(pygame.image.load('wall.png'), (32, 32))
    def draw(self):
        screen.blit(self.image_wall, (self.rect.x, self.rect.y))

class Spike(object):
    def __init__(self, pos):
        spikes.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], S_SIZE, S_SIZE)
        self.image_spike = pygame.transform.scale(pygame.image.load('spike2.png'), (S_SIZE, S_SIZE))

    def draw(self):
        screen.blit(self.image_spike, (self.rect.x, self.rect.y))



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
        self.image_monster = pygame.transform.scale(pygame.image.load('monster.png'), (16, 16))
    def draw(self):
        screen.blit(self.image_monster, (self.rect.x, self.rect.y))

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
        if len(self.freedirection) > 0:
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

def calculatehalls(level):
    hallNum = 0
    halllist = []
    for i in range(0,15-2):
        for j in range(0,40-2):
            if level[i][j] == "W" and level[i][j+2] == "W" and level[i][j+1] ==" ":
                hallNum = hallNum +1
                halllist.append((i,j+1))
            if level[i][j] == "W" and level[i+2][j] == "W" and level[i+1][j] ==" ":
                hallNum = hallNum +1
                halllist.append((i+1,j))

    print(halllist)
    return halllist

def makingspikes(level):
    freehallist = calculatehalls(level)
    for i in range(spikeNum):
        j = random.randint(0,len(freehallist)-1)
        RanX = freehallist[j][0]
        RanY = freehallist[j][1]
        level[RanX] = replace_C(level[RanX], RanY, "S")




def makingmonster(level):
    for i in range(0,MonsterNum):
        RanX = random.randint(1, 13)
        RanY = random.randint(1, 38)
        level[RanX] = replace_C (level[RanX], RanY , "R")

def makingcoins(level):
    for i in range(0,CoinNum):
        RanX = random.randint(1,13)
        RanY = random.randint(1,38)
        if level[RanX+1][RanY] == "W" and level[RanX][RanY+1] == "W" and level[RanX][RanY-1] == "W" and level[RanX-1][RanY] == "W":
            print("coin error")
        else:
            level[RanX] = replace_C(level[RanX],RanY,"C")

def CreateMonsterInMaze(level):
    # Parse the level string above. W = wall, E = exit
    global end_rect, xPosition, yPosition
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))  # thw wall block
            if col == "E":
                end_rect = pygame.Rect(x, y, 32, 32)  # the exit block
                xPosition = x
                yPosition = y
            if col == "F":
                FlyingSpike((x, 650))
            if col == "S":
                SpikeOffset = 25
                RandomNum = random.randint(0,3)
                if RandomNum == 0:
                    Spike((x, y + SpikeOffset))
                if RandomNum == 1:
                    Spike((x + SpikeOffset,y))
                if RandomNum == 2:
                    Spike((x + SpikeOffset, y + SpikeOffset))
                if RandomNum == 3:
                    Spike((x , y))


            if col == "M":
                behavelist1 = ['left', 60, 'up', 60, 'down', 60, 'right', 60]
                squaremonsters.append(SquareMonster((x, y + 16), 3, 2, behavelist1))
            # if col == "T":
            # temp2 = Trackingmonster([x, y + 16], 2, 2)
            # temp2.makebehaviourlist()
            # trackingmonsters.append(temp2)
            if col == "R":
                temp1 = RandomMonster([x, y + 16], 2, 2)
                temp1.makebehaviourlist()
                randommonsters.append(temp1)
            if col == "C":
                Coin(x, y)

            x += 32
        y += 32
        x = 0
    return end_rect,xPosition,yPosition

def drawtext(window,content,x,y):
    font = pygame.font.SysFont('Arial', 40)
    text = font.render(content,1,color)
    window.blit(text,(x,y))

def drawtextblack(window,content,x,y):
    font = pygame.font.SysFont('Arial', 40)
    text = font.render(content,1,black)
    window.blit(text,(x,y))

def drawtextwhite(window,content,x,y):
    font = pygame.font.SysFont('Arial', 40)
    text = font.render(content,1,white)
    window.blit(text,(x,y))


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
SOUND_DIRECTORY = '/Users/hankli/PycharmProjects/mazegame /AS_Level/'
pygame.mixer.music.load(SOUND_DIRECTORY + "bgm.wav")
pygame.mixer.music.play(-1)


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
CoinNum = 1
TotalCoinNum = CoinNum
MonsterNum = 1
levelNum = 1
playerlives = 3
spikeNum = 10
CollectedCoin = 0
level = makingmaze.createNewMazeWithRooms()
makingmonster(level)
makingcoins(level)
makingspikes(level)
CreateMonsterInMaze(level)

yPos = (STARTY - 16)//32
xPos = STARTX//32
while level[yPos][xPos] == "W":
    STARTY = STARTY - 32
    yPos = (STARTY - 16)//32

player.rect.x = STARTX
player.rect.y = STARTY
#print(level[13][37])
#print(xPosition,yPosition)
xIndex = xPosition//32
yIndex = (yPosition)//32#position of the end_rect
#print(yIndex,xIndex)

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

KEY_PRESSED = False
running = True
Playerdraw = False
Flag = 0
animationindex = 0
gameover = True
gameState = "start"
while running:
    clock.tick(120)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    if gameState == "start":
        screen.fill((0, 0, 0))
        drawtextwhite(screen, "Press S To Start The Game", 0, 0)
        drawtextwhite(screen, "Press Q To Quit The Game", 0, 32)
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            gameover = False
            gameState = "playing"
        if key[pygame.K_q]:
            running = False

    if gameState == "gameover":
        screen.fill((0, 0, 0))
        drawtextwhite(screen, "Game Over", 0, 0)
        drawtextwhite(screen, "Press S To Start The Game", 0, 32)
        drawtextwhite(screen, "Press Q To Quit The Game", 0, 64)
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            playerlives = 3
            gameover = False
            CollectedCoin =0
            gameState = "playing"
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
            CoinNum = 1
            TotalCoinNum = CoinNum
            MonsterNum = 1
            levelNum = 1
            spikeNum = 10
            level = makingmaze.createNewMazeWithRooms()
            player.rect.left = STARTX
            player.rect.top = STARTY
            yPos = (STARTY - 16) // 32
            xPos = STARTX // 32
            playerlives = playerlives
            while level[yPos][xPos] == "W":
                STARTY = STARTY - 32
                yPos = (STARTY - 16) // 32
            player.rect.x = STARTX
            player.rect.y = STARTY
            makingmonster(level)
            makingcoins(level)
            makingspikes(level)
            CreateMonsterInMaze(level)

        if key[pygame.K_q]:
            running = False

    pygame.display.flip()
    while not gameover:
        v = 8
        clock.tick(120)


        if (level[yIndex][xIndex - 1] == "W" and level[yIndex - 1][xIndex] == "W") or (level[yIndex][xIndex - 2] == "W" and level[yIndex - 1][xIndex] == "W" and level[yIndex - 1][xIndex-1] == "W") or (level[yIndex][xIndex - 1] == "W" and level[yIndex - 1][xIndex-1] == "W" and level[yIndex -2][xIndex] == "W") or level[1][38]== "S" or level[1][38]== "R" or level[1][37]== "S" or level[1][37]== "R":
            print("error")
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
            spikeNum = spikeNum
            CoinNum = CoinNum
            MonsterNum = MonsterNum
            levelNum = levelNum
            level = makingmaze.createNewMazeWithRooms()
            player.rect.left = STARTX
            player.rect.top = STARTY
            yPos = (STARTY - 16) // 32
            xPos = STARTX // 32
            playerlives = playerlives
            while level[yPos][xPos] == "W":
                STARTY = STARTY - 32
                yPos = (STARTY - 16) // 32
            player.rect.x = STARTX
            player.rect.y = STARTY
            makingmonster(level)
            makingcoins(level)
            makingspikes(level)
            CreateMonsterInMaze(level)



        for e in pygame.event.get():  # quit function

            if e.type == pygame.QUIT:
                running = False
                gameover = True


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
        if key[pygame.K_SPACE]:
            v = 16
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

        # Draw the scene
        screen.fill((0, 0, 0))  # background color
        for wall in walls:
            wall.draw()

        for coin in coinslist:
            coin.draw()

        for spike in spikes:
            spike.draw()

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
            #pygame.draw.rect(screen, (150, 150, 150), randommonster.rect)
            randommonster.draw()
            randommonster.move()
            # randommonster.drawpath()
        for coin in coinslist:
            if player.rect.collidepoint(coin.rect.x, coin.rect.y) == True or player.rect.collidepoint(coin.rect.x+16, coin.rect.y) == True or player.rect.collidepoint(coin.rect.x, coin.rect.y+16) == True or player.rect.collidepoint(coin.rect.x+16, coin.rect.y+16) == True:
                coin_sound = pygame.mixer.Sound(SOUND_DIRECTORY + "coin.wav")
                pygame.mixer.Sound.play(coin_sound)
                coin.Delete =True
                CollectedCoin = CollectedCoin + 1
        newcoinlist = []
        for coin in coinslist:
            if coin.Delete == False:
                newcoinlist.append(coin)
        coinslist = newcoinlist

        if CollectedCoin < TotalCoinNum :
            color = red
        else:
            color = green

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
        if CollectedCoin < TotalCoinNum:
            pygame.draw.rect(screen, red, end_rect)  # exit color
        else:
            pygame.draw.rect(screen, green, end_rect)  # exit color

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
            player.flashcounter = player.flashcounter - 1
            if player.flashcounter % 2 == 1:
                #pygame.draw.rect(screen, (255, 200, 0), player.rect)
                player.drawright()
            elif player.flashcounter == 0:
                player.status = True
                playerlives = playerlives - 1
                player.flashcounter = 10
        if animationindex < 3:
            animationindex = animationindex + 1
        elif animationindex == 3:
            animationindex = 0

        if playerlives == 0:
            gameState = "gameover"
            gameover = True
        #player.drawborder(screen)
        #print("HERE", STARTX, STARTY)
        #print(level[(STARTY + 16) // 32][STARTX // 32])
        # print(player.flashcounter)

        # drawGrid()
        drawtext(screen,"lives:", 0, 0)
        drawtext(screen, str(playerlives),80 , 0)
        drawtextblack(screen, "LEVEL", 0, 448)
        drawtextblack(screen,str(levelNum),96, 448)






        # pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
        if player.rect.colliderect(end_rect):
            if CollectedCoin == TotalCoinNum:
                levelup_sound = pygame.mixer.Sound(SOUND_DIRECTORY + "levelup.wav")
                pygame.mixer.Sound.play(levelup_sound)
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
                CoinNum = CoinNum + 1
                TotalCoinNum = TotalCoinNum + CoinNum
                MonsterNum = MonsterNum + 2
                levelNum = levelNum + 1
                level = makingmaze.createNewMazeWithRooms()
                player.rect.left = STARTX
                player.rect.top = STARTY
                yPos = (STARTY - 16) // 32
                xPos = STARTX // 32
                playerlives = playerlives + 2
                while level[yPos][xPos] == "W":
                    STARTY = STARTY - 32
                    yPos = (STARTY - 16) // 32

                player.rect.x = STARTX
                player.rect.y = STARTY
                makingmonster(level)
                makingcoins(level)
                freehallist = calculatehalls(level)
                if spikeNum + 5 < len(freehallist):
                    spikeNum = spikeNum +5
                else:
                    spikeNum = len(freehallist)
                makingspikes(level)
                CreateMonsterInMaze(level)
            else:
                color = red
                drawtext(screen, "Please collect all the coins!", 640, 0)

        pygame.display.flip()  # update the contents of the entire display
