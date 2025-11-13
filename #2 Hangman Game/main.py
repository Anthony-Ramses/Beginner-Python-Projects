from hangman import Hangman


if __name__ == "__main__":
    game = Hangman()
    attempts = Hangman().attempts
    print("Welcome to Hangman Game!")
    print("------------------------")
    while True:
        print(f'{"-" * 5} Level: {game.level} {"-" * 5} Score: {game.score} {"-" * 5}')
        category, word, underscores = game.populate_underscores()

        while attempts > 0 and '_' in underscores:
            print(f"Category: {category}")
            print(" ".join(underscores))

            ans = input("Enter your guess (single letter): ").upper()

            game.change_underscore(ans)
            print(f"Category: {category}")
            print(" ".join(game.underscores))

            game.score_level()

        if ans.lower() == 'exit':
            print("Thanks for playing! Goodbye!")
            break