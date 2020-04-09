import os
import pygame
import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
STARTX = 32
STARTY = 432


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
        self.dx = dx
        self.dy = dy

    def moveright(self, dx, dy):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # if dx > 0:  # Moving right; Hit the left side of the wall
                self.rect.right = wall.rect.left

    def moveleft(self, dx, dy):
        self.rect.x -= dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # if dx < 0:  # Moving left; Hit the right side of the wall
                self.rect.left = wall.rect.right

    def moveup(self, dx, dy):
        self.rect.y -= dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def movedown(self, dx, dy):
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top


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

behavelist1 = []
behavelist2 = []

# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                          T           W",
    "W         WWWWWW   WWW    WWWW  WWWWW  W",
    "W   WWWW       W   W   WWWW       W    W",
    "W   W        WWWW  W  WW    W    WW    W",
    "W WWW  WWWW        WW  W  W WW         W",
    "W   W     W W      W   W  W    WWW   WWW",
    "W   W     W W W WWWW   W  W WW W       W",
    "W   WWW WWW W W W  WWW W WWw W W     W W",
    "W     W   W   W        W     W WWWWWWW W",
    "WWW   W   WW WW WWWWW WWWWW    W       W",
    "W W    F  M     W   W W   WWWWWW   WWWWW",
    "W W   WWWWWWWWWWW W WWW W   W          W",
    "W  F  WE    S     W     W         F    W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

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
        if col == "T":
            trackingmonsters.append(Trackingmonster((x, y + 16), 1, 1))
        if col == "R":
            temp = RandomMonster([x, y + 16], 2, 2)
            temp.makebehaviourlist()
            randommonsters.append(temp)

        x += 32
    y += 32
    x = 0
KEY_PRESSED = False
running = True
while running:
    v = 8
    clock.tick(120)

    for e in pygame.event.get():  # quit function
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

        if e.type == pygame.KEYUP:
            monster = randommonsters[0]
            if e.key == pygame.K_a:
                monster.makebehaviourlistkeyboard(LEFT)
            if e.key == pygame.K_d:
                monster.makebehaviourlistkeyboard(RIGHT)
            if e.key == pygame.K_w:
                monster.makebehaviourlistkeyboard(UP)
            if e.key == pygame.K_s:
                monster.makebehaviourlistkeyboard(DOWN)

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
        if player.rect.left < trackingmonster.rect.left:
            trackingmonster.moveleft(trackingmonster.dx, trackingmonster.dy)
        if player.rect.right > trackingmonster.rect.right:
            trackingmonster.moveright(trackingmonster.dx, trackingmonster.dy)
        if player.rect.top > trackingmonster.rect.top:
            trackingmonster.movedown(trackingmonster.dx, trackingmonster.dy)
        if player.rect.bottom < trackingmonster.rect.bottom:
            trackingmonster.moveup(trackingmonster.dx, trackingmonster.dy)

    for randommonster in randommonsters:
        pygame.draw.rect(screen, (150, 150, 150), randommonster.rect)
        randommonster.move()
        # randommonster.drawpath()

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
        pygame.draw.rect(screen, (255, 200, 0), player.rect)
    elif player.status == False:
        player.rect.left = 32
        player.rect.top = 432
        # print("dead")
        player.flashcounter = player.flashcounter - 1
        if player.flashcounter % 2 == 1:
            pygame.draw.rect(screen, (255, 200, 0), player.rect)
        elif player.flashcounter == 0:
            player.status = True
            player.flashcounter = 10
    player.drawborder(screen)
    # print(player.flashcounter)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)  # exit color
    # drawGrid()

    pygame.display.flip()  # update the contents of the entire display
    # pygame.display.update()#update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display
