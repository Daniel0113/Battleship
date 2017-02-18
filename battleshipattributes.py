#BattleshipAttributes
import pygame, sys, random
from pygame.locals import *

#-----------Class Definitions-----------#
class Button:
    def __init__(self, xPos, yPos, width, height, color, screen):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.rectangle = (xPos, yPos, width, height)
        self.color = color
        self.screen = screen
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rectangle)

    #This will be called in the game loop whenever there is a click event
    def wasClicked(self, clickPos):
        if clickPos[0] > self.xPos and clickPos[0] < self.xPos + self.width:
            if clickPos[1] > self.yPos and clickPos[1] < self.yPos + self.height:
                return True
        return False
    
class GameTile:
    #Constants
    MISS = 0
    HIT = 1
    BLANK = -1

    #Members
    def __init__(self, xPos, yPos, width, height, playerNumber, screen):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.status = self.BLANK
        self.screen = screen
        self.hasBeenClicked = False
        self.color = (255, 255, 255)
        self.isClickableOverride = False
        self.rectangle = (xPos, yPos, width, height)
        self.ship = None
        self.playerNumber = playerNumber

    def wasClicked(self, clickPos):
        if self.isClickable():
            if clickPos[0] > self.xPos and clickPos[0] < self.xPos + self.width:
                if clickPos[1] > self.yPos and clickPos[1] < self.yPos + self.height:
                    self.hasBeenClicked = True
                    if self.ship != None:
                        self.setStatus(self.HIT)
                        self.ship.hit()
                        self.shipDestroyedAnimation()
                    else:
                        self.setStatus(self.MISS)
                    return True
        return False

    def isClickable(self):
        if self.isClickableOverride:
            return False
        return not self.hasBeenClicked
    

    def setStatus(self, status):
        self.status = status

    def setClickable(self, setting):
        self.isClickableOverride = setting

    def draw(self, playerTurn):
        self.color = (225, 225, 225)
        if self.ship != None and (playerTurn == True or self.status == self.HIT or self.status == self.MISS):
            if self.playerNumber == 2:
                value = self.getShip().getLength()
                self.color = (100 + value * 30, 100 + value * 30, 100 + value * 30 )
            if self.playerNumber == 1:
                value = self.getShip().getLength()
                self.color = (0, 100 + value * 30, 0 )
        elif self.playerNumber == 2:
            self.color = (0,191,255)
                
        pygame.draw.rect(self.screen, self.color, self.rectangle)

        if not self.isClickable():
            if self.status == self.HIT:
                pygame.draw.line(self.screen, (255,0,0), (self.xPos, self.yPos), (24 + self.xPos, 24 + self.yPos))
                pygame.draw.line(self.screen, (255,0,0), (24 + self.xPos, self.yPos), (self.xPos, 24 + self.yPos))
            elif self.status == self.MISS:
                pygame.draw.circle(self.screen, (255, 0, 0), (12 + self.xPos,12 + self.yPos), 12, 1)

    def setShip(self, ship):
        self.ship = ship

    def shipDestroyedAnimation(self):
        if self.ship.checkDestroyed():
            font = pygame.font.SysFont("none", 24)
            if self.playerNumber == 1:
                text = font.render("An alien spaceship has been destroyed!", True,(255,255,255))
                taunts = ["'Shouldn't have been bad, aliens!'", "'Easiest kill of my life!'", "'Roger, looks like we got a code E-Z.'", "'Might as well quit now aliens.'", "'Oops, did we do that?'", "'You set sail for fail, aliens!'"]
                text2 = font.render(taunts[random.randint(0, 5)], True, (255,255,255))
            if self. playerNumber == 2:
                text = font.render("A human battleship has been destroyed!", True,(255,255,255))
                taunts = ["'That was easy.'", "'Silly humans.'", "'Earth has some pretty easy hiding spots.'", "'FRESH MEAT!'", "'Space ships are strictly better than boats.'", "'Bottom of the food chain you go!'" ]
                text2 = font.render(taunts[random.randint(0, 5)], True, (255,255,255))
            loopFinished = False
            while loopFinished == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                            loopFinished = True
                self.screen.fill((0, 0, 0))
                self.screen.blit(text, (480/2 - text.get_width() / 2, 640 / 2))
                self.screen.blit(text2, (480/2 - text.get_width() / 2, 50 + 640 / 2))
                pygame.display.update()

    def getShip(self):
        return self.ship
        
