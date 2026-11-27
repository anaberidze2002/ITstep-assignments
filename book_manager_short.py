import json
import os


class Book:
    """საბაზისო კლასი: წარმოადგენს წიგნს (ინკაფსულაცია)."""

    def __init__(self, title, author, year):
        self.__title = title          # დაცული ატრიბუტი (Encapsulation)
        self.__author = author
        self.set_year(year)

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def set_year(self, year):
        """ამოწმებს გამოცემის წლის ვალიდურობას."""
        if not isinstance(year, int) or year < 0 or year > 2026:
            raise ValueError("გამოცემის წელი უნდა იყოს სწორი რიცხვი!")
        self.__year = year

    def display_info(self):
        """აბრუნებს წიგნის ინფორმაციას (პოლიმორფიზმი)."""
        return f"[წიგნი] '{self.__title}' | ავტორი: {self.__author} | წელი: {self.__year}"

    def to_dict(self):
        """გარდაქმნის ობიექტს ლექსიკონად ფაილში შესანახად."""
        return {"type": "Book", "title": self.__title, "author": self.__author, "year": self.__year}


class EBook(Book):
    """შვილობილი კლასი: ელექტრონული წიგნი (მემკვიდრეობა და პოლიმორფიზმი)."""

    def __init__(self, title, author, year, file_size):
        super().__init__(title, author, year)
        self.file_size = file_size

    def display_info(self):
        """მეთოდის გადაფარვა (Override) - პოლიმორფიზმი."""
        return super().display_info().replace("[წიგნი]", "[E-Book]") + f" | ზომა: {self.file_size} MB"

    def to_dict(self):
        data = super().to_dict()
        data.update({"type": "EBook", "file_size": self.file_size})
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
            print("\nსია ცარიელია.")
            return
        print("\n--- წიგნების კატალოგი ---")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.display_info()}")

    def search_book(self, query):
        """ეძებს წიგნს სათაურით ან ავტორით."""
        q = query.lower()
        found = [b for b in self.books if q in b.get_title().lower() or q in b.get_author().lower()]
        if not found:
            print("წიგნი ვერ მოიძებნა.")
            return
        for book in found:
            print(book.display_info())

    def delete_book(self, title):
        """შლის წიგნს სათაურის მიხედვით."""
        before = len(self.books)
        self.books = [b for b in self.books if b.get_title().lower() != title.lower()]
        if len(self.books) < before:
            self.save_to_file()
            print("წიგნი წაიშალა!")
        else:
            print("ასეთი სათაურით წიგნი ვერ მოიძებნა.")

    def clear_file(self):
        """შლის მონაცემთა ფაილს (კრიტერიუმი 2.1.5)."""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.books.clear()
            print("მონაცემთა ფაილი წაიშალა!")

    def save_to_file(self):
        """ინახავს წიგნების სიას JSON ფაილში."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, ensure_ascii=False, indent=4)

    def load_from_file(self):
        """კითხულობს წიგნებს ფაილიდან პროგრამის ჩართვისას."""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            for item in json.load(f):
                if item["type"] == "EBook":
                    self.books.append(EBook(item["title"], item["author"], item["year"], item["file_size"]))
                else:
                    self.books.append(Book(item["title"], item["author"], item["year"]))


if __name__ == "__main__":
    manager = BookManager()
    # საჩვენებელი მაგალითი
    if not manager.books:
        manager.add_book(Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1189))
        manager.add_book(EBook("Clean Code", "Robert C. Martin", 2008, 4.5))

    while True:
        print("\n=== წიგნების მართვა ===")
        print("1. დამატება | 2. სიის ნახვა | 3. ძებნა | 4. წაშლა | 5. ფაილის წაშლა | 6. გასვლა")
        choice = input("აირჩიეთ (1-6): ").strip()

        if choice == "1":
            b_type = input("ტიპი (1 - წიგნი, 2 - E-Book): ").strip()
            title, author = input("სათაური: ").strip(), input("ავტორი: ").strip()
            if not title or not author:
                print("შეცდომა: ველები ცარიელია!")
                continue
            try:
                year = int(input("წელი: ").strip())
                if b_type == "2":
                    size = float(input("ზომა (MB): ").strip())
                    manager.add_book(EBook(title, author, year, size))
                else:
                    manager.add_book(Book(title, author, year))
            except ValueError as e:
                print(f"შეცდომა: {e}")
        elif choice == "2":
            manager.show_all_books()
        elif choice == "3":
            manager.search_book(input("საძიებო სიტყვა: ").strip())
        elif choice == "4":
            manager.delete_book(input("წასაშლელი სათაური: ").strip())
        elif choice == "5":
            manager.clear_file()
        elif choice == "6":
            break
        else:
            print("აირჩიეთ 1-6!")
