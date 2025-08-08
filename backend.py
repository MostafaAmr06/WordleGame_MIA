import random
# backend.py
print("Backend module loaded.")

def word_manager(action, guess=None): #handles operations like loading the word list and picking a random word
    if not hasattr(word_manager, 'words'):
        word_manager.words = []
        try:
            with open('words.txt', 'r') as file:
                for line in file:
                    word = line.strip().lower()
                    if len(word) == 5:
                        word_manager.words.append(word)
        except FileNotFoundError:
            print("Error: words.txt file not found!")
            return None
    
    #actions from other functions
    if action == "load":
        return word_manager.words
    elif action == "pick_random":
        if not word_manager.words:
            return None
        return random.choice(word_manager.words)
    elif action == "validate":
        if len(guess) != 5:
            return False
        return guess.lower() in word_manager.words
    else:
        return None

def check_guess(guess, target_word): #checks the guess from user and returns feedback
    if len(guess) != 5 or len(target_word) != 5:
        return None
    
    guess = guess.lower()
    target = target_word.lower()
    
    # here i created a feedback string
    # B = Black (not in word)
    feedback = ['B'] * 5
    
    #first pass: mark correct positions (G = green)
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 'G'
    
    #second pass: mark yellow positions (Y = yellow)
    target_letters = list(target)
    # Remove letters that are already marked as green (G)
    for i in range(5):
        if feedback[i] == 'G':
            target_letters[i] = None
    
    for i in range(5):
        if feedback[i] != 'G':  # Skip already marked positions
            if guess[i] in target_letters:
                feedback[i] = 'Y'
                # Remove the first occurrence of this letter from target_letters
                for j in range(5):
                    if target_letters[j] == guess[i]:
                        target_letters[j] = None
                        break
    
    return ''.join(feedback)

def play_game(): #main game function, will probably move soon or merge with main.py later
    words = word_manager("load")
    target_word = word_manager("pick_random")
    print(f"Game started! Target word: {target_word}")  # TESTING ONLY
    
    attempts = 0
    max_attempts = 6
    
    while attempts < max_attempts:
        print(f"\nAttempt {attempts + 1}/{max_attempts}")
        guess = input("Enter your 5-letter guess: ").strip().lower()
        
        if not word_manager("validate", guess):
            print("Invalid guess!")
            continue
        
        feedback = check_guess(guess, target_word)
        print(f"Feedback: {feedback}")
        
        if feedback == 'GGGGG':
            print(f"Congratulations! You found the word in {attempts + 1} attempts!")
            return
        
        attempts += 1
    
    print(f"Game over! The word was: {target_word}")

# TESTING ONLY
if __name__ == "__main__":
    play_game()