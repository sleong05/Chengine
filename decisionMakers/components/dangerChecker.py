from pieces.piece import *
from ..weights import MOVEINTODANGERFALSE


class DangerChecker():
    def evaluateDanger(self, opposingMoves: tuple[Piece, tuple[int, int]], protectedTiles: set[tuple[int, int]], piece: Piece) -> int:
        opposingTeamsMoves = opposingMoves
        Myposition = piece.getPosition()
        myPieceValue = piece.getValue()
        currentDanger = 0
        protected = True if Myposition in protectedTiles else False

        for opposingMove in opposingTeamsMoves:
            opposingPiece, position = opposingMove

            if position == Myposition:
                if not protected:
                    return myPieceValue
                
                danger = myPieceValue - opposingPiece.getValue()
                currentDanger = max(danger, currentDanger)

        return currentDanger
    
    def moveInDanger(self, x: int, y:int, piece:Piece, board: list[list[int|Piece]], blackAttackTiles: set[tuple[int, int]]) -> int:
        if board[x][y] != 0: #this is a capture and will be assessed elsewhere
            return 0
        return piece.getValue() * -1 if (x, y) in blackAttackTiles else MOVEINTODANGERFALSE
    
