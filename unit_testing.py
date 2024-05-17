from chess_question import get_piece
from chess_question import check_free_space
from chess_question import place_piece
from chess_question import captured
from chess_question import king_moves
from chess_question import queen_moves
from chess_question import rook_moves
from chess_question import bishop_moves
from chess_question import knight_moves
from chess_question import pawn_moves
from chess_question import prettify_board
#from chess_question import main as test_main

def main():
    test_board_update()
    test_free_space()
    test_not_a_free_space()

#############
# get_piece #
#############

### invalid inputs

# not 2 arguments

# not a valid position

# not a valid type

# not enough black pieces

### valid inputs

# done

# position is correct

# readable_position is correct

# piece type is correct

# black pieces count is updated correctly

####################
# check_free_space #
####################

# not a free space
def test_not_a_free_space():
    board = [
        ["X","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
    ]

    assert not check_free_space(board, [0,0])


# free space
def test_free_space():
    board = [
        ["X","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
    ]

    assert check_free_space(board, [1,0])

###############
# place_piece #
###############

# board is updated correctly
def test_board_update():
    board = [
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
    ]

    piece_details = [[3,3], "queen", "d4", "White"]

    expected_board = [
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","",[piece_details[1],piece_details[3],piece_details[2]],"","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
        ["","","","","","","",""],
    ]

    assert place_piece(board, piece_details[0], piece_details[1], piece_details[2], piece_details[3]) == expected_board
    

############
# captured #
############

# correct function used for given type

# piece captured when it should be

# piece not captured when it shouldn't be

# multiple pieces captured when they should be

# piece not captured when it shouldn't be and capturable pieces captured

# blocked pieces not captured correctly

##############
# king_moves #
##############

# correct possible moves returned

###############
# queen_moves #
###############

# correct possible moves returned

##############
# rook_moves #
##############

# correct possible moves returned

################
# bishop_moves #
################

# correct possible moves returned

################
# knight_moves #
################

# correct possible moves returned


##############
# pawn_moves #
##############

# correct possible moves returned


##################
# prettify_board #
##################

# nicely formatted board returned

########
# main #
########

# outputs as expected for several examples