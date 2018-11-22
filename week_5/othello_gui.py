from tkinter import *
from tkinter import messagebox
import othello_module
import othello_ai
import time

HICOLOR = '#598987' # lime
LOCOLOR = '#678F8D' # lilac

class OthelloMenu:
    """ The Class represents the Menu of the Othello game;
    after the options have been selected, it creates an OthelloGame object
    """

    def __init__(self) -> None:
        """ Start the Menu & restart the game if wanted
        """
        self._continue = True
        self._run_menu()
        while self._continue:
            self._restart()
            if self._continue:
                self._run_menu()
                
    
    def _run_menu(self) -> None:
        """ Display the available options for the game of Othello
        """
        self._create_main_menu_root_window()

        self._place_gamename_label()
        self._place_option_menu_row_number()
        self._place_option_menu_col_number()
        self._place_option_menu_first_move_player()
        self._place_option_menu_top_left_disk()
        self._place_option_menu_winning_method()
        self._place_button_box_for_start_cancel()

        self._root_window.mainloop()


    def _create_main_menu_root_window(self) -> None:
        self._root_window = Tk()
        self._root_window.title('REVERSI v.2.01')
        self._root_window.resizable(False,False)
        self._root_window.config(bg='black')


    def _place_gamename_label(self) -> None:
        Label(master=self._root_window, text = 'REVERSI',
            width = 12, height=1, relief = SUNKEN,
            borderwidth=5, background=HICOLOR,
            font = ('Adobe Devanagari',25)).grid(row=0,column=0,columnspan=2)


    def _place_option_menu_row_number(self) -> None:
        text = 'Number of rows: '
        Label(master=self._root_window, text=text, bg='black', foreground='white').grid(row=1,column=0)
        self._row_var = StringVar()
        self._row_var.set('6')
        r_om = OptionMenu(self._root_window, self._row_var, '4','6','8','10','12','14','16')
        r_om.grid(row=1,column=1)
        r_om.config(bg='black')


    def _place_option_menu_col_number(self) -> None:
        text = 'Number of columns: '
        Label(master=self._root_window, text=text, bg='black', foreground='white').grid(row=2,column=0)
        self._col_var = StringVar()
        self._col_var.set('6')
        c_om = OptionMenu(self._root_window, self._col_var, '4','6','8','10','12','14','16')
        c_om.grid(row=2,column=1)
        c_om.config(bg='black')


    def _place_option_menu_first_move_player(self) -> None:
        text = 'Choose the first move player: '
        Label(master=self._root_window, text=text, bg='black', foreground='white').grid(row=3,column=0)
        self._first_move_player_var = StringVar()
        self._first_move_player_var.set('Black')
        fm_om = OptionMenu(self._root_window, self._first_move_player_var, 'Black', 'White')
        fm_om.grid(row=3,column=1)
        fm_om.config(bg='black')


    def _place_option_menu_top_left_disk(self) -> None:
        text = 'Choose the top left disk: '
        Label(master=self._root_window, text=text, bg='black', foreground='white').grid(row=4,column=0)
        self._top_left_disk_var = StringVar()
        self._top_left_disk_var.set('Black')
        tl_om=OptionMenu(self._root_window, self._top_left_disk_var, 'Black', 'White')
        tl_om.grid(row=4,column=1)
        tl_om.config(bg='black')

    def _place_option_menu_winning_method(self) -> None:
        text = 'Choose the winning method: '
        Label(master=self._root_window, text=text, bg='black', foreground='white').grid(row=5,column=0)
        self._winning_method_var = StringVar()
        self._winning_method_var.set('Most')
        wm_om=OptionMenu(self._root_window, self._winning_method_var, 'Most', 'Least')
        wm_om.grid(row=5,column=1)
        wm_om.config(bg='black')

    def _place_button_box_for_start_cancel(self) -> None:
        button_box = Frame(self._root_window)
        button_box.grid(row=6, column=0, columnspan=2)

        start_button = Button(master=button_box, text='START', command=self._on_start_button_clicked)
        start_button.pack(side=LEFT)
        cancel_button = Button(master=button_box, text='CANCEL', command=self._on_cancel_button_clicked)
        cancel_button.pack(side=RIGHT)

    
    def _restart(self) -> None:

        self._restart_root = Tk()
        self._restart_root.title('Restart Othello?')
        self._restart_root.resizable(False,False)

        _label = Label(master = self._restart_root, text = 'Would you like to restart the game?', width = 30, height = 2, borderwidth=2, background = HICOLOR, font = ('Comic Sans MS', 20)).grid(row=0,column=0,columnspan=2)

        ##BUTTONS
        button_box = Frame(master=self._restart_root)
        button_box.grid(row=1,column=0, columnspan=2)
        yes_button = Button(master=button_box, text = 'YES!',
                            command=self._on_yes_clicked).pack(side=LEFT)
        no_button = Button(master=button_box, text = 'No',
                            command=self._on_no_clicked).pack(side=RIGHT)

        self._restart_root.config(bg = 'black')

        self._restart_root.mainloop()       

    
    def _on_yes_clicked(self) -> None:
        self._restart_root.destroy()
    
    
    def _on_no_clicked(self) -> None:
        self._continue = False
        self._restart_root.destroy()
        

    def _on_start_button_clicked(self) -> None:
        """ Create a new GameState object from the info obtained from
        the menu fields
        """
        self._root_window.destroy()

        self._rows = int(self._row_var.get())
        self._cols = int(self._col_var.get())
        self._first_move = self._word_to_letter(self._first_move_player_var.get())
        self._top_left_disk = self._word_to_letter(self._top_left_disk_var.get())
        self._winning_method = self._word_to_letter(self._winning_method_var.get())

        self.game = othello_module.GameState(self._rows, self._cols, self._first_move, self._top_left_disk, self._winning_method)

        OthelloGame(self.game, 'M')
        
        
    def _on_cancel_button_clicked(self) -> None:
        """ Implement the ation of the CANCEL button - close the menu window
        without proceding with the game
        """
        self._root_window.destroy()
        self._continue = False

    
    def _word_to_letter(self, word: str) -> str:
        """ Return the letter that the given word starts with
        """
        return word[0]



