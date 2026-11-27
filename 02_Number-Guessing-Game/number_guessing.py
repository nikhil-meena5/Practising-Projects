#Number guessing game (Day 4–5) Computer picks a random number 1–100.
#User guesses; show "too high" or "too low".
#Show the number of attempts at the end.
#Ask "Play again?". Skills: random module, loops, counters.
#How to check: Hints are correct. Attempt count is correct.
#Wrong input does not crash it.
#Bonus: Easy / Medium / Hard levels with limited attempts.

import random


def play_game():
    print("\n===== NUMBER GUESSING GAME =====")
    print("Guess a number between 1 and 100!")

    levels = {
        "easy": 10,
        "medium": 7,
        "hard": 5
    }

    while True:
        level = input(
            "\nChoose difficulty (Easy/Medium/Hard): "
        ).strip().lower()

        if level in levels:
            max_attempts = levels[level]
            break

        print("Invalid difficulty! Try again.")

    secret_number = random.randint(1, 100)
    attempts = 0

    print(f"\nYou have {max_attempts} attempts.")

    while attempts < max_attempts:
        guess_input = input(
            "\nEnter your guess (or exit): "
        ).strip()

        if guess_input.lower() == "exit":
            print("Game ended!")
            print("Secret number was:", secret_number)
            return

        try:
            guess = int(guess_input)

            if not 1 <= guess <= 100:
                print("Enter a number between 1 and 100.")
                continue

            attempts += 1

            if guess < secret_number:
                print("Too LOW! Try again.")

            elif guess > secret_number:
                print("Too HIGH! Try again.")

            else:
                print("\nCongratulations! Correct guess!")
                print("Attempts used:", attempts)
                return

            print("Attempts remaining:", max_attempts - attempts)

        except ValueError:
            print("Invalid input! Enter a whole number.")

    print("\nGame Over!")
    print("Correct number was:", secret_number)


def main():
    while True:
        play_game()

        again = input("\nPlay again? (yes/no): ").strip().lower()

        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
