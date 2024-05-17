"""
# psuedocode
1. get white piece location and type
    a. check valid input 
        i. valid co-ordinate (e.g. a1 - [a-h][1-8])
        ii. not a valid piece type
2. add white piece to board
3. get black piece(s) location(s) and type(s)
    a. loop until done or 16 pieces
    b. check valid input
        i. valid co-ordinate (e.g. a1 - [a-h][1-8])
        ii. not already taken
        iii. not a valid piece type
        iiv. valid number of pieces (e.g. not more than 2 knights)
        v. done not used too early (must have one piece)
    c. try/except loop until valid
    d. add black piece(s) to board, so in place for next piece
4. check which pieces the white piece can take
5. output black pieces that can be taken 

# chess board layout
a8 | b8 | c8 | d8 | e8 | f8 | g8 | h8
a7 | b7 | c7 | d7 | e7 | f7 | g7 | h7
a6 | b6 | c6 | d6 | e6 | f6 | g6 | h6
a5 | b5 | c5 | d5 | e5 | f5 | g5 | h5
a4 | b4 | c4 | d4 | e4 | f4 | g4 | h4
a3 | b3 | c3 | d3 | e3 | f3 | g3 | h3
a2 | b2 | c2 | d2 | e2 | f2 | g2 | h2
a1 | b1 | c1 | d1 | e1 | f1 | g1 | h1

Board is stored as list of lists, the first list is the top row and the last list is bottom row

# chess board indices
[0][0] | [0][1] | [0][2] | [0][3] | [0][4] | [0][5] | [0][6] | [0][7]
[1][0] | [1][1] | [1][2] | [1][3] | [1][4] | [1][5] | [1][6] | [1][7]
[2][0] | [2][1] | [2][2] | [2][3] | [2][4] | [2][5] | [2][6] | [2][7]
[3][0] | [3][1] | [3][2] | [3][3] | [3][4] | [3][5] | [3][6] | [3][7]
[4][0] | [4][1] | [4][2] | [4][3] | [4][4] | [4][5] | [4][6] | [4][7]
[5][0] | [5][1] | [5][2] | [5][3] | [5][4] | [5][5] | [5][6] | [5][7]
[6][0] | [6][1] | [6][2] | [6][3] | [6][4] | [6][5] | [6][6] | [6][7]
[7][0] | [7][1] | [7][2] | [7][3] | [7][4] | [7][5] | [7][6] | [7][7]



# piece moves
king: one square in any direction
queen: any number of squares diagonally, vertically or horizontally
rook: any number of squares vertically or horizontally
bishop: any number of squares diagonally
knight: L-shaped (2 squares in direction, then 1 one square perpendicular)
pawn: 2 moves forware on the first move, 1 move forward after, diagonally if capturing

# piece numbers
king: 1
queen: 1
rook: 2
bishop: 2
knight: 2
pawn: 8

"""

import re
from tabulate import tabulate
import copy


# custom exceptions
class InvalidLengthError(Exception):
    "Raised when input isn't 2 characters"
    pass


class InvalidCharacters(Exception):
    "Raised when input isn't a leter between a-h followed by a digit between 1-8"
    pass


class SpaceNotAvailable(Exception):
    "Raised when position is not free on the chess board"
    pass


class InvalidPieceType(Exception):
    "Raised when piece is not a known type"
    pass


class NotEnoughPieces(Exception):
    "Raised when no more pieces of the given type can be used"
    pass


class InvalidNumberOfArguments(Exception):
    "Raised when number of arguments input is not 2"
    pass


