from decisionMakers.weights import EQUALTRADE
from pieces.piece import Piece


class pieceTrader:
    def canTakePiece(self, x:int, y:int, piece: Piece, board: list[list[Piece|int]], blackAttackTiles: set[tuple[int, int]]) -> int:
        # is there a piece at location?
        if not isinstance(board[x][y], Piece):
            return 0
        #hanging piece case
        if (x, y) not in blackAttackTiles:
            return board[x][y].getValue()
        
        # trade case
        myWorth = piece.getValue()
        enemyWorth = board[x][y].getValue()
        
        diff = enemyWorth - myWorth

        if diff == 0:
            return EQUALTRADE
        return diff
