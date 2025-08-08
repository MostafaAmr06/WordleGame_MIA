import random

words = []
current_word = ""
guessed_words = []
feedback_history = []

def load_words():
    global words
    try:
        with open('words.txt', 'r') as file:
            for line in file:
                word = line.strip().lower()
                if len(word) == 5:
                    words.append(word)
    except:
        print("cant load words")
        return False
    return True

def pick_word():
    global current_word
    if not words:
        return False
    current_word = random.choice(words)
    return True

def is_valid_word(word):
    if len(word) != 5:
        return False
    return word.lower() in words

def check_guess(guess):
    if len(guess) != 5 or len(current_word) != 5:
        return None
    
    guess = guess.lower()
    target = current_word.lower()
    
    result = ['B'] * 5
    
    # check correct positions first
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'G'
    
    # check wrong positions
    target_letters = list(target)
    for i in range(5):
        if result[i] == 'G':
            target_letters[i] = None
    
    for i in range(5):
        if result[i] != 'G':
            if guess[i] in target_letters:
                result[i] = 'Y'
                for j in range(5):
                    if target_letters[j] == guess[i]:
                        target_letters[j] = None
                        break
    
    return ''.join(result)

def start_game():
    global guessed_words, feedback_history
    guessed_words = []
    feedback_history = []
    return load_words() and pick_word()

def submit_guess(word):
    if not is_valid_word(word):
        return False, "not a word"
    
    guessed_words.append(word)
    feedback = check_guess(word)
    feedback_history.append(feedback)
    
    return True, feedback

def is_game_won():
    return feedback_history and feedback_history[-1] == 'GGGGG'

def is_game_lost():
    return len(guessed_words) >= 6

def get_keyboard_colors():
    colors = {}
    for word, feedback in zip(guessed_words, feedback_history):
        for i, letter in enumerate(word.upper()):
            #only update if we don't have a better color (fixes a logic error)
            if letter not in colors or feedback[i] == 'G':
                if feedback[i] == 'G':
                    colors[letter] = '#6aaa64'
                elif feedback[i] == 'Y':
                    colors[letter] = '#c9b458'
                elif feedback[i] == 'B':
                    colors[letter] = '#3a3a3c'
    return colors 