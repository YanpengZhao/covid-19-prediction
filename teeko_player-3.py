import random
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        move = []
        maxval = 0
        tochoose = None
        aq = 0
        for elem in state:
            for n in elem:
                if n == self.my_piece or n == self.opp:
                    aq = aq + 1
        for succ in self.succ(state):
            if self.game_value(succ)==1:
                tochoose=succ
                break
            if aq<8:
                fornow=self.Max_Value(succ,1)
            else:
                fornow = self.Max_Value(succ, 0)
            if fornow > maxval:
                maxval = fornow
                tochoose = succ
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece and state[i][j] != tochoose[i][j]:
                    move.append((i, j))
                if tochoose[i][j] == self.my_piece and tochoose[i][j] != state[i][j]:
                    move.insert(0, (i, j))
        return move

    def Max_Value(self, state, depth):
        """
        max-value
        """
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state)
        # TODO: change it to be within 5s
        elif depth > 2:
            return self.heuristic_game_value(state)
        else:
            alpha = -999
            succ = self.succ(state)
            for s in succ:
                alpha = max(alpha, self.Min_Value(s, depth + 1))
        return alpha

    def Min_Value(self, state, depth):
        """
        min-value
        """
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state)
        elif depth > 2:
            return self.heuristic_game_value(state)
        else:
            beta = 999
            succ = self.succ(state)
            for s in succ:
                beta = min(beta, self.Max_Value(s, depth + 1))
        return beta

    def succ(self, state):
        toreturn = []
        aw = 0
        for elem in state:
            for n in elem:
                if n == self.my_piece or n == self.opp:
                    aw = aw + 1
        if aw < 8:
            for iu in range(len(state)):
                for ju in range(len(state)):
                    if state[iu][ju] == " ":
                        import copy
                        succ_state = copy.deepcopy(state)
                        succ_state[iu][ju] = self.my_piece
                        toreturn.append(succ_state)
            return toreturn
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece:
                    for k in range(i - 1, i + 2):
                        for u in range(j - 1, j + 2):
                            if k < 0 or k >= len(state) or u < 0 or u >= len(state[i]):
                                continue
                            if state[k][u] != " ":
                                continue
                            import copy
                            succ_state = copy.deepcopy(state)
                            succ_state[i][j] = " "
                            succ_state[k][u] = self.my_piece
                            toreturn.append(succ_state)

        return toreturn

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def heuristic_game_value(self, state):
        if self.game_value(state) != 0:
            return self.game_value(state)
        my_score = 0
        for row in state:
            for i in range(3):
                if row[i] == self.my_piece and row[i] == row[i + 1] == row[i + 2]:
                    my_score = my_score + 3
                    break
        for col in range(5):
            for i in range(3):
                if state[i][col] == self.my_piece and state[i][col] == state[i + 1][col] == state[i + 2][col]:
                    my_score = my_score + 3
                    break
        for y in range(2):
            for i in range(2):
                if state[y][i] == self.my_piece and state[y][i] == state[y + 1][i + 1] == state[y + 2][i + 2]:
                    my_score = my_score + 3
                    break
        for y in range(4, 2):
            for i in range(2):
                if state[y][i] == self.my_piece and state[y][i] == state[y - 1][i + 1] == state[y - 2][i + 2]:
                    my_score = my_score + 3
                    break

        for y in range(4):
            for i in range(4):
                if state[y][i] == self.my_piece:
                    count = 0
                    if state[y + 1][i + 1] == self.my_piece:
                        count = count + 1
                    if state[y + 1][i] == self.my_piece:
                        count = count + 1
                    if state[y][i + 1] == self.my_piece:
                        count = count + 1
                    my_score = my_score + count

        return my_score/25
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1
        for y in range(2):
            for i in range(2):
                if state[y][i] != " " and state[y][i] == state[y + 1][i + 1] == state[y + 2][i + 2] == state[y + 3][
                    i + 3]:
                    return 1 if state[y][i] == self.my_piece else -1
        for y in range(4, 2):
            for i in range(2):
                if state[y][i] != " " and state[y][i] == state[y - 1][i + 1] == state[y - 2][i + 2] == state[y - 3][
                    i + 3]:
                    return 1 if state[y][i] == self.my_piece else -1
        for y in range(4):
            for i in range(4):
                if state[y][i] != " " and state[y][i] == state[y + 1][i] == state[y + 1][i + 1] == state[y][i + 1]:
                    return 1 if state[y][i] == self.my_piece else -1
        # TODO: check \ diagonal wins
        # TODO: check / diagonal wins
        # TODO: check 2x2 box wins

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
        print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                  (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
