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
from chess_question import main as test_main

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

# free space

###############
# place_piece #
###############

# board is updated correctly

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