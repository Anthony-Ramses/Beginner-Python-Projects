import re
import random


class Hang:
    def __init__(self):
        self.countries = ['Argentina', 'Australia', 'Brazil', 'Canada', 'Cameroon', 'Egypt', 'France', 'Germany', 'India', 'Japan']
        self.animals = ['Elephant', 'Giraffe', 'Kangaroo', 'Lion', 'Penguin', 'Rhinoceros', 'Tiger', 'Zebra', 'Cheetah', 'Dolphin']
        self.foods = ['Pizza', 'Burger', 'Pasta', 'Sushi', 'Taco', 'Salad', 'Steak', 'Curry', 'Dumplings', 'Donut']
        self.sports = ['Football', 'Basketball', 'Baseball', 'Soccer', 'Tennis', 'Golf', 'Boxing', 'Swimming', 'Cycling', 'Hockey']
        self.music = ['Guitar', 'Piano', 'Violin', 'Drums', 'Saxophone', 'Flute', 'Trumpet', 'Cello', 'Harp', 'Clarinet']
        self.categories = {
            'Countries': self.countries,
            'Animals': self.animals,
            'Food': self.foods,
            'Sports': self.sports,
            'Music': self.music
    }

class Hangman:
    def __init__(self):
        self.underscores = ''
        self.word = ''
        self.attempts = 0
        self.score = 0
        self.level = 1

    def populate_underscores(self):
        choice = random.choice(list(Hang().categories.keys()))
        word = random.choice(Hang().categories[choice]).upper()
        underscores = ['_'] * len(word)
        self.underscores = underscores
        self.word = word
        self.attempts = len(word) + 2 # The number of errors acceptable for each word
        return choice, word, underscores

    def validate_choice(self, choice):
        if re.match("^[A-Z]$", choice):
            return True
        return False
    
    def change_underscore(self, choice):
        if self.validate_choice(choice):
            for index, letter in enumerate(self.word):
                if letter == choice:
                    self.underscores[index] = choice
                    self.score += 10
        else:
            print("Invalid choice. Please enter a single letter A-Z.")
        return self.underscores
    
    def check_win(self):
        if self.attempts > 0:
            if '_' not in self.underscores:
                return True
        elif self.attempts <= 0:
            self.level = 1
            self.score = 0
            return 'Lose'
    
    def score_level(self):
        if self.check_win() is True:
            self.level += 1
            self.score += self.attempts * 5
            print(' '.join(self.underscores[i] for i in range(len(self.underscores))))
            print(f"Congratulations! You've advanced to level {self.level}.")
            print(f"Your score is now {self.score}.")
        elif self.check_win() == 'Lose':
            print("Game Over! You've run out of attempts.")
            print(f"The correct word was: {self.word}")
            print("Your score has been reset to 0.")
        return self.level, self.score