def main():
    # set a blank board - this will be updated as pieces are added and used to validate moves
    board = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]

    # list possible types - used to validate input
    piece_types = ["king", "queen", "rook", "bishop", "knight", "pawn"]

    # max number of pieces available to black - used to validate input
    black_pieces_count = {
        "king": 1,
        "queen": 1,
        "rook": 2,
        "bishop": 2,
        "knight": 2,
        "pawn": 8,
    }

    # list available types
    print(f"Available types: {', '.join(piece_types)}")

    # get white piece
    while True:
        try:
            white_position, readable_position, white_piece_type, black_pieces_count = (
                get_piece(board, piece_types, black_pieces_count, "White")
            )
        except InvalidLengthError:
            print("Invalid position format: should only be 2 characters")
        except InvalidCharacters:
            print("Invalid position format: should a letter (a-h) and a number (1-8)")
        except SpaceNotAvailable:
            print("Position not free - please enter a new position")
        except InvalidPieceType:
            print(
                "Not a valid piece - valid pieces: king, queen, rook, bishop, knight, pawn"
            )
        except NotEnoughPieces:
            print("There are no more of that piece, please choose another")
        except InvalidNumberOfArguments:
            print("Please enter only a piece and a position")
        else:
            # if 'done' is entered, False will be returned in white_position
            if white_position:
                break
            else:
                print("Done can not be used, piece required")

    # place white piece
    board = place_piece(
        board, white_position, white_piece_type, readable_position, "White"
    )
    print(
        f"{white_piece_type.title()} added successfully at position {readable_position}"
    )

    # print out board
    temp_board = copy.deepcopy(board)
    pretty_board = prettify_board(temp_board)
    print(tabulate(pretty_board, tablefmt="jira"))

    # get black pieces - max 16 so looping 16 times
    for i in range(16):
        # get black piece(s)
        while True:
            try:
                position, readable_position, piece_type, black_pieces_count = get_piece(
                    board, piece_types, black_pieces_count
                )
            except InvalidLengthError:
                print("Invalid format: should only be 2 characters")
            except InvalidCharacters:
                print("Invalid format: should a letter (a-h) and a number (1-8)")
            except SpaceNotAvailable:
                print("Position not free - please enter a new position")
            except InvalidPieceType:
                print(
                    "Not a valid piece - valid pieces: king, queen, rook, bishop, knight, pawn"
                )
            except NotEnoughPieces:
                print("There are no more of that piece, please choose another")
            else:
                # if 'done' is entered, False will be returned in position
                if position:
                    # place black piece
                    board = place_piece(board, position, piece_type, readable_position)
                    print(
                        f"{piece_type.title()} added successfully at position {readable_position}"
                    )
                    break
                else:
                    # only finish loop on 'done' if at least one iteration complete
                    if i == 0:
                        print("Must enter at least one co-ordinate")
                    else:
                        break
        # print out board
        temp_board = copy.deepcopy(board)
        pretty_board = prettify_board(temp_board)
        print(tabulate(pretty_board, tablefmt="jira"))

        # exit loop if 'done' condition provided
        if not position:
            break

    # find pieces that can be captured
    captured_pieces = captured(board, white_position, white_piece_type)

    # print out capture-able pieces
    if len(captured_pieces) == 0:
        print("Your piece can not capture anything")
    else:
        for i in captured_pieces:
            print(f"Your piece can capture a {i[0]} at position {i[1]}")


