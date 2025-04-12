from constants import *
import pygame as py
from abc import abstractmethod
import pygame as py
from typing import List
class Piece:
    def __init__(self, screen: py.Surface, teamColor: int, chessCoord: tuple[int, int], board: List[List[int]], piece: str) -> None:
            self.screen = screen
            self.color = teamColor
            self.position =chessCoord
            self.board = board
            self.hasMoved = False
            #load image
            img = py.image.load(f"Chengine/pieceIcons/black{piece}.png").convert_alpha() if self.color==BLACK else py.image.load(f"Chengine/pieceIcons/white{piece}.png").convert_alpha()
            self.image = py.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.piece = piece
    
    def getPositionToDraw(self, chessCoord: tuple[int, int]) -> tuple[int, int]:
        return (chessCoord[0]*TILE_SIZE, chessCoord[1]*TILE_SIZE)
    
    def draw(self) -> None:
        self.screen.blit(self.image, self.getPositionToDraw(self.position))

    @abstractmethod
    def getPossibleMoves(self) -> List[tuple[int, int]]:
         """Finds all possible moves of the type of piece"""
         pass
    
    @abstractmethod
    def getAttackPositions(self) -> List[tuple[int, int]]:
         """Finds all possible atacked squares of the type of piece"""
         pass

    def isOtherTeamAtSpot(self, X: int, Y: int, color: int) -> bool:
        """Checks if there is a piece of the opposit team at a location"""
        return X in range(BOARD_SIZE) and Y in range(BOARD_SIZE) and isinstance(self.board[X][Y], Piece) and self.board[X][Y].getColor() == self.color*-1
    
    def changePosition(self, newPosition: tuple[int, int]) -> None:
        """Changes internal position of piece. Must be redrawn to update"""
        self.position = newPosition
        self.hasMoved = True
    
    def testChangePosition(self, newPosition: tuple[int, int]) -> None:
        """Changes internal position of piece for testing checks. does not count as a actual move"""
        self.position = newPosition

    def getPosition(self) -> tuple[int, int]:
        return self.position
    
    def getColor(self) -> int:
        return self.color
    
    def getPiece(self) -> str:
         return self.piece

    def findMyKing(self):
         for row in self.board:
              for piece in row:
                
                if piece != 0 and piece.getPiece() == "King" and piece.getColor() == self.getColor():
                    return piece
    
    def getValue(self) -> int:
        return self.value