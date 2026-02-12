import json
import os
from datetime import datetime, timedelta


# =========================
# BOOK CLASS
# =========================
class Book:
    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["isbn"], data["year"])
        book.available = data["available"]
        book.borrowed_by = data["borrowed_by"]
        book.due_date = data["due_date"]
        return book


# =========================
# MEMBER CLASS
# =========================
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.max_limit = 5

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        member = Member(data["name"], data["member_id"])
        member.borrowed_books = data["borrowed_books"]
        return member


# =========================
# LIBRARY CLASS
# =========================
class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.load_data()

    # -------- FILE HANDLING --------
    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                data = json.load(f)
                for isbn, book in data.items():
                    self.books[isbn] = Book.from_dict(book)

        if os.path.exists("members.json"):
            with open("members.json", "r") as f:
                data = json.load(f)
                for mid, member in data.items():
                    self.members[mid] = Member.from_dict(member)

    def save_data(self):
        with open("books.json", "w") as f:
            json.dump({isbn: book.to_dict() for isbn, book in self.books.items()}, f, indent=4)

        with open("members.json", "w") as f:
            json.dump({mid: member.to_dict() for mid, member in self.members.items()}, f, indent=4)

    # -------- BOOK MANAGEMENT --------
    def add_book(self):
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        year = input("Year: ")

        if isbn in self.books:
            print("Book already exists!")
            return

        self.books[isbn] = Book(title, author, isbn, year)
        print("Book added successfully!")

    def register_member(self):
        name = input("Name: ")
        member_id = input("Member ID: ")

        if member_id in self.members:
            print("Member already exists!")
            return

        self.members[member_id] = Member(name, member_id)
        print("Member registered successfully!")

    def borrow_book(self):
        isbn = input("Enter ISBN: ")
        member_id = input("Enter Member ID: ")

        if isbn not in self.books:
            print("Book not found!")
            return

        if member_id not in self.members:
            print("Member not found!")
            return

        book = self.books[isbn]
        member = self.members[member_id]

        if not book.available:
            print("Book already borrowed!")
            return

        if len(member.borrowed_books) >= member.max_limit:
            print("Member reached borrow limit!")
            return

        book.available = False
        book.borrowed_by = member_id
        book.due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        member.borrowed_books.append(isbn)

        print(f"Book borrowed successfully! Due Date: {book.due_date}")

    def return_book(self):
        isbn = input("Enter ISBN: ")

        if isbn not in self.books:
            print("Book not found!")
            return

        book = self.books[isbn]

        if book.available:
            print("Book is already available!")
            return

        member = self.members[book.borrowed_by]
        member.borrowed_books.remove(isbn)

        # Overdue check
        due_date = datetime.strptime(book.due_date, "%Y-%m-%d")
        today = datetime.now()

        if today > due_date:
            days = (today - due_date).days
            fine = days * 2  # ₹2 per day fine
            print(f"Book was overdue by {days} days. Fine: ₹{fine}")

        book.available = True
        book.borrowed_by = None
        book.due_date = None

        print("Book returned successfully!")

    def search_books(self):
        keyword = input("Enter title/author/ISBN: ").lower()
        found = False

        for book in self.books.values():
            if (keyword in book.title.lower() or
                keyword in book.author.lower() or
                keyword == book.isbn):

                status = "Available" if book.available else f"Borrowed (Due: {book.due_date})"
                print(f"{book.title} | {book.author} | {book.isbn} | {status}")
                found = True

        if not found:
            print("No books found!")

    def view_statistics(self):
        total = len(self.books)
        available = len([b for b in self.books.values() if b.available])
        borrowed = total - available

        print("\nLibrary Statistics")
        print("Total Books:", total)
        print("Available Books:", available)
        print("Borrowed Books:", borrowed)
        print("Total Members:", len(self.members))


# =========================
# MAIN MENU
# =========================
def main():
    library = Library()

    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. View Statistics")
        print("7. Save & Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.register_member()
        elif choice == "3":
            library.borrow_book()
        elif choice == "4":
            library.return_book()
        elif choice == "5":
            library.search_books()
        elif choice == "6":
            library.view_statistics()
        elif choice == "7":
            library.save_data()
            print("Data saved successfully!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