class Player:
    #Constants
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    
    def __init__(self, setting, playerNumber, screen):
        self.myTurn = setting
        self.playerNumber = playerNumber
        self.screen = screen
        self.buttonTiles = []
        self.ships = [Ship(5), Ship(4), Ship(3), Ship(3), Ship(2)]
        for i in range(10):
            temp = []
            for j in range(10):
                if self.playerNumber == 1:
                    temp.append(GameTile(120 + 24*i, 40 + 24*j, 24, 24, 1, self.screen))
                else:
                    temp.append(GameTile(120 + 24*i, 360 + 24*j, 24, 24, 2, self.screen))
            self.buttonTiles.append(temp)
        self.distributeShips()
            
    def drawTiles(self):
        for row in self.buttonTiles:
            for tile in row:
                tile.draw(self.myTurn)
                
    def flipTurn(self):
        self.myTurn = not self.myTurn

    def getButtonTiles(self):
        return self.buttonTiles

    def distributeShips(self):
        for ship in self.ships:
            done = False
            while not done:
                row = random.randint(0, 9)
                column = random.randint(0, 9)
                direction = random.randint(self.LEFT, self.DOWN)
                if self.checkIfSectionEmpty(row, column, direction, ship):
                    self.placeShip(row, column, direction, ship)
                    done = True

    def getTurn(self):
        return self.myTurn

    def checkIfSectionEmpty(self, row, column, direction, ship):
        if self.buttonTiles[row][column].getShip() == None:
            if direction == self.LEFT:
                if column - ship.getLength() < 0:
                    return False
                else:
                    for i in range(column, column - ship.getLength(), -1):
                        if self.buttonTiles[row][i].getShip() != None:
                            return False
                    return True
                
            elif direction == self.UP:
                if row - ship.getLength() < 0:
                    return False
                else:
                    for i in range(row, row - ship.getLength(), -1):
                        if self.buttonTiles[i][column].getShip() != None:
                            return False
                    return True
                
            elif direction == self.RIGHT:
                if column + ship.getLength() > 9:
                    return False
                else:
                    for i in range(column, column + ship.getLength()):
                        if self.buttonTiles[row][i].getShip() != None:
                            return False
                    return True
                
            elif direction == self.DOWN:
                if row + ship.getLength() > 9:
                    return False
                else:
                    for i in range(row, row + ship.getLength()):
                        if self.buttonTiles[i][column].getShip() != None:
                            return False
                    return True
        else:
            return False

    def placeShip(self, row, column, direction, ship):
        if direction == self.LEFT:
            for i in range(column, column - ship.getLength(), -1):
                self.buttonTiles[row][i].setShip(ship)
                
        if direction == self.UP:
            for i in range(row, row - ship.getLength(), -1):
                self.buttonTiles[i][column].setShip(ship)
                
        if direction == self.RIGHT:
            for i in range(column, column + ship.getLength(), 1):
                self.buttonTiles[row][i].setShip(ship)
                
        if direction == self.DOWN:
            for i in range(row, row + ship.getLength(), 1):
                self.buttonTiles[i][column].setShip(ship)
    def getPlayerNumber(self):
        return self.playerNumber

    def allShipsDestroyed(self):
        for ship in self.ships:
            for value in ship.getHitList():
                if value == False:
                    return False
        return True
            
        
class Ship:
    def __init__(self, length):
        self.length = length
        self.hitList = [False] * self.length

    def hit(self):
        shipRemoved = False
        iterator = 0
        while shipRemoved == False:
            if self.hitList[iterator] == False:
                self.hitList[iterator] = True
                shipRemoved = True
            iterator += 1

    def getLength(self):
        return self.length

    def checkDestroyed(self):
        for i in self.hitList:
            if i == False:
                return False
        return True
    def getHitList(self):
        return self.hitList

#-----------Function Definitions-----------#

def titleSequence(screen):
    done = False

    ###MAKING THE FONTS
    font = pygame.font.SysFont("none", 24)
    smallFont = pygame.font.SysFont("none", 16)

    ###MAKING THE DIFFERENT TEXTS
    text = smallFont.render("Admiral! we have an enemy fleet in our sights", True, (255,255,255))
    text2 = smallFont.render("We need to get into formation", True,(255,255,255))
    text3 = smallFont.render("Wait a second, Commander! they don't seem human", True,(255,255,255))
    text4 = smallFont.render("They are floating over the water and heading our way",True,(255,255,255))
    continueprompt = smallFont.render("Press ENTER to deploy", True, (255,255,255))

    ###Main loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

        screen.fill((0, 0, 0))
    
    ### MAGIC

        screen.blit(text,(100, 40 - text.get_height() // 2))
        screen.blit(text2,(320- text2.get_width()// 2, 70 - text2.get_height()//2))
        screen.blit(text3,(100, 180 - text3.get_height() // 2))
        screen.blit(text4,(100, 250 - text4.get_height() // 2))

        screen.blit(continueprompt,(320 - continueprompt.get_width()//2 , 440 - continueprompt.get_height()//2))

        pygame.display.update()

def startScreen(screen):

    #Making the start button. FIX MAGIC NUMBERS when you implement constants in bs.py
    startButton = Button(140, 480, 200, 100, (0, 0, 0), screen)

    #Load image and make it a background for start screen
    img = pygame.image.load('battleship6402.jpg')
    screen.blit(img, (0,0))
    
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if startButton.wasClicked(pygame.mouse.get_pos()):
                    finished = True
        startButton.draw()
        pygame.display.update()    
    #Will use the button class above, incorporate a background design.
    #use a draw loop like in battleship.py, and exit the loop when button is pressed so that the function ends and the program moves on.

def drawGrid(screen):
    #First grid
    pygame.draw.line(screen, (0,0,0), (120, 40), (360, 40))
    pygame.draw.line(screen, (0,0,0), (360, 40), (360, 280))
    pygame.draw.line(screen, (0,0,0), (120, 40), (120, 280))
    pygame.draw.line(screen, (0,0,0), (120, 280), (360, 280))

    for i in range(120, 384, 24):
        pygame.draw.line(screen, (0,0,0), (i, 40), (i, 280))
    for i in range(40, 280, 24):
        pygame.draw.line(screen, (0,0,0), (120, i), (360, i))

    #Second grid
    pygame.draw.line(screen, (0,0,0), (120, 360), (360, 360))
    pygame.draw.line(screen, (0,0,0), (360, 360), (360, 600))
    pygame.draw.line(screen, (0,0,0), (120, 360), (120, 600))
    pygame.draw.line(screen, (0,0,0), (120, 600), (360, 600))

    for i in range(120, 384, 24):
        pygame.draw.line(screen, (0,0,0), (i, 360), (i, 600))
    for i in range(360, 600, 24):
        pygame.draw.line(screen, (0,0,0), (120, i), (360, i))
    #pygame.draw.line() function will be used
    #See more at https://www.pygame.org/docs/ref/draw.html#pygame.draw.lines