class OthelloGame:
    """ The class implements the GUI of Othello Game by using the
        GameState object
    """
    def __init__(self, game_state: othello_module.GameState, level: str) -> None:
        """ Create a window that holds the game canvas and the game information
        inside it
        """
        self._game_state = game_state
        
        self._AI = othello_ai.AI(game_state.winning_method, level) #####
        self._ai_player = 'W'      #####
        
        self._root_window = Tk()
        self._root_window.title('OTHELLO v.2.01')
        self._root_window.config(bg='black')
        self._canvas = Canvas(master=self._root_window, width=600, height=600,
                              background = HICOLOR)
        
        if self._game_state.current_turn == self._ai_player: #####
            self._make_ai_move()
            
        self._canvas.grid(row=1,column=0, padx=20,pady=20, sticky = N + S + E + W)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._score_box = Frame(self._root_window)
        self._score_box.config(bg='black')
        self._score_box.grid(row=0,column=0, padx=5,pady=5, sticky = N)###

        self._display_turn()
        self._display_score()

        
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)


    def _on_canvas_resized(self, event: Event) -> None:
        """ Redraw the canvas with all its elements when the root window
        is resized (also recalculates the window fractions)
        """
        self._redraw_canvas()

    
    def _on_canvas_clicked(self, event: Event) -> None:
        """ Drop the piece into the row&column if it is a valid move;
        if the next move is not valid for the current player, inform the
        user via a popup window; if there are no moves for either of the
        players, the game is over
        """
        self._calculate_fractions()
        self._get_row_col_from_click(event.x, event.y)
        self._handle_move()
        self._check_next_move()
        
        while self._game_state.current_turn == self._ai_player and self._game_state.winner == None: #####
            self._root_window.after(1000)
            self._AI.make_move(self._game_state)
            self._redraw_canvas()
            self._check_next_move()
            
    def _check_next_move(self) -> None:
        if self._game_state.winner == None:
            if self._game_state.are_any_valid_moves():
                pass
            else:
                self._game_state.switch_turn()
                self._redraw_canvas()
                if not self._game_state.are_any_valid_moves():
                    self._game_state.determine_winner()
                    self._compile_winner_message()
                    self._game_over_window()
                else:
                    text = "There is no moves for the other player."
                    messagebox.showinfo(message=text)
                    return False

        

    def _redraw_canvas(self) -> None:
        """ Redraw the canvas window with all its elements after having
        recalculated the fractional positions of those elements
        """
        self._calculate_fractions()
        self._canvas.delete(ALL)
        self._score_label.destroy()
        self._turn_label.destroy()

        self._draw_grid()
        self._draw_all_disks()
        self._display_turn()
        self._display_score()
        self._root_window.update()

# Gameplay

    def _handle_move(self) -> None:
        """ If the game is not over & there are valid moves, procede to
        dropping a piece
        """
        if self._game_state.winner == None and self._game_state.are_any_valid_moves():
            self._drop_piece()
        
    
    def _drop_piece(self) -> None:
        """ Drop a piece into row and col specified by self._current_coordinate
        tuple if it is a valid move
        """
        try:
            self._game_state.drop_piece(self._current_coordinate[0],
                                        self._current_coordinate[1])
            self._redraw_canvas()
            
        except othello_module.InvalidMoveError:
            pass

    def _make_ai_move(self) -> None:
        self._AI.make_move(self._game_state)

    def _get_row_col_from_click(self, x: 'x-coord', y: 'y-coord') -> None:
        """ Find what row and col, according to the grid, the x and y
        mouse click coordinates are in
        """
        for r in range(self._game_state.rows):
            if r * self._row_width <= y < (r+1) * self._row_width:
                row = r
        for c in range(self._game_state.cols):
            if c * self._col_width <= x < (c+1) * self._col_width:
                col = c

        self._current_coordinate = (row,col)

    def _game_over_window(self) -> None:
        self._game_over_window = Tk()
        self._game_over_window.title('GAME OVER')
        message = "The game is over! {}".format(self._winner_message)
        Label(master=self._game_over_window, text = message,
              bg=HICOLOR, font=('Times New Roman', 23)).grid(row=0, column=0)
        Label(master=self._game_over_window, text="Black: {}\nWhite: {}".format(self._game_state.score[0], self._game_state.score[1]),
              bg='black', foreground='#FFFFFF', font=('Times New Roman', 25)).grid(row=1,column=0)
        Button(master=self._game_over_window, text = 'OK', command=self._on_ok_clicked).grid(row=2,column=0)
        self._game_over_window.config(bg='black')
        self._game_over_window.mainloop()

    def _on_ok_clicked(self) -> None:
        self._root_window.destroy()
        self._game_over_window.destroy()
        
