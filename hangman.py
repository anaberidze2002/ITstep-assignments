import random
import os

# ფაილის სახელის კონსტანტა (სტრიქონული ცვლადი)
FILE_NAME = "words.txt"

def init_file():
    """ქმნის საწყის ტექსტურ ფაილს სიტყვებით, თუ ის ჯერ არ არსებობს."""
    if not os.path.exists(FILE_NAME):
        default_words = ["პროგრამირება", "კომპიუტერი", "ალგორითმი", "ინტერნეტი", "კონსოლი"]
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for word in default_words:
                file.write(word + "\n")

def read_words():
    """კითხულობს ყველა სიტყვას ფაილიდან და აბრუნებს სიის (list) სახით."""
    init_file()
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]

def add_word():
    """ფაილში ამატებს მომხმარებლის მიერ შეყვანილ ახალ სიტყვას."""
    new_word = input("შეიყვანეთ დასამატებელი სიტყვა: ").strip().lower()
    words = read_words()
    
    # ვალიდაცია: ვამოწმებთ, რომ სიტყვა შედგებოდეს ქართული ასოებისგან და არ მეორდებოდეს
    if len(new_word) < 2 or not all("ა" <= char <= "ჰ" for char in new_word):
        print("შეცდომა: სიტყვა უნდა შედგებოდეს მინიმუმ 2 ქართული ასოსგან!")
    elif new_word in words:
        print("ეს სიტყვა უკვე არსებობს ბაზაში.")
    else:
        with open(FILE_NAME, "a", encoding="utf-8") as file:
            file.write(new_word + "\n")
        print(f"სიტყვა '{new_word}' წარმატებით დაემატა!")

def delete_word():
    """შლის მითითებულ სიტყვას ფაილიდან (ფაილის რედაქტირება/წაშლა)."""
    words = read_words()
    if len(words) <= 1:
        print("შეცდომა: ფაილში მინიმუმ 1 სიტყვა მაინც უნდა დარჩეს!")
        return

    print("არსებული სიტყვები:", ", ".join(words))
    target = input("შეიყვანეთ წასაშლელი სიტყვა: ").strip().lower()

    if target in words:
        words.remove(target)
        # ფაილის განახლება დარჩენილი სიტყვებით
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for word in words:
                file.write(word + "\n")
        print(f"სიტყვა '{target}' წაიშალა!")
    else:
        print("ასეთი სიტყვა ვერ მოიძებნა.")

def get_valid_guess(guessed_letters):
    """იღებს და ამოწმებს მომხმარებლის შეყვანილ ერთ ასოს."""
    while True:
        guess = input("შეიყვანეთ ერთი ასო: ").strip().lower()
        # ვამოწმებთ სიგრძეს, უნიკალურობას და ქართული ასოების დიაპაზონს
        if len(guess) == 1 and guess not in guessed_letters and "ა" <= guess <= "ჰ":
            return guess
        print("არასწორი შეყვანა! ჩაწერეთ მხოლოდ ერთი ახალი ქართული ასო.")

def play_hangman():
    """მართავს თამაშის ერთ სრულ რაუნდს."""
    words = read_words()
    secret_word = random.choice(words)   # სტრიქონი (str)
    guessed_letters = []                 # სია (list)
    attempts = 6                         # მთელი რიცხვი (int)
    is_won = False                       # ლოგიკური ცვლადი (bool)

    print("\n--- თამაში დაიწყო! ---")
    while attempts > 0:
        # ქვედა ტირეებისა და გამოცნობილი ასოების აწყობა
        display = " ".join([char if char in guessed_letters else "_" for char in secret_word])
        print(f"\nსიტყვა: {display}")
        print(f"დარჩენილი მცდელობები: {attempts}")
        if guessed_letters:
            print("ნაცადი ასოები:", ", ".join(guessed_letters))

        # მოგების პირობის შემოწმება
        if "_" not in display:
            is_won = True
            break

        guess = get_valid_guess(guessed_letters)
        guessed_letters.append(guess)

        if guess in secret_word:
            print("სწორია!")
        else:
            attempts -= 1
            print("არასწორია!")

    if is_won:
        print(f"\nგილოცავთ, თქვენ მოიგეთ! სიტყვა იყო: {secret_word}")
    else:
        print(f"\nმცდელობები ამოიწურა, წააგეთ! ჩაფიქრებული სიტყვა იყო: {secret_word}")

def main():
    """პროგრამის მთავარი მენიუ."""
    while True:
        print("\n=== HANGMAN - მთავარი მენიუ ===")
        print("1. თამაშის დაწყება")
        print("2. ახალი სიტყვის დამატება ფაილში")
        print("3. სიტყვის წაშლა ფაილიდან")
        print("4. გასვლა")
        
        choice = input("აირჩიეთ მოქმედება (1-4): ").strip()
        
        if choice == "1":
            play_hangman()
        elif choice == "2":
            add_word()
        elif choice == "3":
            delete_word()
        elif choice == "4":
            print("პროგრამა დასრულდა. ნახვამდის!")
            break
        else:
            print("შეცდომა: აირჩიეთ ციფრი 1-დან 4-მდე!")

if __name__ == "__main__":
    main()
