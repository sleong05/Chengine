import threading
import time
from constants import *
import pygame as py
from pieces import *
from typing import List
from moveFinder import MoveFinder

class Board:
    def __init__(self, screen: py.display) -> None:
        self.screen = screen
        self.content =[[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.selectedPiece = None
        self.possibleMoveCircles = []
        self.possibleSpecialMoveCircles = []
        self.whiteKing = King(self.screen, WHITE, (3, 0), self.content)
        self.blackKing = King(self.screen, BLACK, (3, 7), self.content)
        self.playersTurn = WHITE
        # load potential piece icon
        circleImage = py.image.load("Chengine/pieceIcons/potentialMove.png").convert_alpha()
        self.potentialMoveImage = py.transform.scale(circleImage, (TILE_SIZE, TILE_SIZE))
        # load special move icons
        circleImage = py.image.load("Chengine/pieceIcons/potentialSpecialMove.png").convert_alpha()
        self.potentialSpecialMoveImage = py.transform.scale(circleImage, (TILE_SIZE, TILE_SIZE))
        # for en passant
        self.pawnCanPassant = None
        # move finder for engine
        self.moveFinder = MoveFinder()
        #engine thread for letting engine think
        self.engineThread = None

    def drawBoard(self) -> None:
        blackOrWhite = 1
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                py.draw.rect(
                    self.screen,
                    TILE_COLOR_ONE if blackOrWhite%2==0 else TILE_COLOR_TWO,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
                blackOrWhite+=1
            blackOrWhite-=1

    def initilizePieces(self) -> None:
        #pawns
        for i in range(8):
            self.content[i][6] = Pawn(self.screen, BLACK, (i, 6), self.content)

        for i in range(8):
            self.content[i][1] = Pawn(self.screen, WHITE, (i, 1), self.content)

        #knights
        self.content[1][0] = Knight(self.screen, WHITE, (1, 0), self.content)
        self.content[6][0] = Knight(self.screen, WHITE, (6, 0), self.content)

        self.content[6][7] = Knight(self.screen, BLACK, (6, 7), self.content)
        self.content[1][7] = Knight(self.screen, BLACK, (1, 7), self.content)

        #bishops
        self.content[2][7] = Bishop(self.screen, BLACK, (2, 7), self.content)
        self.content[5][7] = Bishop(self.screen, BLACK, (5, 7), self.content)

        self.content[2][0] = Bishop(self.screen, WHITE, (2, 0), self.content)
        self.content[5][0] = Bishop(self.screen, WHITE, (5, 0), self.content)

        #rooks
        self.content[7][0] = Rook(self.screen, WHITE, (7, 0), self.content)
        self.content[0][0] = Rook(self.screen, WHITE, (0, 0), self.content)

        self.content[7][7] = Rook(self.screen, BLACK, (7, 7), self.content)
        self.content[0][7] = Rook(self.screen, BLACK, (0, 7), self.content)

        #Queens
        self.content[4][0] = Queen(self.screen, WHITE, (4, 0), self.content)

        self.content[4][7] = Queen(self.screen, BLACK, (4, 7), self.content)

        #Kings
        self.content[3][7] = self.blackKing

        self.content[3][0] = self.whiteKing
    
    def drawPieces(self) -> None:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = self.content[i][j]
                if piece != 0:
                    piece.draw()

    def click(self, position: tuple[int, int], highlightSquares=True) -> int:
        X = position[0]//TILE_SIZE
        Y = position[1]//TILE_SIZE

        #clicked on a special move (castle, promotion, or enpassant)
        if (X, Y) in self.possibleSpecialMoveCircles:

            # dont spawn enter a move if the engine is thinking
            if self.engineThread != None and self.engineThread.is_alive():
                return 0
            
            #castling
            if isinstance(self.selectedPiece, King):
                self.Castle(X, Y)
                self.pawnCanPassant = None

            # en passant
            if isinstance(self.selectedPiece, Pawn):
                x, y = self.pawnCanPassant.getPosition()
                self.moveSelectedPiece(x, y + self.selectedPiece.getColor())
                self.content[x][y] = 0
                self.playersTurn *= -1

                #check for mate
                hasAMove = self.checkForMate(self.selectedPiece) 
                if not hasAMove: #if not moves a player has won or tied 
                    return self.playersTurn
            self.resetVariables()
            return 0
        # clicked on a movecircle
        if (X, Y) in self.possibleMoveCircles:
            # dont spawn enter a move if the engine is thinking
            if self.engineThread != None and self.engineThread.is_alive():
                return 0
            
            piece = self.selectedPiece
            self.moveSelectedPiece(X, Y)
            self.playersTurn *= -1
            
            #check for mate
            hasAMove = self.checkForMate(piece) 
            if not hasAMove: #if not moves a player has won or tied 
                return self.playersTurn
            self.resetVariables()
            return 0
        
        #empty square
        if self.content[X][Y] == 0:
            self.resetVariables()
            return 0
        
        # we have clicked on a piece
        piece = self.content[X][Y]
        if highlightSquares:
            #Highlight square
            if piece.getColor() != self.playersTurn:
                self.drawRectAtSpot(X, Y, RED)
                return 0
            self.drawRectAtSpot(X, Y, HIGHLIGHT)

        self.selectedPiece = piece

        #get possible moves and spawn circles on those squares
        self.spawnCirclesOnPossibleMoves(piece, highlightSquares)
        return 0

    def drawRectAtSpot(self, X: int, Y: int, color: tuple[int, int, int]) -> None:
        py.draw.rect(
                    self.screen,
                    color,
                    (X * TILE_SIZE, Y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    def resetVariables(self) -> None:
        self.possibleMoveCircles = []
        self.possibleSpecialMoveCircles = []
        self.selectedPiece = None

    def checkForMate(self, piece: Piece) -> bool:
        otherTeamPieces = self.getAllPieces(piece.getColor()*-1)
        allMovesForOtherTeam = []
        hasAMove = False
        for otherTeam in otherTeamPieces:
            legalMoves = self.getAllLegalMoves(otherTeam)
            if legalMoves:
                hasAMove = True
            allMovesForOtherTeam.append((otherTeam, legalMoves))
        return hasAMove

    def Castle(self, X, Y) -> None:
        self.moveSelectedPiece(X, Y) # move king

        if X == 1:  #short castle
            rook = self.content[0][Y]
            self.movePiece(X+1, Y, rook)
        elif X == 5: #long castle
            rook = self.content[7][Y]
            self.movePiece(X-1, Y, rook)
                
        self.playersTurn *= -1
    
    def getAllPieces(self, color: int) -> List[Piece]:
        listOfPieces = []
        for row in self.content:
            for tile in row:
                if isinstance(tile, Piece) and tile.getColor() == color:
                    listOfPieces.append(tile)
        return listOfPieces

    def spawnCirclesOnPossibleMoves(self, piece: Piece, showCircles=True) -> None:
        self.possibleMoveCircles = []
        self.possibleSpecialMoveCircles = []
        acutalMoveCircles = self.getAllLegalMoves(piece)
        
        # checks for castling
        self.checkIfCanCastle(piece)
        
        # check for en passant

        self.checkEnPassant(piece)
        if showCircles:
            for move in self.possibleSpecialMoveCircles:
                x, y = map(lambda v: v*TILE_SIZE, move)
                self.screen.blit(self.potentialSpecialMoveImage, (x,y))

            for move in acutalMoveCircles:
                x, y = map(lambda v: v*TILE_SIZE, move)
                self.screen.blit(self.potentialMoveImage, (x,y))

    def checkIfCanCastle(self, piece):
        if isinstance(piece, King):
            if (not piece.hasMoved):
                x, y = piece.getPosition()
                kingColor = piece.getColor()
            
                #rook exists and hasnt moved
                attackedSquares = self.getAttackedTiles(kingColor*-1)
                if (isinstance(self.content[0][y], Rook) and not self.content[0][y].hasMoved):
                    #king is not in check and no spots along the path of castling are in check
                    tilesAlongCastlePathLong = [(x, y), (x-1, y), (x-2, y)]
                    self.checkCastle(tilesAlongCastlePathLong, attackedSquares, x, y)
                    
                
                if (isinstance(self.content[7][y], Rook) and not self.content[7][y].hasMoved):
                    tilesAlongCastlePathShort = [(x, y), (x+1, y), (x+2, y)]
                    self.checkCastle(tilesAlongCastlePathShort, attackedSquares, x, y)

    def checkEnPassant(self, piece):
        if isinstance(piece, Pawn) and self.pawnCanPassant != None:
            passantX, passantY = self.pawnCanPassant.getPosition()
            team = self.pawnCanPassant.getColor()
            x, y = piece.getPosition()

            #check if side by side and opposite teams
            if passantY == y and (passantX == x-1 or passantX == x+1) and piece.getColor() != team:
                #check if puts king in check
                self.testMovePiece(passantX, passantY + piece.getColor(), piece)
                myKing = self.blackKing if piece.getColor() == BLACK else self.whiteKing
                attackedSquares = self.getAttackedTiles(piece.getColor() * -1)
                self.testMovePiece(x, y, piece)

                if myKing.getPosition() not in attackedSquares:
                    self.possibleSpecialMoveCircles.append((passantX, passantY + piece.getColor()))

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
            attackedTiles = self.convert_GUI_X_Y_To_Board_X_Y(self.getAttackedTilesToDraw(otherTeam)) 
            if (myKing.getPosition() not in attackedTiles): #check if king is now in danger
                #record where possible moves are at so they can be selected later
                self.possibleMoveCircles.append((x, y))
                actualMoves.append((x, y))
            
            self.testMovePiece(oldX, oldY, piece) #move piece back
            #put piece that was at the tested positon back in
            self.content[x][y] = pieceAtTest
        return actualMoves

    def checkCastle(self, tilesAlongCastlePath: List[tuple[int, int]], attackedSquares: List[tuple[int, int]], x: int, y: int) -> bool:
        for tile in tilesAlongCastlePath:
            X, Y = tile
            #tiles are not attacked. tile spot is empty. tile spot is not the king itself
            if tile in attackedSquares or self.content[X][Y] != 0 and (X, Y) != (x, y):
                return False
            #if long castle check that there is no knight
            if X == 5:
                knightStartingSpot = self.content[X+1][Y]
                if knightStartingSpot != 0:
                    return False
        self.possibleSpecialMoveCircles.append((X, Y))
        return True
        
    def convert_GUI_X_Y_To_Board_X_Y(self, positions: List[tuple[int, int]]):
        modifiedPositions = []
        for spot in positions:
            x, y = map(lambda v: v//TILE_SIZE, spot)
            modifiedPositions.append((x, y))
        return modifiedPositions

    def testMovePiece(self, X:int, Y:int, piece: Piece) -> None: 
        """tests the moving a piece without actually updating needed variables for an actual move"""
        oldPosition = piece.getPosition()
        self.content[X][Y] = piece
        piece.testChangePosition((X, Y))
        self.content[oldPosition[0]][oldPosition[1]] = 0

    def moveSelectedPiece(self, X: int, Y: int) -> None:
        oldPosition = self.selectedPiece.getPosition()

        self.content[X][Y] = self.selectedPiece
        self.selectedPiece.changePosition((X, Y))

        piece = self.selectedPiece
        #reset variables
        self.selectedPiece = None
        self.content[oldPosition[0]][oldPosition[1]] = 0
        self.possibleMoveCircles = []
        self.possibleSpecialMoveCircles = []
        self.pawnCanPassant = None
        # check if this piece can now be en passanted
        if isinstance(piece, Pawn):
            if oldPosition[1]+2 == Y or oldPosition[1] -2 == Y:
                self.pawnCanPassant = piece
    
    def isPromotionNeeded(self) -> tuple[bool, tuple[int, int], int]:
        for i in range(BOARD_SIZE):

            if isinstance(self.content[i][0], Pawn):
                return (True, (i, 0), self.content[i][0].getColor())
            elif isinstance(self.content[i][7], Pawn):
                return (True, (i, 7), self.content[i][7].getColor())
            
        return (False, (-1, -1), 0)
    
    def movePiece(self, X: int, Y: int, piece: Piece) -> None:
        oldPosition = piece.getPosition()

        self.content[X][Y] = piece
        piece.changePosition((X, Y))
        self.content[oldPosition[0]][oldPosition[1]] = 0


    def getAttackedTilesToDraw(self, color: int) -> set[tuple[int, int]]:
        attackedPositions = set()

        for row in self.content:
            for piece in row:
                if isinstance(piece, Piece) and piece.getColor()==color:
                    attackedPositions.update(piece.getAttackPositions())

        return attackedPositions
    
    def getAttackedTiles(self, color: int) -> List[tuple[int, int]]:
        tiles = self.getAttackedTilesToDraw(color)
        adjustedTiles = set()

        for tile in tiles:
            X, Y = tile
            if X//TILE_SIZE in range(8) and Y//TILE_SIZE in range(8):
                
                newTile = (X//TILE_SIZE, Y//TILE_SIZE)
                adjustedTiles.add(newTile)
        return adjustedTiles
    
    def getPossibleMoves(self, color: int) -> List[tuple[int, int]]:
        possibleMoves = set()

        for row in self.content:
            for piece in row:
                if isinstance(piece, Piece) and piece.getColor()==color:
                    possibleMoves.update(piece.getPossibleMoves())

        return possibleMoves

    def highLightAttackTiles(self, color: int) -> None:
        attackedPositions = self.getAttackedTilesToDraw(color)
        for tile in attackedPositions:
            #Highlight square
            position = tile
            py.draw.rect(
                        self.screen,
                        (100, 100, 0),
                        (position[0], position[1], TILE_SIZE, TILE_SIZE)
                    )
    
    def isAKingInCheck(self) -> bool:
        attackedBlack = self.getAttackedTiles(BLACK)
        whiteKingPosition = self.whiteKing.getPosition()
        if whiteKingPosition in attackedBlack:
            return True
        
        attackedWhite = self.getAttackedTiles(WHITE)
        blackKingPosition = self.blackKing.getPosition()
        if blackKingPosition in attackedWhite:
            return True
        
        return False

    def isWhiteTurn(self) -> int:
        return True if self.playersTurn == WHITE else False

    def getPieces(self, team: int) -> list[Piece]:
        piecesOfTeam = []
        for row in self.content:
            for tile in row:
                if isinstance(tile, Piece) and tile.getColor() == team:
                    piecesOfTeam.append(tile)

        return piecesOfTeam
    
    def engineMove(self) -> None:
        allPossibleMoves = self.getMovesForEngine()
    
        engineMoveThread = threading.Thread(target=self.doEngineMove, args=(allPossibleMoves,))
        engineMoveThread.start()
        self.playersTurn *= -1

    def getMovesForEngine(self):
        allPossibleMoves = []
        whitePieces = self.getPieces(WHITE)

        for piece in whitePieces:
            allLegalMoves = self.getAllLegalMoves(piece)
            for legalMove in allLegalMoves:
                allPossibleMoves.append((piece, legalMove))

        #check castling
        x, y = self.whiteKing.getPosition()
        self.click((x*TILE_SIZE, y*TILE_SIZE), highlightSquares=False)
        for move in self.possibleSpecialMoveCircles:
            allPossibleMoves.append((self.whiteKing, move))
        self.click((x*TILE_SIZE, y*TILE_SIZE), highlightSquares=False)
        return allPossibleMoves

    def doFirstMove(self) -> None:
            firstMoves = []
            ePawn = self.content[4][1]
            e4 = (ePawn, (4, 3))

            dPawn = self.content[3][1]
            d4 = (dPawn, (3, 3))
            
            firstMoves.append(e4)
            firstMoves.append(d4)

            engineMoveThread = threading.Thread(target=self.doEngineMove, args=(firstMoves,))
            engineMoveThread.start()
            self.playersTurn *= -1
    
    def doEngineMove(self, allPossibleMoves: list[tuple[Piece, tuple[int, int]]]) -> None:
        decidedMoves = self.findMovesOfInterest(allPossibleMoves, WHITE)
        #game is over
        if not decidedMoves:
            return
        
        #TREE TIME
        highestRankedMove = self.lookIntoFutureMoves(decidedMoves, 3, BLACK)
        move, valuation = highestRankedMove
        
        #once best move is found
        piece, position = move
        x, y = position
        oldX, oldY = piece.getPosition()
        #simulate move
        self.playersTurn *= -1
        self.click((oldX*TILE_SIZE, oldY*TILE_SIZE), highlightSquares=False)
        self.click((x*TILE_SIZE, y*TILE_SIZE), highlightSquares=False)
        self.resetVariables()
        #check if we need to promote a pawn
        if isinstance(piece, Pawn) and y == 7:
            self.content[x][y] = Queen(self.screen, WHITE, (x, y), self.content)
        #redraw
        self.drawBoard()
        self.drawRectAtSpot(x, y, HIGHLIGHT_ENGINE)
        self.drawPieces()

    def findMovesOfInterest(self, allPossibleMoves, player: int):
        decidedMoves = []
        self.moveFinder.feedData(self.content, player*-1, allPossibleMoves, self.getAttackedTiles(WHITE),self.getAttackedTiles(BLACK))
        self.moveFinder.getBestMove(decidedMoves)
        return decidedMoves
    
    def lookIntoFutureMoves(self, movesOfinterest: list[tuple[Piece, tuple[int, int]]], depth: int, player: int) -> tuple[tuple[Piece, tuple[int, int]], int]:
        childrenValues = []
        if depth==0:
            print(f"DEPTH: {depth}")
            for move in movesOfinterest:
                childrenValues.append((move, self.staticEval()))
        else:
            for move in movesOfinterest:
                print(f"DEPTH: {depth} looking at move {move}")
                #data to remember
                castle = False
                piece, position = move
                newX, newY = position
                oldX, oldY = piece.getPosition()
                pieceAtMove = self.content[newX][newY]
                pieceHasMovedValue = piece.hasMoved
                #do the move
                if player == WHITE:
                    self.playersTurn *= -1
                self.click((oldX*TILE_SIZE, oldY*TILE_SIZE), highlightSquares=False)
                self.drawBoard()
                self.drawPieces()
                self.click((newX*TILE_SIZE, newY*TILE_SIZE), highlightSquares=False)
                self.drawBoard()
                self.drawPieces()
                #check if move was a castle
                if isinstance(piece, King) and abs(newX - oldX) == 2:
                    castle = True
                #lookinto future
                print(F"Diving Deeper")
                interestingMoves = self.findMovesOfInterest(self.getMovesForEngine(), player)
                childrenValues.append(self.lookIntoFutureMoves(interestingMoves, depth-1, player*-1))
                # undo move
                if castle:
                    print("CASTLING")
                    pass
                else:
                    self.movePiece(oldX, oldY, piece)
                    self.content[newX][newY] = pieceAtMove
                    piece.hasMoved = pieceHasMovedValue
                    self.drawBoard()
                    self.drawPieces()
        print(f"RETRACING STEPS")
        #min max values
        bestChoiceValue = 9999999 if player == BLACK else -9999999
        bestChild = None

        for child in childrenValues:
            value = child[1]
            if player == WHITE:
                if bestChoiceValue < value:
                    bestChoiceValue = value
                    bestChild = child
            else:
                if bestChoiceValue > value:
                    bestChoiceValue = value
                    bestChild = child

        return bestChild
    def staticEval(self) -> int:
        score = 0

        for row in self.content:
            for tile in row:
                if isinstance(tile, Piece):
                    score += tile.getValue() if tile.getColor() == WHITE else tile.getValue() * -1
        
        return score
    