def get_piece(board, piece_types, black_pieces_count, colour="Black"):
    """
    Function to get the position and type of the piece in a useable format.

    This function get an input from the user (expected format "piece position" e.g. "knight a2"),
    then checks for the user stopping adding pieces (if "done" is entered),
    then checks for a valid position,
    then converts the position from the human readable format ("a1") to the indices for the board ([7][0]),
    then checks if the position is available on the current board,
    then checks for a valid piece type,
    then, if a black piece, checks if there are any of that type remaining.

    Input values:
    board - the current board
    piece_types - the list of available types
    black_pieces_count - the current number of black pieces remaining
    colour - White or Black, used to determine whether we need to check the number of pieces remaining

    Return values:
    position - a list of 2 values that are the indices of the position on the board ([Y index, X index])
    readable_position - the human readable position (e.g. "a1"), used to make message easier to output
    piece_type - the piece type selected
    black_pieces_count - the update dictionary keeping count of the black pieces remaining, with the selected
                         piece decreased by 1
    """

    # get user input - expected "type position" or "done"
    user_input = input(f"{colour}: ").strip().lower()

    # check if user is attempting to finish entering pieces
    if user_input == "done":
        return False, None, None, None

    # split input into type and position
    temp_list = user_input.split(" ")

    # check valid number of arguments
    if len(temp_list) != 2:
        raise InvalidNumberOfArguments

    piece_type, position = temp_list[0], temp_list[1]

    # check if position is a valid co-ordinate no.1 - 2 characters only
    if len(position) != 2:
        raise InvalidLengthError

    readable_position = position  # storing the human readable position to make it easier to output later
    position = [
        position[1],
        position[0],
    ]  # re-ordering cordinate to make it match indices (x is [1], y is [0])

    # check if position is a valid co-ordinate no.2 - a letter between a and h followed by a digit between 1 and 8
    if not re.search("[a-h]", position[1]) or not re.search("[1-8]", position[0]):
        raise InvalidCharacters

    # convert the co-ordinates to the indices (refer to layout in the starting notes)
    # x co-ordinate converted to second index
    match position[1]:
        case "a":
            position[1] = 0
        case "b":
            position[1] = 1
        case "c":
            position[1] = 2
        case "d":
            position[1] = 3
        case "e":
            position[1] = 4
        case "f":
            position[1] = 5
        case "g":
            position[1] = 6
        case "h":
            position[1] = 7

    # y co-ordinate converted to first index
    match position[0]:
        case "1":
            position[0] = 7
        case "2":
            position[0] = 6
        case "3":
            position[0] = 5
        case "4":
            position[0] = 4
        case "5":
            position[0] = 3
        case "6":
            position[0] = 2
        case "7":
            position[0] = 1
        case "8":
            position[0] = 0

    # check if the position is free
    if not check_free_space(board, position):
        raise SpaceNotAvailable

    # check if piece type is valid type
    if piece_type not in piece_types:
        raise InvalidPieceType

    # if a black piece, check if any piece remain and update dict recording
    if colour == "Black":
        if black_pieces_count[piece_type] == 0:
            raise NotEnoughPieces
        black_pieces_count[piece_type] -= 1

    return position, readable_position, piece_type, black_pieces_count


def check_free_space(board, position):
    """
    Function to check if the provided position has not already been updated - an empty string is a free space

    Input values:
    board - the current board
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    Boolean of whether the position is already used
    """
    return board[position[0]][position[1]] == ""


def place_piece(board, position, piece_type, readable_position, colour="Black"):
    """
    Function that updates the board with the provided piece

    Input values:
    board - the current board
    position - a list of length 2 with the indices that piece should be placed at
    piece_type - the type of piece to be placed
    readable_position - the human readable position, stored for messages
    colour - the colour, stored to help differeniate pieces

    Return value:
    board - the updated board
    """

    # add the piece (with details for future ref) at the requested position
    board[position[0]][position[1]] = [piece_type, colour, readable_position]

    return board


