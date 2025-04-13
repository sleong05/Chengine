import threading
from constants import *
from pieces import *
from typing import List
from moveFinder import MoveFinder

class Board:
    def __init__(self) -> None:
        self.content = None
        self.selectedPiece = None
        self.possibleMoveCircles = []
        self.possibleSpecialMoveCircles = []
        self.whiteKing = None
        self.blackKing = None
        self.playersTurn = None
        # for en passant
        self.pawnCanPassant = None
        # move finder for engine
        self.moveFinder = MoveFinder()
        #engine thread for letting engine think
        self.engineThread = None

    def copyInfo(self, boardState: list[list[int|Piece]], whiteKing: King, blackKing: King, playersTurn: int):
        self.content = boardState
        self.whiteKing = whiteKing
        self.blackKing = blackKing
        self.playersTurn = playersTurn
    
    def getAllLegalMoves(self, piece: Piece) -> List[tuple[int, int]]:
        possibleMoves = piece.getPossibleMoves()
        actualMoves = []
        for move in possibleMoves:
            #test if move puts king in check
            x, y = map(lambda v: v//TILE_SIZE, move) #turns the x, y position on the gui into x y in the board
            oldX, oldY = piece.getPosition()
            pieceAtTest = self.content[x][y]
            
            otherTeam = piece.getColor()*-1
            
            myKing = self.blackKing if piece.getColor() == BLACK else self.whiteKing
            #move piece to spot
            self.testMovePiece(x, y, piece)
            attackedTiles = self.getAttackedTiles(otherTeam)
            if (myKing.getPosition() not in attackedTiles): #check if king is now in danger
                #record where possible moves are at so they can be selected later
                self.possibleMoveCircles.append((x, y))
                actualMoves.append((x, y))
            
            self.testMovePiece(oldX, oldY, piece) #move piece back
            #put piece that was at the tested positon back in
            self.content[x][y] = pieceAtTest
        return actualMoves
    
    def testMovePiece(self, X:int, Y:int, piece: Piece) -> None: 
        """tests the moving a piece without actually updating needed variables for an actual move"""
        oldPosition = piece.getPosition()
        self.content[X][Y] = piece
        piece.testChangePosition((X, Y))
        self.content[oldPosition[0]][oldPosition[1]] = 0
    
    def getAttackedTiles(self, color: int) -> set[tuple[int, int]]:
        attackedPositions = set()

        for row in self.content:
            for piece in row:
                if isinstance(piece, Piece) and piece.getColor()==color:
                    attackedPositions.update(piece.getPossibleMoves())