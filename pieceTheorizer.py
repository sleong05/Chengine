from pieces import *
from weights import *

class PieceTheorizer:
    def __init__(self):
        self.piece_actions = {
    King: self.handle_king,
    Bishop: self.handle_bishop,
    Rook: self.handle_rook,
    Knight: self.handle_knight,
    Pawn: self.handle_pawn,
    Queen: self.handle_queen,
}
        self.oldX = None
        self.oldY = None
        self.newX = None
        self.newY = None

    def evaluatePiece(self, piece: Piece, newX:int, newY:int, oldX:int, oldY:int) -> int:
        self.newX = newX
        self.newY = newY
        self.oldX = oldX
        self.oldY = oldY

        handler = self.piece_actions.get(type(piece))
        score = handler(piece)
        return score

    def handle_king(self, king: King) -> int:
        #logic for king

        #detect castling
        if abs(self.newX-self.oldX) == 2:
            return CASTLINGWEIGHT
        # else return a slight negative

        return KINGMOVE

    def handle_bishop(self, bishop: Bishop) -> int:
        #print(f"RATING BISHOP MOVE FOR BISHOP AT {self.oldX}, {self.oldY} going to {self.newX}, {self.newY}")

        squaresSeenFromCurrent = bishop.getPossibleMovesInPosition(self.oldX, self.oldY)
        squaresSeenFromfuture = bishop.getPossibleMovesInPosition(self.newX, self.newY)
        diff = len(squaresSeenFromfuture) - len(squaresSeenFromCurrent )
        #max move gain is 7 and we want to return max a value of 1 for this weight
        changeRating = diff/7
        #print(f"Changerating = {changeRating}")

        #additionally we want to add some specific weight to some squares to encourage good gameplay
        #fianchetto 
        fianchettoRating = 0
        if (self.newX, self.newY) == (1, 1) or (self.newX, self.newY) == (6, 1):
            fianchettoRating += FIANCHETTO_VALUE
        #print(f"fiacnhetto = {fianchettoRating}")

        #usual bishop development locations (discourages blocking pawns as well)
        standardSpotRating = 0
        if (self.newX, self.newY) == (2, 3) or (self.newX, self.newY) == (1, 4) or (self.newX, self.newY) == (5, 3) or (self.newX, self.newY) == (6, 4):
            standardSpotRating += STANDARD_BISHOP_SPOT
        #print(f"normal = {standardSpotRating}")

        #encourage to develop off starting squre
        notDevelopedRating = 0
        if not bishop.hasMoved:
            notDevelopedRating += BISHOP_NOT_MOVED
        return changeRating + fianchettoRating + standardSpotRating + notDevelopedRating

    def handle_rook(self, rook):
        # logic for rook
        print(f"RATING BISHOP MOVE FOR ROOK AT {self.oldX}, {self.oldY} going to {self.newX}, {self.newY}")
        squaresSeenFromCurrent = rook.getPossibleMovesInPosition(self.oldX, self.oldY)
        squaresSeenFromfuture = rook.getPossibleMovesInPosition(self.newX, self.newY)

        diff = len(squaresSeenFromfuture) - len(squaresSeenFromCurrent )
        #max move gain is 7 and we want to return max a value of 1 for this weight but we are going to scale it down a bit because rooks moving isnt ideal and isnt so much
        #about seeing more since they are valuable
        changeRating = diff/(7*3)
        print(f"Change in rating is {changeRating}")
        return changeRating

    def handle_knight(self, knight):
        # logic for knight
        return 0

    def handle_pawn(self, pawn):
        # logic for pawn
        return 0

    def handle_queen(self, queen):
        # logic for queen
        return 0