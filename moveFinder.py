from pieces.piece import Piece
import random
import time

class MoveFinder:
    def __init__(self) -> None:
        pass

    def getBestMove(self, board: list[list[Piece|int]], team: int, possibleMoves: list[tuple[Piece, tuple[int, int]]], bestMoveContainer: list) -> tuple[Piece, tuple[int, int]]: 
        #simulate thinking

        num = random.randint(10000000, 20000000)
        i= 0
        while i<num:
            i += 1

        bestMoveContainer.append(self.pickRandomMove(possibleMoves))

    def pickRandomMove(self, possibleMoves: list[tuple[Piece,tuple[int, int]]]) -> tuple[Piece, tuple[int, int]]:
        ranNum = random.randint(0, len(possibleMoves)-1)
        print(f" random move selected to be: {possibleMoves[ranNum]}")
        return possibleMoves[ranNum]


    def getPieces(self, team: int, board: list[list[Piece|int]]) -> list[Piece]:
        piecesOfTeam = []
        for row in board:
            for tile in row:
                if isinstance(tile, Piece) and tile.getColor() == team:
                    piecesOfTeam.append(tile)

        return piecesOfTeam
        