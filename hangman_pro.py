import random
import os

# კატეგორიების მიხედვით დალაგებული სიტყვების ლექსიკონი
CATEGORIES = {
    "1": ("პროგრამირება", ["ალგორითმი", "პითონი", "ინკაფსულაცია", "დეველოპერი", "ცვლადი"]),
    "2": ("ქვეყნები", ["საქართველო", "იტალია", "იაპონია", "ბრაზილია", "ესპანეთი"]),
    "3": ("ცხოველები", ["ვეფხვი", "დელფინი", "არწივი", "პინგვინი", "ლეოპარდი"])
}

# კონსოლური ვიზუალი მცდელობების მიხედვით (0-დან 6-მდე)
HANGMAN_PICS = [
    """
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          ===
    """,
    """
      +---+
      |   |
      O   |
     /|\  |
     /    |
          ===
    """,
    """
      +---+
      |   |
      O   |
     /|\  |
          |
          ===
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          ===
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          ===
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          ===
    """,
    """
      +---+
      |   |
          |
          |
          |
          ===
    """
]


def choose_category():
    """მომხმარებელს არჩევინებს სიტყვების კატეგორიას ვალიდაციით."""
    print("\nაირჩიეთ კატეგორია:")
    for key, (name, _) in CATEGORIES.items():
        print(f"{key}. {name}")

    while True:
        choice = input("შეიყვანეთ ნომერი (1-3): ").strip()
        if choice in CATEGORIES:
            cat_name, words = CATEGORIES[choice]
            print(f"არჩეული კატეგორია: {cat_name}")
            return random.choice(words).lower()
        print("შეცდომა: აირჩიეთ მხოლოდ 1, 2 ან 3!")


def save_score(player_name, word, won):
    """ინახავს თამაშის შედეგს ტექსტურ ფაილში."""
    status = "მოიგო" if won else "წააგო"
    with open("hangman_history.txt", "a", encoding="utf-8") as file:
        file.write(f"მოთამაშე: {player_name} | სიტყვა: {word} | შედეგი: {status}\n")
    print("შედეგი შენახულია ფაილში 'hangman_history.txt'.")


def show_history():
    """აჩვენებს წინა თამაშების ისტორიას ფაილიდან."""
    if not os.path.exists("hangman_history.txt"):
        print("\nისტორია ჯერ ცარიელია.")
        return
    print("\n--- თამაშების ისტორია ---")
    with open("hangman_history.txt", "r", encoding="utf-8") as file:
        print(file.read())


def display_board(secret_word, guessed_letters, attempts_left):
    """ბეჭდავს ნახატს, დაფარულ სიტყვას და გამოყენებულ ასოებს."""
    print(HANGMAN_PICS[attempts_left])
    display_word = [letter if letter in guessed_letters else "_" for letter in secret_word]
    print("სიტყვა: " + " ".join(display_word))
    print(f"დარჩენილი სიცოცხლე: {attempts_left}")
    if guessed_letters:
        print(f"ნაცადი ასოები: {', '.join(sorted(guessed_letters))}")
    print("-" * 35)


def play_hangman():
    """თამაშის მთავარი ფუნქცია."""
    secret_word = choose_category()
    guessed_letters = set()
    attempts_left = 6
    won = False

    while attempts_left > 0:
        display_board(secret_word, guessed_letters, attempts_left)

        # მოგების შემოწმება
        if all(letter in guessed_letters for letter in secret_word):
            won = True
            break

        guess = input("შეიყვანეთ ერთი ასო (ან სცადეთ მთლიანი სიტყვა): ").strip().lower()

        # ვალიდაცია: ცარიელი ან არაანბანური სიმბოლოები
        if not guess.isalpha():
            print("შეცდომა: გამოიყენეთ მხოლოდ ასოები!")
            continue

        # თუ მომხმარებელმა მთლიანი სიტყვის გამოცნობა სცადა
        if len(guess) > 1:
            if guess == secret_word:
                won = True
                break
            else:
                attempts_left -= 1
                print("არასწორი სიტყვაა! დაგაკლდათ 1 სიცოცხლე.")
                continue

        # ერთი ასოს შემოწმება
        if guess in guessed_letters:
            print("ეს ასო უკვე გამოიყენეთ!")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"ყოჩაღ! ასო '{guess}' სწორია.")
        else:
            attempts_left -= 1
            print(f"სამწუხაროდ, ასო '{guess}' არ არის სიტყვაში.")

    # თამაშის დასრულების შეტყობინება
    if won:
        print(f"\nგილოცავთ! თქვენ გამოიცანით სიტყვა: '{secret_word}'")
    else:
        print(HANGMAN_PICS[0])
        print(f"\nთამაში წააგეთ! ჩაფიქრებული სიტყვა იყო: '{secret_word}'")

    # შედეგის შენახვა ფაილში
    name = input("შეიყვანეთ თქვენი სახელი შედეგის შესანახად: ").strip() or "უცნობი"
    save_score(name, secret_word, won)


# მთავარი მენიუ
if __name__ == "__main__":
    while True:
        print("\n=== HANGMAN მენიუ ===")
        print("1. ახალი თამაშის დაწყება")
        print("2. თამაშების ისტორიის ნახვა")
        print("3. გასვლა")

        menu_choice = input("აირჩიეთ მოქმედება (1-3): ").strip()

        if menu_choice == "1":
            play_hangman()
        elif menu_choice == "2":
            show_history()
        elif menu_choice == "3":
            print("პროგრამა დასრულდა.")
            break
        else:
            print("შეცდომა: აირჩიეთ 1, 2 ან 3!")
