import sys
import pygame
from constants import *
from board import Board
from pawnPromotion import promotionDialogue
#init
pygame.init()

#Display
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))


# initilize board
board = Board(screen)
board.drawBoard()
board.initilizePieces()
board.drawPieces()
pygame.display.flip()
#Clock for frames
clock = pygame.time.Clock()
#Title
pygame.display.set_caption("Chess Computer")
exit = False
gameOver = False
#end game text
font = pygame.font.Font('freesansbold.ttf', 32)
whiteWins = font.render('White Wins', True, (0, 0, 0), (255, 255, 255))
blackWins = font.render('Black Wins', True, (0, 0, 0), (255, 255, 255))
draw = font.render('Draw', True, (0, 0, 0), (255, 255, 255))
textRect = whiteWins.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
drawTextRect = draw.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
#
pawnPromotion = promotionDialogue(screen, board.content)
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                board.drawBoard()
                gameOver = board.click(event.pos)
            board.drawPieces()
            pygame.display.update()
            #asks board if promotion is needed
            promotionNeeded, position, team = board.isPromotionNeeded()
            if promotionNeeded:
                pawnPromotion.loadImages(team)
                pawnPromotion.showDialogue()
                pygame.display.update()
                #wait till response is picked
                optionSelected = False
                while not optionSelected:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            break
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left click
                                clickPosition = event.pos
                                optionSelected = pawnPromotion.selectOption(clickPosition, position)
                                board.drawBoard()

            board.drawPieces()
            pygame.display.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                board.highLightAttackTiles(WHITE)
            elif event.key == pygame.K_b:
                board.highLightAttackTiles(BLACK)
            board.drawPieces()
            pygame.display.update()

    if gameOver:

        if not board.isAKingInCheck():
            text = draw
            screen.blit(text, drawTextRect)
        else:
            text = whiteWins if gameOver==-1 else blackWins
            screen.blit(text, textRect)
        pygame.display.update()
        
    # set FPS
    clock.tick(60)
pygame.quit()