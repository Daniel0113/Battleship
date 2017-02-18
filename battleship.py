import pygame, sys, battleshipattributes
from pygame.locals import *
from battleshipattributes import *

#Initiating Pygame
pygame.init()
        
#Clock and Framerate
clock = pygame.time.Clock()
FPS = 30

#Screen width and height
SCRWIDTH = 480
SCRHEIGHT = 640

#Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


#Setting up the screen
screen = pygame.display.set_mode((SCRWIDTH, SCRHEIGHT))
#screen.fill(WHITE)

player1 = Player(True, 1, screen)
player2 = Player(False, 2, screen)

titleSequence(screen)
startScreen(screen)

upNext = 2
limboMode = False 

font = pygame.font.SysFont("none", 24)
#smallFont = pygame.font.SysFont("none", 16)
text2 = font.render("Click to begin turn", True,(255,255,255))
#continueprompt = smallFont.render("Press ENTER to deploy", True, (0,0,0))

while True:
    #msElapsed = clock.tick(FPS)
    #Checking for game events'
    tileClicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONUP:
            if player2.getTurn() == True:
                for row in player1.getButtonTiles():
                    for tile in row:
                        feels = tile.wasClicked(pygame.mouse.get_pos())
                        if feels == True:
                            tileClicked = True

            if player1.getTurn() == True:        
                for row in player2.getButtonTiles():
                    for tile in row:
                        feels = tile.wasClicked(pygame.mouse.get_pos())
                        if feels == True:
                            tileClicked = True
                            
            if limboMode == True:
                if upNext == 2:
                    player2.flipTurn()
                    upNext = 1
                    limboMode = False
                else:
                    player1.flipTurn()
                    upNext = 2
                    limboMode = False
        
                        
        if tileClicked == True:
            if player1.getTurn() == True:
                player1.flipTurn()
                limboMode = True
            elif player2.getTurn() == True:
                player2.flipTurn()
                limboMode = True

    screen.fill(BLACK)
    player1.drawTiles()
    player2.drawTiles()
    if not limboMode:
        if upNext == 1:
            text = font.render("Player 2's turn!", True, (255,255,255))
        else:
            text = font.render("Player 1's turn!", True, (255,255,255))
        screen.blit(text,(480/2 - text.get_width() / 2, 640 / 2))
    else:
        text = font.render("Player " + str(upNext) + " is up next! Click to continue", True, (255,255,255))
        screen.blit(text,(480/2 - text.get_width() / 2, 640 / 2))
    drawGrid(screen)
    pygame.display.update()

    if player1.allShipsDestroyed():
        loopFinished = False
        font = pygame.font.SysFont("none", 24)
        text = font.render("The humans destroyed all alien spaceships!", True,(255,255,255))
        while loopFinished == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    loopFinished = True
            screen.fill((0,0,0))
            screen.blit(text, (480/2 - text.get_width() / 2, 640 / 2))
            pygame.display.update()
        upNext = 2
        limboMode = False
        player1 = Player(True, 1, screen)
        player2 = Player(False, 2, screen)
    if player2.allShipsDestroyed():
        loopFinished = False
        font = pygame.font.SysFont("none", 24)
        text = font.render("The aliens destroyed all human ships!", True,(255,255,255))
        while loopFinished == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    loopFinished = True
            screen.fill((0,0,0))
            screen.blit(text, (480/2 - text.get_width() / 2, 640 / 2))
            pygame.display.update()
        upNext = 2
        limboMode = False
        player1 = Player(True, 1, screen)
        player2 = Player(False, 2, screen)
        
    
