import tkinter as tk
from tkinter import messagebox
import logic

#global variables
root = None
cells = []
status_label = None
keyboard_buttons = {}

def create_gui():
    global root, cells, status_label
    
    #start game logic, will move soon or merge with main.py later
    if not logic.start_game():
        print("cant start game")
        return
    
    root = tk.Tk()
    root.title("Wordle")
    root.geometry("400x600")
    root.minsize(350, 550)
    root.configure(bg='white')
    
    #grid weights for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    #main container
    main_frame = tk.Frame(root, bg='white')
    main_frame.grid(row=0, column=0, sticky='nsew') #nsew = north, south, east, west
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    #top bar with title and icons
    top_bar = tk.Frame(main_frame, bg='white', height=40)
    top_bar.grid(row=0, column=0, sticky='ew', pady=2) #ew = east, west
    top_bar.grid_propagate(False)
    top_bar.grid_columnconfigure(1, weight=1)
    
    #help icon (left)
    help_icon = tk.Label(top_bar, text="?", font=('Arial', 14), bg='white', fg='black')
    help_icon.grid(row=0, column=0, padx=10)
    
    #title (wordle word)
    title = tk.Label(top_bar, text="WORDLE", font=('Arial', 24, 'bold'), bg='white', fg='black')
    title.grid(row=0, column=1, padx=15)
    
    #icons (right), i was trying to match the image in the task as much as possible
    stats_icon = tk.Label(top_bar, text="📊", font=('Arial', 14), bg='white', fg='black')
    stats_icon.grid(row=0, column=2, padx=3)
    
    settings_icon = tk.Label(top_bar, text="⚙", font=('Arial', 14), bg='white', fg='black')
    settings_icon.grid(row=0, column=3, padx=10)
    
    #game area (grid + keyboard)
    game_area = tk.Frame(main_frame, bg='white')
    game_area.grid(row=1, column=0, sticky='nsew', padx=5, pady=0)
    game_area.grid_rowconfigure(0, weight=1)
    game_area.grid_rowconfigure(1, weight=0)
    game_area.grid_columnconfigure(0, weight=1)
    grid_frame = tk.Frame(game_area, bg='white')
    grid_frame.grid(row=0, column=0, pady=0)
    
    cells = []
    for row in range(6):
        row_cells = []
        for col in range(5):
            cell = tk.Label(grid_frame, width=4, height=2, font=('Arial', 20, 'bold'), 
                          bg='white', fg='black', relief='solid', bd=2,
                          anchor='center')
            cell.grid(row=row, column=col, padx=0, pady=0, sticky='nsew')
            row_cells.append(cell)
        cells.append(row_cells)
    
    for i in range(6):
        grid_frame.grid_rowconfigure(i, weight=1)
    for i in range(5):
        grid_frame.grid_columnconfigure(i, weight=1)
    
    #create virtual keyboard, the function is down in this file
    create_keyboard(game_area)
    
    #status
    status_label = tk.Label(game_area, text="", font=('Arial', 12), bg='white', fg='black')
    status_label.grid(row=2, column=0, pady=0)
    
    #keyboard events
    root.bind('<Key>', handle_key)
    root.bind('<Return>', submit_guess)
    root.bind('<BackSpace>', handle_backspace)
    
    #bind resize to the function defined below
    root.bind('<Configure>', on_resize)
    
    root.focus_set()
    root.mainloop()

