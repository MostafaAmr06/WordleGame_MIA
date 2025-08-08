import tkinter as tk
from tkinter import messagebox
import backend

#global variables for use in each function
root = None
cells = []
current_row = 0
current_col = 0
target_word = None
game_over = False
status_label = None
keyboard_buttons = {}

def create_gui():
    global root, cells, target_word, status_label
    
    root = tk.Tk()
    root.title("Wordle")
    root.geometry("400x700")
    root.configure(bg='white')
    root.minsize(350, 600)  #minimum window size
    
    #main container
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # top bar with title and icons
    top_bar = tk.Frame(main_frame, bg='white', height=60)
    top_bar.pack(fill='x', pady=5)
    top_bar.pack_propagate(False)
    
    # title (wordle just like the image)
    title = tk.Label(top_bar, text="WORDLE", font=('Arial', 28, 'bold'), bg='white', fg='black')
    title.pack(side='left', padx=20)
    
    # Icons (I tried to use another library instead of icons like that but it didnt work and was time consuming for a small issue)
    help_icon = tk.Label(top_bar, text="?", font=('Arial', 16), bg='white', fg='black')
    help_icon.pack(side='right', padx=10)
    
    stats_icon = tk.Label(top_bar, text="📊", font=('Arial', 16), bg='white', fg='black')
    stats_icon.pack(side='right', padx=5)
    
    settings_icon = tk.Label(top_bar, text="⚙", font=('Arial', 16), bg='white', fg='black')
    settings_icon.pack(side='right', padx=10)
    
    #game grid
    grid_frame = tk.Frame(main_frame, bg='white')
    grid_frame.pack(pady=15, expand=True)
    
    #grid weights configuration for responsive layout
    for i in range(6):
        grid_frame.grid_rowconfigure(i, weight=1)
    for i in range(5):
        grid_frame.grid_columnconfigure(i, weight=1)
    
    cells = []
    for row in range(6):
        row_cells = []
        for col in range(5):
            cell = tk.Label(grid_frame, font=('Arial', 18, 'bold'), 
                          bg='white', fg='black', relief='solid', bd=2,
                          anchor='center', width=6, height=3)
            cell.grid(row=row, column=col, padx=1, pady=1, sticky='nsew')
            row_cells.append(cell)
        cells.append(row_cells)
    
    
    #create the virtual keyboard, function is under
    create_keyboard(main_frame) 

    
    # Keyboard events
    root.bind('<Key>', handle_key)
    root.bind('<Return>', submit_guess)
    root.bind('<BackSpace>', handle_backspace)
    
    # START GAME
    target_word = backend.word_manager("pick_random")
    root.focus_set()
    root.mainloop()

def create_keyboard(parent):
    global keyboard_buttons
    
    keyboard_frame = tk.Frame(parent, bg='white')
    keyboard_frame.pack(pady=10, fill='x')
    
    #keyboard layout
    rows = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
    ]
    
    for row_idx, row in enumerate(rows):
        row_frame = tk.Frame(keyboard_frame, bg='white')
        row_frame.pack(pady=1, fill='x')
        
        # center the row
        spacer_left = tk.Frame(row_frame, bg='white')
        spacer_left.pack(side='left', fill='x', expand=True)
        
        for letter in row:
            if letter == 'ENTER':
                btn = tk.Button(row_frame, text=letter, width=8, height=2, 
                              font=('Arial', 9, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=submit_guess)
            elif letter == '⌫': #same issue as the icons, I tried to use another library but it didnt work and was time consuming
                btn = tk.Button(row_frame, text=letter, width=8, height=2,
                              font=('Arial', 12, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=lambda: handle_backspace(None))
            else:
                btn = tk.Button(row_frame, text=letter, width=5, height=2,
                              font=('Arial', 11, 'bold'), bg='#d3d6da', fg='black',
                              relief='flat', command=lambda l=letter: handle_key_click(l))
            btn.pack(side='left', padx=1)
            keyboard_buttons[letter] = btn
        
        spacer_right = tk.Frame(row_frame, bg='white')
        spacer_right.pack(side='right', fill='x', expand=True)

def handle_key_click(letter):
    global current_col
    if game_over:
        return
    if current_col < 5:
        cells[current_row][current_col].config(text=letter)
        current_col += 1


def handle_key(event):
    global current_col
    if game_over:
        return
    if event.char.isalpha() and current_col < 5:
        cells[current_row][current_col].config(text=event.char.upper())
        current_col += 1

def handle_backspace(event):
    global current_col
    if game_over:
        return
    if current_col > 0:
        current_col -= 1
        cells[current_row][current_col].config(text="")


# will move it to logic.py when i do it, it already uses some functions from backend.py so i will revamp it
def submit_guess(event=None):
    global current_row, game_over
    
    if game_over:
        return
    
    # Get word
    word = ""
    for col in range(5):
        letter = cells[current_row][col].cget("text")
        word += letter.lower() if letter else " "
    
    word = word.strip()
    
    # Check word
    if len(word) != 5:
        status_label.config(text="Need 5 letters!")
        return
    
    if not backend.word_manager("validate", word):
        status_label.config(text="Not a word!")
        return
    
    # Check guess
    feedback = backend.check_guess(word, target_word)
    color_row(current_row, feedback)
    update_keyboard_colors(word, feedback)
    
    # Check win
    if feedback == 'GGGGG':
        game_over = True
        status_label.config(text=f"Won in {current_row + 1} tries!")
        messagebox.showinfo("Win!", f"You won in {current_row + 1} tries!")
        return
    
    # Next row
    current_row += 1
    
    # Check lose
    if current_row >= 6:
        game_over = True
        status_label.config(text=f"Lost! Word was: {target_word}")
        messagebox.showinfo("Lose!", f"Word was: {target_word}")
        return
    
    global current_col
    current_col = 0

# will move to logic.py when i do it
def color_row(row, feedback):
    colors = {'G': '#6aaa64', 'Y': '#c9b458', 'B': '#3a3a3c'}
    for col in range(5):
        color = colors.get(feedback[col], '#3a3a3c')
        cells[row][col].config(bg=color, fg='white')

def update_keyboard_colors(word, feedback):
    for i, letter in enumerate(word.upper()):
        if letter in keyboard_buttons:
            if feedback[i] == 'G':
                keyboard_buttons[letter].config(bg='#6aaa64', fg='white')
            elif feedback[i] == 'Y':
                keyboard_buttons[letter].config(bg='#c9b458', fg='white')
            elif feedback[i] == 'B':
                keyboard_buttons[letter].config(bg='#3a3a3c', fg='white')

def new_game():
    global current_row, current_col, target_word, game_over
    
    current_row = 0
    current_col = 0
    target_word = backend.word_manager("pick_random")
    game_over = False
    
    # Clear grid
    for row in range(6):
        for col in range(5):
            cells[row][col].config(text="", bg='white', fg='black')
    
    # Reset keyboard colors
    for btn in keyboard_buttons.values():
        btn.config(bg='#d3d6da', fg='black')

if __name__ == "__main__":
    create_gui() 