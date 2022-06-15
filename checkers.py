"""
    File: checkers.py
    Author: Luke Bradley
    Purpose: a class to be used as a library for a play checkers program
    CSC 120
"""

class Checkers():
    """creates a new checkers board object"""

    def __init__(self, state = "default"):
        """
            initializes the board using a string as
            an argument for the state of the board
            if there is no input, a default state is made
        """
        #  assert that the input is a string
        assert type(state) == str

        #  if no input is given, use the default state
        if state == "default":
            self.state = ("r r.r.r.r. .r.r.r.r r.r.r.r. ........ ........ "
                           ".b.b.b.b b.b.b.b. .b.b.b.b")

        #  use input for the state if given
        else:
            self.state = state

        assert len(self.state) == 73

        tmp_assert_check_spaces = []

        #  iterate through each part of string where
        #  there should be a space and assert it is a space
        #  while also storing index values in an array
        for i in range(1,len(self.state),9):
            assert self.state[i] == ' '
            tmp_assert_check_spaces.append(i)

        #  iterate through string and ignore all spaces using array
        for i in range(len(self.state)):
            if i in tmp_assert_check_spaces:
                pass
            else:

                #  assert values are valid
                assert (self.state[i] == 'r' or self.state[i] == 'R'
                        or self.state[i] == 'b' or self.state[i] == '.'
                        or self.state[i] == 'B')


    def __str__(self):
        """return string representing state of the board"""
        return self.state


    def get_cur_player(self):
        """
            return current player.
            used with board state as info
            for new object
        """
        if self.state[0] == 'r':
            return "red"

        elif self.state[0] == 'b':
            return "black"

    def get_square(self, x, y):
        """get state of a given space on the board"""

        #  assert type of input is valid and in valid range
        assert type(x) == int and type(y) == int
        assert x >= 0 and x <= 7
        assert y >=0 and y <= 7

        #  use y value to slice and find range of string
        #  where the lookup value is
        slice1 = y*9 + 2

        tmp = self.state[slice1:]

        #  use x value as index since string now starts
        #  according to y value
        ret_val = tmp[x]

        return ret_val

    def get_printable_string(self):
        """
            build a string to use in printing
            board
        """
        ret_val = ''

        for i in range(7,-1,-1):

            ret_val += '\n'
            ret_val += "+---+---+---+---+---+---+---+---+\n"
            slice1 = i*9 +2
            tmp = self.state[slice1:slice1+8]

            ret_val += str(i+1)

            for e in tmp:

                if e == '.':
                    ret_val += '   |'

                else:
                    ret_val += ' '
                    ret_val += e
                    ret_val += ' |'

        ret_val += "\n+-a-+-b-+-c-+-d-+-e-+-f-+-g-+-h-+\n"

        ret_val = ret_val[1:]

        return ret_val

    def get_piece_count(self, player):
        """
            return the amount of pieces a player has
        """

        #  assert input is a valid player
        assert player == 'r' or player == 'b'

        #  counters for different types of pieces
        counter_reg = 0
        counter_king = 0
        king_piece = player.upper()

        #  iterate over string starting where
        #  pieces are
        for i in range(2,len(self.state)):

            if self.state[i] == player:
                counter_reg += 1

            if self.state[i] == king_piece:
                counter_king += 1

        return (counter_reg, counter_king)


    def is_game_over(self):
        """
            return a boolean value
            for if the game is over
        """
        is_over = False

        #  check if either player has no pieces left
        r_res = self.get_piece_count('r')
        b_res = self.get_piece_count('b')

        if r_res[0] == 0 and r_res[1] == 0:
            is_over = True

        if b_res[0] == 0 and b_res[1] == 0:
            is_over = True

        return is_over


    def list_to_string(self, array):
        """converts an arrray to a string"""

        string = ''

        for e in array:
            string += e

        return string


    def string_to_2d_array(self, string):
        """converts a string into a 2d array"""

        board = []
        counter = -1

        for i in range(2,len(string),9):
            board.append([])

            counter += 1
            for j in range(8):
                if j < 8:
                    board[counter].append(string[i+j])

        return board


    def king_moves(self, board, vert_dist, horiz_dist, from_y, from_x,
                    to_y, to_x):
        """
            called when a king is moved
            checks if it is hopping a pieces
            and takes if it does
        """

        #  check who the current player is to
        #  find what pieces they should be able
        #  to take
        if self.get_cur_player() == "red":
            get_this_piece = 'b'

        elif self.get_cur_player() == "black":
            get_this_piece = 'r'

        if vert_dist > 0:
            #  if piece moves up and left
            if horiz_dist == -2:
                #  remove the hopped piece from the board
                if board[to_x-1][to_y+1].lower() == get_this_piece:
                    board[to_x-1][to_y+1] = '.'

                else:
                    #  moved 2 spaces without hopping opponents piece
                    return None

            #  if piece moves up and right
            elif horiz_dist == 2:
                #  removes hopped piece from the board
                if board[to_x-1][to_y-1].lower() == get_this_piece:
                    board[to_x-1][to_y-1] = '.'

                else:
                    #  moved 2 spaces without hopping
                    return None

        if vert_dist < 0:
                #  moved down and left
                if horiz_dist == -2:
                    #  remove hopped piece from the board
                    if board[to_x+1][to_y+1].lower() == get_this_piece:
                        board[to_x+1][to_y+1] = '.'

                    else:
                        #  moved 2 spaces without hopping opponents piece
                        return None

                #  moved down and right
                elif horiz_dist == 2:
                    #  remove hopped piece
                    if board[to_x+1][to_y-1].lower() == get_this_piece:
                        board[to_x+1][to_y-1] = '.'

                    else:
                    #  moved 2 spaces without hopping oppenents piece
                        return None

        return board


    def r_takes(self, board, vert_dist, horiz_dist, from_y, from_x,
                to_y, to_x):
        """
            called when red moves
            checks if a piece is hopped
            and removes it from the board
        """

        #  if moved left
        if horiz_dist == -2:
            #  remove opponent's piece from the board
            if board[to_x-1][to_y+1].lower() == 'b':
                board[to_x-1][to_y+1] = '.'

            else:
                #  moved 2 spaces without hopping opponent's piece
                return None
        #  if moved right
        elif horiz_dist == 2:
            #  remove opponent's piece from the board
            if board[to_x-1][to_y-1].lower() == 'b':
                board[to_x-1][to_y-1] = '.'

            else:
                # moved 2 spaces without hopping piece
                return None


    def b_takes(self, board, vert_dist, horiz_dist, from_y, from_x,
                to_y, to_x):
        """
            called when black moves
            checks if a piece is hopped
            and removes it from the board
        """

        #  if move left
        if horiz_dist == -2:
            #  remove piece from the board
            if board[to_x+1][to_y+1].lower() == 'r':
                board[to_x+1][to_y+1] = '.'

            else:
                #  moved 2 spaces without hopping
                return None

        #  moved right
        elif horiz_dist == 2:
            #  remove piece from the board
            if board[to_x+1][to_y-1].lower() == 'r':
                board[to_x+1][to_y-1] = '.'

            else:
                # moved 2 spaces without hopping
                return None


    def do_move(self, frm, to):
        """
            perform a move and create a new
            checkers object
        """
        #  assert input is good
        assert type(frm) == str
        assert type(to) == str
        assert len(frm) == 2 and len(to) == 2
        assert frm[0].isalpha() and to[0].isalpha()
        assert frm[1].isnumeric() and to[1].isnumeric()

        #  convert input to integers
        from_y = ord(frm[0]) -97
        from_x = int(frm[1]) -1
        to_y = ord(to[0]) -97
        to_x = int(to[1]) -1
        #  calculate distance moved
        vert_dist = to_x - from_x
        horiz_dist = to_y - from_y


        if abs(vert_dist) > 2:
            #  moved too far up or down
            return None

        if abs(horiz_dist) > 2:
            #  moved too far left or right
            return None

        if vert_dist == 0:
            #  must move up or down
            return None

        if horiz_dist == 0:
            #  must move left or right
            return None

        if abs(vert_dist) == 2:
            if abs(horiz_dist) != 2:
                #  if moved vertically 2 spaces
                #  must move horizontally 2 spaces
                return None

        if abs(horiz_dist) == 2:
            if abs(vert_dist) != 2:
                #  if moved horizontally 2 spaces
                #  must move vertically 2 spaces
                return None

        #  convert string to 2d array
        board = self.string_to_2d_array(self.state)

        if board[from_x][from_y].lower() != self.state[0]:
            #  if wrong player moves or
            #  attempt to move empty space
            return None

        if board[from_x][from_y] == 'r':
            if vert_dist < 0:
                #  must move up if piece is 'r'
                return None

        if board[from_x][from_y] == 'b':
            if vert_dist > 0:
                #  must move down if piece is 'b'
                return None


        if board[to_x][to_y] != '.':
            #  must move to empty space
            return None

        #  attempting to hop a piece
        if abs(vert_dist) == 2:
            #  if using a king
            if board[from_x][from_y] == 'R' or board[from_x][from_y] == 'B':
                board = self.king_moves(board, vert_dist, horiz_dist,
                                        from_y, from_x, to_y, to_x)

            #  if using 'r'
            if board[from_x][from_y] == 'r':

                self.r_takes(board, vert_dist, horiz_dist,
                            from_y, from_x, to_y, to_x)

            #  if using 'b'
            elif board[from_x][from_y] == 'b':

                self.b_takes(board, vert_dist, horiz_dist,
                            from_y, from_x, to_y, to_x)

        #  move piece to new space
        board[to_x][to_y] = board[from_x][from_y]
        board[from_x][from_y] = '.'

        #  change piece to king if it rieces the end
        if to_x == 7 or to_x == 0:
            board[to_x][to_y] = board[to_x][to_y].upper()

        ret_val = self.state[0]

        #  change turns
        if ret_val == 'r':
            ret_val = 'b'

        elif ret_val == 'b':
            ret_val = 'r'

        #  convert array back to string
        for e in board:
            ret_val += ' '
            string2 = self.list_to_string(e)
            ret_val += string2

        return Checkers(ret_val)



def main():
    """
        Main function to play game of
        checkers with another person
    """
    board = Checkers()

    while True:

        print(board.get_printable_string())
        inputed = input()
        inputed = inputed.split()

        i = inputed[0]
        j = inputed[1]

        if board.do_move(i,j) == None:
            print("invalid move")
            continue
        board = board.do_move(i,j)


    if __name__ == "__main__":
        main()

board = Checkers()

while True:

    print(board.get_printable_string())
    inputed = input()
    inputed = inputed.split()

    i = inputed[0]
    j = inputed[1]

    if board.do_move(i,j) == None:
        print("invalid move")
        continue
    board = board.do_move(i,j)