#piece is under attack
UNDERATTACKTRUE = 3
UNDER_ATTACK_BUT_DEFENDED = 1

#piece to take values
HANGINGPIECE = 5
EQUALTRADE = 2

#moving into danger
MOVEINTODANGERTRUE = -5
MOVEINTODANGERFALSE = 0.15

#MOVE THEORY

#KING
CASTLINGWEIGHT = 2
KINGMOVE = - 0.5 #generally we dont want king to move

#BISHOP
FIANCHETTO_VALUE = .3 #small boost to encourage fianchettoing
STANDARD_BISHOP_SPOT = .2
BISHOP_NOT_MOVED = .2