### Scoring & Turns
        
    def _display_turn(self) -> None:
        """ Display the current turn on the side of the game canvas
        """
        turn = "{}'s turn".format(self._letter_to_name(self._game_state.current_turn))
        if self._game_state.current_turn == 'B':
            background_color, foreground_color = 'black',LOCOLOR
        else:
            background_color, foreground_color = HICOLOR,'black'
            
        self._turn_label = Label(master=self._score_box, text=turn,
                                 width=50, height=2, relief = SUNKEN,
                                 background = background_color,
                                 foreground = foreground_color,
                                 font=('Times New Roman', 25))
        self._turn_label.pack()

    def _display_score(self) -> None:
        """ Display the current score on the side of the game canvas
        """
        score = "Black: {}\nWhite: {}".format(self._game_state.score[0],
                                              self._game_state.score[1])
        self._score_label = Label(master=self._score_box, text=score, width = 10, height = 2, relief = GROOVE, background = LOCOLOR, font=('Times New Roman', 20))
        self._score_label.pack()
        
        
    def _letter_to_name(self, letter: str) -> str:
        """ Return Black for letter B and White for letter W
        """
        if letter == 'B':
            return "Black"
        elif letter == 'W':
            return "White"
        
    def _compile_winner_message(self) -> None:
        """ Put together the message containing the gameover information
        """
        if self._game_state.winner == 'B' or self._game_state.winner == 'W':
            message = "{} player has won!".format(self._letter_to_name(self._game_state.winner))
            message += "\nCongratulations!"

        else:
            message = "It is a tie! (There's no winner)"
            
        self._winner_message = message

### Drawing
        
    def _calculate_fractions(self) -> None:
        """ Calculate the fractional positions of the columns and rows on the
            canvas with respect to the canvas' size
        """
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()

        self._col_width = self._canvas_width/self._game_state.cols
        self._row_width = self._canvas_height/self._game_state.rows 
        

    def _draw_all_disks(self) -> None:
        """ Draw all disks on the game canvas
        """ 
        for r in range(self._game_state.rows):
            for c in range(self._game_state.cols):
                if self._game_state.board[r][c] == ' ':
                    pass
                else:
                    self._draw_disk(r,c, self._game_state.board[r][c])
                

    def _draw_disk(self, row: int, col: int, player: 'B or W') -> None:
        """ Call the appropriate color function to draw one disk on the game
        canvas at row and column 'col'
        """
        y1 = self._row_width * row
        y2 = self._row_width * (row +1)
        x1 = self._col_width * col
        x2 = self._col_width * (col+1)

        if player == 'B':
            self._draw_b_disk_at_xy(x1,y1,x2,y2)
        else:
            self._draw_w_disk_at_xy(x1,y1,x2,y2)
        

    def _draw_b_disk_at_xy(self, x1:int,y1:int,x2:int,y2:int) -> None:
        """ Draw a black disk at the given coordinates
        """
        self._canvas.create_oval(x1,y1,x2,y2, fill = 'black')
        

    def _draw_w_disk_at_xy(self, x1:int,y1:int,x2:int,y2:int) -> None:
        """ Draw a white disk at the ginve coordinates
        """
        self._canvas.create_oval(x1,y1,x2,y2, fill = 'white')


    def _draw_grid(self) -> None:
        """ Draw the game board grid on game canvas
        """
        rows = self._game_state.rows 
        cols = self._game_state.cols

        self._col_width = self._canvas_width/cols
        self._row_width = self._canvas_height/rows

        for c in range(cols):
            self._draw_vertical_at_x(self._col_width*c, self._canvas_height)

        for r in range(rows):
            self._draw_horisontal_at_y(self._row_width*r, self._canvas_width)
            

    def _draw_vertical_at_x(self, x: int, canvas_height: int) -> None:
        """ Draw a vertical line across the canvas at the x coordinate
        """
        self._canvas.create_line(x, 0, x, canvas_height)


    def _draw_horisontal_at_y(self, y: int, canvas_width: int) -> None:
        """ Draw a horisontal line across the canvas at the y coordinate
        """
        self._canvas.create_line(0, y, canvas_width, y)
        
            
if __name__ == "__main__":
    OthelloMenu()
