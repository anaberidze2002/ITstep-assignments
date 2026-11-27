import random
import os

# კატეგორიების მიხედვით დალაგებული სიტყვების ლექსიკონი
CATEGORIES = {
    "1": ("პროგრამირება", ["ალგორითმი", "პითონი", "ინკაფსულაცია", "დეველოპერი", "ცვლადი"]),
    "2": ("ქვეყნები", ["საქართველო", "იტალია", "იაპონია", "ბრაზილია", "ესპანეთი"]),
    "3": ("ცხოველები", ["ვეფხვი", "დელფინი", "არწივი", "პინგვინი", "ლეოპარდი"])
}

# კომპაქტური ASCII ნახატები (6-დან 0 მცდელობამდე)
HANGMAN_PICS = [
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n     ===",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n     ===",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n     ===",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n     ===",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n     ===",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n     ===",
    "  +---+\n  |   |\n      |\n      |\n      |\n     ==="
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
    """ინახავს თამაშის შედეგს ტექსტურ ფაილში (ფაილის შექმნა/ჩაწერა)."""
    status = "მოიგო" if won else "წააგო"
    with open("hangman_history.txt", "a", encoding="utf-8") as file:
        file.write(f"მოთამაშე: {player_name} | სიტყვა: {word} | შედეგი: {status}\n")
    print("შედეგი შენახულია ფაილში.")


def show_history():
    """აჩვენებს წინა თამაშების ისტორიას ფაილიდან (ფაილის წაკითხვა)."""
    if not os.path.exists("hangman_history.txt"):
        print("\nისტორია ცარიელია.")
        return
    print("\n--- თამაშების ისტორია ---")
    with open("hangman_history.txt", "r", encoding="utf-8") as file:
        print(file.read())


def clear_history():
    """შლის თამაშების ისტორიის ფაილს (ფაილის წაშლა)."""
    if not os.path.exists("hangman_history.txt"):
        print("\nწასაშლელი ისტორია არ არსებობს.")
        return
    confirm = input("ნამდვილად გსურთ ისტორიის წაშლა? (კი/არა): ").strip().lower()
    if confirm in ("კი", "დიახ", "y", "yes"):
        os.remove("hangman_history.txt")
        print("ისტორიის ფაილი წაიშალა!")


def display_board(secret_word, guessed_letters, attempts_left):
    """ბეჭდავს ნახატს, დაფარულ სიტყვას და გამოყენებულ ასოებს."""
    print(HANGMAN_PICS[attempts_left])
    display_word = [letter if letter in guessed_letters else "_" for letter in secret_word]
    print("სიტყვა: " + " ".join(display_word))
    print(f"დარჩენილი სიცოცხლე: {attempts_left}")
    if guessed_letters:
        print(f"ნაცადი ასოები: {', '.join(sorted(guessed_letters))}")


def play_hangman():
    """თამაშის მთავარი ციკლი."""
    secret_word = choose_category()
    guessed_letters = set()
    attempts_left = 6
    won = False

    while attempts_left > 0:
        display_board(secret_word, guessed_letters, attempts_left)
        if all(letter in guessed_letters for letter in secret_word):
            won = True
            break

        guess = input("ასო ან მთლიანი სიტყვა: ").strip().lower()
        if not guess.isalpha():
            print("შეიყვანეთ მხოლოდ ასოები!")
            continue

        if len(guess) > 1:
            if guess == secret_word:
                won = True
                break
            attempts_left -= 1
            print("არასწორი სიტყვაა!")
            continue

        if guess in guessed_letters:
            print("ეს ასო უკვე სცადეთ!")
            continue

        guessed_letters.add(guess)
        if guess not in secret_word:
            attempts_left -= 1
            print(f"ასო '{guess}' არ არის სიტყვაში.")

    if won:
        print(f"\nგილოცავთ! გამოიცანით სიტყვა: '{secret_word}'")
    else:
        print(HANGMAN_PICS[0])
        print(f"\nწააგეთ! სიტყვა იყო: '{secret_word}'")

    name = input("შეიყვანეთ სახელი: ").strip() or "უცნობი"
    save_score(name, secret_word, won)


if __name__ == "__main__":
    while True:
        print("\n=== HANGMAN მენიუ ===")
        print("1. თამაში | 2. ისტორია | 3. ისტორიის წაშლა | 4. გასვლა")
        choice = input("აირჩიეთ (1-4): ").strip()
        
        if choice == "1":
            play_hangman()
        elif choice == "2":
            show_history()
        elif choice == "3":
            clear_history()
        elif choice == "4":
            break
        else:
            print("აირჩიეთ 1, 2, 3 ან 4!")
