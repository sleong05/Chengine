from constants import *
from pieces import *
from ..weights import *

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
        self.board = None

    def evaluatePiece(self, piece: Piece, newX:int, newY:int, oldX:int, oldY:int, board: list[list[int|Piece]]) -> int:
        self.newX = newX
        self.newY = newY
        self.oldX = oldX
        self.oldY = oldY
        self.board = board
        self.team = piece.getColor()
    

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

        squaresSeenFromCurrent = bishop.getPossibleMovesInPosition(self.oldX, self.oldY)
        squaresSeenFromfuture = bishop.getPossibleMovesInPosition(self.newX, self.newY)
        diff = len(squaresSeenFromfuture) - len(squaresSeenFromCurrent )
        #max move gain is 7 and we want to return max a value of 1 for this weight
        changeRating = diff/7

        #additionally we want to add some specific weight to some squares to encourage good gameplay
        #fianchetto 
        fianchettoRating = 0
        if self.team == WHITE:
            if (self.newX, self.newY) == (1, 1) or (self.newX, self.newY) == (6, 1):
                fianchettoRating += FIANCHETTO_VALUE

            #usual bishop development locations (discourages blocking pawns as well)
            standardSpotRating = 0
            if (self.newX, self.newY) == (2, 3) or (self.newX, self.newY) == (1, 4) or (self.newX, self.newY) == (5, 3) or (self.newX, self.newY) == (6, 4):
                standardSpotRating += STANDARD_BISHOP_SPOT
                

            #encourage to develop off starting squre
            notDevelopedRating = 0
            if not bishop.hasMoved:
                notDevelopedRating += BISHOP_NOT_MOVED
        else:
            if (self.newX, self.newY) == (1, 6) or (self.newX, self.newY) == (6, 6):
                fianchettoRating += FIANCHETTO_VALUE

            #usual bishop development locations (discourages blocking pawns as well)
            standardSpotRating = 0
            if (self.newX, self.newY) == (2, 4) or (self.newX, self.newY) == (1, 3) or (self.newX, self.newY) == (5, 4) or (self.newX, self.newY) == (6, 3):
                standardSpotRating += STANDARD_BISHOP_SPOT
                

            #encourage to develop off starting squre
            notDevelopedRating = 0
            if not bishop.hasMoved:
                notDevelopedRating += BISHOP_NOT_MOVED

        return changeRating + fianchettoRating + standardSpotRating + notDevelopedRating

    def handle_rook(self, rook):
        # logic for rook
        squaresSeenFromCurrent = rook.getPossibleMovesInPosition(self.oldX, self.oldY)
        squaresSeenFromfuture = rook.getPossibleMovesInPosition(self.newX, self.newY)

        diff = len(squaresSeenFromfuture) - len(squaresSeenFromCurrent )
        #max move gain is 7 and we want to return max a value of 1 for this weight but we are going to scale it down a bit because rooks moving isnt ideal and isnt so much
        #about seeing more since they are valuable
        changeRating = diff/(7*3) #TODO this one is iffy lets take a look later

        notDevelopedRating = 0
        if not rook.hasMoved:
            notDevelopedRating += ROOK_NOT_MOVED #negative weight. we want it to be pretty sure when moving the rook and once it has moved to let it move it a lot
        return changeRating + notDevelopedRating

    def handle_knight(self, knight):
        # logic for knight
        squaresSeenFromCurrent = knight.getPossibleMovesInPosition(self.oldX, self.oldY)
        squaresSeenFromfuture = knight.getPossibleMovesInPosition(self.newX, self.newY)
        
        diff = len(squaresSeenFromfuture) - len(squaresSeenFromCurrent )
        changeRating = diff/7 #this weight is trial and errored. if knights not retreating increase the weight

        notDevelopedRating = 0
        if not knight.hasMoved:
            notDevelopedRating += KNIGHT_NOT_MOVED

        return changeRating + notDevelopedRating

    def handle_pawn(self, pawn):
        # logic for pawn: this will be a lot of manual input for base movemnet
        initialMoveValue = 0
        pawnChainValue = 0
        if not pawn.hasMoved:
            if self.team == WHITE:
            #checks for fianchetto pawn movement spot and if the bishop is still there
                if (self.newX, self.newY) in (finachetto := {(1, 2), (6, 2)}):
                    if ((self.oldX != 0 and isinstance(self.board[self.oldX-1][self.oldY-1], Bishop)) or (self.oldX != 7 and isinstance(self.board[self.oldX+1][self.oldY-1], Bishop))): # bishop is actulaly there
                        initialMoveValue += FIANCHETTO_VALUE
                elif (self.newX, self.newY) in (central := {(5, 3), (3, 3), (4, 3)}):
                    initialMoveValue += CENTRAL_PAWN_VALUE
                elif (self.newX, self.newY) in (outside := {(0, 3), (7, 3)}):
                    initialMoveValue += SIDE_PAWN_VALUE
            else:
                #checks for fianchetto pawn movement spot and if the bishop is still there
                if (self.newX, self.newY) in (finachetto := {(1, 5), (6, 5)}):
                    if ((self.oldX != 0 and isinstance(self.board[self.oldX-1][self.oldY+1], Bishop)) or (self.oldX != 7 and isinstance(self.board[self.oldX+1][self.oldY+1], Bishop))):
                        initialMoveValue += FIANCHETTO_VALUE
                elif (self.newX, self.newY) in (central := {(5, 4), (3, 4), (4, 4)}):
                    initialMoveValue += CENTRAL_PAWN_VALUE
                elif (self.newX, self.newY) in (outside := {(0, 4), (7, 4)}):
                    initialMoveValue += SIDE_PAWN_VALUE


        #if i can make a chain of defensive pawns
        if self.team == WHITE:
            spot1 = (self.newX+1, self.newY+1)
            spot2 = (self.newX-1, self.newY+1)
        else:
            spot1 = (self.newX+1, self.newY-1)
            spot2 = (self.newX-1, self.newY-1)
        x1, y1 = spot1
        x2, y2 = spot2

        if x1 in range(8) and y1 in range(8) and isinstance(self.board[x1][y1], Pawn) and self.board[x1][y1].getColor() == pawn.getColor():
            pawnChainValue += PAWN_CHAIN_VALUE
        if x2 in range(8) and y2 in range(8) and isinstance(self.board[x2][y2], Pawn) and self.board[x2][y2].getColor() == pawn.getColor():
            pawnChainValue += PAWN_CHAIN_VALUE
        
        #check if its a passed pawn
        passedPawn = True
        passedPawnValue = 0
        start = self.oldY+1 if self.team == WHITE else self.oldY -1
        end = 7 if self.team == WHITE else 0
        direction = 1 if self.team == WHITE else -1

        for y in range(start, end, direction):
            #check left column
            if self.oldX != 0 and isinstance(self.board[self.oldX-1][y], Pawn): 
                
                if self.board[self.oldX-1][y].getColor() != pawn.getColor():
                    passedPawn = False
                    break

            #cehck right column
            if self.oldX != 7 and isinstance(self.board[self.oldX+1][y], Pawn):

                if self.board[self.oldX+1][y].getColor() != pawn.getColor(): 
                    passedPawn = False
                    break

            #check current column
            if isinstance(self.board[self.oldX][y], Pawn): 
                if self.board[self.oldX][y].getColor() != pawn.getColor(): 
                    passedPawn = False
                    break
        if passedPawn:
            passedPawnValue += PASSED_PAWN_VALUE

        #promotion logic
        promotionValue = 0
        if self.newY == 7:
            promotionValue += PAWN_PROMOTION
        return initialMoveValue + pawnChainValue + passedPawnValue + promotionValue + SLIGHT_PAWN_VALUE

    def handle_queen(self, queen):
        #TODO figure out what maeks queen moves good. it seems to respond ok so far
        # logic for queen
        initialMoveValue = 0
        if not queen.hasMoved:
            initialMoveValue += QUEEN_NOT_MOVED #negative weight(dont want queen moving early in general)
        return initialMoveValue