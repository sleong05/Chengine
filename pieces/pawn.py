import pygame
from constants import *
from pieces.piece import Piece
from typing import TYPE_CHECKING
from typing import List

class Pawn(Piece):
    def __init__(self, screen: pygame.Surface, team: int, chessCoord: tuple[int, int], board: List[List[int]]) -> None:
        super().__init__(screen, team, chessCoord, board, "Pawn")
        self.value = 1
    def getPossibleMoves(self) -> List[tuple[int, int]]:
        possibleLocations = []
        X = self.position[0]
        Y= self.position[1]

        # can move 1 space
        if  Y+self.color in range(BOARD_SIZE) and self.board[X][Y+self.color] == 0:
            possibleLocations.append(self.getPositionToDraw((X, Y+self.color)))
        
            #can move 2 spaces off start
            if not self.hasMoved and  Y+self.color*2 in range(BOARD_SIZE) and self.board[X][Y+ self.color*2] == 0:
                possibleLocations.append(self.getPositionToDraw((X, Y+self.color*2)))

        # can capture
        
        #left
        if self.isOtherTeamAtSpot(X-1, Y+self.color, self.color):
                possibleLocations.append(self.getPositionToDraw((X-1, Y+ self.color)))

            #right
        if self.isOtherTeamAtSpot(X+1, Y+self.color, self.color):
                possibleLocations.append(self.getPositionToDraw((X+1, Y+ self.color)))
                
        return possibleLocations
    
    def getAttackPositions(self) -> List[tuple[int, int]]:
        possibleAttacks = []
        X = self.position[0]
        Y= self.position[1]
        if Y+self.color in range(BOARD_SIZE):
            #left
            if X-1 in range(BOARD_SIZE):
                    possibleAttacks.append(self.getPositionToDraw((X-1, Y+ self.color)))

                #right
            if X+1 in range(BOARD_SIZE):
                    possibleAttacks.append(self.getPositionToDraw((X+1, Y+ self.color)))

        return possibleAttacks