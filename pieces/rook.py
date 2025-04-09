import pygame as py
from constants import *
from pieces.piece import Piece
from typing import List

class Rook(Piece):
    def __init__(self, screen: py.display, team: int, chessCoord: tuple[int, int], board: List[List[int]]) -> None:
        super().__init__(screen, team, chessCoord, board, "Rook")
    
    def getPossibleMoves(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y = self.position[1]

        x = X
        y= Y

        i = 1
        j = 0
        #top right
        while (True):
            #start with searching right
            x= x+i
            y= y+j
            if (x in range(BOARD_SIZE) and y in range(BOARD_SIZE)) and self.board[x][y] == 0:
                possibleLocations.append(self.getPositionToDraw((x, y)))
            else:
                if self.isOtherTeamAtSpot(x, y, self.color):
                    possibleLocations.append(self.getPositionToDraw((x, y)))
                if i>0 and j==0: #done with going  right. swap to left
                    i = -1
                    x = X
                    y = Y
                elif i<0 and j==0: #done with going left. swap to going up
                    j = 1
                    i = 0
                    x = X
                    y = Y
                elif i==0 and j>0: #done with going up. swap to going down
                    j = -1
                    x = X
                    y = Y
                else: 
                    break              

        return possibleLocations
    
    def getAttackPositions(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y = self.position[1]

        x = X
        y= Y

        i = 1
        j = 0
        #top right
        while (True):
            #start with searching right
            x= x+i
            y= y+j
            if (x in range(BOARD_SIZE) and y in range(BOARD_SIZE)) and self.board[x][y] == 0:
                possibleLocations.append(self.getPositionToDraw((x, y)))
            else:
                possibleLocations.append(self.getPositionToDraw((x, y)))
                if i>0 and j==0: #done with going  right. swap to left
                    i = -1
                    x = X
                    y = Y
                elif i<0 and j==0: #done with going left. swap to going up
                    j = 1
                    i = 0
                    x = X
                    y = Y
                elif i==0 and j>0: #done with going up. swap to going down
                    j = -1
                    x = X
                    y = Y
                else: 
                    break              

        return possibleLocations