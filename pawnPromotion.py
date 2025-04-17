import pygame as py
from constants import *
from typing import List
from pieces.piece import Piece
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
class promotionDialogue():
    def __init__(self, screen: py.display, board: List[List[Piece]]) -> None:
        self.screen = screen
        self.board = board
        #images for promotion
        self.promotionRook = None
        self.promotionKnight = None
        self.promotionBishop = None
        self.promotionQueen = None

        #team of dialogue
        self.team = None
    def loadImages(self, team:int) -> None:
        TILE_SCALING = 1
        self.team = team
        team = "black" if team == BLACK else "white"

        img = py.image.load(f"pieces/pieceIcons/{team}Rook.png").convert_alpha()
        self.promotionRook = py.transform.scale(img, (TILE_SIZE*TILE_SCALING, TILE_SIZE*TILE_SCALING))

        img = py.image.load(f"pieces/pieceIcons/{team}Knight.png").convert_alpha()
        self.promotionKnight = py.transform.scale(img, (TILE_SIZE*TILE_SCALING, TILE_SIZE*TILE_SCALING))

        img = py.image.load(f"pieces/pieceIcons/{team}Bishop.png").convert_alpha()
        self.promotionBishop = py.transform.scale(img, (TILE_SIZE*TILE_SCALING, TILE_SIZE*TILE_SCALING))

        img = py.image.load(f"pieces/pieceIcons/{team}Queen.png").convert_alpha()
        self.promotionQueen = py.transform.scale(img, (TILE_SIZE*TILE_SCALING, TILE_SIZE*TILE_SCALING))

    def showDialogue(self) -> None:
        for tile in range(4):
            py.draw.rect(
                    self.screen,
                    (230, 230, 230),
                    (tile * TILE_SIZE*2, 3.5 * TILE_SIZE, TILE_SIZE*2, TILE_SIZE*2)
                )
            py.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (tile * TILE_SIZE*2, 3.5 * TILE_SIZE, TILE_SIZE*2, TILE_SIZE*2),
                    width=2
                )
            
        self.screen.blit(self.promotionKnight, (1 * TILE_SIZE*2-TILE_SIZE*1.5, 4 * TILE_SIZE))
        self.screen.blit(self.promotionBishop, (2 * TILE_SIZE*2-TILE_SIZE*1.5, 4 * TILE_SIZE))
        self.screen.blit(self.promotionRook, (3 * TILE_SIZE*2-TILE_SIZE*1.5, 4 * TILE_SIZE))
        self.screen.blit(self.promotionQueen, (4 * TILE_SIZE*2-TILE_SIZE*1.5, 4 * TILE_SIZE))

    def selectOption(self, positionOfClick: tuple[int, int], positionToInsert: tuple[int, int]) -> bool:
        x, y = positionOfClick
        X, Y = positionToInsert
        if x < 125 and y > 215 and y < 340:
            knight = Knight(self.screen, self.team, (X, Y), self.board)
            self.board[X][Y] = knight
            return True
        elif x < 250 and y > 215 and y < 340:
            bishop = Bishop(self.screen, self.team, (X, Y), self.board)
            self.board[X][Y] = bishop
            return True
        elif x < 375 and y > 215 and y < 340:
            rook = Rook(self.screen, self.team, (X, Y), self.board)
            self.board[X][Y] = rook
            return True
        elif x < 500 and y > 215 and y < 340:
            queen = Queen(self.screen, self.team, (X, Y), self.board)
            self.board[X][Y] = queen
            return True

        return False