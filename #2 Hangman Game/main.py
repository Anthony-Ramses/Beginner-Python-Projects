from hangman import Hangman


if __name__ == "__main__":
    game = Hangman()

    print("Welcome to Hangman Game!")
    print("------------------------")
    while True:
        print(f'{"-" * 5} Level: {game.level} {"-" * 5} Score: {game.score} {"-" * 5}')
        category, word, underscores = game.populate_underscores()
        attempts = len(word) + 2

        while '_' in underscores:
            if attempts > 0:
                print(f"You have {attempts} attempts remaining.")

                print(f"Category: {category}")
                print(" ".join(underscores))

                ans = input("Enter your guess (single letter): ").upper()

                game.change_underscore(ans)
                attempts -= 1

                game.score_level()

                if ans.lower() == 'exit':
                    print("Thanks for playing! Goodbye!")
                    break
                if game.check_win() == 'Lose':
                    # Reset the game state for a new game
                    attempts = 0
                    game.score = 0
                    game.level = 1
                    break
            else:
                # implement score and level reset
                game.score = 0
                game.level = 1
                print(' '.join(underscores))
                print("Game Over! You've run out of attempts.")
                print(f"The correct word was: {word}")
                print("Your score has been reset to 0.")
                break     