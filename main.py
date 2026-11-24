import json
import os
from datetime import datetime


class LibraryItem:
    """
    საბაზო კლასი ბიბლიოთეკის ნებისმიერი ერთეულისთვის (მემკვიდრეობის დემონსტრირებისთვის).
    """

    def __init__(self, title: str):
        self._title = title

    @property
    def title(self) -> str:
        """აბრუნებს ერთეულის სათაურს."""
        return self._title

    def display_info(self) -> str:
        """საბაზო მეთოდი ინფორმაციის გამოსატანად (პოლიმორფიზმისთვის)."""
        return f"სათაური: {self._title}"


class Book(LibraryItem):
    """
    წიგნის კლასი, რომელიც მემკვიდრეობით იღებს LibraryItem-ს.
    """

    def __init__(self, title: str, author: str, year: int):
        super().__init__(title)
        self._author = author
        self._year = year

    @property
    def author(self) -> str:
        """აბრუნებს წიგნის ავტორს."""
        return self._author

    @property
    def year(self) -> int:
        """აბრუნებს წიგნის გამოცემის წელს."""
        return self._year

    def display_info(self) -> str:
        """
        პოლიმორფიზმი: გადაფარავს მშობელი კლასის მეთოდს და აბრუნებს წიგნის სრულ დეტალებს.
        """
        return f"სათაური: '{self._title}' | ავტორი: {self._author} | გამოცემის წელი: {self._year}"

    def to_dict(self) -> dict:
        """გარდაქმნის წიგნის ობიექტს ლექსიკონად (JSON ფაილში შესანახად)."""
        return {
            "title": self._title,
            "author": self._author,
            "year": self._year
        }


class BookManager:
    """
    კლასი წიგნების სიისა და ფაილური ოპერაციების სამართავად.
    """

    def __init__(self, filename: str = "books.json"):
        self.filename = filename
        self.books: list[Book] = []
        self.load_from_file()

    def load_from_file(self) -> None:
        """კითხულობს წიგნების სიას JSON ფაილიდან, თუ ფაილი არსებობს."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.books = [
                        Book(item["title"], item["author"], item["year"])
                        for item in data
                    ]
            except (json.JSONDecodeError, KeyError):
                self.books = []

    def save_to_file(self) -> None:
        """ინახავს/არედაქტირებს წიგნების მიმდინარე სიას JSON ფაილში."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def delete_data_file(self) -> None:
        """შლის მონაცემთა ფაილს და ასუფთავებს სიას."""
        self.books.clear()
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print("მონაცემთა ფაილი და წიგნების სია წარმატებით წაიშალა.")
        else:
            print("წასაშლელი ფაილი ვერ მოიძებნა.")

    def add_book(self, title: str, author: str, year: int) -> None:
        """ამატებს ახალ წიგნს სიაში და ინახავს ფაილში."""
        new_book = Book(title, author, year)
        self.books.append(new_book)
        self.save_to_file()
        print(f"\nწიგნი '{title}' წარმატებით დაემატა!")

    def show_all_books(self) -> None:
        """აჩვენებს ყველა წიგნის დეტალურ ინფორმაციას."""
        if not self.books:
            print("\nწიგნების სია ცარიელია.")
            return

        print("\n--- ყველა წიგნის სია ---")
        for index, book in enumerate(self.books, start=1):
            print(f"{index}. {book.display_info()}")

    def search_by_title(self, search_query: str) -> None:
        """ეძებს წიგნს სათაურის მიხედვით (რეგისტრის გაუთვალისწინებლად)."""
        found_books = [
            book for book in self.books
            if search_query.lower() in book.title.lower()
        ]

        if not found_books:
            print(f"\nსათაურით '{search_query}' წიგნი ვერ მოიძებნა.")
        else:
            print(f"\n--- ძიების შედეგები ('{search_query}') ---")
            for book in found_books:
                print(book.display_info())


def get_valid_string(prompt: str) -> str:
    """ამოწმებს, რომ შეყვანილი ტექსტი არ იყოს ცარიელი."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("შეცდომა: ველი არ შეიძლება იყოს ცარიელი. სცადეთ თავიდან.")


def get_valid_year(prompt: str) -> int:
    """ამოწმებს, რომ გამოცემის წელი იყოს ვალიდური მთელი რიცხვი."""
    current_year = datetime.now().year
    while True:
        raw_year = input(prompt).strip()
        if raw_year.isdigit():
            year = int(raw_year)
            if 1000 <= year <= current_year:
                return year
            else:
                print(f"შეცდომა: შეიყვანეთ წელი 1000-დან {current_year}-მდე.")
        else:
            print("შეცდომა: გამოცემის წელი უნდა შედგებოდეს მხოლოდ ციფრებისგან.")


def run_application() -> None:
    """უშვებს კონსოლ აპლიკაციის მთავარ მენიუს."""
    manager = BookManager()

    if not manager.books:
        manager.books.extend([
            Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1712),
            Book("1984", "ჯორჯ ორუელი", 1949)
        ])
        manager.save_to_file()

    while True:
        print("\n===============================")
        print(" წიგნების მართვის აპლიკაცია")
        print("===============================")
        print("1. ახალი წიგნის დამატება")
        print("2. ყველა წიგნის ნახვა")
        print("3. წიგნის ძიება სათაურით")
        print("4. ყველა მონაცემის (ფაილის) წაშლა")
        print("5. გასვლა")

        choice = input("\nაირჩიეთ მოქმედება (1-5): ").strip()

        if choice == "1":
            title = get_valid_string("შეიყვანეთ წიგნის სათაური: ")
            author = get_valid_string("შეიყვანეთ წიგნის ავტორი: ")
            year = get_valid_year("შეიყვანეთ გამოცემის წელი: ")
            manager.add_book(title, author, year)

        elif choice == "2":
            manager.show_all_books()

        elif choice == "3":
            query = get_valid_string("შეიყვანეთ საძიებო სათაური: ")
            manager.search_by_title(query)

        elif choice == "4":
            confirm = input("დარწმუნებული ხართ, რომ გსურთ ფაილის წაშლა? (დიახ/არა): ").strip().lower()
            if confirm == "დიახ":
                manager.delete_data_file()

        elif choice == "5":
            print("პროგრამა დასრულდა. ნახვამდის!")
            break

        else:
            print("არასწორი არჩევანი! გთხოვთ, აირჩიოთ რიცხვი 1-დან 5-მდე.")


if __name__ == "__main__":
    run_application()
