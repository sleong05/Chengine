from pieces.pawn import Pawn
from pieces.piece import Piece
import random
import time
from constants import *
from weights import *
from pieceTheorizer import PieceTheorizer

class MoveFinder:
    def __init__(self) -> None:
        self.weights = {}
        self.whiteAttackTiles = None
        self.blackAttackTiles = None
        self.possibleMoves = None
        self.board = None
        self.team = WHITE
        self.pieceTheorizer = PieceTheorizer()

        
    
    def feedData(self, board: list[list[Piece|int]], team: int, possibleMoves: list[tuple[Piece, tuple[int, int]]], whiteAttack: set[tuple[int, int]], blackAttack: set[tuple[int, int]]) -> None:
        """ Method to mass feed all info to the move finder """
        self.board = board
        self.team = team
        self.possibleMoves = possibleMoves
        self.whiteAttackTiles = whiteAttack
        self.blackAttackTiles = blackAttack

    def getBestMove(self, bestMoveContainer: list) -> tuple[Piece, tuple[int, int]]: 
        """ LOAD DATA BEFORE"""

        # SIMULATE THINKGING #TODO REMOVE LATER
        i = 0
        while i < 20000000:
            i+=1

        self.weights = {}
        #assign weights
        for move in self.possibleMoves:
            weight = self.evaluateMove(move)
            self.weights[move] = weight


        fiveBestMoves = self.getFiveBestMoves()
        bestMove = None
        bestMoveValue = -999999999
        print("------Five Best--------")
        for move in fiveBestMoves:
            piece, position = move
            print(f"{piece} at {piece.getPosition()} to {position}: score {self.weights[move]}")
            if self.weights[move] > bestMoveValue:
                bestMoveValue = self.weights[move]
                bestMove = move

        
        bestMoveContainer.append(bestMove)

    def getFiveBestMoves(self):
        fiveBestMoves = []
        for move in self.possibleMoves:
            if len(fiveBestMoves) < 5:
                fiveBestMoves.append(move)
            else:
                worstMoveWeight = 99999999
                worstMove = None

                for bestMove in fiveBestMoves:
                    if worstMoveWeight > self.weights[bestMove]:
                        worstMoveWeight = self.weights[bestMove]
                        worstMove = bestMove

                if self.weights[worstMove] < self.weights[move]:
                    fiveBestMoves.remove(worstMove)
                    fiveBestMoves.append(move)
        return fiveBestMoves

    def evaluateMove(self, move: tuple[Piece, tuple[int, int]]) -> int:
        score = 0
        piece, position = move
        x, y = position
        curX, curY = piece.getPosition()
        #evaluate current Position
        score += self.underAttack(curX, curY, piece)
        #TODO
        #evaluate future position
        score += self.canTakePiece(x, y, piece)
        score += self.moveInDanger(x, y, piece)
        
        #TODO
        #theory man
        pieceEvaluation = self.pieceTheorizer.evaluatePiece(piece, x, y, curX, curY, self.board)
        
        score += pieceEvaluation
        return score

    """ WEIGTHING METHODS """

    def underAttack(self, curX:int, curY:int, piece: Piece) -> int:
        """ returns a positive bias if attacked else negative """
        if isinstance(piece, Pawn): # dont really care about pawns being attacked
            return .5
        valueofPiece = piece.getValue()
        #piece is defended
        if (curX, curY) in self.whiteAttackTiles and (curX, curY) in self.blackAttackTiles: #TODO MUST FIX SO THAT CAN FIGURE OUT APPROPRIETE DANGER
            return valueofPiece - 2 # is defended. just check if its actuall important
        
        return valueofPiece if (curX, curY) in self.blackAttackTiles else 0

    def canTakePiece(self, x:int, y:int, piece: Piece) -> int:
        """ Value of taking a piece """
        # is there a piece at location?
        if not isinstance(self.board[x][y], Piece):
            return 0
        #hanging piece case
        if (x, y) not in self.blackAttackTiles:
            return self.board[x][y].getValue() + .5
        
        # trade case
        myWorth = piece.getValue()
        enemyWorth = self.board[x][y].getValue()

        # equal trade
        if myWorth == enemyWorth:
            return EQUALTRADE
        
        diff = enemyWorth - myWorth

        return diff #TODO ASSESS IF THIS A REASONABLE WAY TO DO IT
    
    def moveInDanger(self, x: int, y:int, piece:Piece) -> int:
        if self.board[x][y] != 0: #this is a capture and will be assessed elsewhere
            return 0
        if (x, y) in self.blackAttackTiles  and (x, y) in self.whiteAttackTiles: #TODO evaluate if this messses stuff
            return MOVEINTODANGERTRUE+4 #basically a slight weight against just in general
        return MOVEINTODANGERTRUE if (x, y) in self.blackAttackTiles else MOVEINTODANGERFALSE

    """ END WEIGTHING METHODS """

    def pickRandomMove(self, possibleMoves: list[tuple[Piece,tuple[int, int]]]) -> tuple[Piece, tuple[int, int]]|list:
        ranNum = random.randint(0, len(possibleMoves)-1)
        print(f" random move selected to be: {possibleMoves[ranNum]}")
        return [] if not possibleMoves else possibleMoves[ranNum]

    def getPieces(self, team: int, board: list[list[Piece|int]]) -> list[Piece]: #depricate?
        piecesOfTeam = []
        for row in board:
            for tile in row:
                if isinstance(tile, Piece) and tile.getColor() == team:
                    piecesOfTeam.append(tile)

        return piecesOfTeam
        