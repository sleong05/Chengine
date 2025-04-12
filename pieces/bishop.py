import pygame as py
from constants import *
from pieces.piece import Piece
from typing import TYPE_CHECKING
from typing import List

class Bishop(Piece):
    def __init__(self, screen: py.display, team: int, chessCoord: tuple[int, int], board: List[List[int]]) -> None:
        super().__init__(screen, team, chessCoord, board, "Bishop")
        self.value = 3
    def getPossibleMoves(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y = self.position[1]

        x = X
        y= Y

        i = 1
        j = 1
        #top right
        while (True):
            #start with searching up right
            x= x+i
            y= y+j
            if (x in range(BOARD_SIZE) and y in range(BOARD_SIZE)) and self.board[x][y] == 0:
                possibleLocations.append(self.getPositionToDraw((x, y)))
            else:
                if self.isOtherTeamAtSpot(x, y, self.color):
                    possibleLocations.append(self.getPositionToDraw((x, y)))
                if i>0 and j>0: #done with going up right. swap to up left
                    i = -1
                    x = X
                    y = Y
                elif i<0 and j>0: #done with going up up left. swap to bottom left
                    j = -1
                    x = X
                    y = Y
                elif i<0 and j<0: #done with going up up left. swap to bottom left
                    i = 1
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
        j = 1
        #top right
        while (True):
            #start with searching up right
            x= x+i
            y= y+j
            if (x in range(BOARD_SIZE) and y in range(BOARD_SIZE)) and self.board[x][y] == 0:
                possibleLocations.append(self.getPositionToDraw((x, y)))
            else:
                possibleLocations.append(self.getPositionToDraw((x, y)))
                if i>0 and j>0: #done with going up right. swap to up left
                    i = -1
                    x = X
                    y = Y
                elif i<0 and j>0: #done with going up up left. swap to bottom left
                    j = -1
                    x = X
                    y = Y
                elif i<0 and j<0: #done with going up up left. swap to bottom left
                    i = 1
                    x = X
                    y = Y
                else: 
                    break
        return possibleLocations

    def getPossibleMovesInPosition(self, X:int, Y:int) -> List[tuple[int, int]]:
        possibleLocations = []

        x = X
        y= Y

        i = 1
        j = 1
        #top right
        while (True):
            #start with searching up right
            x= x+i
            y= y+j
            if (x in range(BOARD_SIZE) and y in range(BOARD_SIZE)) and self.board[x][y] == 0:
                possibleLocations.append(self.getPositionToDraw((x, y)))
            else:
                if self.isOtherTeamAtSpot(x, y, self.color):
                    possibleLocations.append(self.getPositionToDraw((x, y)))
                if i>0 and j>0: #done with going up right. swap to up left
                    i = -1
                    x = X
                    y = Y
                elif i<0 and j>0: #done with going up up left. swap to bottom left
                    j = -1
                    x = X
                    y = Y
                elif i<0 and j<0: #done with going up up left. swap to bottom left
                    i = 1
                    x = X
                    y = Y
                else: 
                    break
                

        return possibleLocations