
class GameState:
    
    def __init__(self,
                 rows: int,
                 cols: int,
                 first_move_player: "B or W",
                 top_left_disk: "B or W",
                 winning_method: "M for most or L for least") -> None:
        
        """ Get the game of Othello started
        """
        
        self.rows = rows
        self.cols = cols

        self._demand_valid_board()
        
        self.winner = None
        self.current_turn = first_move_player
        self._top_left_disk = top_left_disk
        self.winning_method = winning_method
        
        
        self._create_blank_game_board()
        self._set_up_the_board()
        self._calc_score()


    def drop_piece(self, row, col) -> None:
        """ Drop piece @ row&col and switch turns if it is a valid move for
        the current player; if it is not, raise an error
        """
        self._demand_valid_row_col(row, col)
        self._demand_game_not_over()
        
        if self.board[row][col] == ' ':
            disks_to_flip = self._find_all_flips_for_cell(row,col)
            if disks_to_flip != []:
                self._flip_disks(disks_to_flip)                        
                self.switch_turn()
                self._calc_score()

            else:
                raise InvalidMoveError()
        else:
            raise InvalidMoveError()
            

    def switch_turn(self) -> None:
        """ Switch the current turn to the opposite player
        """
        self.current_turn = self._opposite_turn(self.current_turn)


    def are_any_valid_moves(self) -> bool:
        """ Return True if there are any valid moves on the board for
        the current player
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == ' ':
                    if self._find_all_flips_for_cell(row, col) != []:
                        return True
        return False


    def _opposite_turn(self, player: 'B or W') -> str:
        """ Return the opposite turn of the current player
        """
        if player == 'B':
            return 'W'
        else:
            return 'B'


    def _find_all_flips_for_cell(self, row:int, col:int) -> [tuple]:
        """ Return the coordinates of all the flips in all possible
        directions if the current player's disk were to be dropped @ row&col;
        if there is no flips to be made, return an empty list
        """
        rowdelta_range = self._calc_valid_rowdelta_range(row) #optional
        coldelta_range = self._calc_valid_coldelta_range(col) #optional
        disks_to_flip = []
        
        for rowdelta in rowdelta_range:
            for coldelta in coldelta_range:
                if self._is_next_to_opposite_in_d(row,col,rowdelta,coldelta):
                    one_d_flips = self._find_flips_in_one_direction(row, col, rowdelta, coldelta)
                    if one_d_flips != []: #optional
                        disks_to_flip.extend(one_d_flips)
        if disks_to_flip != []:
            disks_to_flip.append((row,col))
        return disks_to_flip


    def _find_flips_in_one_direction(self, row, col, rowdelta, coldelta) -> [tuple]:
        """ Return the coordinates of all the flips in one specified
        direction if the current player's disk were to be dropped @ row&col;
        if there is no flips to be made, return an empty list
        """
        i = 0

        disks_to_flip = []

        current_cells = []

        while self._is_valid_row(row+rowdelta*(i+1)) and self._is_valid_col(col+coldelta*(i+1)):
            i += 1
            current_row = row+rowdelta*i
            current_col = col+coldelta*i

            if self.board[current_row][current_col] == self.current_turn and i != 1:
                disks_to_flip = current_cells
                break
            elif self.board[current_row][current_col] == ' ':
                break
            elif self.board[current_row][current_col] == self._opposite_turn(self.current_turn):
                current_cells.append((current_row, current_col))
                
        return disks_to_flip
    

    def _flip_disks(self, disks_to_flip:[tuple]) -> None:
        """ Flip all disks at the coordinators given by the list disks_to_flip
        """
        for row,col in disks_to_flip:
            self.board[row][col] = self.current_turn
    

    def _calc_valid_rowdelta_range(self, row:int) -> range:
        """ Return the valid rowdelta range, depending on whether
        the row is the first/last row
        """
        if 0 < row < self.rows -1:
            return range(-1, 2)
        elif row == 0:
            return range(0, 2)
        elif row == self.rows - 1:
            return range(-1, 1)


    def _calc_valid_coldelta_range(self, col:int) -> range:
        """ Return the valid coldelta range, depending on whether
        the column col is the first/last column
        """
        if 0 < col < self.cols -1:
            return range(-1, 2)
        elif col == 0:
            return range(0, 2)
        elif col == self.cols - 1:
            return range(-1, 1) 


    def _is_next_to_opposite_in_d(self, row, col, rowdelta, coldelta) -> bool:
        """ Return True if the cell @ row&col is next to the opposite player in
        the direction specified by the rowdelta and coldelta
        """
        if self._is_valid_row(row+rowdelta) and self._is_valid_col(col+coldelta):
            return self.board[row+rowdelta][col+coldelta] == self._opposite_turn(self.current_turn)
        return False

# scoring
    
    def _calc_score(self) -> None:
        """ Calculate the current score of the game, and set the score variable
        equal to the the tuple of the number of Black and White disks on the
        board
        """
        ws = 0
        bs = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'B':
                    bs += 1
                elif self.board[r][c] == 'W':
                    ws += 1
                    
        self.score = (bs, ws)
                
        
    def determine_winner(self) -> None:
        """ Determine the winner by the specified method (L for least or M for
        most), and set the winner variable of GameState object equal to the
        winner (T is for tie)
        """
        
        Bs = self.score[0]
        Ws = self.score[1]
                    
        if Ws < Bs:
            if self.winning_method == 'L':
                self.winner = 'W'
            else:
                self.winner = 'B'
            
        elif Ws > Bs:
            if self.winning_method == 'L':
                self.winner = 'B'
            else:
                self.winner = 'W'
                
        elif Ws == Bs:
            self.winner = 'T'

# assertions
            
    def _demand_valid_row_col(self, row:int, col:int) -> None:
        """ Raise an error if either row or col is invalid
        """
        if not (self._is_valid_row(row) or self._is_valid_col(col)):
            raise InvalidRowColNumberError()


    def _demand_game_not_over(self) -> None:
        """ Raises an error if the winner has already been determined
        """
        if self.winner != None:
            raise GameOverError()


    def _is_valid_col(self, col:int) -> bool:
        """ Return True if the column number is valid
        """
        return 0 <= col < self.cols


    def _is_valid_row(self, row:int) -> bool:
        """ Return True if the row number is valid
        """
        return 0 <= row < self.rows

# set up
    
    def _set_up_the_board(self) -> None:
        """ Set up the board that is newly created with the 4 disks in the
        middle as specified by the parameters passed to the object GameState
        """
        top_left_row = int(self.rows/2) - 1
        top_left_col = int(self.cols/2) -1
        
        self.board[top_left_row][top_left_col] = self._top_left_disk
        self.board[top_left_row + 1][top_left_col + 1] = self._top_left_disk

        secondary_player = self._opposite_turn(self._top_left_disk)
        self.board[top_left_row][top_left_col + 1] = secondary_player
        self.board[top_left_row + 1][top_left_col] = secondary_player

    
    def _create_blank_game_board(self) -> None:
        """ Create a new game board that is blank
        """
        board = []
        for r in range(self.rows):
            cols = []
            for c in range(self.cols):
                cols.append(' ')
            board.append(cols)
        self.board = board

    
    def _demand_valid_board(self) -> None:
        """ Raises an error if the given number of row and/or columns is not
        valid
        """
        if type(self.rows) != int or type(self.cols) != int:
            raise InvalidBoardRowsCols()
        elif not(4 <= self.rows <= 16) or not (4 <= self.cols <= 16):
            raise InvalidBoardRowsCols()
        elif self.rows%2 == 1 or self.cols%2 == 1:
            raise InvalidBoardRowsCols()
                            
class InvalidMoveError(Exception):
    """ Raised when there's an attempt to make an invalid move 
    """
    

class InvalidPlayerError(Exception):
    """ Raised when the player is not listed as 'B' or 'W'
    """
    pass


class InvalidRowColNumberError(Exception):
    """ Raised when the row or column number is not valid, according to
    the rows and cols in the already existing board 
    """
    pass


class InvalidBoardRowsCols(Exception):
    """ Raised when the total number of rows and columns for the board are not
    an integer between 4 and 16
    """
    pass


class GameOverError(Exception):
    """ Raised when the game is over
    """
    pass

