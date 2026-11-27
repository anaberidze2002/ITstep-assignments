from abc import ABC, abstractmethod
import json
import os


class LibraryItem(ABC):
    """აბსტრაქტული საბაზისო კლასი ბიბლიოთეკის ერთეულებისთვის (აბსტრაქცია)."""

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class Book(LibraryItem):
    """წარმოადგენს ჩვეულებრივ წიგნს (ინკაფსულაცია და მემკვიდრეობა)."""

    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.year = year  # იყენებს setter-ს ვალიდაციისთვის

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("სათაური არ უნდა იყოს ცარიელი!")
        self.__title = value.strip()

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        if not value.strip():
            raise ValueError("ავტორი არ უნდა იყოს ცარიელი!")
        self.__author = value.strip()

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 0 or value > 2026:
            raise ValueError("გამოცემის წელი უნდა იყოს სწორი მთელი რიცხვი!")
        self.__year = value

    def display_info(self):
        """აბრუნებს წიგნის ინფორმაციას (პოლიმორფიზმი)."""
        return f"[წიგნი] '{self.title}' | ავტორი: {self.author} | წელი: {self.year}"

    def to_dict(self):
        return {"type": "Book", "title": self.title, "author": self.author, "year": self.year}


class EBook(Book):
    """ელექტრონული წიგნი: მემკვიდრეობით იღებს Book-ს."""

    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb

    def display_info(self):
        """მეთოდის გადაფარვა E-Book-ისთვის (პოლიმორფიზმი)."""
        return f"[E-Book] '{self.title}' | ავტორი: {self.author} | წელი: {self.year} | ზომა: {self.file_size_mb} MB"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "EBook"
        data["file_size_mb"] = self.file_size_mb
        return data


class BookManager:
    """კლასი წიგნების სიისა და JSON ფაილის სამართავად."""

    def __init__(self, filename="books_db.json"):
        self.filename = filename
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        """ამატებს ახალ წიგნს და ინახავს ფაილში."""
        self.books.append(book)
        self.save_to_file()
        print("წიგნი წარმატებით დაემატა!")

    def show_all_books(self):
        """აჩვენებს ყველა წიგნს."""
        if not self.books:
            print("\nწიგნების სია ცარიელია.")
            return
        print("\n--- წიგნების კატალოგი ---")
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. {book.display_info()}")

    def search_books(self, query):
        """ეძებს წიგნს სათაურით ან ავტორით."""
        q = query.lower()
        found = [b for b in self.books if q in b.title.lower() or q in b.author.lower()]
        if not found:
            print(f"\nმოთხოვნით '{query}' წიგნი ვერ მოიძებნა.")
            return
        print("\n--- ძიების შედეგები ---")
        for book in found:
            print(book.display_info())

    def update_book(self, title):
        """არედაქტირებს არსებული წიგნის მონაცემებს (Update)."""
        for book in self.books:
            if book.title.lower() == title.lower():
                new_title = input(f"ახალი სათაური (დატოვეთ ცარიელი '{book.title}'-სთვის): ").strip()
                new_author = input(f"ახალი ავტორი (დატოვეთ ცარიელი '{book.author}'-სთვის): ").strip()
                new_year = input(f"ახალი წელი (დატოვეთ ცარიელი '{book.year}'-სთვის): ").strip()
                try:
                    if new_title:
                        book.title = new_title
                    if new_author:
                        book.author = new_author
                    if new_year:
                        book.year = int(new_year)
                    self.save_to_file()
                    print("წიგნის მონაცემები განახლდა!")
                except ValueError as e:
                    print(f"შეცდომა განახლებისას: {e}")
                return
        print("ასეთი სათაურით წიგნი ვერ მოიძებნა.")

    def delete_book(self, title):
        """შლის კონკრეტულ წიგნს."""
        initial = len(self.books)
        self.books = [b for b in self.books if b.title.lower() != title.lower()]
        if len(self.books) < initial:
            self.save_to_file()
            print(f"წიგნი '{title}' წაიშალა.")
        else:
            print("წიგნი ვერ მოიძებნა.")

    def show_statistics(self):
        """აჩვენებს ბიბლიოთეკის მოკლე სტატისტიკას."""
        if not self.books:
            print("\nსტატისტიკისთვის სია ცარიელია.")
            return
        ebooks_count = sum(1 for b in self.books if isinstance(b, EBook))
        oldest = min(self.books, key=lambda b: b.year)
        print("\n--- ბიბლიოთეკის სტატისტიკა ---")
        print(f"სულ წიგნები: {len(self.books)} (ჩვეულებრივი: {len(self.books) - ebooks_count}, E-Book: {ebooks_count})")
        print(f"ყველაზე ძველი წიგნი: '{oldest.title}' ({oldest.year} წ.)")

    def delete_database_file(self):
        """შლის მონაცემთა ფაილს (კრიტერიუმი 2.1.5)."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.books.clear()
            print("მონაცემთა ფაილი სრულად წაიშალა!")
        else:
            print("წასაშლელი ფაილი არ არსებობს.")

    def save_to_file(self):
        """ინახავს წიგნებს JSON ფაილში."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([b.to_dict() for b in self.books], file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        """კითხულობს წიგნებს ფაილიდან."""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as file:
            for item in json.load(file):
                if item.get("type") == "EBook":
                    self.books.append(EBook(item["title"], item["author"], item["year"], item["file_size_mb"]))
                else:
                    self.books.append(Book(item["title"], item["author"], item["year"]))


def get_valid_int(prompt):
    """ვალიდაცია მთელი რიცხვებისთვის."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("შეცდომა: შეიყვანეთ მხოლოდ რიცხვი!")


def run_book_manager():
    """წიგნების მართვის მთავარი მენიუ."""
    manager = BookManager()

    if not manager.books:
        manager.add_book(Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1189))
        manager.add_book(EBook("Clean Code", "Robert C. Martin", 2008, 4.5))

    while True:
        print("\n=== წიგნების მართვის სისტემა ===")
        print("1. წიგნის დამატება | 2. ყველა წიგნი | 3. ძებნა | 4. რედაქტირება")
        print("5. წიგნის წაშლა   | 6. სტატისტიკა  | 7. ფაილის წაშლა | 8. გასვლა")

        choice = input("აირჩიეთ (1-8): ").strip()

        if choice == "1":
            b_type = input("ტიპი (1 - წიგნი, 2 - E-Book): ").strip()
            title = input("სათაური: ").strip()
            author = input("ავტორი: ").strip()
            if not title or not author:
                print("შეცდომა: სათაური და ავტორი სავალდებულოა!")
                continue
            try:
                year = get_valid_int("გამოცემის წელი: ")
                if b_type == "2":
                    size = float(input("ფაილის ზომა (MB): ").strip())
                    manager.add_book(EBook(title, author, year, size))
                else:
                    manager.add_book(Book(title, author, year))
            except ValueError as e:
                print(f"შეცდომა: {e}")
        elif choice == "2":
            manager.show_all_books()
        elif choice == "3":
            manager.search_books(input("სათაური ან ავტორი: ").strip())
        elif choice == "4":
            manager.update_book(input("დასარედაქტირებელი წიგნის სათაური: ").strip())
        elif choice == "5":
            manager.delete_book(input("წასაშლელი წიგნის სათაური: ").strip())
        elif choice == "6":
            manager.show_statistics()
        elif choice == "7":
            manager.delete_database_file()
        elif choice == "8":
            print("წიგნების მართვის სისტემა დაიხურა.")
            break
        else:
            print("შეცდომა: აირჩიეთ 1-დან 8-მდე!")


if __name__ == "__main__":
    run_book_manager()
