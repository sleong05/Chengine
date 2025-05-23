from pieces.piece import Piece

from constants import *
from decisionMakers.weights import *

from decisionMakers.components.dangerChecker import DangerChecker
from decisionMakers.components.hangingPieceTaker import pieceTrader
from decisionMakers.components.pieceTheorizer import PieceTheorizer

class MoveFinder:
    def __init__(self) -> None:
        self.weights = {}
        self.whiteAttackTiles = None
        self.blackAttackTiles = None
        self.possibleMoves = None
        self.otherTeamsMoves = None
        self.board = None
        self.team = WHITE
        self.pieceTheorizer = PieceTheorizer()
        self.dangerChecker = DangerChecker()
        self.hangingPieceTaker = pieceTrader()
        
    
    def feedData(self, board: list[list[Piece|int]], team: int, possibleMoves: list[tuple[Piece, tuple[int, int]]], whiteAttack: set[tuple[int, int]], blackAttack: set[tuple[int, int]], otherTeamMoves: list[Piece, tuple[int, int]]) -> None:
        """ Method to mass feed all info to the move finder """
        self.board = board
        self.team = team
        self.possibleMoves = possibleMoves
        self.otherTeamsMoves = otherTeamMoves
        #in the context of whiteattack/blackattack. white is always the player going
        if team==WHITE:
            self.whiteAttackTiles = whiteAttack
            self.blackAttackTiles = blackAttack
        else:
            self.whiteAttackTiles = blackAttack
            self.blackAttackTiles = whiteAttack

    def getBestMove(self, bestMoveContainer: list) -> tuple[Piece, tuple[int, int]]: 
        """ LOAD DATA BEFORE"""
        # SIMULATE THINKGING #TODO REMOVE LATER
        if SHOWMOVES:
            i = 0
            while i < SPEED * 10000000:
                i+=1
            
        self.weights = {}
        #assign weights
        for move in self.possibleMoves:
            weight = self.evaluateMove(move)
            self.weights[move] = weight

        fiveBestMoves = self.getBestMoveForEachPiece()

        for bestMove in fiveBestMoves:
            bestMoveContainer.append(bestMove)

    def evaluateMove(self, move: tuple[Piece, tuple[int, int]]) -> int:
        score = 0
        piece, position = move
        x, y = position
        curX, curY = piece.getPosition()
        
        score += self.dangerChecker.evaluateDanger(self.otherTeamsMoves, self.whiteAttackTiles, piece)
        score += self.dangerChecker.moveInDanger(x, y, piece, self.board, self.blackAttackTiles)

        score += self.hangingPieceTaker.canTakePiece(x, y, piece, self.board, self.blackAttackTiles)

        pieceEvaluation = self.pieceTheorizer.evaluatePiece(piece, x, y, curX, curY, self.board)
        
        score += pieceEvaluation
        return score
    
    def getBestMoves(self):
        fiveBestMoves = []
        for move in self.possibleMoves:
            if len(fiveBestMoves) < WIDTH:
                fiveBestMoves.insert(0, move)
            else:
                worstMoveWeight = 99999999
                worstMove = None

                for bestMove in fiveBestMoves:
                    if worstMoveWeight > self.weights[bestMove]:
                        worstMoveWeight = self.weights[bestMove]
                        worstMove = bestMove

                if self.weights[worstMove] < self.weights[move]:
                    fiveBestMoves.remove(worstMove)
                    fiveBestMoves.insert(0, move)
        return fiveBestMoves
    
    def getBestMoveForEachPiece(self) -> dict[Piece: int]:
        pieceValues = {}
        pieceMoves = {}
        for move in self.weights:
            piece, position = move

            if piece not in pieceValues:
                pieceMoves[piece] = move
                pieceValues[piece] = self.weights[move]

            else:
                if pieceValues[piece] < self.weights[move]:
                    pieceMoves[piece] = move
                    pieceValues[piece] = self.weights[move]

        #sort dic
        sortedPieceValues = {k: v for k, v in sorted(pieceValues.items(), key=lambda item: item[1], reverse=True)}
        width = 0
        bestMoves = []
        for piece in sortedPieceValues: 
            if width == WIDTH:
                break

            bestMoves.append(pieceMoves[piece])
            width += 1
        return bestMoves