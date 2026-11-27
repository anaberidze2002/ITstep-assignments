import json
import os


class Book:
    """საბაზისო კლასი: წარმოადგენს ჩვეულებრივ წიგნს (ინკაფსულაცია)."""

    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.year = year  # იყენებს setter-ს ვალიდაციისთვის

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        """ამოწმებს გამოცემის წლის ვალიდურობას."""
        if not isinstance(value, int) or value < 0 or value > 2026:
            raise ValueError("გამოცემის წელი უნდა იყოს სწორი მთელი რიცხვი!")
        self.__year = value

    def display_info(self):
        """აბრუნებს წიგნის დეტალურ ინფორმაციას (პოლიმორფიზმი)."""
        return f"[წიგნი] '{self.title}' | ავტორი: {self.author} | წელი: {self.year}"

    def to_dict(self):
        """გარდაქმნის ობიექტს ლექსიკონად ფაილში შესანახად."""
        return {"type": "Book", "title": self.title, "author": self.author, "year": self.year}


class EBook(Book):
    """შვილობილი კლასი: მემკვიდრეობით იღებს Book-ს (მემკვიდრეობა და პოლიმორფიზმი)."""

    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb

    def display_info(self):
        """მეთოდის გადაფარვა (Override) - პოლიმორფიზმის დემონსტრირება."""
        return f"[E-Book] '{self.title}' | ავტორი: {self.author} | წელი: {self.year} | ზომა: {self.file_size_mb} MB"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "EBook"
        data["file_size_mb"] = self.file_size_mb
        return data


class BookManager:
    """კლასი წიგნების სიისა და ფაილების სამართავად."""

    def __init__(self, filename="books_db.json"):
        self.filename = filename
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        """ამატებს ახალ წიგნს სიაში და ინახავს ფაილში."""
        self.books.append(book)
        self.save_to_file()
        print("წიგნი წარმატებით დაემატა!")

    def show_all_books(self):
        """აჩვენებს ყველა წიგნის დეტალურ ინფორმაციას."""
        if not self.books:
            print("\nწიგნების სია ცარიელია.")
            return
        print("\n--- წიგნების კატალოგი ---")
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. {book.display_info()}")

    def search_books(self, query):
        """ეძებს წიგნს სათაურის ან ავტორის მიხედვით."""
        found = [b for b in self.books if query.lower() in b.title.lower() or query.lower() in b.author.lower()]
        if not found:
            print(f"\nმოთხოვნით '{query}' წიგნი ვერ მოიძებნა.")
            return
        print("\n--- ძიების შედეგები ---")
        for book in found:
            print(book.display_info())

    def delete_book(self, title):
        """შლის კონკრეტულ წიგნს სათაურის მიხედვით (ფაილის რედაქტირება)."""
        initial_count = len(self.books)
        self.books = [b for b in self.books if b.title.lower() != title.lower()]
        if len(self.books) < initial_count:
            self.save_to_file()
            print(f"წიგნი '{title}' წაიშალა.")
        else:
            print("ასეთი სათაურით წიგნი ვერ მოიძებნა.")

    def delete_database_file(self):
        """შლის მონაცემთა ფაილს (კრიტერიუმი 2.1.5 - ფაილის წაშლა)."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.books.clear()
            print("მონაცემთა ფაილი სრულად წაიშალა!")
        else:
            print("წასაშლელი ფაილი არ არსებობს.")

    def save_to_file(self):
        """ინახავს წიგნების სიას JSON ფაილში."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([b.to_dict() for b in self.books], file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        """კითხულობს წიგნებს ფაილიდან პროგრამის ჩართვისას."""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if item.get("type") == "EBook":
                    self.books.append(EBook(item["title"], item["author"], item["year"], item["file_size_mb"]))
                else:
                    self.books.append(Book(item["title"], item["author"], item["year"]))


def get_valid_int(prompt):
    """ვალიდაციის ფუნქცია მთელი რიცხვების მისაღებად."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("შეცდომა: გთხოვთ შეიყვანოთ მხოლოდ რიცხვი!")


def run_book_manager():
    """წიგნების მართვის აპლიკაციის მთავარი მენიუ."""
    manager = BookManager()

    # საწყისი საჩვენებელი მაგალითი
    if not manager.books:
        manager.add_book(Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1189))
        manager.add_book(EBook("Clean Code", "Robert C. Martin", 2008, 4.5))

    while True:
        print("\n=== წიგნების მართვის სისტემა ===")
        print("1. ახალი წიგნის დამატება")
        print("2. ყველა წიგნის ნახვა")
        print("3. წიგნის ძებნა (სათაურით ან ავტორით)")
        print("4. წიგნის წაშლა")
        print("5. მონაცემთა ფაილის გასუფთავება (წაშლა)")
        print("6. გასვლა")

        choice = input("აირჩიეთ მოქმედება (1-6): ").strip()

        if choice == "1":
            book_type = input("ტიპი (1 - წიგნი, 2 - E-Book): ").strip()
            title = input("სათაური: ").strip()
            author = input("ავტორი: ").strip()
            if not title or not author:
                print("შეცდომა: სათაური და ავტორი არ უნდა იყოს ცარიელი!")
                continue
            try:
                year = get_valid_int("გამოცემის წელი: ")
                if book_type == "2":
                    size = float(input("ფაილის ზომა (MB): ").strip())
                    manager.add_book(EBook(title, author, year, size))
                else:
                    manager.add_book(Book(title, author, year))
            except ValueError as e:
                print(f"შეცდომა: {e}")

        elif choice == "2":
            manager.show_all_books()

        elif choice == "3":
            query = input("შეიყვანეთ სათაური ან ავტორი: ").strip()
            manager.search_books(query)

        elif choice == "4":
            title = input("წასაშლელი წიგნის ზუსტი სათაური: ").strip()
            manager.delete_book(title)

        elif choice == "5":
            manager.delete_database_file()

        elif choice == "6":
            print("წიგნების სისტემა დასრულდა.")
            break
        else:
            print("შეცდომა: აირჩიეთ 1-დან 6-მდე!")


if __name__ == "__main__":
    run_book_manager()
