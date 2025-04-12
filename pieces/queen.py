from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.piece import Piece
from typing import List
import pygame as py
class Queen(Bishop, Rook):
    def __init__(self, screen: py.display, team: int, chessCoord: tuple[int, int], board: List[List[int]]) -> None:
        Piece.__init__(self, screen, team, chessCoord, board, "Queen")
        self.value = 9
    def getPossibleMoves(self) -> List[tuple[int, int]]:
        bishopMoves = Bishop.getPossibleMoves(self)
        rookMoves = Rook.getPossibleMoves(self)
        return bishopMoves + rookMoves
    
    def getAttackPositions(self) -> List[tuple[int, int]]:
        bishopMoves = Bishop.getAttackPositions(self)
        rookMoves = Rook.getAttackPositions(self)
        return bishopMoves + rookMoves