def captured(board, position, piece_type):
    """
    Function to calculate which pieces can be captured on the current board,
    based on the moves the white piece can make

    Input values:
    board - the current board
    position - a list of length 2 with the indices that piece should be placed at
    piece_type - the type of piece to be placed

    Return value:
    captured_pieces - a list of the pieces that can be captured, each piece is a list
                      with the type and position of the captured piece
    """
    # check which function to use, based on the piece type
    # get the list of possible moves the white piece can make
    match piece_type:
        case "king":
            possible_moves = king_moves(position)
        case "queen":
            possible_moves = queen_moves(position)
        case "rook":
            possible_moves = rook_moves(position)
        case "bishop":
            possible_moves = bishop_moves(position)
        case "knight":
            possible_moves = knight_moves(position)
        case "pawn":
            possible_moves = pawn_moves(position)

    # initialise list for captured pieces
    captured_pieces = []

    # for each of the possible moves, check if a black piece is there
    for move in possible_moves:
        if board[move[0]][move[1]] != "":
            captured_pieces.append(
                [board[move[0]][move[1]][0], board[move[0]][move[1]][2], move]
            )

    # for pieces that can move any number of spaces, capture only the first encoutered white piece
    if piece_type in ["queen", "rook", "bishop"]:
        # to make things easier for me to code, I am splitting up pieces vertical to the white piece,
        # pieces horizontal, and pieces diagonal
        vertical_pieces = []
        horizontal_pieces = []
        diagonal_pieces = []

        # checking if the captured piece is vertical, horizontal, or diagonal to the white piece
        for piece in captured_pieces:
            # if x co-ordinate is the same, vertical
            if piece[2][1] == position[1]:
                vertical_pieces.append(piece[2])
            # if y co-ordinate is the same, horizontal
            elif piece[2][0] == position[0]:
                horizontal_pieces.append(piece[2])
            # otherwise diagonal
            else:
                diagonal_pieces.append(piece[2])

        # sorting the vertical pieces by y
        vertical_pieces = sorted(vertical_pieces, key=lambda x: x[0])
        
        # list to store the new list of captured pieces
        vertical_pieces_captured = []

        # checking if the current vertical piece and the next vertical piece
        # are on opposite sides of the white piece and replacing the vertical
        # list with just those 2 if there
        # if the next vertical doesn't exist or the first piece is already after the
        # white piece, select the current piece only
        for i, value in enumerate(vertical_pieces):
            # check next piece exists
            try:
                vertical_pieces[i + 1]
            # if not, select the current piece
            except IndexError:
                vertical_pieces_captured = [value]
            else:
                # check if the current piece is before the white piece
                # and the next piece is after the white piece
                if vertical_pieces[i][0] < position[0]:
                    if vertical_pieces[i + 1][0] > position[0]:
                        # if so, select current and next pieces
                        vertical_pieces_captured = [
                            vertical_pieces[i],
                            vertical_pieces[i + 1],
                        ]
                        break
                # if not before the white piece, select current piece
                elif i == 0:
                    vertical_pieces_captured = [value]
                    break

        # sorting the horizontal pieces by x
        horizontal_pieces = sorted(horizontal_pieces, key=lambda x: x[1])

        # list to store the new list of captured pieces
        horizontal_pieces_captured = []

        # same process as vertical, just on the other axis
        for i, value in enumerate(horizontal_pieces):
            # check next piece exists
            try:
                horizontal_pieces[i + 1]
            # if not, select the current piece
            except IndexError:
                horizontal_pieces_captured = [value]
            else:
                # check if the current piece is before the white piece
                # and the next piece is after the white piece
                if horizontal_pieces[i][1] < position[1]:
                    if horizontal_pieces[i + 1][1] > position[1]:
                        # if so, select current and next pieces
                        horizontal_pieces_captured = [
                            horizontal_pieces[i],
                            horizontal_pieces[i + 1],
                        ]
                        break
                # if not before the white piece, select current piece
                elif i == 0:
                    horizontal_pieces_captured = [value]
                    break

        # sort diagonal pieces by y - this makes it easier to select the closest piece(s)
        diagonal_pieces = sorted(diagonal_pieces, key=lambda x: x[0])

        # to make the process easier for me to understand,
        # splitting the diagonal pieces into 4 quadrents
        # below and to the left (-x, -y), below and to the right (-x, +y),
        # up and to the left (+x, -y), up and to the right (+x, +y)
        diagonal_pieces_q1 = []  # (-x, -y), < <
        diagonal_pieces_q2 = []  # (-x, +y), < >
        diagonal_pieces_q3 = []  # (+x, -y), > <
        diagonal_pieces_q4 = []  # (+x, +y), > >

        for i, value in enumerate(diagonal_pieces):
            if value[1] < position[1]:
                if value[0] < position[0]:
                    diagonal_pieces_q1.append(value)
                elif value[0] > position[0]:
                    diagonal_pieces_q2.append(value)
            elif value[1] > position[1]:
                if value[0] < position[0]:
                    diagonal_pieces_q3.append(value)
                elif value[0] > position[0]:
                    diagonal_pieces_q4.append(value)

        diagonal_pieces_captured = []

        # if any in Q1, append the last (x < white piece x, so largest x is closest)
        if len(diagonal_pieces_q1) > 0:
            diagonal_pieces_q1 = sorted(diagonal_pieces_q1, key=lambda x: x[1])
            diagonal_pieces_captured.append(diagonal_pieces_q1[-1])

        # if any in Q2, append the last (x < white piece x, so largest x is closest)
        if len(diagonal_pieces_q2) > 0:
            diagonal_pieces_q2 = sorted(diagonal_pieces_q2, key=lambda x: x[1])
            diagonal_pieces_captured.append(diagonal_pieces_q2[-1])

        # if any in Q3, append the first (x > white piece x, so smallest x is closest)
        if len(diagonal_pieces_q3) > 0:
            diagonal_pieces_q3 = sorted(diagonal_pieces_q3, key=lambda x: x[1])
            diagonal_pieces_captured.append(diagonal_pieces_q3[0])

        # if any in Q4, append the first (x > white piece x, so smallest x is closest)
        if len(diagonal_pieces_q4) > 0:
            diagonal_pieces_q4 = sorted(diagonal_pieces_q4, key=lambda x: x[1])
            diagonal_pieces_captured.append(diagonal_pieces_q4[0])

        # combine captured pieces
        temp_pieces = (
            vertical_pieces_captured
            + horizontal_pieces_captured
            + diagonal_pieces_captured
        )

        # because I need more than just the position but I've only got positions
        # using indices to remove un-capturable pieces
        indices = []

        # check if the pieces in the original captured_pieces list
        # are on the new list
        # record index if not
        for i, piece in enumerate(captured_pieces):
            if piece[2] not in temp_pieces:
                indices.append(i)

        # reverse sort the indices, so I can remove the last one first and
        # not mess up the indices
        indices = sorted(indices, reverse=True)

        # remove the indices that can't be captured because they're blocked
        for i in indices:
            captured_pieces.pop(i)

    return captured_pieces