def on_resize(event): #function to handle resizing the window
    if hasattr(root, 'winfo_width') and hasattr(root, 'winfo_height'):
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        cell_size = min(window_width // 8, window_height // 12)  
        font_size = max(12, min(24, cell_size // 3))
        
        #update all cells
        for row in cells:
            for cell in row:
                cell.configure(font=('Arial', font_size, 'bold'))
        
        #update keyboard font size
        keyboard_font_size = max(8, min(14, window_width // 50))
        for btn in keyboard_buttons.values():
            if btn.cget('text') == 'ENTER':
                btn.configure(font=('Arial', max(6, keyboard_font_size-2), 'bold'))
            elif btn.cget('text') == '⌫':
                btn.configure(font=('Arial', keyboard_font_size, 'bold'))
            else:
                btn.configure(font=('Arial', keyboard_font_size, 'bold'))

def create_keyboard(parent):
    global keyboard_buttons
    
    keyboard_frame = tk.Frame(parent, bg='white')
    keyboard_frame.grid(row=1, column=0, pady=0, sticky='ew')
    keyboard_frame.grid_columnconfigure(0, weight=1)
    
    #keyboard layout, tried to do something different for the enter and backspace buttons but didnt work
    rows = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
    ]
    
    for row_idx, row in enumerate(rows):
        row_frame = tk.Frame(keyboard_frame, bg='white')
        row_frame.pack(pady=0, fill='x')
        
        # Configure row to expand
        row_frame.grid_columnconfigure(0, weight=1)
        
        for letter in row:
            if letter == 'ENTER':
                btn = tk.Button(row_frame, text=letter, height=2, 
                              font=('Arial', 8, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=submit_guess)
            elif letter == '⌫':
                btn = tk.Button(row_frame, text=letter, height=2,
                              font=('Arial', 10, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=lambda: handle_backspace(None))
            else:
                btn = tk.Button(row_frame, text=letter, height=2,
                              font=('Arial', 10, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=lambda l=letter: handle_key_click(l))
            btn.pack(side='left', padx=1, fill='x', expand=True)
            keyboard_buttons[letter] = btn

def handle_key_click(letter):
    if logic.is_game_lost() or logic.is_game_won():
        return
    
    current_row = len(logic.guessed_words)
    current_col = len([c for c in cells[current_row] if c.cget("text")])
    
    if current_col < 5:
        cells[current_row][current_col].config(text=letter)

def handle_key(event):
    if logic.is_game_lost() or logic.is_game_won():
        return
    
    current_row = len(logic.guessed_words)
    current_col = len([c for c in cells[current_row] if c.cget("text")])
    
    if event.char.isalpha() and current_col < 5:
        cells[current_row][current_col].config(text=event.char.upper())

def handle_backspace(event):
    if logic.is_game_lost() or logic.is_game_won():
        return
    
    current_row = len(logic.guessed_words)
    current_col = len([c for c in cells[current_row] if c.cget("text")])
    
    if current_col > 0:
        current_col -= 1
        cells[current_row][current_col].config(text="")

def submit_guess(event=None):
    if logic.is_game_lost() or logic.is_game_won():
        return
    
    current_row = len(logic.guessed_words)
    
    #Get word
    word = ""
    for col in range(5):
        letter = cells[current_row][col].cget("text")
        word += letter.lower() if letter else " "
    
    word = word.strip()
    
    #submit to logic
    success, feedback = logic.submit_guess(word)
    if not success:
        status_label.config(text=feedback)
        return
    
    #clear status message
    status_label.config(text="")
    
    #color the row
    color_row(current_row, feedback)
    update_keyboard_colors()
    
    #check win/lose
    if logic.is_game_won():
        status_label.config(text=f"Won in {len(logic.guessed_words)} tries!")
        result = messagebox.askyesno("Win!", f"You won in {len(logic.guessed_words)} tries!\n\nPlay again?")
        if result:
            new_game()
    elif logic.is_game_lost():
        status_label.config(text=f"Lost! Word was: {logic.current_word}")
        result = messagebox.askyesno("Lose!", f"Word was: {logic.current_word}\n\nPlay again?")
        if result:
            new_game()

def color_row(row, feedback):
    colors = {'G': '#6aaa64', 'Y': '#c9b458', 'B': '#3a3a3c'}
    for col in range(5):
        color = colors.get(feedback[col], '#3a3a3c')
        cells[row][col].config(bg=color, fg='white')

def update_keyboard_colors():
    colors = logic.get_keyboard_colors()
    for letter, color in colors.items():
        if letter in keyboard_buttons:
            keyboard_buttons[letter].config(bg=color, fg='white' if color != '#d3d6da' else 'black')

def new_game():
    #restart logic
    logic.start_game()
    
    #clear grid
    for row in range(6):
        for col in range(5):
            cells[row][col].config(text="", bg='white', fg='black')
    
    #reset keyboard colors
    for btn in keyboard_buttons.values():
        btn.config(bg='#d3d6da', fg='black')
    
    #clear status
    status_label.config(text="")

if __name__ == "__main__":
    create_gui() 