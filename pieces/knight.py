import pygame as py
from constants import *
from pieces.piece import Piece
from typing import TYPE_CHECKING
from typing import List

class Knight(Piece):
    def __init__(self, screen: py.display, team: int, chessCoord: tuple[int, int], board: List[List[int]]) -> None:
        super().__init__(screen, team, chessCoord, board, "Knight")
        self.value = 3
    def getPossibleMoves(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y= self.position[1]

        #possiblePositions should be 8
        possiblePositions = [(X+2, Y-1), (X+2, Y+1), (X-2, Y-1), (X-2, Y+1), (X+1, Y-2), (X+1, Y+2), (X-1, Y-2), (X-1, Y+2)]

        for move in possiblePositions:
            x = move[0]
            y = move[1]
            if x in range(BOARD_SIZE) and y in range(BOARD_SIZE):
                if self.isOtherTeamAtSpot(x, y, self.color) or self.board[x][y] == 0:
                    possibleLocations.append(self.getPositionToDraw((x, y)))
        return possibleLocations
    
    def getAttackPositions(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y= self.position[1]

        #possiblePositions should be 8
        possiblePositions = [(X+2, Y-1), (X+2, Y+1), (X-2, Y-1), (X-2, Y+1), (X+1, Y-2), (X+1, Y+2), (X-1, Y-2), (X-1, Y+2)]

        for move in possiblePositions:
            x = move[0]
            y = move[1]
            if x in range(BOARD_SIZE) and y in range(BOARD_SIZE):
                possibleLocations.append(self.getPositionToDraw((x, y)))
        return possibleLocations
    