def king_moves(position):
    """
    Function to calculate the position that a king can move to

    Requirement:
    Kings can move one space in any direction

    Logic:
    Check each possible move (8 in total), check they are possible (not less
    than 0 or more than 7), add if possible

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """

    possible_moves = []

    # row above king
    if position[0] - 1 >= 0:
        # col to the left of king
        if position[1] - 1 >= 0:
            possible_moves.append([position[0] - 1, position[1] - 1])
        # col to the right of king
        if position[1] + 1 <= 7:
            possible_moves.append([position[0] - 1, position[1] + 1])
        # same col as king
        possible_moves.append([position[0] - 1, position[1]])

    # row below king
    if position[0] + 1 <= 7:
        # col to the left of king
        if position[1] - 1 >= 0:
            possible_moves.append([position[0] + 1, position[1] - 1])
        # col to the right of king
        if position[1] + 1 <= 7:
            possible_moves.append([position[0] + 1, position[1] + 1])
        # same col as king
        possible_moves.append([position[0] + 1, position[1]])

    # same row as king (no need to check if valid)
    # col to the left of king
    if position[1] - 1 >= 0:
        possible_moves.append([position[0], position[1] - 1])
    # col to the right of king
    if position[1] + 1 <= 7:
        possible_moves.append([position[0], position[1] + 1])

    return possible_moves


def queen_moves(position):
    """
    Function to calculate the position that a queen can move to

    Requirements:
    Queens can move any number of spaces vertically, horizontally or diagonally

    Logic:
    Use rook function (vertically and horizonatally) and bishop function (diagonally)

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """
    possible_moves = []

    # get possible vertical and horizontal moves
    possible_moves.extend(rook_moves(position))

    # get possible diagonal moves
    possible_moves.extend(bishop_moves(position))

    return possible_moves


def rook_moves(position):
    """
    Function to calculate the position that a rook can move to

    Requirements:
    Rooks can move any number of spaces vertically or horizontally

    Logic:
    Loop through 8 squares (to cover the full width/height of the board), ignore the occupied square
    (when i is equal to X or Y), and add all co-ordinates (1 with [i,X] and 1 with [Y,i])

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """
    possible_moves = []

    # loop through all each col/row of the board, ignore the occupied square (i=X, i=Y)
    for i in range(8):
        # vertical moves (x is the same)
        if i != position[0]:
            possible_moves.append([i, position[1]])

        # horizontal moves (y is the same)
        if i != position[1]:
            possible_moves.append([position[0], i])

    return possible_moves


def bishop_moves(position):
    """
    Function to calculate the position that a piece can move to

    Requirements:
    Bishops can move any number of spaces diagonally

    Logic:
    Looping 8 times to cover each column of the board

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """
    possible_moves = []

    # diagonal moves (x +/- n, y +/- n)
    # check each col and see if any of diagonal move n steps away are possible
    for i in range(8):
        # ignore when checking the column the piece is on
        if i == position[1]:
            continue

        # find how many columns away
        n = abs(position[1] - i)

        # find all moves n steps away
        moves = [
            [position[0] - n, position[1] - n],
            [position[0] + n, position[1] - n],
            [position[0] - n, position[1] + n],
            [position[0] + n, position[1] + n],
        ]

        # check if the moves n steps away are real positions
        for move in moves:
            if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0:
                pass
            else:
                if move not in possible_moves:
                    possible_moves.append(move)

    return possible_moves


def knight_moves(position):
    """
    Function to calculate the position that a piece can move to

    Requirements:
    Knights can move in an L shape. There are 8 places they can move:
    up 2, left 1 or right 1
    down 2, left 1 or right 1
    left 2, up 1 or down 1
    right 2, up 1 or down 1

    Logic:
    Check each move to see if exists, add if it does

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """
    possible_moves = []

    # up 2
    if position[0] - 2 >= 0:
        # left 1
        if position[1] - 1 >= 0:
            possible_moves.append([position[0] - 2, position[1] - 1])

        # right 1
        if position[1] + 1 <= 7:
            possible_moves.append([position[0] - 2, position[1] + 1])

    # right 2
    if position[1] + 2 <= 7:
        # up 1
        if position[0] - 1 >= 0:
            possible_moves.append([position[0] - 1, position[1] + 2])

        # down 1
        if position[0] + 1 <= 7:
            possible_moves.append([position[0] + 1, position[1] + 2])

    # down 2
    if position[0] + 2 <= 7:
        # left 1
        if position[1] - 1 >= 0:
            possible_moves.append([position[0] + 2, position[1] - 1])

        # right 1
        if position[1] + 1 <= 7:
            possible_moves.append([position[0] + 2, position[1] + 1])

    # left 2
    if position[1] - 2 >= 0:
        # up 1
        if position[0] - 1 >= 0:
            possible_moves.append([position[0] - 1, position[1] - 2])

        # down 1
        if position[0] + 1 <= 7:
            possible_moves.append([position[0] + 1, position[1] - 2])

    return possible_moves


def pawn_moves(position):
    """
    Function to calculate the position that a piece can move to

    Requirements:
    Pawns can only captured 1 space diagonally in front of them
    Assume white starts from the bottom of the board (so only up)

    Logic:
    Check up one column, to the left and right, check if they exist,
    add if they do

    Input value:
    position - a list of length 2 with the indices that piece should be placed at

    Return value:
    possible_moves - a list of the positions the piece can move to
    """
    possible_moves = []

    # left move - up a column, left a row
    move = [position[0] - 1, position[1] - 1]
    if not (move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0):
        possible_moves.append(move)

    # right move - up a column, right a row
    move = [position[0] - 1, position[1] + 1]
    if not (move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0):
        possible_moves.append(move)

    return possible_moves


def prettify_board(pretty_board):
    """
    Function to convert the pieces on the board from the lists (which don't display very nicely)
    to either the name of the piece (for the white piece) or an "X" (for the black piece(s)) so
    the board can be output in a clear(er) way

    Should only be used on a properly copied version of the original board, so the details
    on the original board are preserved

    Input value:
    pretty_board - the current board, copied such that it will not replace the original board (deep copy required)

    Return value:
    pretty_board - the current board, updated to print better
    """

    # loop through each element of the board and if a piece is there, update
    # update to "X" if black, the piece type if white
    for i in range(len(pretty_board)):
        for j in range(len(pretty_board[i])):
            if len(pretty_board[i][j]) > 1:
                if pretty_board[i][j][1] == "Black":
                    pretty_board[i][j] = "X"
                else:
                    pretty_board[i][j] = pretty_board[i][j][0][0].upper()

    return pretty_board


if __name__ == "__main__":
    main()
